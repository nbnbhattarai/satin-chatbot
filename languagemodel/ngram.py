from nltk import sent_tokenize
import tokenizer
import pickle
import operator
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
        return [tuple(tokens_vec[i:i + n]) for i in
                range(0, len(tokens_vec) - n + 1)]

    def add_tokens(self, tokens):
        """
        Update nGram data with given token list.
        """
        for t in tokens:
            if t not in self.words:
                self.words.append(t)

        for i in range(1, self.N + 1):
            ngram_tup = self.gram[i - 1].keys()
            n_gram = self.get_grams(tokens, i)
            # print(n_gram)
            for g in n_gram:
                if g in ngram_tup:
                    self.gram[i - 1][g] += 1  # increase count by one
                else:
                    self.gram[i - 1][g] = 1  # if first entry then count is 1

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
        # sents = sent_tokenize(text_data)
        # let's iterate over sentences and tokenize words and update
        # n-gram data
        tok = tokenizer.Tokenizer()
        tokens = tok.word_tokenize(text_data)
        self.add_tokens(tokens)
        # for s in sents:
        #     tokens = tok.word_tokenize(s)
        #     self.add_tokens(tokens)

    def get_nw_ngram(self, pw, n):
        """
        It returns list of next words having high probabilities by
        using last (n-1) words of pw(previous words) using n gram.
        """
        next_words = []
        # if pw(previous words) count is lesser than n-1 then we
        # cannot use ngram(markov model) to find next word.
        if len(pw) < n - 1:
            return []

        previous_words = pw[-n - 1:]
        for (wt, c) in self.gram[n - 1].items():
            words_list = list(wt)
            if previous_words == words_list:
                # save next word with probability as tuple
                next_words.append((words_list[-1], c))
        next_words = sorted(next_words, key=operator.itemgetter(1),
                            reverse=True)
        return next_words[:5]   # return list of (word,prob) tuple

    def prob(self, word_list):
        """
        It returns unique next word from word_list list of tuples
        it adds probability if words are appearing more than once.
        """
        words = list(set([w[0] for w in word_list]))
        words_with_probs = []
        for w in words:
            prob = 0
            for wl in word_list:
                if w == wl[0]:
                    prob += wl[1]
            words_with_probs.append((w, prob))
        return words_with_probs

    def get_next_word(self, till):
        # get list of tupels (word_id, count)
        from_bigram = self.get_nw_ngram(till, 2)
        from_trigram = self.get_nw_ngram(till, 3)
        from_fourgram = self.get_nw_ngram(till, 4)

        word_list = from_bigram + from_trigram + from_fourgram
        word_list = self.prob(word_list)
        word_list = sorted(word_list, key=operator.itemgetter(1),
                           reverse=True)
        return word_list[:10]

    def get_count(self, sents, conts):
        count = 0
        for c in conts:
            if c in sents:
                ++count
        return count

    def get_word_id(self, token):
        """
        Return word id from ngram database.
        If word doesn't exist, then return -1.
        """
        try:
            return self.words.index(token.lower())
        except:
            return -1

    def sent_generate(self, out_sents, till, count, contain=None):
        """
        contain = ['president', 'nepal']
        it returns list of sentences that is constructed using this ngram model
        start : starting word for sentence
        contain : list object which contains words that should be contained in
        constructed sentence.
        """
        n_words = self.get_next_word(till)
        print('inside sent_generate!')
        print('next words: ', n_words)
        print('till:', till)
        for w in n_words:
            ++count
            till_tmp = till
            if w == tokenizer.END_TOKEN or count > 10:
                print('hahaha')
                contain_count = self.get_count(till, contain)
                if contain_count > 0:
                    out_sents.append((till, contain_count))
                    return True
                else:
                    print('no contain')
            else:
                till_tmp.append(w)
                self.sent_generate(out_sents, till_tmp, count, contain)
        else:
            print("I don't know what you are talking about")
