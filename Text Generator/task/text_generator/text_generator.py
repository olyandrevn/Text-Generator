# Write your code here
from nltk.tokenize import WhitespaceTokenizer
from collections import Counter, OrderedDict
import random
import re


class TextGenerator:
    def __init__(self, filename):
        self.corpus = self.make_corpus(filename)
        self.tokens = self.make_tokens()
        self.bigrams = self.make_bigrams()
        self.compressed_bigrams = self.compress_bigrams()

    def make_corpus(self, filename):
        f = open(filename, "r", encoding="utf-8")
        return f.read()

    def make_tokens(self):
        tokenizer = WhitespaceTokenizer()
        tokens = tokenizer.tokenize(self.corpus)

        return tokens

    def get_tokens_stat(self):
        counter = Counter(self.tokens)

        print('Corpus statistics')
        print(f'All tokens: {len(self.tokens)}')
        print(f'Unique tokens: {len(counter)}')

    def get_token(self, idx):
        try:
            idx = int(idx)
        except (TypeError, ValueError):
            print('Type Error. Please input an integer.')
            return -1
        try:
            print(self.tokens[idx])
        except IndexError:
            print('Index Error. Please input an integer that is in the range of the corpus.')
            return -1

        return 0

    def make_bigrams(self):
        bigrams = [bigram for bigram in zip(self.tokens[:-1], self.tokens[1:])]

        return bigrams

    def get_bigrams_stat(self):
        print(f'Number of bigrams: {len(self.bigrams)}')

    def get_bigram(self, idx):
        try:
            idx = int(idx)
        except (TypeError, ValueError):
            print('Type Error. Please input an integer.')
            return -1
        try:
            print(f'Head: {self.bigrams[idx][0]} Tail: {self.bigrams[idx][1]}')
        except IndexError:
            print('Index Error. Please input an integer that is in the range of the corpus.')
            return -1

        return 0

    def compress_bigrams(self):
        compressed_bigrams = dict()

        for bigram in self.bigrams:
            head = bigram[0]
            tail = bigram[1]

            if head not in compressed_bigrams:
                compressed_bigrams[head] = list()

            compressed_bigrams[head].append(tail)

        for head in compressed_bigrams:
            compressed_bigrams[head] = OrderedDict(Counter(compressed_bigrams[head]))

        return compressed_bigrams

    def get_bigram_tails(self, head):
        try:
            print(f'Head: {head}')
            for tail in self.compressed_bigrams[head]:
                print(f'Tail: {tail} Count: {self.compressed_bigrams[head][tail]}')
        except KeyError:
            print('Key Error. The requested word is not in the model. Please input another word.')
            return -1

        return 0

    def predict_sentence(self, min_len=5):
        sentence = []
        first_word = r'^[A-Z]{1}[^\.\!\?]*?$'
        last_word = r'[a-zA-Z0-9]*[\.\!\?]{1}$'
        word = ''

        first_word_found = False

        while not first_word_found:
            idx = random.randint(0, len(self.tokens) - 1)
            word = self.tokens[idx]
            first_word_found = re.search(first_word, word) is not None

        sentence.append(word)
        end_of_sentence = False

        while not end_of_sentence:
            population = list(self.compressed_bigrams[sentence[-1]].keys())
            weights = list(self.compressed_bigrams[sentence[-1]].values())

            word = random.choices(population, weights)[0]
            sentence.append(word)
            end_of_sentence = re.search(last_word, word) is not None and len(sentence) >= min_len

        print(' '.join(sentence))

filename = input()
text_generator = TextGenerator(filename)

for i in range(10):
    text_generator.predict_sentence()




