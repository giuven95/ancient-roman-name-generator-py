import numpy.random as npr


def abs_to_rel_dict(d):
    new_d = dict()
    tot = sum(d[key] for key in d)
    if tot == 0:
        return d
    else:
        for key in d:
            new_d[key] = d[key] / tot
        return new_d


class Updater:
    def __init__(self, step):
        self.start = dict()
        self.cont = dict()
        self.step = step

    def choose_starter(self):
        d = self.start
        keys = list(d.keys())
        probs = [d[key] for key in keys]
        return npr.choice(keys, p=probs)

    def choose_next_letter(self, key):
        d = self.cont[key]
        keys = list(d.keys())
        probs = [d[key] for key in keys]
        return npr.choice(keys, p=probs)

    def main_update(self, words):
        self.starter_update(words)
        self.next_letter_update(words)
        self.start = abs_to_rel_dict(self.start)
        for s in self.cont:
            self.cont[s] = abs_to_rel_dict(self.cont[s])

    def starter_update(self, words):
        def func(s, next_letter):
            if s not in self.start:
                self.start[s] = 0
            self.start[s] += 1
            return True

        for word in words:
            self.update_loop(word, func)

    def next_letter_update(self, words):
        def func(s, next_letter):
            if s not in self.cont:
                self.cont[s] = dict()
            d = self.cont[s]

            if next_letter not in d:
                d[next_letter] = 0
            d[next_letter] += 1
            return False

        for word in words:
            self.update_loop(word, func)

    def update_loop(self, word, func):
        s = ""
        i = -self.step
        over = False
        for letter in word:
            s += letter
            i += 1

            try:
                next_letter = word[i + self.step]
            except IndexError:
                next_letter = "\n"

            if i < 0:
                pass
            else:
                over = func(s, next_letter)
                s = s[1:]

            if over:
                break
