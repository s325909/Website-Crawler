from validators import url as validate_url      # import url from validators module to simply checks if an url is valid
from web_dictionary import WebDictionary        # import class from web_dictionary.py to count word occurrences on page
from web_scraper import WebScraper              # import class from web_scraper.py to find links + data whilst crawling
from website_crawler.utils import file_handler  # import (utils) functions from file_handler.py to handle data files
from website_crawler.utils import utils         # import (utils) functions from util.py to help with clean code
from website_crawler.utils import web_domain    # import (utils) functions from web_domain.py to connect and parse urls

""" WebCrawler class responsible for crawling and jumping from webpage to webpage 
"""


class WebCrawler:
    """ class variables (shared among all instances) """
    user_regex = r''
    max_jump, max_word = 0, 10

    # variables to store name of domain and crawler files ("queue" and "crawled") - declare using function from utils.py
    domain, queue_file, crawled_file = utils.init_variables("string", 3)  # declare each variable as empty strings ""

    # variables to check conditions and enable features - use function from util.py to declare each (boolean) variable
    download_webpage, show_data, show_links, show_words, show_misc = utils.init_variables("false", 5)  # == False
    find_email, find_phone, find_comment, find_user_data, find_dictionary = utils.init_variables("false", 5)

    # sets to store the various links and data found while crawling each webpage; each (set) variable declared as set()
    queue_set, crawled_set, email_set, phone_set, comment_set, user_set, misc_set = utils.init_variables("set", 7)

    # dictionary to store words + occurrences found on crawled web pages
    web_dictionary, word_occurrences = {}, {}

    # private (string) variable to separate found data into print blocks whilst crawling
    __block_print = "-" * 179

    def __init__(self, start_url, max_depth, user_regex):
        self.base_url = start_url
        self.max_depth = int(max_depth)
        self.user_regex = str(user_regex)

        self.valid_url = True
        self.domain_name = ""
        self.boot()

    def boot(self):
        """ this function checks if the provided url is valid and creates a dedicated directory/folder for the crawler
        inside the directory, two data files ("queue" and "crawled") are created in which to store the urls found
        and keep track of which url to crawl (next) and which urls that have already been crawled.
        corresponding sets for the "queue" and "crawled" files are also created for the program to use while crawling
        """
        if validate_url(self.base_url):  # url method from the validators module; returns true if the string is url
            # create dedicated crawler directory/folder using the domain name
            WebCrawler.domain = str(web_domain.get_domain(self.base_url))  # function to get domain name from url
            self.domain_name = WebCrawler.domain.split(".")[0]
            file_handler.create_website_dir(self.domain_name)

            # create crawler (data) files to store urls - queue and crawled web pages
            file_handler.create_data_files(self.domain_name, self.base_url)
            WebCrawler.queue_file = file_handler.get_queue_file_path(self.domain_name)
            WebCrawler.crawled_file = file_handler.get_crawled_file_path(self.domain_name)

            # create sets for queue and crawled urls from corresponding data files
            WebCrawler.queue_set = file_handler.file_to_set(WebCrawler.queue_file)
            WebCrawler.crawled_set = file_handler.file_to_set(WebCrawler.crawled_file)
        else:
            WebCrawler.valid_url = False
            print("Invalid URL provided!")

    def commence_crawling(self):
        jump = 0
        if self.valid_url:
            WebCrawler.user_regex = self.user_regex  # assign user_defined regex to class variable
            WebCrawler.max_jump = self.max_depth  # assign max_depth to class variable
            while jump < WebCrawler.max_jump:
                jump += 1
                print(WebCrawler.__block_print)

                # function to crawl each web page and find links and data inside the (text-formatted) html
                WebCrawler.crawl_web_page(self.domain_name, jump)

                self.print_crawler_info(jump)

                if len(WebCrawler.queue_set) == 0:
                    print(WebCrawler.__block_print)
                    print("Queue empty - no more webpages left to crawl")
                    break
        else:
            print("Provide a proper (full) URL for the [Web Crawler] program to start crawling")
            return
        # print crawler results showing all found data
        self.print_crawler_results()

    @staticmethod
    def crawl_web_page(domain, jump):

        if len(WebCrawler.queue_set) > 0:
            # get an url from queue set to crawl using .pop() (random)
            webpage = WebCrawler.queue_set.pop()

            print("[{}/{}] Crawling: {}".format(jump, WebCrawler.max_jump, webpage))

            # Instantiate WebScraper class
            scraper = WebScraper(domain, webpage, jump)

            print("------------------------------")

            # add found (URL) links to crawler "queue"
            WebCrawler.add_links_to_queue(scraper.get_webpage_links())

            # add crawled (url) links to "crawled"
            WebCrawler.crawled_set.add(webpage)

            # find additional data inside crawled (html) web page using regular expressions
            WebCrawler.find_crawler_data(scraper, webpage, jump)

            # updates crawler files ("queue" and "crawled") with found links
            WebCrawler.update_crawler_files()
        else:
            print("QUEUE EMPTY - NO MORE WEBPAGES TO CRAWL")
            return

    @staticmethod
    def add_links_to_queue(links):
        for url in links:
            if url in WebCrawler.queue_set:
                continue  # skip if url already exists in queue
            if url in WebCrawler.crawled_set:
                continue  # skip if url has already been crawled
            # add found (url) links to crawler queue - only adds to queue if url has same domain; else adds to misc
            if web_domain.check_domain_link(url, WebCrawler.domain):  # returns true if the url contains the domain name
                WebCrawler.queue_set.add(url)
            else:
                WebCrawler.misc_set.add(url)

    @staticmethod
    def find_crawler_data(scraper, webpage, depth):
        show_data = WebCrawler.show_data
        if WebCrawler.find_email:
            # get a set of found emails - found using pre-defined regex on (text-formatted) html page
            email_set = scraper.get_emails()

            # add emails (if) found to crawler (email) set; disregards duplicates when adding to set
            if len(email_set) > 0:
                for email in email_set:
                    WebCrawler.email_set.add(email)  # add each email found with regex to set; disregards duplicates
                if show_data:
                    WebCrawler.print_found_data("[{}] Emails found:".format(len(email_set)), email_set)
        if WebCrawler.find_phone:
            # get a set of found phone numbers - found using pre-defined regex on html page
            phone_set = scraper.get_phone_numbers()

            # if phone number(s) found - add to crawler (phone) set; disregards duplicates when adding to set
            if len(phone_set) > 0:
                for phone_number in phone_set:
                    WebCrawler.phone_set.add(phone_number)  # add phone number to set
                if show_data:
                    WebCrawler.print_found_data("[{}] Phone numbers found:".format(len(phone_set)), phone_set)
        if WebCrawler.find_comment:
            html_file, comment_set = scraper.get_source_comments(depth)

            # if html comments found - add to crawler (comment) set; disregards duplicates when adding to set
            if len(comment_set) > 0:
                for comment in comment_set:  # add comment to set
                    WebCrawler.comment_set.add((html_file, comment))
                if show_data:
                    WebCrawler.print_found_data("[{}] HTML comments found:".format(len(comment_set)), comment_set)
        if WebCrawler.find_user_data:
            # get a set of found user data - found using user-defined regex on html page
            user_set = scraper.get_special_data(WebCrawler.user_regex)

            # if user data found - add to crawler (user) set; disregards duplicates when adding to set
            if len(user_set) > 0:
                for data in user_set:  # add data to set
                    WebCrawler.user_set.add(data)
                if show_data:
                    WebCrawler.print_found_data("[{}] Special data found:".format(len(user_set)), user_set)
        if WebCrawler.find_dictionary:
            web_dictionary = WebDictionary(webpage)
            words = web_dictionary.get_word_occurrences()

            WebCrawler.word_occurrences = words

            word_dictionary = web_dictionary.append_word_dictionary(WebCrawler.web_dictionary)
            WebCrawler.web_dictionary = word_dictionary

            if show_data:
                WebCrawler.print_found_data("[{}] Word occurrences found:".format(len(words)), words)

        # get a set of found (miscellaneous) links such as images (.png) and (external) links to other domains
        misc_set = scraper.get_miscellaneous()

        # if miscellaneous links/data found - add to crawler (misc) set; disregards duplicates when adding to set
        if len(misc_set) > 0:
            for misc in misc_set:
                WebCrawler.misc_set.add(misc)  # add misc to set
            if WebCrawler.show_data:
                WebCrawler.print_found_data("[{}] Miscellaneous links found:".format(len(misc_set)), misc_set)

    @staticmethod
    def update_crawler_files():
        file_handler.set_to_file(WebCrawler.queue_set, WebCrawler.queue_file)
        file_handler.set_to_file(WebCrawler.crawled_set, WebCrawler.crawled_file)

    # @staticmethod
    def clear_crawler_files(self):
        WebCrawler.queue_set, WebCrawler.crawled_set = set(), set()
        WebCrawler.queue_set.add(self.base_url)
        file_handler.delete_file_contents(WebCrawler.queue_file)
        file_handler.delete_file_contents(WebCrawler.crawled_file)

    @staticmethod
    def print_found_data(print_string, data_set):
        if WebCrawler.show_data:
            print(print_string, data_set)
        else:
            print(print_string)

    def found_data_to_file(self):
        pass

    """ SETTERS """

    @staticmethod
    def set_download_webpages():
        WebCrawler.download_webpage = True

    @staticmethod
    def set_find_emails():
        WebCrawler.find_email = True

    @staticmethod
    def set_find_phone_numbers():
        WebCrawler.find_phone = True

    @staticmethod
    def set_find_comments():
        WebCrawler.find_comment = True

    @staticmethod
    def set_find_special_data():
        WebCrawler.find_user_data = True

    @staticmethod
    def set_find_word_dictionary():
        WebCrawler.find_dictionary = True

    @staticmethod
    def set_show_found_data():
        WebCrawler.show_data = True

    @staticmethod
    def set_show_queue_and_crawled():
        WebCrawler.show_links = True

    @staticmethod
    def set_show_misc_links():
        WebCrawler.show_misc = True

    @staticmethod
    def set_show_most_common_words(param):
        WebCrawler.show_words = True
        WebCrawler.max_word = param

    """ GETTERS """

    def get_user_regex(self):
        return self.user_regex

    @staticmethod
    def get_found_emails():
        return WebCrawler.email_set

    @staticmethod
    def get_found_phone_numbers():
        return WebCrawler.phone_set

    @staticmethod
    def get_found_comments():
        return WebCrawler.comment_set

    @staticmethod
    def get_found_special_data():
        return WebCrawler.user_set

    @staticmethod
    def get_found_words_dictionary():
        return WebCrawler.web_dictionary

    """ CRAWLER PRINTS """

    def print_crawler_info(self, depth):
        print("------------------------------")
        if WebCrawler.show_links:
            print("Queue [{}]: {}".format(len(WebCrawler.queue_set), WebCrawler.queue_set))
            print("Crawled [{}/{}]: {}".format(depth, self.max_depth, WebCrawler.crawled_set))
        else:
            print("[{}] Links in Queue".format(len(WebCrawler.queue_set)))
            print("[{}/{}] Links Crawled".format(depth, self.max_depth))

        if WebCrawler.find_dictionary:
            if WebCrawler.show_data:
                WebCrawler.print_found_data("[{}] Word Dictionary:".format(len(WebCrawler.web_dictionary)),
                                            WebCrawler.web_dictionary)
            else:
                print("[%i] Word Dictionary" % len(WebCrawler.web_dictionary))

    def print_crawler_results(self):
        print(WebCrawler.__block_print + "\n\n\n")
        print(WebCrawler.__block_print + "\nCRAWLER RESULTS:\n" + WebCrawler.__block_print)

        print("[%i] Crawled links: see crawler file <crawler_files/%s/crawled.txt>"
              % (len(WebCrawler.crawled_set), self.domain_name))
        print("[%i] Links in Queue: see crawler file <crawler_files/%s/queue.txt>"
              % (len(WebCrawler.queue_set), self.domain_name))
        print("[%i] Miscellaneous Links:" % len(WebCrawler.misc_set), WebCrawler.misc_set)
        print("[%i] Emails:" % len(WebCrawler.email_set), WebCrawler.email_set)
        print("[%i] Phone Numbers:" % len(WebCrawler.phone_set), WebCrawler.phone_set)
        print("[%i] Special Data:" % len(WebCrawler.user_set), WebCrawler.user_set)

        if len(WebCrawler.comment_set) == 0:
            print("[%i] HTML Comments (inside source code)" % len(WebCrawler.comment_set))

        print("\n[%i] Most Common Words: " % len(WebCrawler.web_dictionary))
        print(WebCrawler.__block_print)

        word_counter = WebCrawler.web_dictionary
        count = WebCrawler.max_word

        if WebCrawler.show_words:
            for i, word in enumerate(
                    sorted(word_counter, key=word_counter.get, reverse=True)[:count]):
                # sorts the dict by the values, from top to bottom, and prints the top values,
                print("%s. %s: %s" % (i + 1, word, WebCrawler.web_dictionary[word]))
            print(WebCrawler.__block_print)

        if len(WebCrawler.comment_set) > 0:
            # print("(%i) Comments:" % len(WebCrawler.comment_set), WebCrawler.comment_set)
            print("\n[%i] HTML Comments (inside source code)" % len(WebCrawler.comment_set))
            print(WebCrawler.__block_print)
            for comments in WebCrawler.comment_set:
                file_path, comment = comments
                print("Comment located inside %s: " % file_path)
                print(comment)
                print(WebCrawler.__block_print)

