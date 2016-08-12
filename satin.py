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
activate_reinforcement = ['F']
previous_contains = []
questions_dict = {'who': 'proper_nouns', 'where': 'places',
                  'how': 'adjectives', 'when': 'time',
                  'what': 'object', ('is', 'am', 'are', 'has', 'have', 'would',
                                     'shoud', 'will', 'shall'): 'affirmation'}
list_of_tm = [qgram, agram, vgram]


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
    if (args_in[len(args_in) - 1]) == '.':
        gram = qgram
    else:
        gram = agram
    # args = tok.word_tokenize(args_in)
    pos_tags = nltk.pos_tag(nltk.word_tokenize(args_in), tagset='universal')

    print('pos_tag', pos_tags)
    # pronouns = []
    # adjective =[]
    # nouns = []
    # verbs = []

    # for p in pos_tags:
    #     if p[1].find('PRP') >= 0:
    #         pronouns.append(p[0])
    #     elif p[1].find('JJ') >= 0:
    #         adjective.append(p[0])
    #     elif p[1].find('NN') >= 0:
    #         print('noun', p[0], 'added')
    #         nouns.append(p[0])
    #     elif p[1].find('VB') >= 0:
    #         verbs.append(p[0])
    # #print('pronouns:',pronouns)
    # for i in range(len(pronouns)):
    #     if pronouns[i] == 'you':
    #         pronouns[i] = 'I'
    #     elif pronouns[i] == 'your':
    #         pronouns[i] = 'My'
    # print('pronouns',pronouns)
    # print('nouns', nouns)
    contains = []
    # contains.extend(nouns)
    # contains.extend(pronouns)
    # contains.extend(verbs)
    # contains.extend(adjective)

    for p in pos_tags:
        if p[1] == 'PRON' or p[1] == 'NOUN' or p[1] == 'ADV' or\
           p[1] == 'VERB' or p[1] == 'ADJ' or p[1] == 'AD':
            if p[1] == 'PRON':
                if p[0] == 'you':
                    contains.append('i')
                elif p[0] == 'your':
                    contains.append('my')
                else:
                    contains.append(p[0])
            else:
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
    temp_contains = contains
    print('contains:', temp_contains)

    # updates a database based on user response on a subject chatbot doesn't
    # know anything.
    temp_checker = []
    if activate_reinforcement[0] == 'T':
        for i in previous_contains:
            if i in contains:
                temp_checker.append(i)
        if previous_contains == temp_checker:
            with open('data/language/english/ans.txt', 'a') as file:
                file.write('\n')
                file.write(args_in)
            activate_reinforcement.clear()
            activate_reinforcement.insert(0, 'F')
            temp_checker = []
            return ["Thank", "you", "for", "describing"]
        activate_reinforcement.clear()
        activate_reinforcement.insert(0, 'F')
        temp_checker = []

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
        activate_reinforcement.insert(0, 'T')
        previous_contains = temp_contains
        return ['I', "don't", 'know', 'you', 'tell', 'me!']


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
