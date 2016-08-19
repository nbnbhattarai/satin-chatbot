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
                  'what': 'object', ('is', 'am', 'are', 'has', 'have', 'will',
                                     'would', 'shall', 'should'): 'affirmation'}

list_of_tm = [qgram, agram, vgram]


# agram.trainFromFile('data/language/english/stephen_hawking_a_brief_history_of_time.txt')
qgram.trainFromFile('data/language/english/questions.txt')
agram.trainFromFile('data/language/english/ans.txt')
# vgram.print_grams()
# agram.trainFromFile('data/language/english/valveteen_rabbit.txt')
tok = tokenizer.Tokenizer()
just_repeated = ['F']
greetings = ['hi', 'hello', 'hey']

queue = []
object_type = []
structure = []
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


def get_contains(args_in):
    print("type args_in", type(args_in))
    pos_tags = nltk.pos_tag(tok.word_tokenize(args_in)[1:-1])
    # pos_tags = nltk.pos_tag(nltk.word_tokenize(args_in), tagset='universal')

    print('pos_tag from function', pos_tags)
    pronouns = []
    adjective = []
    nouns = []
    verbs = []
    args_in_list = list(args_in.split(" "))
    for p in pos_tags:
        if p[1].find('PRP') >= 0:
            pronouns.append(p[0])
        elif p[1].find('JJ') >= 0:
            adjective.append(p[0])
        elif p[1].find('NN') >= 0:
            print('noun', p[0], 'added')
            nouns.append(p[0])
        elif p[1].find('VB') >= 0:
            verbs.append(p[0])
            #structure.append(args_in_list[pos_tags[1].index('VB')+1:])
        elif p[1].find('VBP') >= 0:
            verbs.append(p[0])
            #structure.append(args_in_list[pos_tags[1].index('VBP')+1:])
        elif p[1].find('VBZ') >= 0:
            verbs.append(p[0])
        #    structure.append(args_in_list[pos_tags[1].index('VBZ')+1:])
        elif p[1].find('WP') >= 0:
            if args_in.find('who') >= 0:
                object_type.append(questions_dict['who'])

            elif args_in.find('what') >= 0:
                object_type.append(questions_dict['what'])
        elif p[1].find('WRB') >= 0:
            if args_in.find('where')>=0:
                object_type.append(questions_dict['where'])
            elif args_in.find('how') >= 0:
                object_type.append(questions_dict['how'])
            elif args_in.find('when') >= 0:
                object_type.append(questions_dict['when'])
        elif args_in[1] == 'is' or 'am' or 'are' or 'has' or 'have' or 'will' or \
                    'would' or 'shall' or 'should':
            #    object_type = questions_dict('is','am','are','has','have','will','would','shall','should')
            pass
    try:
        structure = (args_in_list[pos_tags[1].index('VBP'):])
    except ValueError:
        try:
            structure = (args_in_list[pos_tags[1].index('VBZ'):])
        except:
            try:
                structure = (args_in_list[pos_tags[1].index('VBD'):])
            except:
                structure = (args_in_list[pos_tags[1].index('MD'):])
    except IndexError:
        structure = []
    try:
        if structure[len(structure)-1] == '?' or '.':

            print(type(structure[len(structure)-1]))
            temp = structure[len(structure)-1]

            if temp.endswith('?'):
                k = temp.replace('?','')

                structure.pop()
                structure.append(k)
            elif temp.endswith('.'):
                k= temp.replace('.','')
                structure.pop()
                structure.append(k)

    except IndexError:
        pass

    print("Structure", structure)
    for i,k in enumerate(structure):
        if k.lower() == 'you':
            structure[i] = 'I'
            if structure[0] == 'are':
                structure[0] = 'am'
                #structure[0],structure[i] = structure[i],structure[0]
            elif structure[0] == 'were':
                structure[0] = 'was'
                #structure[0],structure[i] = structure[i],structure[0]
            structure[0],structure[i] = structure[i],structure[0]
        elif k.lower() =='your':
            structure[i] = 'My'
            structure.append(structure[0])
            structure.remove(structure[0])
        elif k.lower() =='my':
            structure[i] = 'Your'
            structure.append(structure[0])
            structure.remove(structure[0])
        elif k.lower() =='i':
            structure[i] = 'You'
            if structure[0] == 'am':
                structure[0] ='are'
                structure[0],structure[i] = structure[i],structure[0]
            structure[0],structure[i] = structure[i],structure[0]
        elif k.lower() == 'it':
            pass
    print("Final Structure of sentence:", structure)
    #print("Object type",object_type)
    # #print('pronouns:',pronouns)
    for i in range(len(pronouns)):
        if pronouns[i] == 'you':
            pronouns[i] = 'i'
        elif pronouns[i] == 'your':
            pronouns[i] = 'my'

    #print('pronouns from function', pronouns)
    #print('nouns', nouns)
    contains = []
    contains.extend(nouns)
    contains.extend(pronouns)
    contains.extend(verbs)
    contains.extend(adjective)
    #print('contains:', contains)
    return contains


def prompt():
    """
    prompt which asks for input and return splited words.
    """
    while True:
        intext = input('input :> ')
        if intext == '':
            print('satin :> Please say something!')
            continue
        else:
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
    # pos_tags=nltk.pos_tag(nltk.word_tokenize(args_in), tagset = 'universal')

    # print('pos_tag', pos_tags)
    contains = get_contains(args_in)
    #print('contains : ', contains)

    for c in contains[:]:
        if c == tokenizer.END_TOKEN or c == tokenizer.START_TOKEN:
            contains.remove(c)

    # print('contains:', contains)
    # temp_conta ins.extend(contains)
    # print('Temp contains:',temp_contains)

    # updates a database based on user response on a subject chatbot doesn't
    # know anything.

    temp_checker = []
    if activate_reinforcement[0] == 'T':
        # previous_text = queue[3]
        previous_contains = get_contains(queue[1])
        print("Previous contains:", previous_contains)
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
        object_type.clear()
        structure.clear()
        return actual_sent
    else:
        activate_reinforcement.insert(0, 'T')
        object_type.clear()
        structure.clear()
        return ['I', "don't", 'know', 'you', 'tell', 'me!']

if __name__ == '__main__':
    prompt()
