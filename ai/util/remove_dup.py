import os, csv, json, codecs, re
from pyvi import ViTokenizer, ViPosTagger
import math
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity

# khong tin idf boi vi dang so sanh 1 tai lieu A vs tl B xem co trung k --> N=1, Idf = 1 or vo cung
# co tinh "type" check trung lap khong?, gia tri type cua cac trang co khac nhau, chua nhau k ?

class RemoveDuplication():
    SPECIAL_CHARACTER = '?%@$.,=+-!;/()*"&^:#|\n\t\'[]}{\\0123456789'
    STOPWORDS_PATH = "../data/stopwords.txt"

    def __init__(self, pathFile1, pathListFile):
        # file1: file check trung lap
        # listFile: file ung vien check trung lap
        self.pathFile1 = pathFile1
        self.pathListFile = pathListFile
        self.stopwords = [stopword.split('\n')[0] for stopword in codecs.open(self.STOPWORDS_PATH, "r", "utf-8").readlines()]
        
        self.file1 = json.load(codecs.open(self.pathFile1,'r','utf-8'))
        self.listFile = json.load(codecs.open(self.pathListFile,'r','utf-8'))
    def removeStopwords(self, data):
        try:
            return [token for token in data.split() if (token not in self.stopwords) and (token.upper().isupper())]
        except:
            return []
    
    def tokenizer(self, item):

        # tokenizer
        title_token = self.removeStopwords(re.sub("(\d+(\,*\.*\d+)+)", "_NUMBER", ViTokenizer.tokenize(item['title'])))
        description_token = self.removeStopwords(re.sub("(\d+(\,*\.*\d+)+)", "_NUMBER", ViTokenizer.tokenize(item['description'])))
    
        # word count
        item['title_wc'] = {word:title_token.count(word) for word in title_token}
        item['description_wc'] = {word:description_token.count(word) for word in description_token}

        # remove col
        self.list_key = ['title_wc', 'square', 'price', 'description_wc']
        for key in list(item.keys()):
            if key not in self.list_key:
                del item[key]
        
        return item

    def sim_square(self, s1, s2):
        # voi nhung dien tich lon, chenh lech co the cao hon, 1 thay bang 5, 10 --> visualize dl
        return 1 - abs(float(s1) - float(s2))

    def sim_price(self, p1, p2):
        # thay 5 bang so lay nguong loc giam so luong check tin trung luc truoc
        return (5 - abs(float(p1)-float(p2)))/5

    def similarity(self, threshold=1):
        # tokenizer, remove stopword, word count
        item1 = self.tokenizer(self.file1[list(self.file1.keys())[0]])
        listItem = {key:self.tokenizer(self.listFile[key]) for key in list(self.listFile.keys())[:1]}
        w = np.array([0.3, 0.3, 0.1, 0.2])
        sim_item1_item2 = np.empty(shape=(0,4))

        for key in listItem.keys():
            # khong can check bvi truoc khi check dup da sd buoc loc ban ghi co the trung lap dua tren cac tieu chi ve gia, dien tic
            # if self.sim_square(item1['square'], item2['square']) <0:
            #     continue
            item2 = listItem[key]

            vector_sim = [self.sim_square(item1['square'], item2['square']), self.sim_price(item1['price'], item2['price'])]
            for attr in ['title_wc', 'description_wc']:
                wordSet = set(item1[attr]).union(set(item2[attr]))
                vector_item1 = [ item1[attr][word] if word in item1[attr].keys() else 0 for word in wordSet] 
                vector_item2 = [ item2[attr][word] if word in item2[attr].keys() else 0 for word in wordSet]           
                vector_sim.append(cosine_similarity([vector_item1], [vector_item2]).tolist()[0][0])
            sim_item1_item2 = np.vstack([sim_item1_item2, np.array(vector_sim)])
        return np.any(np.dot(sim_item1_item2, w) > threshold)

rmDup = RemoveDuplication('./tfidf_sim/data_need_check.json', './tfidf_sim/data.json')
print(rmDup.similarity(0.2))