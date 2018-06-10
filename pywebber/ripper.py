"""Create a BeautifulSoup object of a webpage"""

import os
import sys
import re
import time
import codecs
import string
import unicodedata

import requests
from requests.exceptions import MissingSchema, InvalidSchema
from bs4 import BeautifulSoup
from utils import unique_everseen

class Ripper:
    """Harvest words and links from a webpage

    Parameters
    ----------

    str
        Page url. Default is 'http://python.org'

    int
        parser. Default value is 'html.parser'. Others are 'html5lib' and 'lxml'

    Notes
    ------

    Usage:

    1. Ripper("http://python.org").soup
    2. Ripper("http://python.org").raw_links
    3. Ripper("http://python.org").links()
    4. Ripper("http://python.org").words()
    """
    def __init__(self, url="http://python.org", parser="html.parser", refresh=True, save_path=None, stop_words=None, split_string=None):
        """__init__
        Parameters
        -----------
        bool : refresh
            Specifies if page should be read from source. Defaults to True
        str : save_path
            Specifies folder to save the text file of scraped page
        list : stop_words
            A list of words to not include in the output of words()
        list : split_string
            A list of strings with which to split the words on the page
        """
        self.url = url#.strip()
        self.split_string = self.word_splitters(split_string)
        self.stop_words = self.stop_words(stop_words)
        self.refresh = refresh
        self.parser = parser
        if save_path:
            self.save_path = save_path
        else:
            self.save_path = self.get_save_path()

        try:
            req_text = requests.get(self.url, timeout=(10.0, 10.0)).text
        except MissingSchema:
            raise MissingSchema("url should be in the form <http://domain.extension>")
        except InvalidSchema:
            raise InvalidSchema("Your url, {}, has an invalid schema".format(self.url))

        if self.refresh:
            self.soup = BeautifulSoup(req_text, self.parser)
            self.save_page(self.soup, self.get_save_path())
        else:
            try:
                with open(self.get_save_path(), 'r+') as rh:
                    self.soup = BeautifulSoup(rh.read(), self.parser)
            except FileNotFoundError:
                raise FileNotFoundError("File may have been moved. Try again with 'refresh=True'")
        self.raw_links = self.soup.find_all('a', href=True)

    def __str__(self):
        return "Rip: {}".format(self.url)

    @staticmethod
    def simple_slugify(value):
        value = unicodedata.normalize('NFKD', value).encode('ascii', 'ignore').decode('ascii')
        value = re.sub(r'[^\w\s-]', '_', value).strip().lower()
        return re.sub(r'[-\s]+', '-', value)

    @staticmethod
    def save_page(soup, file_name):
        file_name += '.txt'
        with codecs.open(file_name, 'w+', encoding='utf-8') as fh:
            fh.write(soup.prettify())

    @staticmethod
    def word_splitters(split_string):
        """Get a list of words for splitting scraped results"""
        splitters = [each for each in string.punctuation]
        splitters.extend(["n", " ", "://",])
        if split_string:
            splitters.extend(self.split_string)
        return "[{}]".format(" ".join(splitters))

    @staticmethod
    def stop_words(word_list):
        stop_words = ['', '#', '\n', 'the', 'to', "but", "and"]
        if word_list:
            stop_words.extend(word_list)
        return stop_words

    def get_save_path(self):
        # set save directory
        DESKTOP = os.path.abspath(os.path.abspath(os.path.expanduser('~')) + '/Desktop/')
        FILE_DIR = os.path.join(DESKTOP, self.get_site_folder_name())

        if os.path.exists(FILE_DIR) is False:
            os.mkdir(FILE_DIR) # create save directory
        return os.path.join(FILE_DIR, self.simple_slugify(self.url))

    def get_site_folder_name(self):
        """This prevents the program from even getting to the MissingSchema part"""
        try:
            folder = self.url.split("://")[1]
            folder = folder.split(".")
            site = folder[0]
            ext = folder[1].split("/")[0]
            return "{}_{}".format(site, ext)
        except IndexError:
            raise IndexError("Your url schema is not complete.\nPlease include the <http://> part")

    def links(self):
        """Return all crawlable links (clickable url) on webpage

        Parameters
        ----------

        Yields
        ------
        str
            Clickable url

        Notes
        ------
        Links with "#" are excluded
        """
        links = self.raw_links
        if links == []:
            return None

        link_refs = [link.get('href') for link in links]

        unique_links = filter(lambda x: '#' not in x, link_refs)
        links = []
        for each_link in unique_links:
            if each_link.startswith('http'):
                links.append(each_link)
            else:
                links.append(self.url + each_link)
        return set(links)

    def words(self):
        """Harvest all words enclosed in <p> tags in webpage source

        Yields
        -------
        str
            Single word which is not in list of excluded words
        """
        if self.soup is None:
            return None

        paragraphs = self.soup.find_all('p')
        # header_text = [self.soup.find_all("h{}".format(i)) for i in range(1, 7)]

        if paragraphs == []:
            return None
        all_words = [each.text for each in paragraphs]
        paragraph_text = ' '.join(all_words)
        # text_all_page = self.soup.get_text()

        words = [word.lower().strip() for word in re.split(self.split_string, paragraph_text) if word not in self.stop_words]

        for each_word in unique_everseen(words): # unique words
            yield each_word
