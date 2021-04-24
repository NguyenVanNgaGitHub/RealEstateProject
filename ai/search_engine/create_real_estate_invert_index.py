from ai.search_engine.invert_index import InvertIndex
from ai.search_engine.frequence_dict import FrequenceDict
from joblib import dump
from ai.search_engine.text_process import TextProcess
import os
from config import ROOT_DIR

def create_real_estate_invert_index(data):
    text_processor = TextProcess()
    address_frequence_dict = FrequenceDict()
    content_frequence_dict = FrequenceDict()
    type_frequence_dict = FrequenceDict()
    address_invert_index = InvertIndex(frequence_dict=address_frequence_dict)
    content_invert_index = InvertIndex(frequence_dict=content_frequence_dict)
    type_invert_index = InvertIndex(frequence_dict=type_frequence_dict)

    for item in data:
        set_content_words = text_processor.extract_words(item["description"]+" "+item["title"])
        set_address_words = text_processor.extract_words(item["address"])
        set_type_words = text_processor.extract_words(item["type"])
        address_frequence_dict.add_words(set_words=set_address_words)
        content_frequence_dict.add_words(set_words=set_content_words)
        type_frequence_dict.add_words(set_words=set_type_words)
        address_invert_index.add_doc(doc_name=str(item["_id"]), set_tokens=set_address_words)
        content_invert_index.add_doc(doc_name=str(item["_id"]), set_tokens=set_content_words)
        type_invert_index.add_doc(doc_name=str(item["_id"]), set_tokens=set_type_words)

    dump(address_frequence_dict, os.path.join(ROOT_DIR, "ai", "search_engine", "address_frequence_dict.lib"))
    dump(content_frequence_dict, os.path.join(ROOT_DIR, "ai", "search_engine", "content_frequence_dict.lib"))
    dump(type_frequence_dict, os.path.join(ROOT_DIR, "ai", "search_engine", "type_frequence_dict.lib"))

    dump(address_invert_index, os.path.join(ROOT_DIR, "ai", "search_engine", "address_invert_index.lib"))
    dump(content_invert_index, os.path.join(ROOT_DIR, "ai", "search_engine", "content_invert_index.lib"))
    dump(type_invert_index, os.path.join(ROOT_DIR, "ai", "search_engine", "type_invert_index.lib"))


