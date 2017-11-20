"""
Lorem Pysum: Name, email, title, sentence and paragraph generator
"""

from __future__ import unicode_literals
import string
from random import randint, choice, sample, shuffle

class LoremPysum(object):
    """Generate random sentences and paragraphs

    parameters
    -----------
    *args : any number of text files, optional

    Notes
    ------
    Now updated LoremPysum to take any number of text files as input.

    """

    def __init__(self, *args, domains=None, lorem=True):
        """Docstring"""
        self.lorem_ipsum = [
            'exercitationem', 'perferendis', 'perspiciatis', 'laborum', 'eveniet', 
            'sunt', 'iure', 'nam', 'nobis', 'eum', 'cum', 'officiis', 'excepturi',
            'odio', 'consectetur', 'quasi', 'aut', 'quisquam', 'vel', 'eligendi',
            'itaque', 'non', 'odit', 'tempore', 'quaerat', 'dignissimos',
            'facilis', 'neque', 'nihil', 'expedita', 'vitae', 'vero', 'ipsum',
            'nisi', 'animi', 'cumque', 'pariatur', 'velit', 'modi', 'natus',
            'iusto', 'eaque', 'sequi', 'illo', 'sed', 'ex', 'et', 'voluptatibus',
            'tempora', 'veritatis', 'ratione', 'assumenda', 'incidunt', 'nostrum',
            'placeat', 'aliquid', 'fuga', 'provident', 'praesentium', 'rem',
            'necessitatibus', 'suscipit', 'adipisci', 'quidem', 'possimus',
            'voluptas', 'debitis', 'sint', 'accusantium', 'unde', 'sapiente',
            'voluptate', 'qui', 'aspernatur', 'laudantium', 'soluta', 'amet',
            'quo', 'aliquam', 'saepe', 'culpa', 'libero', 'ipsa', 'dicta',
            'reiciendis', 'nesciunt', 'doloribus', 'autem', 'impedit', 'minima',
            'maiores', 'repudiandae', 'ipsam', 'obcaecati', 'ullam', 'enim',
            'totam', 'delectus', 'ducimus', 'quis', 'voluptates', 'dolores',
            'molestiae', 'harum', 'dolorem', 'quia', 'voluptatem', 'molestias',
            'magni', 'distinctio', 'omnis', 'illum', 'dolorum', 'voluptatum', 'ea',
            'quas', 'quam', 'corporis', 'quae', 'blanditiis', 'atque', 'deserunt',
            'laboriosam', 'earum', 'consequuntur', 'hic', 'cupiditate',
            'quibusdam', 'accusamus', 'ut', 'rerum', 'error', 'minus', 'eius',
            'ab', 'ad', 'nemo', 'fugit', 'officia', 'at', 'in', 'id', 'quos',
            'reprehenderit', 'numquam', 'iste', 'fugiat', 'sit', 'inventore',
            'beatae', 'repellendus', 'magnam', 'recusandae', 'quod', 'explicabo',
            'doloremque', 'aperiam', 'consequatur', 'asperiores', 'commodi',
            'optio', 'dolor', 'labore', 'temporibus', 'repellat', 'veniam',
            'architecto', 'est', 'esse', 'mollitia', 'nulla', 'a', 'similique',
            'eos', 'alias', 'dolore', 'tenetur', 'deleniti', 'porro', 'facere',
            'maxime', 'corrupti',]

        if args and lorem:
            for file in args:
                with open(file, 'r+') as fhand:
                    new_words = (word.strip().lower() for word in fhand.read().split())
                self.words = self.lorem_ipsum.extend(new_words)

            shuffle(self.words)
            length = len(self.words)//3 # pick the first third of words to make common
            self.common = self.words[:length]
            self.standard = ' '.join(self.common)

        elif args and (not lorem):
            self.words = []

        elif (not args) and lorem:
            self.words = self.lorem_ipsum

            self.common = ('lorem', 'ipsum', 'dolor', 'sit', 'amet',
                        'consectetur', 'adipisicing', 'elit', 'sed',
                        'do', 'eiusmod', 'tempor', 'incididunt', 'ut',
                        'labore', 'et', 'dolore', 'magna', 'aliqua',)

            self.standard = ('Lorem ipsum dolor sit amet, consectetur adipisicing elit, sed do eiusmod '
                            'tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim '
                            'veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea '
                            'commodo consequat. Duis aute irure dolor in reprehenderit in voluptate '
                            'velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint '
                            'occaecat cupidatat non proident, sunt in culpa qui officia deserunt '
                            'mollit anim id est laborum.')

        if not domains:
            self.domains = [".com", ".info", ".net", ".org"]
        else:
            with open(domains, "r+") as rh:
                self.domains = list([each.lower().strip() for each in rhand.read().split()])


    def title(self, n=5):
        """return a title consisting of between 2 to n words. Default is 5"""
        wordings = [(choice(self.words)).title() for i in range(randint(2, n))]
        return ' '.join(list(wordings)).title()

    def word(self):
        """Return a single word"""
        return choice(self.words)
        
    def name(self):
        """Return any name with a middle initial."""
        initial = choice(self.words).upper()[0]
        return ("{} {}. {}".format(self.word(), initial, self.word())).title()

    def username(self):
        return "{}{}{}".format(choice(self.words), randint(1, 10), choice(self.words))

    def email(self):
        """Return a single email address"""
        return "{}@{}{}".format(choice(self.words), choice(self.words), choice(self.domains))

    def sentence(self, m=4, n=10):
        """
        Return a sentence of between m to n words. First word is capitalized.
        Defaults to between 4 to 10
        """
        first = self.word().title()
        others = " ".join([self.word() for _ in range(m, n)])
        return " ".join([first, others, choice(string.punctuation)])

    def sentences(self, count=2):
        """Return a count number of sentences joined by a random punctuation mark"""
        return choice(string.punctuation).join([self.sentence() for _ in range(count)])
        
    def paragraph(self, count=1, m=3, n=5, common=True):
        """
        Return paragraphs

        Parameters
        -----------
        count : int
            The number of required paragraph. Default is 1
        common : bool
            Whether the first paragraph will be the standard lorem ipsum text. Default is True
        """

        if count == 1:
            paragraph = '\n\n'.join([self.sentences() for _ in range(randint(m, n))])
            return paragraph
        else:
            paragraphs = '\n\n'.join([self.sentences() for _ in range(randint(m, n))])
            if common:                
                return '\n\n'.join([self.standard, paragraphs])
            else:
                return paragraphs
