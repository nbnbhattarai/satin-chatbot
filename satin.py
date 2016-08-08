#!/usr/bin/python
import sys
import operator
import tokenizer
import nltk
import re
import random
import languagemodel


ngram = languagemodel.nGram()
qgram = languagemodel.nGram()
agram = languagemodel.nGram()
qgram.trainFromFile('data/language/english/questions.txt')
agram.trainFromFile('data/language/english/ans.txt')
ngram.trainFromFile('data/language/english/valveteen_rabbit.txt')
tok = tokenizer.Tokenizer()


greetings = ['hi', 'hello', 'hey']


def prompt():
    """
    prompt which asks for input and return splited words.
    """
    while True:
        intext = input('input :> ')
        args = tok.word_tokenize(intext)
        output = talker(args)
        # for g in greetings:
        #     if g in args:
        #         output = greetings[random.randint(0, len(greetings)-1)]+'!'
        print('satin :> '+' '.join(output))


def talker(args_in):
    """
    It takes input text given by user and returns the reply
    to user.
    """
    pos_tags = nltk.pos_tag(args_in)
    nouns = []
    pronouns = []
    for p in pos_tags:
        if p[1] == 'PRP' or p[1] == 'PR' or p[1] == 'PRP$':
            pronouns.append(p[0])

    for p in pos_tags:
        if p[1] == 'NN' or p[1] == 'NNP':
            nouns.append(p[0])

    for i in range(len(pronouns)):
        if pronouns[i] == 'you':
            pronouns[i] = 'i'
        elif pronouns[i] == 'your':
            pronouns[i] = 'my'

    contains = []
    contains.extend(nouns)
    contains.extend(pronouns)
    contains = list(set(contains))
    if tokenizer.START_TOKEN in contains:
        contains.remove(tokenizer.START_TOKEN)
    if tokenizer.END_TOKEN in contains:
        contains.remove(tokenizer.END_TOKEN)
    print('contains:', contains)
    contains = [agram.get_word_id(a) for a in contains[:]]
    sentences = []
    agram.sent_generate(sentences, [0], 0, contain=contains)
    print(sentences)
    if len(sentences) >= 1:
        sentences = sorted(sentences, key=operator.itemgetter(1),
                           reverse=True)
        print('the sent: ', sentences)
        actual_sent = agram.get_sent_from_ids(sentences[0][0])
        return actual_sent
    else:
        return ['I', 'don"t', 'understand!']


def satin():
    prompt()
    # while True:
    #     args_in = prompt()
    #     args_out = talker(args_in)
    #     print('satin :> ' + args_out)


if __name__ == '__main__':
    prompt()
    first_word = sys.argv[1]
    out_s = []
    st = [ngram.get_word_id(first_word)]
    # st = int(first_word)
    # print(ngram.gram[1].items())
    for k in ngram.gram[1].keys():
        if k[0] == st:
            print(k)
    ngram.sent_generate(out_s, st, 0, [])
    for s in out_s:
        print('sent: ', s)
    else:
        print('no sentences, huhuhuhu :)!')
