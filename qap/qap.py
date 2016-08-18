# Let's make predefined questions patterns. and with given answer to a
# specific question pattern, let's update answer pattern.

# from worldmodel import World
import nltk
import random
import re

questions_tx = ['who', 'what', 'where', 'how']


def interpreat_qa(q, a):
    """
    q: questions' token list
    a: answer's token list
    replace name with respective symbols <obj0>, <obj1>, ...
    <obj> are nouns in question and same noun in answer are replaced
    with respective <objx> symbol.

    example:
    q = ['what', 'is', 'a', 'cat', '?']
    a = ['a', 'cat', 'is', 'a', 'animal', '.']

    the result will be
    pq_res = 'what is a <obj0> ?'
    pa_res = 'a <obj0> is a animal .'
    objs = ['cat']
    """

    pq = nltk.pos_tag(q)  # , tagset='universal')
    pa = nltk.pos_tag(a)  # , tagset='universal')

    i = 0
    objs = []              # list of objects in question/answer
    pq_res = []                 # final result of xml syntax question
    pa_res = []                 # final result of xml syntax answer
    ques = ''                   # find question types list from question_tx
    answer = []
    pronouns = []
    for k in questions_tx:
        if k in q:
            ques = k
            break

    print('ques:', ques)

    for a in pq:
        if 'NN' in a[1]:
            pq_res.append('<obj' + str(i) + '>')
            objs.append(a[0])
            i = i + 1
        else:
            if 'PRP' in a[1]:
                pronouns.append(a[0])
            pq_res.append(a[0] + ' ')

    for i in range(len(pa)):
        a = pa[i]
        if a[0] in objs:
            j = objs.index(a[0])
            pa_res.append('<obj' + str(j) + '>')
        else:
            pa_res.append(a[0])
    print('answer:', answer)
    return [pq_res, pa_res, objs]


def interpreat_q(q):
    pq = nltk.pos_tag(q, tagset='universal')
    objs = []
    pq_result = []
    i = 0
    for q in pq:
        if q[1] == 'NOUN':
            pq_result.append('<obj' + str(i) + '>')
            objs.append(q[0])
            i = i + 1
        else:
            pq_result.append(q[0])
    return [pq_result, objs]


def get_default_ans(q):
    """
    get a default answer according to the type of question
    asked. It is called if no pattern in database is matched
    with the asked question pattern.
    """
    return "I don't know what you are talking about .".split()


class QAP:
    """
    Question
    """

    def __init__(self, filename=None, wmodel=None):
        self.filename = filename
        if filename:
            self.load_from_file(filename)
        self.qas = []
        self.worldmodel = wmodel

    def train_from_tokens(self, qt, at):
        [q_st, a_st, objs] = interpreat_qa(qt, at)
        # add tuple in database with first two question and answer
        # pattern and last one is object name to which the pattern
        # can be used.
        self.qas.append((q_st, a_st, objs))

    def get_answer_from_question(self, q):
        q_pattern, objs = interpreat_q(q)
        ans = []
        for qa in self.qas:
            if qa[0] == q_pattern:
                ans.append(qa[1])
        if len(ans) == 1:
            return ans[0]
        elif len(ans) == 0:
            return get_default_ans(q_pattern)
        else:
            breaker_counter = 0
            while breaker_counter < 100:
                ans_r = ans[random.randint(0, len(ans) - 1)]
                count = 0
                for k in ans_r:
                    if '<obj' in k:
                        count = count + 1
                if len(objs) == count:
                    break
                breaker_counter = breaker_counter + 1
            for i in range(len(ans_r)):
                if '<obj' in ans_r[i]:
                    ans_r[i] = objs[i]
            return ans_r

    def print(self):
        for qa in self.qas:
            print(qa)

    def save_to_file(self, filename):
        try:
            file = open(filename, 'w')
            restr = '<qap>'
            for qa in self.qas:
                restr += '<qa>\n'
                restr += '<q>'+' '.join(qa[0])+'</q>\n'
                restr += '<a>'+' '.join(qa[1])+'</a>\n'
                restr += '<o>'+';'.join(qa[2])+'</o>\n'
            file.write(restr)
        except Exception as e:
            print('Exception :', str(e))

    def load_from_file(self, filename):
        """
        Get patterns and objects from a xml type file.
        example:
        <qa></qa> : inside it, question/answer pattern are saved.
        <q></q>   : question pattern with <objx> tags.
        <objx>    : object which is replaced in answer with actual
        objects.
        <a></a>   : inside it, there will be a pattern for answer
        which contains <objx> to be replaced by actual object to
        form an answer.
        <aa></aa> : it contains a alternate answer pattern, which is used
        if no answer pattern is appropriate.
        <o></o>   : it contains name of objets with comma seperated format,
        that answer pattern is used for those specific objects. if all objects
        from a specific class exist, then a class name is added insted of
        object name.
        """
        try:
            file = open(filename, 'r')
            lines = file.read().replace('\n', ' ')
            # for now, there is only one question, one answer pair
            # if two same questions are there, they are written seperately
            # with seperate answer pattern.
            questions = re.findall(r'<q>(.*?)</q>', lines)
            answers = re.findall(r'<a>(.*?)</a>', lines)

            objects = [x.split(',') for x in re.findall(r'<o>(.*?)</o>',
                                                        lines)]
            if len(answers) < len(questions):
                raise Exception('Error')
            for i in range(len(questions)):
                self.qas.append((questions[i], answers[i],
                                 objects[i]))
        except Exception as e:
            print('Exception :', str(e))

if __name__ == '__main__':
    in_question = "what do you know about maruti car"
    # world = World()
    # world.read_readable('data_test.xml')
    qap = QAP()
    qap.load_from_file('en01.qap')
    qap.print()
