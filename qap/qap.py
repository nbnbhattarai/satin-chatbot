import worldmodel


class QAP:

    def __init__(self, filename=None):
        if filename:
            self.filename = filename
            self.load_from_file(filename)
            self.qas = []
            self.wm = World(filename='./data/language/english/wm')

    def train_from_tokens(self, qt, at):
        

    def load_from_file(self, filename):
        
