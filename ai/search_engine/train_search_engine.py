from ai.search_engine.data import get_data_by_ids
from ai.search_engine.real_estate_search_engine import RealEstateSearchEngine
from ai.search_engine.data import get_data
from ai.search_engine.create_real_estate_invert_index import create_real_estate_invert_index

data = get_data()
create_real_estate_invert_index(data=data)
