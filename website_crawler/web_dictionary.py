from bs4 import BeautifulSoup as bSoup
from collections import Counter
from website_crawler.utils.data_finder import remove_string_punctuations
from website_crawler.utils.web_domain import open_web_page

""" WebDictionary class responsible for making word dictionary and counting word occurrences on the crawled websites
"""


class WebDictionary:

    def __init__(self, url):
        self.url = url

        # use method from web_domain.py to open and parse url
        self.web_page = open_web_page(self.url)

        # dictionary to add and count each word used on a webpage
        self.word_occurrences = {}

    def get_word_occurrences(self):
        # returns empty dictionary if webpage (string) is empty - could not open url and establish connection
        if not self.web_page:
            return self.word_occurrences

        # parse and get clean (readable) text from web page using BeautifulSoup
        soup = bSoup(self.web_page, 'html.parser')
        self.__get_clean_soup(soup)

        # print(soup.get_text())

        words = "".join(s for s in soup.get_text() if not s.isdigit())  # excludes numerical values (numbers)
        for word in words.split():
            # regex method from data_finder.py to remove punctuations from each word
            word = remove_string_punctuations(word.lower())  # method word.lower() returns the lower-cased word

            if 1 < len(word) < 15:
                # add each word to dictionary and count occurrences
                self.word_occurrences[word] = self.word_occurrences.setdefault(word, 0) + 1

        self.delete_empty_keys()

        return self.word_occurrences

    def delete_empty_keys(self):
        for key in list(self.word_occurrences):
            if not key:
                del self.word_occurrences[key]

    def append_word_dictionary(self, dictionary):
        words = Counter(self.word_occurrences)
        dictionary = Counter(dictionary)
        list_of_counts = [words, dictionary]

        total = sum(list_of_counts, Counter())

        # return dict(total)
        return total

    @staticmethod
    def __get_clean_soup(soup):
        """ private (static) method to help remove certain tags from webpage using methods from BeautifulSoup """
        for tag in soup.find_all(['title', 'head', 'meta', 'script', 'style', '[document]']):
            tag.decompose()  # decompose() from BeautifulSoup get rids of all the tags found using find_all()
