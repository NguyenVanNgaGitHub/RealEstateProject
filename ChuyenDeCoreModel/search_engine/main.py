from search_engine.data import get_data_by_ids
from search_engine.real_estate_search_engine import RealEstateSearchEngine

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



