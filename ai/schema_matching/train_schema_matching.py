from ai.schema_matching.schema_matching import SchemaMatching
from ai.schema_matching.data import get_data
from joblib import load
import pandas as pd
from config import ROOT_DIR
import os

'''
schema_matching = SchemaMatching()
data = get_data()

schema_matching.fit_data(data=data)
'''


schema_matching : SchemaMatching = load(os.path.join(ROOT_DIR,"ai","schema_matching", "schema_matching.lib"))
data = pd.read_csv(os.path.join(ROOT_DIR,"ai","schema_matching",'crawling_real_estate_alonhadat.com.vn.csv')
                   ,header=None,
                   names=['title', 'giá cả', 'diện tích', 'địa chỉ', 'xã phường', 'quận huyện', 'tỉnh thành phố',
                          'loại hình', 'mô tả', 'người bán', 'thời gian', 'nguồn', 'ảnh'])
result = schema_matching.matching_data(data.sample(100, random_state=99))
