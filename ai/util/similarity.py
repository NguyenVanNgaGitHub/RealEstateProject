from nltk.metrics import edit_distance
from ai.util.helper import Helper
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.metrics.pairwise import linear_kernel

class Similarity(object):
    @staticmethod
    def ed_similarity(s1, s2):
        return 1 - edit_distance(s1, s2) / max(len(s1), len(s2))


    @staticmethod
    def tf_idf_similarity(s1, s2, tf_idf_vec):
        s1, s2 = Helper.simple_preprocessing_sentences([s1, s2])
        v = tf_idf_vec.transform([s1, s2])

        return cosine_similarity([v[0].todense()], [v[1].todense()])[0][0]

    @staticmethod
    def tf_idf_similarities(s, other, tf_idf_vec):
        s = Helper.simple_preprocessing_sentences([s])[0]
        other = Helper.simple_preprocessing_sentences(other)

        s_v = tf_idf_vec.transform([s])
        other_v = tf_idf_vec.transform(other)

        cosine_similarities = linear_kernel(s_v, other_v).flatten()

        return cosine_similarities

    @staticmethod
    def similarity_for_price(p_source, p_another):

        if (p_another >= p_source*0.25) and (p_another <= p_source * 2):
            return 1
        elif (p_another >= p_source*0.1) and (p_another < p_source * 3):
            return 0.7
        else:
            return 0.55

    @staticmethod
    def similarity_for_square(s_source, s_another):
        if (s_another >= s_source * 0.25) and (s_another <= s_source * 1.75):
            return 1
        elif (s_another >= s_source * 0.1) and (s_another < s_source * 2.5):
            return 0.7
        else:
            return 0.55


# print(cosine_similarity([[1,2,3]], [[1,2,3]])[0][0])