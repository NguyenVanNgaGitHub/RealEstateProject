import pandas as pd
import pymongo
from sklearn.linear_model import LinearRegression
import numpy as np
from bson.objectid import ObjectId
from typing import Dict
from sklearn.ensemble import RandomForestRegressor

class Feature:
    def __init__(self):
        self.type_dict = {}
        self.district_dict = {}
        self.user_model = {}
        self.train_encode()
        self.get_recommend_data()

    def get_recommend_data(self):
        client = pymongo.MongoClient("mongodb+srv://nguyenvannga1507:nguyenvannga1507@cluster0.faxqo.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")
        db = client.get_database("RealEstate")
        collection = pymongo.collection.Collection(db, "RealEstateClean")
        data = collection.find(filter={}).sort("_id",-1)
        data = list(data)
        client.close()
        self.X = self.transform_items(data)
        self.list_ids = [str(item["_id"]) for item in data]

    def get_data(self, filters = {}, columns=["type", "district"]):
        client = pymongo.MongoClient("mongodb+srv://nguyenvannga1507:nguyenvannga1507@cluster0.faxqo.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")
        db = client.get_database("RealEstate")
        collection = pymongo.collection.Collection(db, "RealEstateClean")
        data = collection.find(filter=filters, projection=columns)
        client.close()
        data = list(data)
        return data

    def train_encode(self):
        data = self.get_data()
        type_set = set(item["type"] for item in data)
        district_set = set(item["district"] for item in data)

        for idx, type in enumerate(type_set):
            self.type_dict[type] = idx
        for idx, district in enumerate(district_set):
            self.district_dict[district] = idx

    def transform_items(self, items):
        vector_len = 2+len(self.type_dict)+len(self.district_dict)
        X = np.zeros(shape=(len(items),vector_len))
        for idx, item in enumerate(items):
            type_idx = 2+self.type_dict[item["type"]]
            district_idx = 2+self.district_dict[item["district"]] + len(self.type_dict)
            X[idx,0] = item["square"]
            X[idx,1] = item["price"]
            X[idx,type_idx] = 1
            X[idx,district_idx] = 1
        return X

    def train_user(self):
        client = pymongo.MongoClient("mongodb+srv://nguyenvannga1507:nguyenvannga1507@cluster0.faxqo.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")
        db = client.get_database("RealEstate")
        collection = pymongo.collection.Collection(db, "scores")
        data = collection.find(filter={}, projection=["user_id", "score"])
        data = list(data)

        collection = pymongo.collection.Collection(db, "RealEstateClean")

        score_data : Dict[str,Dict[str,object]] = {}
        for user in data:
            try:
                list_items = []
                score = []
                for id in user["score"]:
                    try:
                        list_items.append(collection.find_one(filter={"_id": ObjectId(id)}, projection=["square","price","type","district"]))
                        score.append(user["score"][id])
                    except:
                        pass
                X = self.transform_items(list_items)
                score_data[user["user_id"]] = {}
                score_data[user["user_id"]]["X"] = X
                score_data[user["user_id"]]["Y"] = np.array(score)
            except:
                pass
        client.close()

        for user in score_data:
            try:
                X_1 = score_data[user]["X"][:,:2]
                X_2 = score_data[user]["X"][:,2:]
                Y = score_data[user]["Y"]
                model_1 = RandomForestRegressor(n_estimators=max(int(len(X)/2),2))
                model_1.fit(X_1,Y)
                model_2 = LinearRegression()
                model_2.fit(X_2,Y)
                self.user_model[user] = [model_1, model_2]
            except:
                pass
        return data

    def recommend(self, user_id):
        if user_id not in self.user_model:
            return []
        else:
            model_1 = self.user_model[user_id][0]
            model_2 = self.user_model[user_id][1]
            Y_1 = model_1.predict(self.X[:,:2])
            Y_2 = model_2.predict(self.X[:,2:])
            Y = 0.2*Y_1+0.8*Y_2
            result = pd.DataFrame({"_id" : self.list_ids, "Y": Y})
            result = result.sort_values("Y", ascending=False)
            return result["_id"][:99].tolist()
