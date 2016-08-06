from nltk import sent_tokenize
import tokenizer
import pickle
# import dictionary
# import word2vec


class nGram:
    """
    This is a class which represent n-gram and helps to
    calculate probability too.
    """
    def __init__(self, filename=None, N=4):
        """
        filename : open nGram data from file.
        N : value of n in nGram, it's default value
        is 4, so it's four gram and stores bigram, trigram and 4 gram.
        """
        self.filename = filename
        self.N = N
        self.words = []
        self.gram = [{} for i in range(0, N)]

    def get_grams(self, tokens, n):
        # word_vec_er = word2vec.WordVectorRep(dict=self.dict)
        # tokens_vec = tokens
        tokens_vec = []
        for t in tokens:
            tokens_vec.append(self.words.index(t))
        return [tuple(tokens_vec[i:i+n]) for i in
                range(0, len(tokens_vec)-n+1)]

    def add_tokens(self, tokens):
        """
        Update nGram data with given token list.
        """
        for t in tokens:
            if t not in self.words:
                self.words.append(t)

        for i in range(2, self.N+1):
            ngram_tup = self.gram[i-2].keys()
            n_gram = self.get_grams(tokens, i)
            # print(n_gram)
            for g in n_gram:
                if g in ngram_tup:
                    self.gram[i-2][g] += 1  # increase count by one
                else:
                    self.gram[i-2][g] = 1  # if first entry then count is 1

    def write(self, filename):
        """
        We are going to use pickle to write data object to file.
        """
        print("Writing file.")
        try:
            file = open(filename, 'wb')
            file.write(pickle.dumps(self.__dict__))
            print("[ done ]")
        except FileNotFoundError:
            print("[ error ]")

    def open_from_file(self, filename):
        print("Opening from file.")
        try:
            file = open(filename, 'rb')
            datapickle = file.read()
            file.close()
            self.__dict__ = pickle.loads(datapickle)
            print("[ done ]")
        except FileNotFoundError:
            print("[ error ]")

    def trainFromFile(self, filename):
        self.filename = filename
        file = open(filename, 'r')
        text_data = file.read().lower()
        # let's replace newline char with white space
        text_data = text_data.replace('\n', ' ')
        # let's tokenize sentences from text_data.
        # I use sent_tokenize nltk function to tokenize the sentences.
        sents = sent_tokenize(text_data)
        # let's iterate over sentences and tokenize words and update
        # n-gram data
        tok = tokenizer.Tokenizer()
        for s in sents:
            tokens = tok.word_tokenize(s)
            self.add_tokens(tokens)

    def get_nw_bigram(self, this_word):
        next_words = []
        for t in self.grams[0].keys():
            if t[0] == this_word:
                next_words.append(t[1])
        probs = []
        for w in next_words:
            probs.append(self.gram[0][(this_word, w)])
        final = dict(zip(next_words, probs))
        sorted(final)
        return final[:6]

    def get_nw_trigram(self, pw):
        next_words = []
        if len(pw) < 2:
            return []
        for t in self.grams[1].keys():
            if t[0] == pw[0] and t[1] == pw[1]:
                next_words.append(t[2])
        probs = []
        for w in next_words:
            probs.append(self.gram[1][(pw[0], pw[1], w)])
        final = dict(zip(next_words, probs))
        sorted(final)
        return final[:6]

    def get_next_word(self, till):
        
        pass

    def construct_sent(self, start, contain=None):
        """
        it returns list of sentences that is constructed using this ngram model
        start : starting word for sentence
        contain : list object which contains words that should be contained in
        constructed sentence.
        """
        
