from nltk.tokenize import TweetTokenizer

class Analyzer():

    def __init__(self, positives, negatives):
        file = open(positives, "r")
        self.positives = [line.rstrip() for line in file.readlines() if line[0] != ";" and not line.isspace()]
        file.close()

        file = open(negatives, "r")
        self.negatives = [line.rstrip() for line in file.readlines() if line[0] != ";" and not line.isspace()]
        file.close()

        self.tokenizer = TweetTokenizer()

    def analyze(self, text):
        result = 0
        text = self.tokenizer.tokenize(text)
        for word in text:
            if word in self.positives:
                result += 1
            elif word in self.negatives:
                result -= 1
        return result
