from website_crawler.utils import data_finder  # imports data_finder.py from utils
from website_crawler.utils import file_handler  # imports file_handler.py from utils
from website_crawler.utils import web_domain  # import web_domain.py from utils

""" WebScraper class responsible for finding links and various types of data inside webpage using regular expressions
"""


class WebScraper:

    def __init__(self, domain_name, page_url, depth):
        self.domain_name = domain_name
        self.page_url = page_url
        self.depth = depth

        self.link_set = set()       # set to store crawled links
        self.email_set = set()      # set to store crawled emails
        self.phone_set = set()      # set to store crawled phone numbers
        self.user_set = set()       # set to store crawled user-defined (sensitive) data
        self.misc_set = set()       # set to store crawled (miscellaneous) links such as images and scripts.

        self.__html_page = web_domain.get_html_response(page_url)  # get full html code string from a webpage
        self.__download_html_page()   # download html (web) page and write to a html file

    def __download_html_page(self):
        file_handler.create_html_files(self.domain_name, self.depth, self.__html_page)
        pass

    def get_webpage_links(self):
        link_counter = 0
        if len(self.__html_page) > 0:
            for url in data_finder.get_url_list(self.__html_page):  # list of all links/href tags found in html page
                link = web_domain.get_absolute_url(self.page_url, url)  # parse to full page url in case of relative url

                self.handle_links_to_sets(link)

                link_counter += 1
            print("[%i] Links found" % link_counter)
        return self.link_set

    def handle_links_to_sets(self, link):
        link_attrs = ("mailto:", "tel:", "javascript:")
        misc_formats = (".png", ".svg", ".ico", ".css", ".json")

        if web_domain.get_protocol(link) in link_attrs:
            self.handle_link_attributes(link)
        elif web_domain.get_href_format(link) in misc_formats:
            self.misc_set.add(link)
        else:
            self.link_set.add(link)

    def handle_link_attributes(self, link):
        # html attributes for various hyperlinks (href)
        link_attrs = ("mailto:", "tel:", "javascript:")

        if link.startswith(link_attrs[0]):  # href = mailto:
            email = link.replace(link_attrs[0], "")
            self.email_set.add(email)
            # print(link_attrs[0], link)
            return
        elif link.startswith(link_attrs[1]):  # href = tel:
            phone_number = link.replace(link_attrs[1], "")
            if len(phone_number) < 15:
                self.phone_set.add(phone_number)
            else:
                self.misc_set.add("(href) tel: " + phone_number)
            # print(link_attrs[1], link)
            return
        elif link.startswith(link_attrs[2]):  # href = javascript:
            # todo: check to get onclick links in js
            self.misc_set.add(link.replace(link_attrs[2], ""))
            # print(link_attrs[2], link)
            return

    def get_emails(self):
        # uses regex to find all emails in the html page
        emails = data_finder.get_found_emails(self.__html_page)

        # loop and add each email found with regex to the set of emails which contains emails gathered from hyperlinks
        for email in emails:
            self.email_set.add(email)  # disregards duplicates when adding to set

        return self.email_set

    def get_phone_numbers(self):
        # uses regex to find all phone numbers in the html page
        phone_numbers = data_finder.get_found_phone_numbers(self.__html_page)
        unwanted_phone_numbers = ("", "+47")
        for numbers in phone_numbers:
            for number in numbers:
                # print("PHONE NUMBER: %s ; %i" % (number, len(number)))
                if number not in unwanted_phone_numbers:
                    self.phone_set.add(number)
        return self.phone_set

    def get_special_data(self, user_regex):
        user_set = data_finder.get_found_special_data(self.__html_page, user_regex)
        for data in user_set:
            self.user_set.add(data)
        return self.user_set

    def get_source_comments(self, depth):
        html_file_path = "<crawler_files/%s/webpage_%i.html>" % (self.domain_name, depth)
        # uses regex to find all comments inside in the html (source code) page
        source_comments = data_finder.get_found_html_comments(self.__html_page)
        return html_file_path, source_comments

    def get_miscellaneous(self):
        return self.misc_set
