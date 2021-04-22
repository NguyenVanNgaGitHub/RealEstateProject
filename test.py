from search_engine.data import get_data_by_ids,get_data
from search_engine.real_estate_search_engine import RealEstateSearchEngine
from search_engine.invert_index import InvertIndex
from search_engine.frequence_dict import FrequenceDict
from search_engine.information_retrival import InformationRetrival
from search_engine.create_real_estate_invert_index import create_real_estate_invert_index
'''
data = get_data()
create_real_estate_invert_index(data=data)
'''

search_engine = RealEstateSearchEngine()
recomend_docs = search_engine.find("chung cư quận Đống Đa")

recomend_real_estates = get_data_by_ids(ids=recomend_docs.keys())

for item in recomend_real_estates:
    print("\n\n---------------------------------")
    print("Address",item["address"])
    print("Type",item["type"])
    print("Title",item["title"])
    print("Description",item["description"][:200])



