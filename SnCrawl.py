import SnCrawler.crawler as crawler
import argparse
import requests
import sys
import json

def parseCookies(cookies, sess):
	cookiedict = { cookie.split("=")[0]:"".join(cookie.split("=")[1:]) for cookie in cookies.replace(" ", "").split(";")}
	for key in cookiedict:
		sess.cookies[key] = cookiedict[key]

def postForJson(post):
	return [{"Action": X[0], "Data":X[1]} for X in post]

parser = argparse.ArgumentParser()

requiredWebsite = parser.add_argument_group('required arguments')

requiredWebsite.add_argument("-w", "--website",
                    help="The website you want to crawl", metavar='"http(s)://domain.com/"')
parser.add_argument("-d", "--depth", help="How many layers deep to crawl(defaults to 3)", type=int, default=3)
parser.add_argument("-c", "--cookie", help="The cookies to use(if doing authenticated crawling)", metavar='"cooke1=val1; cookie2=val2"')
parser.add_argument("--subdomains", help="To include subdomains", action='store_true')
parser.add_argument("-e", "--exclude", help="The url to exclude from being crawled(like logout page)", metavar='"http://domain.com/logout"', action="append")
parser.add_argument("-v", "--verbose", help="To display verbose output", action='store_true')
parser.add_argument("-o", "--output", help="The output file where you want to write the scraped URL's(in Json)", metavar="/home/user/saveLocation.txt")
parser.add_argument("-j", "--js", help="Include the .js files", action='store_true')

args = parser.parse_args()#Just parsing arguments

s = requests.Session()

if args.website == None:
	parser.print_help()
	sys.exit(0)

url = args.website
depth = args.depth
if args.cookie is not None:
	parseCookies(args.cookie, s)
if args.exclude is not None:
	excluded = args.exclude
else: excluded = []
outFile = args.output


get, post, jscript = crawler.crawl(s, url,depth=depth, subdomains=args.subdomains, Debug=args.verbose, excluded=excluded, js=args.js)

print "\n"
print "Crawler completed"
print "="*40
print "GET URL's"
for each in get:
	print each

print "\n\n"
print "="*40
print "POST forms"
for each in post:
	print ""
	print "POST Form: %s"%each[0]
	print "Form Data: %s"%each[1]

print "\n\n"
print "="*40
print "JS files"
for each in jscript:
	print each

if outFile is not None:
	f = open(outFile, "w")
	jsonOut = {"GET": get}
	jsonOut["POST"] = postForJson(post)
	jsonOut["JS"] = jscript
	f.write(json.dumps(jsonOut, indent=4))
	f.close()
