# SnCrawler

A simple web crawler, written with bug bounties and pentesting in mind and some hacks for smart crawling

-----

# Features

Recursively crawls a given website upto specified depth, extracting all the hrefs of the same domain(or subdomains if speified) 

Finds all the input and POST forms on the crawled webpages too

Supports cookies

Reduces the total number of requests sent by only crawling an unique parameter once(explained below)

----------

# Reason

Of-course there are a lot of other crawlers available on the internet(Burp being the best imo), but they all have the problem of duplicate parameters, which sometimes puts them in a positing of infinite crawling

For eg, All of us bug hunters face URLs like site.com/?id=1, and the ?id parameter can have a huge amount of values, it could go upto ?id=99999 or more. Other crawlers would visit every single of those pages, treating each of them as a unique URL, which sometimes might generate a shitload of traffic, and an infinite crawling(which slows down overall crawling).

For that specific reason, I wrote this crawler which will detect duplicate parameters, and only visit a unique parameter once. Thus, it can crawl very large websites in a matter of minutes.

-------

# Aim

The main aim for this crawler is to gather as many GET and POST parameters, in a shortest amount of time. It does this by reducing the amount of URLs it has to visit by only visiting unique parameters,thus reducing the total URL's to crawl exponentially

---

# Installation

Just clone this repo, and then install the requirements
`git clone https://github.com/drigg3r/SnCrawler.git`
`cd SnCrawler/`
`pip install -r requirements.txt`

# TODO

Format the output, so that the crawled URL's are displayed beautifully

PS: This is still in beta and I am still testing it, any feedbacks or bugs/issues will be appreciated. It is actually a part of the web fuzzing suite i am currently working on, but i thought to release this crawler as a standalone tool too, as this might be helpfull to a lot of people :)
