"""Create a BeautifulSoup object of a webpage"""

import re
import codecs
import requests
import requests.exceptions as rqe
from bs4 import BeautifulSoup
from .utils import unique_everseen

class PageRipper:
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

    1. PageRipper("http://python.org").soup
    2. PageRipper("http://python.org").raw_links
    3. PageRipper("http://python.org").links()
    4. PageRipper("http://python.org").words()
    """
    def __init__(self, url="http://python.org", parser="html.parser"):
        self.url = url
        self.conn_time_out = 10.0
        self.read_time_out = 10.0
        self.split_str = r'[\; \, \* \n \.+\- \( \) - \/ : \? \ — \']'
        self.stop_words = ['', '#', '\n', 'the', 'to'] # add more stop words
        self.parser = parser

        try:
            page = requests.get(self.url, timeout=(self.conn_time_out, self.read_time_out))
            self.req_text = page.text
        except rqe.MissingSchema:
            print("Please check your url format")
            print("It should be in the form <http://something.extension>")
            return None
        except rqe.InvalidSchema:
            try:
                with open(self.url, "r+") as rhand:
                    self.req_text = rhand.read()
            except OSError:
                print("{} does not exist".format(self.url))

        self.soup = BeautifulSoup(self.req_text, self.parser)
        self.raw_links = self.soup.find_all('a', href=True)

    def __str__(self):
        return "PageRipper for {}".format(self.url)

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

        words = [word.lower().strip() for word in re.split(self.split_str, paragraph_text)]

        for each_word in unique_everseen(words): # unique words
            if each_word not in self.stop_words:
                yield each_word
