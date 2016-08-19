# Let's make predefined questions patterns. and with given answer to a
# specific question pattern, let's update answer pattern.

from worldmodel import World
import sys
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


def fill_ans_pattern(a, objs, world):
    """
    Replace <obj.prop> with property of <obj> and
    return the resultant list.
    for <obj0.obj1> it converts to ('obj', '0', 'obj', '1')
    and and replace that with value of obj at index 0 with
    property of name of obj at index 1
    for <obj1.name> it returns ('obj', '1', 'name', '')
    """
    obj_prop = []
    result = []
    for k in range(len(a)):
        print(a[k])
        if '<obj' in a[k]:      # filter token with obj or nonobj.
            r = re.findall(
                re.compile("(\{([^}]+)\})?<(\D+)(\d+)(.(\D+)(\d+)?)?>"),
                a[k])
            # r[0]
            # r = re.findall("<(.*?)([0-9]+)*\.(.*?)([0-9]+)*>",
            #                a[k])
            print(r)
            if len(r) > 0:
                r = r[0]
                classname = r[1]
                first_id = int(r[3])
                print('f:', first_id)
                if len(classname) > 0:
                    objname = classname + '_' + objs[first_id]
                else:
                    objname = objs[first_id]
                print('objname:', objname)
                prop_text = ''
                if len(r[6]) == 0:
                    if len(r[5]) > 0:
                        prop_text = r[5]
                else:
                    second_id = int(r[6])
                    print('s:', second_id)
                    prop_text = objs[second_id]
                print('prop_text:', prop_text)
                if len(prop_text) > 0:
                    if objname in world.objects.keys():
                        obj = world.objects[objname]
                        if prop_text in obj.informations.keys():
                            result.append(obj.informations[prop_text])
                        else:
                            result.append(", i don't know")
                else:
                    result.append(objname)
        else:
            result.append(a[k])
    # It returns tuple of (obj, id, prop_or_obj, obj_id_if_obj)
    return result


def get_default_ans(q):
    """
    get a default answer according to the type of question
    asked. It is called if no pattern in database is matched
    with the asked question pattern.
    """
    return "I don't know what you are talking about .".split()


class QAP:
    """
    Question Answer Pattern Matching for answer generation.
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
            print(qa, q_pattern)
            if list(qa[0]) == q_pattern:
                print('matched')
                ans.append((qa[1], qa[2]))
        if len(ans) == 1:
            return ans[0]
        elif len(ans) == 0:
            return get_default_ans(q_pattern)
        else:
            true_ans = []
            for a in ans:
                if sorted(a[1]) == sorted(objs):
                    true_ans.append(a[0])
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
        print('writing to file ...')
        try:
            file = open(filename, 'w')
            restr = '<qap>'
            for qa in self.qas:
                if len(qa) < 3:
                    continue
                restr += '<qa>\n'
                restr += '<q>' + qa[0] + '</q>\n'
                restr += '<a>' + qa[1] + '</a>\n'
                restr += '<o>' + ','.join(qa[2]) + '</o>\n'
                restr += '</qa>\n'
            restr += '</qap>'
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
            for i in range(len(questions)):
                self.qas.append((questions[i], answers[i],
                                 objects[i]))
        except Exception as e:
            print('Exception :', str(e))


def main():
    world = World()
    world.read_readable('./data/traindata/objects')
    filename = './data/traindata/questionanswers'
    if len(sys.argv) > 1:
        filename = sys.argv[1]
    qap = QAP()
    qap.load_from_file(filename)
    # qap.save_to_file(' '.join(filename.split('.')[:-1]) + '_test.' +
    #                  filename.split('.')[-1])
    # qap.print()
    # ques = 'what is <obj0> of <obj1> ?'.split()
    # ans = 'the <obj0> of <obj1> is <obj1.obj0>'.split()
    ans = ['<obj0.what>']
    objs = ['earth']
    res = fill_ans_pattern(ans, objs, world)
    print(res)

if __name__ == '__main__':
    main()
