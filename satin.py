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
just_repeated = ['F']
greetings = ['hi', 'hello', 'hey']
queue = []
max_length_queue = 3

def isrepeated(text, just_repeated):
    #print('just_repeated', just_repeated)
    if len(queue) == max_length_queue:
        queue.pop()
    if len(queue) < max_length_queue:
        queue.insert(0,text)
        print(queue)
    if just_repeated[0]=='T' and queue[1] == text:
       return True
    elif len(queue)== max_length_queue and len(set(queue)) == 1 and set(queue).pop() == text:
        #just_repeated = True
        return True



def prompt():
    """
    prompt which asks for input and return splited words.
    """
    while True:
        intext = input('input :> ')
        if isrepeated(intext,just_repeated):
            just_repeated.insert(0,'T')
            print('satin :> You are repeating a text')
            continue
        else:
            just_repeated.pop()
            just_repeated.insert(0,'F')
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
    verbs = []
    for p in pos_tags:
        if p[1] == 'PRP' or p[1] == 'PR' or p[1] == 'PRP$':
            pronouns.append(p[0])

    for p in pos_tags:
        if p[1] == 'NN' or p[1] == 'NNP':
            nouns.append(p[0])
    for p in pos_tags:
        if p[1] == 'VBP':
            verbs.append(p[0])


    for i,p in enumerate(pronouns):
        if p == 'you':
            pronouns[i] = 'I'
        elif p == 'your':
            pronouns[i] = 'my'


    for i in range(len(pronouns)):
        if pronouns[i] == 'you':
            pronouns[i] = 'i'
        elif pronouns[i] == 'your':
            pronouns[i] = 'my'

    contains = []
    contains.extend(nouns)
    contains.extend(pronouns)

    contains.extend(verbs)

    print('contains:', contains)
    contains = [qgram.get_word_id(a) for a in contains[:]]
    contains = list(set(contains))
    if tokenizer.START_TOKEN in contains:
        contains.remove(tokenizer.START_TOKEN)
    if tokenizer.END_TOKEN in contains:
        contains.remove(tokenizer.END_TOKEN)

    print('contains:', contains)
    sentences = []
    qgram.sent_generate(sentences, [0], 0, contain=contains)
    print("Sentences",sentences)
    if len(sentences) >= 1:
        sentences = sorted(sentences, key=operator.itemgetter(1),
                           reverse=True)
        actual_sent = qgram.get_sent_from_ids(sentences[0][0])

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
