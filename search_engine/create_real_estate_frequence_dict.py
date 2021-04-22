from search_engine.frequence_dict import FrequenceDict
from search_engine.text_process import TextProcess
from joblib import dump
import os
from config import ROOT_DIR
def create_real_estate_frequence_dict(data):
    text_processor = TextProcess()
    address_frequence_dict = FrequenceDict()
    content_frequence_dict = FrequenceDict()
    type_frequence_dict = FrequenceDict()

    for item in data:
        set_content_words = text_processor.extract_words(item["description"]+" "+item["title"])
        set_address_words = text_processor.extract_words(item["address"])
        set_type_words = text_processor.extract_words(item["type"])
        address_frequence_dict.add_words(set_words=set_address_words)
        content_frequence_dict.add_words(set_words=set_content_words)
        type_frequence_dict.add_words(set_words=set_type_words)


    dump(address_frequence_dict, os.path.join(ROOT_DIR,"search_engine","address_frequence_dict.lib"))
    dump(content_frequence_dict, os.path.join(ROOT_DIR,"search_engine","content_frequence_dict.lib"))
    dump(type_frequence_dict, os.path.join(ROOT_DIR,"search_engine","type_frequence_dict.lib"))



