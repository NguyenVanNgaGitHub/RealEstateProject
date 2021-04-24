from ai.search_engine.invert_index import InvertIndex
from ai.search_engine.information_retrival import InformationRetrival
from joblib import load
from operator import itemgetter
import os
from config import ROOT_DIR

class RealEstateSearchEngine:
    def __init__(self, address_weight = 2/5, content_weight = 1/5, type_weight = 2/5, max_result = 100):
        self.address_invert_index : InvertIndex = load(os.path.join(ROOT_DIR, "ai", "search_engine", "address_invert_index.lib"))
        self.content_invert_index : InvertIndex = load(os.path.join(ROOT_DIR, "ai", "search_engine", "content_invert_index.lib"))
        self.type_invert_index : InvertIndex = load(os.path.join(ROOT_DIR, "ai", "search_engine", "type_invert_index.lib"))
        self.address_information_retrieval = InformationRetrival(invert_index=self.address_invert_index)
        self.content_information_retrieval = InformationRetrival(invert_index=self.content_invert_index)
        self.type_information_retrieval = InformationRetrival(invert_index=self.type_invert_index)
        self.address_weight = address_weight
        self.content_weight = content_weight
        self.type_weight = type_weight
        self.max_result = max_result

    def find(self, find_str):
        list_docs_address = self.address_information_retrieval.find(find_str=find_str,max_result=self.max_result)
        list_docs_content = self.content_information_retrieval.find(find_str=find_str,max_result=self.max_result)
        list_docs_type = self.type_information_retrieval.find(find_str=find_str,max_result=self.max_result)
        sumup_docs = {}
        for doc in list_docs_address:
            sumup_docs[doc] = self.address_weight*list_docs_address[doc]
        for doc in list_docs_content:
            if doc in sumup_docs:
                sumup_docs[doc] += self.content_weight*list_docs_content[doc]
            else:
                sumup_docs[doc] = self.content_weight*list_docs_content[doc]
        for doc in list_docs_type:
            if doc in sumup_docs:
                sumup_docs[doc] += self.type_weight*list_docs_type[doc]
            else:
                sumup_docs[doc] = self.type_weight*list_docs_type[doc]
        return dict(sorted(sumup_docs.items(), key=itemgetter(1), reverse=True)[:self.max_result])