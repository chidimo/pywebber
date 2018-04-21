# pywebber

Python Web Development Tools

![Alt text](https://img.shields.io/badge/py__webber-stable-blue.svg)

## Utilities

1. Link and words harvester [Ripper](https://pywebber.readthedocs.io/en/latest/#pageripper)

1. Text generator [LoremPysum](https://pywebber.readthedocs.io/en/latest/#lorempysum)

## Installation

    pip install pywebber --upgrade
    pip install https://github.com/Parousiaic/pywebber/archive/master.zip

## Usage

### Ripper - harvest words and links on a static web page.

    $ from pywebber import Ripper

Access words and links is easy

    $ page = Ripper('http://python.org')
    $ soup = page.soup
    $ uncleaned_links = page.raw_links # all raw <a> tags on page as bs4 objects
    $ cleaned_links = page.links() # generator of all links in the form `http://www.domain.location`
    $ words = page.words() # a generator of words between <p> tags

The following instance creation options are available

1. `url` : Default to `url="http://python.org"`
1. `parser` : Default to `parser="html.parser"`. To see a complete list of parsers, user `object_instance.parsers`
1. `refresh`: Default to `refresh=False`. The first time `Ripper` hits a page, it saves the scrapped content in a text file from
 which consequent calling of the class reads. But if set to `True`, `Ripper` will hit the site to get its data
construct its object each time its called.
1. `save_path` : Default to `save_path=None`. In this case, `Ripper` creates a folder on your `USER DESKTOP`. This folder name
 is in the format `domainName_extension`. Every page scrapped from that site is saved inside this foler. Its also possible to
set `save_path=/some/other/path`. The save file name is of the format `page_url.txt`
1. `split_string` : Defaults to `string.punctuation.extend(["n", " ", "://",])`. You can supply a list to add to this set.
1. `stop_words` : Defaults to `['', '#', '\n', 'the', 'to', "but", "and"]`. These are words that should not be included when
`object_instance.words()` is called. You can supply a list to add to this set.

### LoremPysum - Generate random texts

    $ from pywebber import LoremPysum

Create a single LoremPysum instance with default Lorem Ipsum text

    $ p = LoremPysum(*args, domains=None, lorem=True)

You can also decide to include your words with the standard lorem ipsum text. But if you want your words only simply pass `lorem=False` like this ::

    $ p = LoremPysum(*args, domains=None, lorem=False)

`*args` is an optional list of files from which to get the words to be used. Just pass any number of text files as shown below

    $ p = LoremPysum("file1_path.txt1", "file2_path.txt", domains=None, lorem=True)

The following methods are defined

    $ p.email() # return a single email address. You could pass in a file for list of domains. Defaults are `[".com", ".info", ".net", ".org"]`
    $ p.name() # return a name in the form "firstname I. lastname".
    $ p.sentence() # generate a single sentence.
    $ p.paragraphs() # return a single paragraph of standard Lorem Ipsum text.
    $ p.paragraphs(count=3) # return 3 paragraphs where the first paragraph is the standard text.
    $ p.paragraphs(common=False) # return a single paragraph where the first paragraph is random.
    $ p.title() # generate a string (title case) with 2 to n words. Defaults is 5. Good for article titles.

In case you want to look into the words used, the following instance attributes are defined. ::

    $ p.common # A list of the first few words in the lorem ipsum text
    $ p.words # A list of all the words in the lorem ipsum text.
    $ p.standard # Standard lorem ipsum text. Usually the first 1/3rd portion of a sample file.
    $ p.domains # list of domain name endings

## Code

## Credits

1. [Luca De Vitis](http://loremipsum.readthedocs.io/en/latest/) for the inspiration and starter code for `LoremPysum`
