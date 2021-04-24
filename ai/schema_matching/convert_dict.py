from typing import List,Dict

class ConvertDict(Dict[str,List[str]]):
    def add_doc(self, doc_name, set_tokens):
        for token in set_tokens:
            if token in self:
                self[token].append(doc_name)
            else:
                self[token] = [doc_name]

    def find_docs_by_token(self, token):
        if token in self:
            return self[token]
        else:
            return []


