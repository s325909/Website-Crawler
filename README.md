# Website-Crawler

Website Crawler, or Web Crawler for short, is a Python program that is able to download websites and capture sensitive data on the site. 

The program takes in a start URL of the web crawling and downloads the website from the provided URL into a HTML file. 
Moreover, identifies links inside the source code and downloads all website subpages (with the same domain) that are linked. 
For the Web Crawler to not crawl indefinite, the program takes in the depth of the crawling, indicating how many jumps must be considered whilst crawling. 
Consequently, the Web Crawler will continue to crawl and download webpages until the maximum number of jumps are not reached, 
or until all gathered links thus far has been crawled. 

To capture and find sensitive data on the website, the program also takes in a user-defined regular expression. 
This is used to find and gather special data whilst crawling each webpage. 
Some additional features also include using pre-defined regular expressions to find email addresses and (Norwegian) phone numbers and create lists of the captured values.
It can also identify comments inside the source code; furthermore, create a list of the most common words used on the crawled websites.
