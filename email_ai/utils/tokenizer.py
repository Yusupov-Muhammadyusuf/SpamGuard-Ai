from collections import Counter

class Tokenizer:
    def __init__(self, max_words=5000):
        self.max_words = max_words
        self.word2idx = {}

    def fit(self, texts):
        counter = Counter()

        for text in texts:
            words = text.split()
            counter.update(words)

        most_common = counter.most_common(self.max_words)

        self.word2idx = {
            word: idx + 1 for idx, (word, _) in enumerate(most_common)
        }

    def encode(self, text):
        return [self.word2idx.get(word, 0) for word in text.split()]