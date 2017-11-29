from bs4 import BeautifulSoup
import requests

#This is a minimal crawler specially made for web scanning, in a way that it would only visit a single page only once,
#even if it has different parameters
#Eg, if there are two hrefs="/?id=1" & "/?id=2", it would only visit one of them, and then add it to our list
#As it is a web scanner and it only needs to crawl a site for different GET parameters, thus visiting them only once would
#save a lot of bandwidth and time, as the "?id=XXX" can go upto very large
#So only visiting a specific parameter once, and getting all links from it, and doing the same to rest, upto the specified depth

#It will only visit the main domain which is specified, not any other subdomains

#I know the code quality is kinda bad and hackish, but that's how i write ;)

#So at every page, it will get all the <a> tags, then make a hash table of them, and if there are two 'a'
#tags with different parameters, it would store it like this
#{url: [{param1 : val1, param2 : Val2}, {param3 : val3, param1 : val1}]}
#Then at the end it would parse them into the normal GET and return to us

#Added support for POST forms also, will extract all forms from a page and display them

def joinParsedGet(urls): #Turning a list of Hash tabled URL's into normal GET ones
	parsed = []
	for url in urls:
		if len(urls[url]) == 0:#If no parameters
			parsed.append(url) #Just add
		else:
			for eachUrl in urls[url]:
				parsed.append(url + "?" +"&".join([X+"="+eachUrl[X] for X in eachUrl]))
	return parsed

def joinParsedPost(urls):
	parsed = []
	for url in urls:
		for eachParam in urls[url]:
			parsed.append([url, "&".join([X+"="+eachParam[X] for X in eachParam])])
	return parsed

def addAllParameters(urlAndParams, url):#A function to take all different parameters of url, remove the duplicate ones, and flag them in dictionary so that they aren't repeated again
	nonRepeated = []#Non repeated params
	for link in url:#For the link,(it would only have a single item so..)
		if link not in urlAndParams:#If that URL isn't in table already
			urlAndParams[link] = {}
		for param in url[link]:#For every group of parameters
			ADDED = False #It hasn't been added
			for eachParam in param:#For every parameter is group of parameters
				if eachParam not in urlAndParams[link]:#If it's hasn't been already added(means it's new)
					urlAndParams[link][eachParam] = True#Flag it as added
					if ADDED: continue #Do not add it again
					ADDED = True#Flag the added param flag as true
					nonRepeated.append(param)#Add it to non repeated list
	return nonRepeated

def mergeParsedGet(mainParsed, newUrls, urlAndParams): #Taking a list of already visited URL's and new hrefs found and returning new ones
	#Also urlAndParams dict which has all the URL's and parameters which have been visited Once
	newlyAdded = {}#A table for new unique url's
	for url in newUrls:#For each in new URL's
		if url not in urlAndParams:#If the base url hasn't been visited
			toAdd = addAllParameters(urlAndParams, {url:newUrls[url]})#Flag all the parameters as visited and remove duplicates
			mainParsed[url] = toAdd#assigning the unique url's
			newlyAdded[url] = toAdd#Adding to newlyAdded also
		else:
			for param in newUrls[url]:#Else for every group of parameters
				ADDED = False #It hasn't been added
				for eachParam in param:#For every parameter in the group
					if eachParam not in urlAndParams[url]:#If not visited
						urlAndParams[url][eachParam] = True #Visited is true
						if ADDED: continue #If already added the param, then just continue
						ADDED = True
						if url not in newlyAdded:#Else if the URL is not in newlyAdded
							newlyAdded[url] = [param]#Then add it
						else:
							newlyAdded[url].append(param)#Else append it
						mainParsed[url].append(param)#Add it to the main List too
	return joinParsedGet(newlyAdded)

def mergeParsedPost(mainParsed, newUrls, urlAndParams):
	for url in newUrls:#For each in new URL's
		if url not in urlAndParams:#If the base url hasn't been visited
			toAdd = addAllParameters(urlAndParams, {url:newUrls[url]})#Flag all the parameters as visited and remove duplicates
			mainParsed[url] = toAdd#assigning the unique url's
		else:
			for param in newUrls[url]:#Else for every group of parameters
				ADDED = False #It hasn't been added
				for eachParam in param:#For every parameter in the group
					if eachParam not in urlAndParams[url]:#If not visited
						urlAndParams[url][eachParam] = True #Visited is true
						if ADDED: continue #If already added the param, then just continue
						ADDED = True
						mainParsed[url].append(param)#Add it to the main List too

