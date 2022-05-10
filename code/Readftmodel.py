import fasttext
import re
fasttext.FastText.eprint = lambda x: None

class Model:
    def __init__(self, model_path):
        self.model = fasttext.load_model(model_path)

    def clue_to_list_of_words(self, clue, regex):
        words = []
        pcts = []
        results = self.model.predict(clue, k=1000000)
        regex = re.compile(regex)
        i = 0
        for word in results[0]:
            word = word.replace("__label__", "")
            if regex.search(word):
                words.append(word)
                pcts.append(results[1][i])
                i += 1
        return pcts, words

    def get_precedence(self, across, down):
        precedence = []
        for key, value in down.items():
            precedence.append(('down', key, value, self.model.predict(value, k=1)[1][0]))
        for key, value, in across.items():
            precedence.append(('across', key, value, self.model.predict(value, k=1)[1][0]))
        precedence.sort(key=lambda x: x[3], reverse=True)
        return precedence