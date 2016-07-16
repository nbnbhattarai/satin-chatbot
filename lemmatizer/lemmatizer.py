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


def lemmatize(word):
    """
    Lemmatize the given word and return lemmatized word.
    """
    
