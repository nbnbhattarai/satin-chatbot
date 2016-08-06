import re


class Dictionary:
    """
    Dictionary class which stores
    all the words of a language
    """
    def __init__(self, lan='english'):
        self.filename = './data/language/' + lan + '/dict'
        self.file = open(self.filename, 'r')
        if self.file:
            text = self.file.read().lower()
            self.words = re.findall("[A-Za-z]+", text)
        else:
            self.words = None
