import dictionary
import tokenizer


class WordVectorRep:
    """
    word to vector representation learning
    by using neural network
    """
    def __init__(self, filename='word.vec', dict=None):
        self.ncols = 10          # word converts to list having 10 items
        if dict:
            self.dict = dict
        if not dict:
            self.dict = dictionary.Dictionary()
        self.data = []

    def get_vector(self, word):
        """
        get the vectorial representation of given word
        return the row from data matrix using the index
        from dictionary
        """
        if word == tokenizer.START_TOKEN:
            return -1
        elif word == tokenizer.END_TOKEN:
            return -2

        try:
            return self.dict.words.index(word)
        except ValueError:
            if word in tokenizer.symbols:
                return (-3-tokenizer.symbols.index(word))
            return 0           # if not in dictionary
        # return self.data[self.dictionary.words.index(word)]

    def get_vectors(self, tokens):
        """
        return vector representation of all the tokens provided.
        """
        result = []
        for t in tokens:
            result.append(self.get_vector(t))
        return result
