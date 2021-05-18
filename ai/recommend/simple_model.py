import pickle
import time
import pandas as pd
import os
import config as CONFIG
import sys
from database.database import DataBase
from ai.util.similarity import Similarity
from bson import ObjectId
import codecs


class SimpleRecommendSystem(object):
    # Tim cac tin dua tren do tuong dong giua cac ban tin
    # Luat: Uu tien cac ban tin cung phuong, quan
    PATH_DATA_DIRECTORY = '../ai/data/'
    def __init__(self, sim_threshold=0.3, user=None, post=None, num_of_recommend_post=None):
        self.database = DataBase()
        self.user = user
        self.post = post
        self.num_of_recommend_post = num_of_recommend_post
        self.SIM_THRESHOLD = sim_threshold

    def simple_find_recommend_posts(self, online=False):
        # find candidate which is same district, wards
        recommend_docs = []

        if online:
            candidate_docs = self.find_candidate_docs_online()
        else:
            candidate_docs = self.find_candidate_docs_offline()

        if len(candidate_docs) >= self.num_of_recommend_post:
            return candidate_docs[0:self.num_of_recommend_post]

        for doc in candidate_docs:
            recommend_docs.append(doc)

        if online:
            candidate_docs = self.find_candidate_docs_offline()
        else:
            candidate_docs = self.find_candidate_docs_online()

        if candidate_docs is not None and len(candidate_docs) != 0:
            for doc in candidate_docs[0:(self.num_of_recommend_post - len(recommend_docs))]:
                recommend_docs.append(doc)

        delete_index = -1
        for index, doc in enumerate(recommend_docs):
            if str(doc['_id']) == str(self.post['_id']):
                delete_index = index

        print(delete_index)
        if delete_index != -1:
            del recommend_docs[delete_index]

        return recommend_docs

    def find_recommend_posts(self, online=False):
        # find candidate which is same district, wards
        recommend_docs = []
        start = time.time()
        if online:
            candidate_docs = self.find_candidate_docs_online()
        else:
            candidate_docs = self.find_candidate_docs_offline()
        end = time.time()

        if len(candidate_docs) == 0:
            print('Cannot find candidate doc')
            return []

        for doc in self.find_recommend_docs(source_doc=self.post, docs=candidate_docs, num_doc=self.num_of_recommend_post, sim_threshold=self.SIM_THRESHOLD):
            doc['_id'] = str(doc['_id'])
            recommend_docs.append(doc)

        if len(recommend_docs) < self.num_of_recommend_post:
            if online:
                candidate_docs = self.find_candidate_docs_online()
            else:
                candidate_docs = self.find_candidate_docs_offline()
            print(len(candidate_docs))
            for doc in self.find_recommend_docs(source_doc=self.post, docs=candidate_docs, num_doc=self.num_of_recommend_post - len(recommend_docs), sim_threshold=self.SIM_THRESHOLD):
                doc['_id'] = str(doc['_id'])
                recommend_docs.append(doc)

        delete_index = -1
        for index, doc in enumerate(recommend_docs):
            if str(doc['_id']) == str(self.post['_id']):
                delete_index = index

        print(delete_index)
        if delete_index != -1:
            del recommend_docs[delete_index]

        return recommend_docs

    def find_candidate_docs_online(self):
        filter_district = {
            "$eq": self.post['district']
        }

        filter_ = {

            "district": filter_district
        }

        return self.database.find_real_estate_document(filter_)

    def find_candidate_docs_offline(self):
        df = pd.read_csv(os.path.join(CONFIG.ROOT_DIR, 'ai', 'data', 'mini-data-clean.csv'), index_col=0)

        df_candi = df[df['district'] == self.post['district']]

        try:
            df_candi.drop(index=[str(self.post['_id'])], inplace=True)
        except Exception:
            pass


        ids = df_candi.index.to_numpy()

        for index, id in enumerate(ids):
            ids[index] = ObjectId(id)
        filter_ = {
            "_id": {
                "$in": ids.tolist()
            }
        }
        projection = ['title', 'description', 'price', 'square', 'image']
        start = time.time()
        candidates = self.database.find_real_estate_document(filter_, projection)
        end = time.time()

        return candidates

    @staticmethod
    def find_recommend_docs(source_doc, docs, num_doc, sim_threshold):
        result = []
        count = 0
        with open(os.path.join(CONFIG.ROOT_DIR, 'ai', 'data', 'tf_idf_vec_description.pk'), 'rb') as f:
            tf_idf_vec_description = pickle.load(f)
        with open(os.path.join(CONFIG.ROOT_DIR, 'ai', 'data', 'tf_idf_vec_title.pk'), 'rb') as f:
            tf_idf_vec_title = pickle.load(f)
        titles = [doc['title'] for doc in docs]
        descriptions = [doc['description'] for doc in docs]
        sim_titles = Similarity.tf_idf_similarities(source_doc['title'], titles, tf_idf_vec_title)
        sim_descriptions = Similarity.tf_idf_similarities(source_doc['description'], descriptions, tf_idf_vec_description)

        for index, doc in enumerate(docs):
            sim = 0
            sim_square = Similarity.similarity_for_price(source_doc['price'], doc['price'])
            sim_price = Similarity.similarity_for_square(source_doc['square'], doc['square'])
            sim_title = sim_titles[index]
            sim_description = sim_descriptions[index]

            a = 0.1
            b = 0.1
            c = 0.4
            d = 0.3

            if a*sim_square + b*sim_price + c*sim_title + d*sim_description > sim_threshold:
                result.append(doc)
                count += 1

            if count >= num_doc:
                break

        return result

if __name__ == '__main__':
    with open('../data/example_bds.pk', 'rb') as f:
        post = pickle.load(f)
    for c in post['district']:
        print(c)
    #
    # recommend_sys = SimpleRecommendSystem(post=post, num_of_recommend_post=5)
    # posts = recommend_sys.find_recommend_posts(online=True)
    print(post)
    df = pd.read_csv(os.path.join(CONFIG.ROOT_DIR, 'ai', 'data', 'mini-data.csv'), index_col=0)
    print(str(post['district']).encode('utf-8') == 'Ba Vì'.encode('utf-8'))
    print(df[df['district'] == 'Ba Vì'].head())

