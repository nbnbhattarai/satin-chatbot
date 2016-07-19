"""
Lemmatizer:
-> Specially change symbol into predefined symbol like
'.' -> '_FULLSTOP_'
'?' -> '_QUESTIONMARK_' 
'*' -> '_MULTIPLICATION_'
'/' -> '_DIVISION_' etc.
-> Change given numeral value into '_VARIABLE_#ID', where ID is replaced
by index of variable
eg:
for text ['how','is','10','*','30','?'], after lemmatization it will be
['how','is','_VARIABLE_#0','_MULTIPLICATION_','_VARIABLE_#1','_QUESTIONMARK_']
variable are stored in actual _VARIABLE_ variable and accessed by the index

We are changing mathematical symbol because we are going to use another 
preprogrammed program for mathematical operations and return the result 
back when these symbol are present because computer program are very fast
 compared to trained AI for mathematical operations.
"""

en_punc = {'.': '_FULLSTOP_',
           ',': '_COMMA_',
           '?': '_QUESTIONMARK_',
           '!': '_EXCLAMATIONMARK_',
           }
math_sym = {'+': '_PLUS_',
            '-': '_MINUS_',
            '*': '_MULTIPLICATION_',
            '/': '_DIVISION_',
            '%': '_MODULUS_',
            }

def lemmatize_list(tokenlist):
    """
    Lemmatize all token of tokenlist and return list containing 
    lemmatized tokens.
    """
    for token in tokenlist:
        

def lemmatize_word (word):
    """
    Lemmatize the given token and return lemmatized token.
    """
    if word in en_punc.keys():
        word = en_punc[word]
    elif word in math_sym.keys():
        word = math_sym[word]
    
    return word
