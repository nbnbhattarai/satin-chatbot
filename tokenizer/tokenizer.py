"""
Package Name: tokenizer
Descripton : 
"""
import re

# punctions of english languagexs
punctions = ['.','?',',', '&', '!',':',]

abbreviations = ['Mr.', 'Mrs.', 'Dr.', 'Er.',]


def extract_num(r):
    """
    It extracts the number from string r.
    It takes a string containing number and returns
    a list seperating number from string.
    """
    reg_num = '[0-9]+(.[0-9]+)*'
    reg_obj = re.search(reg_num, r)
    if not reg_obj:
        return r
    res_list = [r[:reg_obj.span(0)[0]], r[reg_obj.span(0)[0]:
                reg_obj.span(0)[1]], r[reg_obj.span(0)[1]:]]
    return res_list


def _extract_abbreviations(r):
    """
    It takes a string input and returns a list of string
    seperating the abbreviations in the given string r
    """
    reg_abb = ''.join([re.escape(x) for x in abbreviations)
    return [r]


def word_tokenize(text):
    """ 
    tokenize a given text of english.
    Seperate text with meaningful words
    """
    split_word = text.split()
    reex = []
    reex.append('('.join([re.escape(k) for k in abbreviations])+')')
    print('reex :', reex)
    text = text.lower()
    
    return split_word


def sent_tokenize(text):
    """
    seperate sentences of text and return list of sentences.
    """
    sentences = []
    
    return sentences
