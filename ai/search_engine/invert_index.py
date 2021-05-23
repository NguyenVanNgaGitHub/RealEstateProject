from typing import List,Dict
from ai.search_engine.frequence_dict import FrequenceDict
from nltk.metrics import edit_distance

class InvertIndex(Dict[str,List[str]]):
    def __init__(self, frequence_dict: FrequenceDict):
        self.frequence_dict = frequence_dict
        self.num_docs = 0

    def add_doc(self, doc_name, set_tokens):
        self.num_docs += 1
        for token in set_tokens:
            if token in self.frequence_dict:
                self.frequence_dict[token] = self.frequence_dict[token]+1
                if token in self:
                    self[token].append(doc_name)
                else:
                    self[token] = [doc_name]

    def find_most_similar_token(self, token):
        if token in self:
            return [token], 0
        min_edit = float("+inf")
        best_fit = []
        for key in self:
            ds = edit_distance(token,key)
            if min_edit>ds:
                best_fit=[key]
                min_edit=ds
            elif min_edit==ds:
                best_fit.append(key)
        if min_edit>min(4,0.1*len(token)):
            return [],float("+inf")
        else:
            return best_fit,min_edit


    def find_docs_by_token(self, token):
        if token in self:
            return self[token]
        else:
            return None


