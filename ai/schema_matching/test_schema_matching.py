from ai.schema_matching.schema_matching import SchemaMatching
from ai.schema_matching.data import get_data
from joblib import load
import pandas as pd
from config import ROOT_DIR
import os
import random

def get_random_columns_name():
    NAME_MAP = {
        0: ["title", "header", "tiêu đề", "đề tựa", "topic", "new_title", "new_header"],
        1: ["price", "value", "giá", "giá cả", "giá trị", "item_value", "item_price"],
        2: ["square", "area", "estate_square", "estate_area", "item_square", "diện tích"],
        3: ["address", "addr", "địa chỉ", "estate_address", "item_address", "item_addr"],
        4: ["wards", "xã phường", "phường", "xã", "estate_wards", "item_wards"],
        5: ["district", "estate_district", "item_district", "huyện", "quận", "quận huyện"],
        6: ["province", "estate_province", "item_province", "tỉnh thành phố", "tỉnh", "thành phố"],
        7: ["type", "item_type", "estate_type", "topic", "item_topic", "loại hình", "kiểu tin"],
        8: ["description", "item_description", "estate_description", "desc", "detail", "mô tả", "chi tiết"],
        9: ["seller", "seller name", "user", "người bán", "người rao", "user name", "account", "tài khoản"],
        10: ["time", "post time", "thời gian", "date", "post date", "ngày đăng", "ngày rao"],
        11: ["source", "item source", "url", "item url", "nguồn đăng", "nguồn", "đường dẫn"],
        12: ["image","list image", "image url", "ảnh", "danh sách ảnh"]
    }
    columns = []
    for i in range(13):
        columns.append(random.choice(NAME_MAP[i]))
    return columns

schema_matching : SchemaMatching = load(os.path.join(ROOT_DIR,"ai","schema_matching", "schema_matching.lib"))
data = pd.read_csv(os.path.join(ROOT_DIR,"ai","schema_matching",'crawling_real_estate_alonhadat.com.vn.csv')
                   ,header=None,
                   names=['title', 'value', 'area', 'address', 'wards', 'district', 'province',
                          'type', 'description', 'sellerName', 'time', 'source', 'image'])

for i in range(10):
    print("\n\n\n------------------------------------------")
    print("TRY TIME",i+1,"\n")
    state = random.randint(1,100)
    sample_data = data.sample(100,random_state=state)
    sample_data.columns = get_random_columns_name()
    result = schema_matching.matching_data(sample_data)