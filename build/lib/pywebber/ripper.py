"""Create a BeautifulSoup object of a webpage"""

import os
import sys
import re
import time
import codecs
import string
import requests
import requests.exceptions as rqe
from bs4 import BeautifulSoup
from .utils import unique_everseen

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
    def __init__(
        self, url="http://python.org", parser="html.parser", refresh=False, save_path=None,
        stop_words=None, split_string=None):
        self.url = url
        self.datetime = time.strftime('%Y-%m-%d')
        self.refresh = refresh
        self.conn_time_out = 10.0
        self.read_time_out = 10.0
        self.parser = parser
        self.parsers = ['html.parser', 'html5lib', 'lxml', 'lxml-xml']
        self.reference = 'https://www.crummy.com/software/BeautifulSoup/bs4/doc/'

        default_splitters = [each for each in string.punctuation]
        default_splitters.extend(["n", " ", "://",])
        if split_string is None:
            self.split_string = self.make_split_string(default_splitters)
        else:
            self.split_string = self.make_split_string(split_string.extend(default_splitters))

        self.stop_words = ['', '#', '\n', 'the', 'to', "but", "and"]
        if stop_words is None:
            pass
        else:
            self.stop_words.extend(stop_words) # add more stop words

        if save_path is None:
            DESKTOP = os.path.abspath(
                os.path.abspath(os.path.expanduser('~')) + '/Desktop/')
            self.FILE_DIR = os.path.join(DESKTOP, self.site_name())
        else:
            self.FILE_DIR = save_path

        try:
            os.mkdir(self.FILE_DIR) # create save directory
        except FileExistsError:
            pass

        try:
            page = requests.get(self.url, timeout=(self.conn_time_out, self.read_time_out))
            self.req_text = page.text
        except rqe.MissingSchema:
            print("Please check your url format.\nIt should be in the form <http://something.extension>")
            return None
        except rqe.InvalidSchema:
            try:
                with open(self.url, "r+") as rhand:
                    self.req_text = rhand.read()
            except OSError:
                print("Your url schema is invalid.\nPlease check your url".format(self.url))
                return

        if refresh is False:
            self.from_source = False
            try:
                with open(self.page_save_path(), 'r+') as rh:
                    self.soup = BeautifulSoup(rh.read(), self.parser)
            except FileNotFoundError:
                self.from_source = True
                self.soup = BeautifulSoup(self.req_text, self.parser)
                self.save_page()
        else:
            self.soup = BeautifulSoup(self.req_text, self.parser)
            self.save_page()
            self.from_source = True

        self.raw_links = self.soup.find_all('a', href=True)

    def __str__(self):
        return "Rip: {}".format(self.url)

    def make_split_string(self, split_string):
        str_format = ["\{}".format(each) for each in split_string]
        return "[{}]".format(" ".join(str_format))

    def site_name(self):
        folder = self.url.split("://")
        try:
            folder = folder[1].split(".")
            site = folder[0]
            ext = folder[1].split("/")[0]
            return "{}_{}".format(site, ext)
        except IndexError:
            print("Your url schema is not complete.\nPlease include the <http://> part")
            sys.exit()

    def page_save_path(self):
        name = [each for each in re.split(self.split_string, self.url) if each != '']
        name = "_".join(name) + "_" + self.datetime + ".txt"
        save_path = os.path.join(self.FILE_DIR, name)
        return save_path

    def save_page(self):
        file_name = self.page_save_path()
        with codecs.open(file_name, 'w+', encoding='utf-8') as fh:
            fh.write(self.soup.prettify())

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
        for each_link in unique_links:
            if each_link.startswith('http'):
                yield each_link
            else:
                yield self.url + each_link

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

