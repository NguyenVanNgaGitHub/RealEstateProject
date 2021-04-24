import pymongo
import pandas as pd

client = pymongo.MongoClient("mongodb+srv://nguyenvannga1507:nguyenvannga1507@cluster0.faxqo.mongodb.net/RealEstate?retryWrites=true&w=majority")
db = client.get_database("RealEstate")
collection = pymongo.collection.Collection(db, "RealEstateRaw")
data = collection.find(projection=["type", "title", "description"])
client.close()
type_list = []
title_list = []
description_list = []
for raw in data:
    type_list.append(raw["type"])
    title_list.append(raw["title"])
    description_list.append(raw["description"])
data1 = pd.DataFrame({"type": type_list, "title": title_list, "description": description_list})

data2 = pd.read_csv("../crawling_real_estate_alonhadat.com.vn.csv", names=["title", "price", "square", "address",
                                                                           "wards", "district", "province",
                                                                           "type", "description", "seller", "time",
                                                                           "source", "image"])
data2 = data2[["title", "description", "type"]]
data = data1.append(data2, ignore_index=True)
data.to_csv("../type_data.csv", index=False)