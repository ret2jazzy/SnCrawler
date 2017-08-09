# SnCrawler

A simple web crawler, written with pentesting in mind and some hacks for smart crawling

-----

# Features

Recursively crawls a given website upto specified depth, extracting all the hrefs of the same domain(or subdomains if specified) 

Finds all the input and POST forms on the crawled webpages

Supports cookies

Reduces the total number of requests sent by only crawling an unique parameter once(explained below)

exclude/include subdomains

----------

# Reason

Of-course there are a lot of other crawlers available on the internet(Burp being the best imo), but they all have the problem of duplicate parameters, which sometimes puts them in a positing of infinite crawling

For eg, All of us have to face URLs like site.com/?id=1, and the ?id parameter can have a huge amount of values, it could go upto ?id=99999 or more. Other crawlers would visit every single of those pages, treating each of them as a unique URL, which sometimes might generate a shitload of traffic, and an infinite crawling(which slows down overall crawling).

For that specific reason, I wrote this crawler which will detect duplicate parameters, and only visit a unique parameter once. Thus, it can crawl very large websites in a matter of minutes.

-------

# Aim

The main aim for this crawler is to gather as many GET and POST parameters, in a short amount of time. It does this by reducing the amount of URLs it has to visit by only visiting unique parameters,thus reducing the total URL's to crawl exponentially

---

# Installation

Just clone this repo, and then install the requirements(or run the following commands)

```
git clone https://github.com/drigg3r/SnCrawler.git

cd SnCrawler/

pip install -r requirements.txt
```

-----

# Usage

To look at all the available options, just run the file with `--help`

```
$ python SnCrawl.py --help
usage: SnCrawl.py [-h] [-w "https://domain.com/"] [-d DEPTH]
                  [-c "cooke1=val1; cookie2=val2"] [--subdomains]
                  [-e "http://domain.com/logout"] [-v]
                  [-o /home/user/saveLocation.txt]

optional arguments:
  -h, --help            show this help message and exit
  -d DEPTH, --depth DEPTH
                        How many layers deep to crawl(defaults to 3)
  -c "cooke1=val1; cookie2=val2", --cookie "cooke1=val1; cookie2=val2"
                        The cookies to use(if doing authenticated crawling)
  --subdomains          To include subdomains
  -e "http://domain.com/logout", --exclude "http://domain.com/logout"
                        The url to exclude from being crawled(like logout
                        page)
  -v, --verbose         To display verbose output
  -o /home/user/saveLocation.txt, --output /home/user/saveLocation.txt
                        The output file where you want to write the scraped
                        URL's(in Json)

required arguments:
  -w "http(s)://domain.com/", --website "http(s)://domain.com/"
                        The website you want to crawl
```

Here is how you can do a simple scaping of a website with the depth 2

```
python SnCrawler.py --website "http://domainToCrawl.com" --depth 2
```

You can also specify if you want to include subdomains, by `--subdomains` argument

```
python SnCrawler.py -w "http://domainToCrawl.com" --subdomain   #It will also crawl the subdomains now
```

By Default, it will display all the scraped URL's and POST parameters on the terminal itself, which can get pretty messy sometimes(especially for larger sites). 

To cope with that, we have a `-o` option, which will write all the scraped URLs in the specified output file in Json(for easier parsing during later use).

```
python SnCrawler.py --website "http://domainToCrawl" -o "/home/user/output.txt"  #Will write all URLs to /home/user/out.txt
```

For cookies, you can specify the `-c` option. You can directly copy them from burp( or any other intercepting proxy )

```
python SnCrawler.py -w "https://domainToCrawl.com" -c "cookie1=val1 ; cookie2=val2"  #Will send all requests with the cookie values
```

Sometimes, there would some URL's you wouldn't want the crawler to visit, like logout pages which might destroy your session. You can specify them with `-e` option. For multiple URLs, you can specify `-e` multiple times

```
python SnCrawler.py -w "http://domainToCrawl.com" -c "cookie1=val1;" -e "http://domainToCrawl/logout" -e "http://domainToCrawl/destroy"   #It will not send request to both of these URLs
```

You can use the `-v` flag for displaying verbose output of every request being sent and data being parsed

```
python SnCrawler.py -w "http://domainToCrawl.com" -v  #will display verbose information about every request being sent
```

----

# TODO

Format the output, so that the crawled URL's are displayed beautifully

Implement multithreading

PS: This is still in beta and I am still testing it, any feedbacks or bugs/issues will be appreciated. It is actually a part of the web fuzzing suite i am currently working on, but i thought to release this crawler as a standalone tool too, as this might be helpfull to a lot of people :)

For any questions/issues, you can also hit me up on twitter @ret2got
