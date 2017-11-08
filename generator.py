import numpy.random as npr
from markov_updater import MarkovUpdater

class Generator:
    def __init__(self, words, steps=[2,3,4], no_aliases=False, length_control=False):
        self.mus = list()
        for step in steps:
            mu = MarkovUpdater(words, step)
            mu.main_update()
            self.mus.append(mu)
        
        self.words = words
        self.no_aliases = no_aliases
        self.length_control = length_control
        if self.length_control:
            self.max_length = max(map(len, self.words))
            self.min_length = min(map(len, self.words))
    
    def generate(self):
        keys = dict()
        
        curr = npr.choice(self.mus)
        s = curr.choose_starter()
        key = keys[curr] = s
        while s[-1] != "\n":
            s += curr.choose_next_letter(key)
            for mu in self.mus:
                keys[mu] = s[-mu.step:]
            prev = curr
            curr = npr.choice(self.mus)
            if curr.step > prev.step + 1:
                curr = prev
            key = keys[curr]
        
        word = s[:-1]    
        if self.no_aliases and word in self.words:
            word = self.generate()
        elif self.length_control:
            cond = self.min_length <= len(word) <= self.max_length
            if not cond:
                word = self.generate()

        return word.title()  # capitalizes first letter
        
