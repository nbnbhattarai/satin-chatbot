#!/usr/bin/python
import tokenizer
import nltk
import languagemodel


ngram = languagemodel.nGram()
tok = tokenizer.Tokenizer()


def prompt():
    """
    prompt which asks for input and return splited words.
    """
    while True:
        intext = input('input :> ')
        args = tok.word_tokenize(intext)
        output = talker(args)
        print('satin :>' + output)


def is_second_person(pt):
    if pt[0] == 'you' or pt[0] == 'your':
        return True
    return False


def talker(args_in):
    """
    It takes input text given by user and returns the reply
    to user.
    """
    pos_tags = nltk.pos_tag(args_in)
    nouns = []
    pronouns = []
    for p in pos_tags:
        if p[1] == 'PRP' or p[1] == 'PR':
            pronouns.append(p[0])

    for p in pos_tags:
        if p[1] == 'NN' or p[1] == 'NNP':
            nouns.append(p[0])

    for p in pronouns:
        if p[0] == 'you':
            p[0] = 'i'
        elif p[0] == 'your':
            p[0] = 'my'
    contains = []
    contains.extend(nouns)
    contains.extend(pronouns)

    next_sents = ngram.construct_sent(contain=contains)
    return next_sents[0]


def satin():
    while True:
        args_in = prompt()
        args_out = talker(args_in)
        print('satin :> ' + args_out)


if __name__ == '__main__':
    satin()
