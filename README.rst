Python Web Development Tools
===============================
Tools to automate common web scraping tasks.

.. image:: https://img.shields.io/badge/py__webber-stable-blue.svg
.. image:: https://img.shields.io/readthedocs/pip/stable.svg
        :alt: Documentation
        :target: (https://pywebber.readthedocs.io/en/latest/)

Provides

1. Link and words gatherer `py_webber.page_ripper.PageRipper`

2. Random text generator `lorem_pysum.LoremPysum`

Installation 
+++++++++++++++
`PyPI <https://pypi.python.org/pypi>`_ or `Github <https://github.com/>`_ ::

    pip install py_webber
    pip install https://github.com/Parousiaic/py_webber/archive/master.zip

Usage
++++++

LoremPysum - Generate random texts
*************************************
Credits to `Luca De Vitis <http://loremipsum.readthedocs.io/en/latest/>`_ for the inspiration and starter code

Import the class ::

    from py_webber import LoremPysum

Create a single LoremPysum instance with default Lorem Ipsum text ::

    p = LoremPysum(*args, domains=None, lorem=True)

You can also decide to include your words with the standard lorem ipsum text. But if that is not the case simply pass `lorem=False` like this ::
    
    p = LoremPysum(*args, domains=None, lorem=False)

`*args` is an optional list of files from which to take the words to be used. Just pass any number of text files::

    p = LoremPysum("file.txt1", "file2.txt", domains=None, lorem=True)

The following methods are defined. ::

    p.email() # return a single email address. You could pass in a file for list of domains. Defaults are `[".com", ".info", ".net", ".org"]`
    p.name() # return a name in the form "firstname I. lastname".
    p.sentence() # generate a single sentence.
    p.paragraphs() # return a single paragraph of standard Lorem Ipsum text.
    p.paragraphs(count=3) # return 3 paragraphs where the first paragraph is the standard text.
    p.paragraphs(common=False) # return a single paragraph where the first paragraph is random.
    p.title() # generate a string (title case) with 2 to n words. Defaults is 5. Good for article titles.

In case you want to look into the words used, the following instance attributes are defined. ::

    p.common # A list of the first few words in the lorem ipsum text
    p.words # A list of all the words in the lorem ipsum text.
    p.standard # Standard lorem ipsum text. Usually the first 1/3rd portion of a sample file.
    p.domains # list of domain name endings

PageRipper - gather words and links on a web page.
****************************************************

Import the class ::

    from py_webber import PageRipper

Create page_ripper objects ::

    PageRipper(url) # The dafault url is 'http://python.org'

Access words and links like so ::

    PageRipper('http://python.org').soup
    PageRipper('http://python.org').raw_links # all raw <a> tags on page as bs4 objects
    PageRipper('http://python.org').links() # generator of all links in the form `http://www.domain.location`
    PageRipper('http://python.org').words() # a generator of words between <p> tags

If you wish to write the BeautifulSoup output to file, use codecs ::

    import codecs
    with codecs.open(f_name, 'w+', encoding='utf-8') as whand:
        whand.write(soup.prettify())

Code
++++++++

LoremPysum
**************
.. automodule :: py_webber.lorem_pysum
.. autoclass :: LoremPysum
   :members:

PageRipper
**************
.. automodule :: py_webber.page_ripper
.. autoclass :: PageRipper
   :members:

Indexing
**********
.. automodule :: py_webber.indexing
   :members:
