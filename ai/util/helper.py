import numpy as np
import gensim
import os
import pickle
import pandas as pd
import config as CONFIG
from database.database import DataBase
from sklearn.feature_extraction.text import TfidfVectorizer
from pyvi import ViTokenizer


ROOT_DIR = os.path.dirname(os.path.abspath(__file__))

class Helper(object):
    FILE_PATH_STOP_WORDS = os.path.join(CONFIG.ROOT_DIR,'ai', 'data', 'stopwords.txt')
    DEFAULT_DIRECTORY_FOR_SAVE = os.path.join(CONFIG.ROOT_DIR, 'ai', 'data')

    @staticmethod
    def build_tf_idf_vector(field_name, path_file_for_save=None):
        # Xây dựng tf-idf cho các trường sử dụng text như: title, description
        # field_values = DataBase.get_field_values(field_name)

        with open(os.path.join(CONFIG.ROOT_DIR, 'ai', 'data', field_name + '.pk'), 'rb') as f:
            # pickle.dump(field_values, f, protocol=pickle.HIGHEST_PROTOCOL)
            field_values = pickle.load(f)

        field_values = Helper.simple_preprocessing_sentences(field_values)
        print(len(field_values))

        tf_idf_vec = TfidfVectorizer()
        tf_idf_vec.fit(field_values)

        if path_file_for_save is None:
            path_file = os.path.join(Helper.DEFAULT_DIRECTORY_FOR_SAVE, 'tf_idf_vec_' + field_name + ".pk")
        else:
            path_file = os.path.join(path_file_for_save, 'tf_idf_vec_' + field_name + ".pk")

        with open(path_file, 'wb') as f:
            pickle.dump(tf_idf_vec, f, protocol=pickle.HIGHEST_PROTOCOL)

        print('Finish Build TF-IDF for', field_name)
        return tf_idf_vec

    @staticmethod
    def simple_preprocessing_sentences(sentences):
        sentences = Helper.clean_sentences(sentences)
        sentences = Helper.tokenizer(sentences)
        sentences = Helper.remove_stop_words(sentences)
        return sentences

    @staticmethod
    def tokenizer(sentences):
        new_sentences = []
        for sentence in sentences:
            new_sentences.append(ViTokenizer.tokenize(sentence))
        return new_sentences

    @staticmethod
    def remove_stop_words(sentences):
        # sentences nên được tokenize trước
        stop_words = np.loadtxt(Helper.FILE_PATH_STOP_WORDS, encoding='utf-8', dtype='str')
        stop_words = stop_words.astype('str')

        new_sentences = []
        for sentence in sentences:
            new_sen = []
            for word in sentence.split(' '):
                if word not in stop_words:
                    new_sen.append(word)
            new_sentences.append(' '.join(new_sen))

        return new_sentences

    @staticmethod
    def clean_sentences(sentences):
        # Xóa bỏ các kí tự không phải là chữ
        new_sentences = []
        for sentence in sentences:
            new_sentences.append(' '.join(gensim.utils.simple_preprocess(sentence)))

        return new_sentences

    @staticmethod
    def save_data_to_local_computer(field_names, path_directory=DEFAULT_DIRECTORY_FOR_SAVE):
        data = DataBase.get_all_data(field_names)

        data_dict = dict()
        for field_name in field_names:
            data_dict[field_name] = []

        for e in data:
            for field_name in field_names:
                if field_name == '_id':
                    data_dict['_id'].append(str(e['_id']))
                else:
                    data_dict[field_name].append(e[field_name])

        df = pd.DataFrame(data_dict)
        df = df.set_index('_id')
        print()
        df.to_csv(os.path.join(CONFIG.ROOT_DIR, 'ai', 'data', "mini-data-clean.csv"))

        print('Number:', len(df))


if __name__ == '__main__':
    # Helper.build_tf_idf_vector('title')
    # Helper.build_tf_idf_vector('description')


    Helper.save_data_to_local_computer([
            "_id",
            "wards",
            "district",
            "price",
            "square"
        ])