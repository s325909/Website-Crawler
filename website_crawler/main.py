from web_crawler import WebCrawler  # import WebCrawler class from web_crawler.py

# the start URL of the web crawling
start_url = "https://www.oslomet.no"

# the (max) depth of the crawling
max_depth = 17   # how many webpages to crawl

# user-defined regular expression to find special data within a (text-formatted) html page - can be any and all regex
user_regex = r'<\!\-\-(?:.)*?-->'  # regex to find single-line comments ("<!-- this is a comment -->") within html page


# make crawler instance by providing a start url, depth of how many webpages to crawl, and a regex to find special data
crawler = WebCrawler(start_url, max_depth, user_regex)

# download each webpage and write to html file whilst crawling (optional)
crawler.set_download_webpages()

# call crawler functions that uses regular expressions to find various data whilst crawling each web page (optional)
crawler.set_find_emails()           # uses (pre-defined) regex to find emails whilst crawling
crawler.set_find_phone_numbers()    # uses (pre-defined) regex to find (norwegian) phone numbers whilst crawling
crawler.set_find_comments()         # uses (pre-defined) regex to find comments inside source code whilst crawling
crawler.set_find_special_data()     # uses (user-defined) regex to find special data whilst crawling
crawler.set_find_word_dictionary()  # uses bs4 module to find/count the words that are used inside each crawled webpage

# function that prints found links and various data (sets) found whilst crawling each web page (optional)
crawler.set_show_found_data()   # prints the found data for each webpage whilst crawling (emails, numbers, etc.)
# crawler.set_show_queue_and_crawled()    # prints found urls (crawler queue + crawled links) whilst crawling
# crawler.set_show_misc_links()   # prints found miscellaneous (href) links (external websites, images, scripts, etc.)
# crawler.set_show_comments()
crawler.set_show_most_common_words(25)

# function to commence crawling website - found urls (with same domain name) are added to crawler queue (/queue.txt)
crawler.commence_crawling()  # uses (pre-defined) regex to find hyperlinks (href) inside html <anchor tags> by default
