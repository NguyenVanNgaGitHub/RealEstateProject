from ai.home_recommend.feature import Feature
from joblib import dump, load
from config import ROOT_DIR
import os
from ai.search_engine.data import get_data_by_ids

model = Feature()
model.train_user()
dump(model, os.path.join(ROOT_DIR,"ai","home_recommend","feature.lib"))


# model = load(os.path.join(ROOT_DIR,"ai","home_recommend","feature.lib"))
# recommends = model.recommend("6096557cabfc1590c2a0323e")
#
# list_items = get_data_by_ids(recommends)
# for item in list_items:
#     print(item["price"], item["square"], item["type"], item["district"])