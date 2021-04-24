from typing import Dict
from operator import itemgetter
import copy

class FrequenceDict(Dict[str,int]):
    def add_words(self, set_words):
        for word in set_words:
            if word in self:
                self[word] = self[word]+1
            else:
                self[word] = 1