def mergeParsedJS(mainParsed, newUrls, urlAndParams):
	for url in newUrls:#For each in new URL's
		if url not in urlAndParams:#If the base url hasn't been visited
			toAdd = addAllParameters(urlAndParams, {url:newUrls[url]})#Flag all the parameters as visited and remove duplicates
			mainParsed[url] = toAdd#assigning the unique url's
		else:
			for param in newUrls[url]:#Else for every group of parameters
				ADDED = False #It hasn't been added
				for eachParam in param:#For every parameter in the group
					if eachParam not in urlAndParams[url]:#If not visited
						urlAndParams[url][eachParam] = True #Visited is true
						if ADDED: continue #If already added the param, then just continue
						ADDED = True
						mainParsed[url].append(param)#Add it to the main List too

def addSlashAfterDomain(url): #A function to handle some domain names like "https://domain.com?param=val", ie with no
	parsed = url.split("?")[0].split("/")#"/" after the domain, which the crawler might not handle properly
	if "?" in url: #If it has parameters
		if len(parsed) <= 3: #if there is not slash after domain name
			return "/".join(parsed) + "/" + "?" + "?".join(url.split("?")[1:])
	else:
		if len(parsed) <= 3:
			return url+"/"
	return url

def getCurrentPath(url): #Getting current path of domain, like if file is "https://xy.com/lol/file.php", it will return "https://xy.com/lol/"
	if url.endswith("/"): return url
	return "/".join(url.split("#")[0].split("?")[0].split("/")[:-1])+"/"

def getCurrentDomain(url): #returning the current domain(includes subdomain)
	return url.split("/")[2]

def getMainDomain(url): #returning current main domainn only
	return url.split("/")[2].split(".")[-2]

def expandLink(link, baseDomain, basePath, sslValue): #Expands a href into a full
	link = link.lstrip()
	if link.startswith("http://") or link.startswith("https://"):
		return link
	if link.startswith("./"):
		link = link[2:]
		return basePath+link
	if link.startswith("//"):
		link = sslValue + link[2:]
		return link
	if link.startswith("/"):
		link = sslValue+baseDomain+link
		return link
	return basePath+link

def notValid(href):#Checks if a href is valid or not
	return href.startswith("javascript:") or href.startswith("mailto:") or href.startswith("#")

def addAHref(hrefs, url):#Add a href into a list, appending if the url is already there or not
	if "?" in url:
		if url.split("?")[0] not in hrefs:
			hrefs[url.split("?")[0]] = [{X.split("=")[0]: "".join(X.split("=")[1:]) for X in url.split("?")[1].split("&")}]
		else:
			hrefs[url.split("?")[0]].append({X.split("=")[0]: "".join(X.split("=")[1:]) for X in url.split("?")[1].split("&")})
	else:
		hrefs[url] = []

def findAHref(parsedHtml, url, subdomains=False, js=False):#Find's all the ahrefs in a page
	hrefs = {}
	sslValue = "https://" if url.startswith("https://") else "http://"
	baseDomain = getCurrentDomain(url) #Current domain
	mainDomain = getMainDomain(url)#Main Domain
	basePath = getCurrentPath(url)#Current path
	for a in parsedHtml.find_all('a'):#For every a tag
		try:
			aVal = a.get('href')#Get the href value
			if notValid(aVal): continue#If not valid, then continue
			aVal = expandLink(aVal,baseDomain, basePath, sslValue)#Else expand it
			if subdomains:#If subdomains allowed
				domain = getMainDomain(aVal)#Get main domain
				if domain == mainDomain:
					addAHref(hrefs,addSlashAfterDomain(aVal.split("#")[0]))
			else:
				domain = getCurrentDomain(aVal)
				if domain == baseDomain:
					addAHref(hrefs,addSlashAfterDomain(aVal.split("#")[0]))
		except:
			continue

	return hrefs

def findJs(parsedHtml, url, subdomains=False, js=False):#Find's all the ahrefs in a page
	jscript = {}
	sslValue = "https://" if url.startswith("https://") else "http://"
	baseDomain = getCurrentDomain(url) #Current domain
	mainDomain = getMainDomain(url)#Main Domain
	basePath = getCurrentPath(url)#Current path
	if js:
		for src in parsedHtml.find_all('script'):#For every a tag
			try:
				aVal = src.get('src')#Get the href value
				if aVal is None: continue#If not valid, then continue
				aVal = expandLink(aVal,baseDomain, basePath, sslValue)#Else expand it
				if subdomains:#If subdomains allowed
					domain = getMainDomain(aVal)#Get main domain
					if domain == mainDomain:
						addAHref(jscript,addSlashAfterDomain(aVal.split("#")[0]))
				else:
					domain = getCurrentDomain(aVal)
					if domain == baseDomain:
						addAHref(jscript,addSlashAfterDomain(aVal.split("#")[0]))
			except:
				continue
	return jscript

def addForm(postF, formInputs, url):#Add a form into a dict
	if url not in postF:
		postF[url] = [formInputs]
	else:
		postF[url].append(formInputs)

