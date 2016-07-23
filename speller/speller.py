import sys
import re

class Dictionary:
    def __init__(self):
        self.filename = "dict"
        self.language = "english"
        self.short[self.language] = "en"
        self.path = "../data/language/" + self.short[self.language] + "/"
        self.file = open(self.path+self.filename, 'r')
        if self.file:
            text = self.file.read()
            self.words = re.findall("[A-Za-z]+", text)
        else:
            self.words = None


def spell_correct_word(word):
    """
    This function takes a word as input and returns
    the possible words list with descending probabilities.
    """
    pass


def spell_correct_sent(sent):
    """
    It takes sentence as input, uses language model and 
    list of possible spelling and finds out the most 
    probable sentences and returns list of sentences
    with descending probabilities.
    """
    pass


def main():
    pass


if __name__ == '__main__':
    main()
