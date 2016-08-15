# Let's make predefined questions patterns. and with given answer to a
# specific question pattern, let's update answer pattern.

# import worldmodel
import nltk

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

    pq = nltk.pos_tag(q, tagset='universal')
    pa = nltk.pos_tag(a, tagset='universal')

    i = 0
    objs = []              # list of objects in question/answer
    pq_res = []                 # final result of xml syntax question
    pa_res = []                 # final result of xml syntax answer
    ques = []                   # find question types list from question_tx

    for k in questions_tx:
        if k in q:
            ques.append(k)

    for a in pq:
        if a[1] == 'NOUN':
            pq_res.append('<obj' + str(i) + '>')
            objs.append(a[0])
            i = i + 1
        else:
            pq_res.append(a[0] + ' ')

    for i in range(len(pa)):
        a = pa[i]
        if a[0] in objs:
            j = objs.index(a[0])
            pa_res.append('<obj' + str(j) + '>')
        else:
            pa_res.append(a[0])
    return [pq_res, pa_res, objs]


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
        pass

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
        pass