def findForms(parsedHtml, url, subdomains=False):#Find's all the forms in a webpage, GET and POST both and then add them in a list
	postF = {}#Dict for POST fomrms
	getF = {}#Dict for GET forms
	sslValue = "https://" if url.startswith("https://") else "http://"
	baseDomain = getCurrentDomain(url) #Current domain
	mainDomain = getMainDomain(url)#Main Domain
	basePath = getCurrentPath(url)#Current path
	for a in parsedHtml.find_all('form'):#Find's all forms
		try:
			formAction = a.get('action')#The forms action
			if notValid(formAction): continue#Invalid, then quit
			formInputs = {}
			for inp in a.find_all('input', attrs={'name': True}):#For all inputs in forms
				if inp.get('value') is None or inp.get('value') is "":#If value is None, or ""
					formInputs[inp['name']] = "XXX"#Then value is "XXX"
				else:
					formInputs[inp['name']] = inp['value']#Else the value described
			if len(formInputs) == 0:
				continue
			formAction = expandLink(formAction,baseDomain, basePath, sslValue)#Expands the form's action
			if subdomains:#If subdomains allowed
				domain = getMainDomain(formAction)
				if domain == mainDomain:#If domains match
					if a.get('method') == None or a.get('method').lower() != "post":#If action is None or GET
						addForm(getF,formInputs,addSlashAfterDomain(formAction.split("#")[0]))#Add get form
					else:
						addForm(postF,formInputs,addSlashAfterDomain(formAction.split("#")[0]))#Else add POST form
			else:
				domain = getCurrentDomain(formAction)
				if domain == baseDomain:
					if a.get('method') == None or a.get('method').lower() != "post":
						addForm(getF,formInputs,addSlashAfterDomain(formAction.split("#")[0]))
					else:
						addForm(postF,formInputs,addSlashAfterDomain(formAction.split("#")[0]))
		except:
			continue
	return postF,getF

def findAllValues(s,url, subdomains=False, js=False): #Extracting all <a> tags from a response, and parsing them
	try:
		parsedHtml = BeautifulSoup(s.get(url, timeout=5).text, "lxml")#Extracting a tags
	except:
		return [],[],[]
	aHrefs = findAHref(parsedHtml, url,subdomains,js)#Get all a hrefs
	postForm,getForm = findForms(parsedHtml, url, subdomains)#Get all POST and GET forms
	jscripts = findJs(parsedHtml,url, subdomains, js)
	return aHrefs,getForm,postForm,jscripts

def normalizeUrl(url):#Find's if url is accessible with https or not
	if url.startswith("https://") or url.startswith("http://"):
		return url
	try:
		requests.get("https://"+url, timeout=5)
		return "https://"+url
	except:
		return "http://"+url

def isUp(url):#Check if site is up or not
	try:
		requests.get(url)
		return True
	except:
		return False

def isExcluded(excluded, url):
	for url1 in excluded:
		if url in url1:
			return True
	return False

def crawl(s,baseUrl, depth=3, subdomains=False, Debug=False, excluded=[],js=False):#The main crawler
	excluded = [X.split("?")[0] for X in excluded]
	baseUrl =  normalizeUrl(addSlashAfterDomain(baseUrl.lower()))#A simple bfs type approach
	if not isUp(baseUrl):
		print "Unable to crawl %s, site is down"%(baseUrl)
		return ([],[])
	print "Crawling: %s\n"%(baseUrl)
	queueU = [baseUrl]#A queue with a type of bf implementation for crawling
	urlParsedGet = {}#All the unique url's and parameters GET
	urlParsedJs = {}#All the unique url's and parameters JS
	urlAndParamsGet = {}#The url's with a dict of their parameters which have been found GET
	urlParsedPost = {} #POST
	urlAndParamsPost = {} #POST
	for m in range(depth):#Going to a certain depth
		print "\nDepth %d of crawling\n"%(m+1)
		if len(queueU) == 0:#If no urls are left
			break
		newQueue = []#The next level of bfs
		for url in queueU:#For every url
			if isExcluded(excluded, url):
				continue
			if Debug:
				print "Sending request to %s"%url
			getUrl,getForm,PostForm,getJs = findAllValues(s,url,subdomains,js)#Gets the hrefs, get and post forms
			newGet = mergeParsedGet(urlParsedGet, getUrl, urlAndParamsGet)#Add the new a-hrefs and returns unique ones
			newGet += mergeParsedGet(urlParsedGet, getForm, urlAndParamsGet)#For GET forms too
			mergeParsedPost(urlParsedPost,PostForm,urlAndParamsPost)#Add the POST forms
			mergeParsedJS(urlParsedJs,getJs,urlAndParamsPost)#Add the POST forms
			newQueue += newGet
			if Debug:
				print "%d new unique URL's found"%(len(newGet))
		queueU = newQueue
	return joinParsedGet(urlParsedGet),joinParsedPost(urlParsedPost),urlParsedJs
