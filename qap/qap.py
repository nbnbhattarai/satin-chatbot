import worldmodel
import nltk

questions_tx = ['who', 'what', 'where', 'how']


def interpreat_qa(q, a):
    """
    q: questions' pos_tag tupples
    a: answer's pos_tag tupples
    replace name with respective symbols <obj1>, <obj2>, ...
    """
    pq = nltk.pos_tag(q, tagset='universal')
    pa = nltk.pos_tag(a, tagset='universal')
    i = 0
    obj_q = []
    pq_res = []
    pa_res = []
    ques = []
    answers = []
    for k in questions_tx:
        if k in q:
            ques.append(k)

    for a in pq:
        if a[1] == 'NOUN':
            pq_res.append('<obj' + str(i) + '>')
            obj_q.append(a[0])
            i = i + 1
        else:
            pq_res.append(a[0] + ' ')
    whatclass = ''
    for i in range(len(pa)):
        a = pa[i]
        if a[0] == 'PRON':
            if len(a) > i + 1:
                if pa[i + 1][0] == 'NOUN':
                    whatclass = ''.join(a[0])
                else:
                    pa_res.append(a[0])
        if a[0] in obj_q:
            j = obj_q.index(a[0])
            pa_res.append('<obj' + str(j) + '>')
        if a[1] == 'VERB':
            pa_res.append(a[0])
            answers = pa[i + 1:-1]
            j = 0
            for oq in obj_q:
                if j > 0:
                    pa_res.append('and')
                pa_res.append('<obj' + str(j) + '.' + ques[0] + '>')
                j = j + 1

            pa_res.append(pa[-1][0])
            break
        else:
            pa_res.append(a[0])
    return [pq_res, pa_res, answers]


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
        [q_st, a_st] = interpreat_qa(qt, at)
        self.qas.append((q_st, a_st))

    def load_from_file(self, filename):
        pass
