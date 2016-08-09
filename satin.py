#!/usr/bin/python
import sys
import operator
import tokenizer
import nltk
import re
import random
import languagemodel


qgram = languagemodel.nGram()
agram = languagemodel.nGram()
vgram = languagemodel.nGram()

list_of_tm = [qgram,agram,vgram]
# vgram = languagemodel.nGram()
# agram.trainFromFile('data/language/english/stephen_hawking_a_brief_history_of_time.txt')
qgram.trainFromFile('data/language/english/questions.txt')
agram.trainFromFile('data/language/english/ans.txt')
# vgram.print_grams()
# agram.trainFromFile('data/language/english/valveteen_rabbit.txt')
tok = tokenizer.Tokenizer()
just_repeated = ['F']
greetings = ['hi', 'hello', 'hey']

queue = []
max_length_queue = 3


def isrepeated(text, just_repeated):
    # print('just_repeated', just_repeated)
    if len(queue) == max_length_queue:
        queue.pop()
    if len(queue) < max_length_queue:
        queue.insert(0, text)
        print(queue)
    if just_repeated[0] == 'T' and queue[1] == text:
        return True
    elif len(queue) == max_length_queue and \
            len(set(queue)) == 1 and set(queue).pop() == text:
        # just_repeated = True
        return True


def prompt():
    """
    prompt which asks for input and return splited words.
    """
    while True:
        intext = input('input :> ')
        if isrepeated(intext, just_repeated):
            just_repeated.insert(0, 'T')
            print('satin :> You are repeating a text')
            continue
        else:
            just_repeated.pop()
            just_repeated.insert(0, 'F')

        output = talker(intext)
        # for g in greetings:
        #     if g in args:
        #         output = greetings[random.randint(0, len(greetings)-1)]+'!'
        print('satin :> ' + ' '.join(output))


def talker(args_in):
    """
    It takes input text given by user and returns the reply
    to user.
    """
    gram = languagemodel.nGram()
    if (args_in[len(args_in)-1]) == '.':
        gram = qgram
    else:
        gram = agram
    # args = tok.word_tokenize(args_in)
    pos_tags = nltk.pos_tag(nltk.word_tokenize(args_in), tagset='universal')

    print('pos_tag', pos_tags)
    contains = []

    for p in pos_tags:
        if p[1] == 'PRON':
            if p[0] == 'you':
                p[0] == 'i'
            elif p[0] == 'your':
                p[0] = 'my'

    for p in pos_tags:
        if p[1] == 'PRON' or p[1] == 'NOUN' or\
           p[1] == 'VERB' or p[1] == 'ADJ' or p[1] == 'AD':
            contains.append(p[0])

    # print('nouns', nouns)
    # contains.extend(nouns)
    # contains.extend(pronouns)
    # contains.extend(verbs)
    # contains.extend(adjective)

    for c in contains[:]:
        if c == tokenizer.END_TOKEN or c == tokenizer.START_TOKEN:
            contains.remove(c)

    print('contains:', contains)

    # get id representation for all words in contains
    contains = [gram.get_word_id(a) for a in contains[:]]

    sentences = []
    gram.sent_generate(sentences, [0], 0, contain=contains)
    # print(sentences)

    if len(sentences) >= 1:
        sentences = sorted(sentences, key=operator.itemgetter(1),
                           reverse=True)
        # print('the sent: ', sentences)
        actual_sent = gram.get_sent_from_ids(sentences[0][0])

        # return list of tokens for string from ids of tokens.
        return actual_sent
    else:
        return ['I', "don't", 'understand!']


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
    st = [vgram.get_word_id(first_word)]
    # st = int(first_word)
    # print(vgram.gram[1].items())
    for k in vgram.gram[1].keys():
        if k[0] == st:
            print(k)
    vgram.sent_generate(out_s, st, 0, [])
    for s in out_s:
        print('sent: ', s)
    else:
        print('no sentences, huhuhuhu :)!')
