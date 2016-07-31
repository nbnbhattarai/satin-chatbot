import dictionary


class WordVectorRep:
    """
    word to vector representation learning
    by using neural network
    """
    def __init__(self, filename='word.vec', dict=dict):
        self.ncols = 10          # word converts to list having 10 items
        self.dict = dict
        self.data = []

    def get_vector(self, word):
        """
        get the vectorial representation of given word
        return the row from data matrix using the index
        from dictionary
        """
        return self.data[self.dictionary.words.index(word)]
