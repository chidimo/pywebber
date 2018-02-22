"""Indexing functions"""

from .page_ripper import PageRipper

def add_to_index(word_index, word, page_url):
    """Add a word to word index and adds a page url to
    the list of urls associated with that word

    Parameters
    -----------
    word_index : dict
        Index of words
    word : str
        Word to be added to the index
    page_url : str
        url to be added in the list of urls associated with "word"

    Returns
    --------
    dict
        Word index with "word" and "page_url" added/updated.

    Notes
    ------
    This function modifies the input dictionary in-situ (in place)
    """
    if word in word_index:
        if page_url in word_index[word]:
            return
        else:
            word_index[word].append(page_url)
            return
    word_index[word] = [page_url]

def add_page_to_index(word_index, page_url):
    """Add all words found in a webpage to the word index

    Parameters
    -----------
    word_index : dict
        Index of words
    page_url : str
        url from which words are to be extracted

    Returns
    --------
    dict
        Word index with entries added/updated

    Notes
    ------
    Modifies the input dictionary in place
    """
    all_words = PageRipper(page_url).words()
    if all_words is not None:
        for word in all_words:
            add_to_index(word_index, word, page_url)
    