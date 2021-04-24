import re
from nltk.metrics import edit_distance
from ai.schema_matching.convert_dict import ConvertDict
from nltk.util import trigrams
from ai.schema_matching.text_process import TextProcess
from joblib import dump
import pandas as pd
from config import ROOT_DIR
import os
import scipy.stats as st
import numpy as np

class SchemaMatching:
    def __init__(self, data_weigth=0.7, meta_weigth=0.3, content_weight=0.7, len_weight=0.3):
        self.text_processor = TextProcess()
        self.data_weight = data_weigth
        self.meta_weight = meta_weigth
        self.content_weight = content_weight
        self.len_weight = len_weight

    def fit_data(self, data):
        self.title_convert_dict = ConvertDict()
        self.type_convert_dict = ConvertDict()
        self.ward_convert_dict = ConvertDict()
        self.district_convert_dict = ConvertDict()
        self.address_convert_dict = ConvertDict()
        self.description_convert_dict = ConvertDict()
        self.seller_convert_dict = ConvertDict()

        self.title_len = []
        self.type_len = []
        self.ward_len = []
        self.district_len = []
        self.address_len = []
        self.description_len = []
        self.seller_len = []

        self.price_list = []
        self.square_list = []

        self.title_dict_len = {}
        self.type_dict_len = {}
        self.ward_dict_len = {}
        self.district_dict_len = {}
        self.address_dict_len = {}
        self.description_dict_len = {}
        self.seller_dict_len = {}

        for item in data:

            title_words = self.text_processor.extract_words(item["title"])
            self.title_convert_dict.add_doc(str(item["_id"]),title_words)
            self.title_len.append(len(item["title"]))
            self.title_dict_len[str(item["_id"])] = len(title_words)

            type_words = self.text_processor.extract_words(item["type"])
            self.type_convert_dict.add_doc(str(item["_id"]), type_words)
            self.type_len.append(len(item["type"]))
            self.type_dict_len[str(item["_id"])] = len(type_words)

            ward_words = self.text_processor.extract_words(item["wards"])
            self.ward_convert_dict.add_doc(str(item["_id"]), ward_words)
            self.ward_len.append(len(item["wards"]))
            self.ward_dict_len[str(item["_id"])] = len(ward_words)

            district_words = self.text_processor.extract_words(item["district"])
            self.district_convert_dict.add_doc(str(item["_id"]), district_words)
            self.district_len.append(len(item["district"]))
            self.district_dict_len[str(item["_id"])] = len(district_words)

            address_words = self.text_processor.extract_words(item["address"])
            self.address_convert_dict.add_doc(str(item["_id"]), address_words)
            self.address_len.append(len(item["address"]))
            self.address_dict_len[str(item["_id"])] = len(address_words)

            description_words = self.text_processor.extract_words(item["description"])
            self.description_convert_dict.add_doc(str(item["_id"]), description_words)
            self.description_len.append(len(item["description"]))
            self.description_dict_len[str(item["_id"])] = len(description_words)

            seller_words = set(trigrams(item["seller"]))
            self.seller_convert_dict.add_doc(str(item["_id"]), seller_words)
            self.seller_len.append(len(item["seller"]))
            self.seller_dict_len[str(item["_id"])] = len(seller_words)

            try:
                self.square_list.append(float(item["square"]))
            except:
                pass

            try:
                self.price_list.append(float(item["price"]))
            except:
                pass

        self.title_confidence_interval = self.compute_confidence_interval(data=self.title_len)
        self.type_confidence_interval = self.compute_confidence_interval(data=self.type_len)
        self.ward_confidence_interval = self.compute_confidence_interval(data=self.ward_len)
        self.district_confidence_interval = self.compute_confidence_interval(data=self.district_len)
        self.address_confidence_interval = self.compute_confidence_interval(data=self.address_len)
        self.description_confidence_interval = self.compute_confidence_interval(data=self.description_len)
        self.seller_confidence_interval = self.compute_confidence_interval(data=self.seller_len)
        self.square_confidence_interval = self.compute_confidence_interval(data=self.square_list)
        self.price_confidence_interval = self.compute_confidence_interval(data=self.price_list)

        dump(self, os.path.join(ROOT_DIR,"ai","schema_matching", "schema_matching.lib"))


    def compute_confidence_interval(self, data, lower=10, upper=90):
        return (np.percentile(data,lower),np.percentile(data,upper))

    def label_similarity(self, label1, label2):
        ds = edit_distance(label1, label2)
        return 1-ds/max(len(label1),len(label2))

    def find_max_string_similar(self, item, convert_dict: ConvertDict, dict_len: {}, use_trigram=False):
        if use_trigram:
            item_words = set(trigrams(item))
        else:
            item_words = self.text_processor.extract_words(item)
        list_docs = {}
        for word in item_words:
            all_docs = convert_dict.find_docs_by_token(word)
            for doc in all_docs:
                if doc in list_docs:
                    list_docs[doc]=list_docs[doc]+1
                else:
                    list_docs[doc]=1
        for doc in list_docs:
            list_docs[doc] = list_docs[doc]/max(len(item_words),dict_len[doc])
        if len(list_docs):
            return max(list_docs.values())
        else:
            return 0

    def title_matching(self, itemList, label):
        sum = 0
        for item in itemList:
            if type(item)==str:
                content_simi = self.find_max_string_similar(item, self.title_convert_dict, self.title_dict_len)
                if len(item)>=self.title_confidence_interval[0] and len(item)<=self.title_confidence_interval[1]:
                    len_simi = 1
                else:
                    len_simi = 0
                sum+=self.content_weight*content_simi+self.len_weight*len_simi
        data_match = sum / len(itemList)
        meta_match = self.label_similarity(label, "title")
        return self.data_weight * data_match + self.meta_weight * meta_match

    def type_matching(self, itemList, label):
        sum = 0
        for item in itemList:
            if type(item)==str:
                content_simi = self.find_max_string_similar(item, self.type_convert_dict, self.type_dict_len)
                if len(item) >= self.type_confidence_interval[0] and len(item) <= self.type_confidence_interval[1]:
                    len_simi = 1
                else:
                    len_simi = 0
                sum += self.content_weight * content_simi + self.len_weight * len_simi
        data_match = sum / len(itemList)
        meta_match = self.label_similarity(label, "type")
        return self.data_weight * data_match + self.meta_weight * meta_match

    def wards_matching(self, itemList, label):
        sum = 0
        for item in itemList:
            if type(item)==str:
                content_simi = self.find_max_string_similar(item, self.ward_convert_dict, self.ward_dict_len)
                if len(item) >= self.ward_confidence_interval[0] and len(item) <= self.ward_confidence_interval[1]:
                    len_simi = 1
                else:
                    len_simi = 0
                sum += self.content_weight * content_simi + self.len_weight * len_simi
        data_match = sum / len(itemList)
        meta_match = self.label_similarity(label, "wards")
        return self.data_weight * data_match + self.meta_weight * meta_match

    def district_matching(self, itemList, label):
        sum = 0
        for item in itemList:
            if type(item)==str:
                content_simi = self.find_max_string_similar(item, self.district_convert_dict, self.district_dict_len)
                if len(item) >= self.district_confidence_interval[0] and len(item) <= self.district_confidence_interval[1]:
                    len_simi = 1
                else:
                    len_simi = 0
                sum += self.content_weight * content_simi + self.len_weight * len_simi
        data_match = sum / len(itemList)
        meta_match = self.label_similarity(label, "district")
        return self.data_weight * data_match + self.meta_weight * meta_match

    def province_matching(self, itemList, label):
        sum = 0
        for item in itemList:
            if item == "Hà Nội":
                sum+=1
        data_match = sum / len(itemList)
        meta_match = self.label_similarity(label, "province")
        return self.data_weight * data_match + self.meta_weight * meta_match

    def address_matching(self, itemList, label):
        sum = 0
        for item in itemList:
            if type(item)==str:
                content_simi = self.find_max_string_similar(item, self.address_convert_dict, self.address_dict_len)
                if len(item) >= self.address_confidence_interval[0] and len(item) <= self.address_confidence_interval[1]:
                    len_simi = 1
                else:
                    len_simi = 0
                sum += self.content_weight * content_simi + self.len_weight * len_simi
        data_match = sum / len(itemList)
        meta_match = self.label_similarity(label, "address")
        return self.data_weight * data_match + self.meta_weight * meta_match

    def square_matching(self, itemList, label):
        sum = 0
        for item in itemList:
            try:
                item = float(item)
                if item >= self.square_confidence_interval[0] and item <= self.square_confidence_interval[1]:
                    sum += 1
            except:
                pass
        data_match = sum / len(itemList)
        meta_match = self.label_similarity(label, "square")
        return self.data_weight * data_match + self.meta_weight * meta_match

    def price_matching(self, itemList, label):
        sum = 0
        for item in itemList:
            try:
                item = float(item)
                if item>= self.price_confidence_interval[0] and item<= self.price_confidence_interval[1]:
                    sum += 1
            except:
                pass
        data_match = sum / len(itemList)
        meta_match = self.label_similarity(label, "price")
        return self.data_weight * data_match + self.meta_weight * meta_match

    def description_matching(self, itemList, label):
        sum = 0
        for item in itemList:
            if type(item)==str:
                content_simi = self.find_max_string_similar(item, self.description_convert_dict, self.description_dict_len)
                if len(item) >= self.description_confidence_interval[0] and len(item) <= self.description_confidence_interval[1]:
                    len_simi = 1
                else:
                    len_simi = 0
                sum += self.content_weight * content_simi + self.len_weight * len_simi
        data_match = sum / len(itemList)
        meta_match = self.label_similarity(label, "description")
        return self.data_weight * data_match + self.meta_weight * meta_match

    def seller_matching(self, itemList, label):
        sum = 0
        for item in itemList:
            if type(item)==str:
                content_simi = self.find_max_string_similar(item, self.seller_convert_dict, self.seller_dict_len, use_trigram=True)
                if len(item) >= self.seller_confidence_interval[0] and len(item) <= self.seller_confidence_interval[1]:
                    len_simi = 1
                else:
                    len_simi = 0
                sum += self.content_weight * content_simi + self.len_weight * len_simi
        data_match = sum / len(itemList)
        meta_match = self.label_similarity(label, "seller")
        return self.data_weight * data_match + self.meta_weight * meta_match

    def source_matching(self, itemList, label):
        key_words_weight = {"http": 0.2,
                            ".com|.vn": 0.5,
                            " ": -0.3,
                            ".jpg|.png": -0.5}
        sum = 0
        for item in itemList:
            if type(item)==str:
                item = item.lower()
                for key_word in key_words_weight:
                    if re.search(key_word, item):
                        sum += key_words_weight[key_word]
        data_match = sum / len(itemList)
        meta_match = self.label_similarity(label, "source")
        return self.data_weight * data_match + self.meta_weight * meta_match

    def image_matching(self, itemList, label):
        key_words_weight = {"http": 0.2,
                            "file": 0.2,
                            " ": -0.3,
                            ".jpg|.png": 0.6}
        sum = 0
        for item in itemList:
            if type(item)==str:
                item = item.lower()
                for key_word in key_words_weight:
                    if re.search(key_word,item):
                        sum+=key_words_weight[key_word]
        data_match = sum/len(itemList)
        meta_match = self.label_similarity(label, "image")
        return self.data_weight * data_match + self.meta_weight * meta_match

    def time_matching(self, itemList, label):
        sum = 0
        for item in itemList:
            if type(item)==str:
                if re.search(r"^[0-9]{2}/[0-9]{2}/[0-9]{4}$",item):
                    sum+=1
        data_match = sum/len(itemList)
        meta_match = self.label_similarity(label,"time")
        return self.data_weight*data_match+self.meta_weight*meta_match


    def matching_data(self, data: pd.DataFrame):
        result = {}
        for col in data.columns:
            itemList = [str(item) for item in data[col]]
            max = 0

            sc = self.title_matching(itemList=itemList,label=col)
            if sc>max:
                max=sc
                result[col] = "title"

            sc = self.type_matching(itemList=itemList, label=col)
            if sc > max:
                max = sc
                result[col] = "type"

            sc = self.wards_matching(itemList=itemList, label=col)
            if sc > max:
                max = sc
                result[col] = "wards"

            sc = self.district_matching(itemList=itemList, label=col)
            if sc > max:
                max = sc
                result[col] = "district"

            sc = self.province_matching(itemList=itemList, label=col)
            if sc > max:
                max = sc
                result[col] = "province"

            sc = self.address_matching(itemList=itemList, label=col)
            if sc > max:
                max = sc
                result[col] = "address"

            sc = self.square_matching(itemList=itemList, label=col)
            if sc > max:
                max = sc
                result[col] = "square"

            sc = self.price_matching(itemList=itemList, label=col)
            if sc > max:
                max = sc
                result[col] = "price"

            sc = self.description_matching(itemList=itemList, label=col)
            if sc > max:
                max = sc
                result[col] = "description"

            sc = self.seller_matching(itemList=itemList, label=col)
            if sc > max:
                max = sc
                result[col] = "seller"

            sc = self.source_matching(itemList=itemList, label=col)
            if sc > max:
                max = sc
                result[col] = "source"

            sc = self.image_matching(itemList=itemList, label=col)
            if sc > max:
                max = sc
                result[col] = "image"

            sc = self.time_matching(itemList=itemList, label=col)
            if sc > max:
                max = sc
                result[col] = "time"

            result[col] = result[col]+" : "+str(max)
            print(col,"<--->", result[col])
        return result




