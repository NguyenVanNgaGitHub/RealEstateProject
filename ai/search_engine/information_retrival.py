from ai.search_engine.invert_index import InvertIndex
from ai.search_engine.text_process import TextProcess
from operator import itemgetter


class InformationRetrival:
    def __init__(self, invert_index : InvertIndex):
        self.invert_index = invert_index
        self.text_process = TextProcess()

    def find(self, find_str, max_result=100):
        set_tokens = self.text_process.extract_words(find_str)

        similar_docs = {}
        for token in set_tokens:
            list_similar, edit_ds = self.invert_index.find_most_similar_token(token)
            for tok in list_similar:
                weight =self.invert_index.frequence_dict[tok] / (self.invert_index.num_docs * (edit_ds + 1))
                list_docs = self.invert_index.find_docs_by_token(tok)
                for doc in list_docs:
                    if doc in similar_docs:
                        similar_docs[doc] += weight
                    else:
                        similar_docs[doc] = weight
        return dict(sorted(similar_docs.items(), key=itemgetter(1), reverse=True)[:max_result])


