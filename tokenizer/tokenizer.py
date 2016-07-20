"""
Package Name: tokenizer
Descripton : 
"""
import re

# abbreviations are stored in this file
# when It learns new abbreviations, It insert
# into this file.
abbreviations_filename = "data/language/en/abbreviations"

# symbols of english languagexs
symbols = ['.', '?', ',', '&', '!', ':', '$', '%', '#', '@', '~',
               '-', '+', '=', '*', '(', ')', '^', '/','\\', '|', ';',
               '\'', '\"' ]

# Every sentences starts from START_TOKEN
# and ends with END_TOKEN
START_TOKEN = '_START_TOKEN_'
END_TOKEN = '_END_TOKEN_'

class Tokenizer:
    def __init__(self):
        abbreviations_file = open(abbreviations_filename, 'r')
        lines = abbreviations_file.readlines()
        self.abbreviations = {}
        for line in lines:
            if len(line) > 0 and line.count('-') == 1:
                [abb, full] = line.split('-')
                self.abbreviations[abb] = full

    def word_tokenize(self, str):
        """
        tokenize a given text of english.
        Seperate text with meaningful words
        """
        abbreviations = list(self.abbreviations.keys())
        regex = '|'.join([re.escape(x.lower()) for x in abbreviations])
        regex += '|[a-z]+|'
        regex += '[+-]?[0-9]+|'
        regex += '|'.join([re.escape(x) for x in symbols])
        print('regex: ', regex)
        result = [START_TOKEN]
        result.extend(re.findall(regex, str.lower()))
        result.append(END_TOKEN)
        return result

    def sent_tokenize(self, text):
        """
        sentence tokenizer:
        seperate sentences of text and return list of sentences
        """
        return re.findall(re.escape('.|,'), text)
