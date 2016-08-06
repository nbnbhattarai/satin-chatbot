import dictionary


class WordVectorRep:
    """
    word to vector representation learning
    by using neural network
    """
    def __init__(self, filename='word.vec', dict=None):
        self.ncols = 10          # word converts to list having 10 items
        if dict:
            self.dict = dict
        self.dict = None
        self.data = []

    def get_vector(self, word):
        """
        get the vectorial representation of given word
        return the row from data matrix using the index
        from dictionary
        """
        try:
            return self.dict.words.index(word)
        except ValueError:
            return -1           # if not in dictionary
        # return self.data[self.dictionary.words.index(word)]

    def get_vectors(self, tokens):
        """
        return vector representation of all the tokens provided.
        """
        result = []
        for t in tokens:
            result.append(self.get_vector(t))
        return result
