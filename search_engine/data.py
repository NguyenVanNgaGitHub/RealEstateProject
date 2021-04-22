import pymongo
from bson.objectid import ObjectId

def get_data(client: pymongo.MongoClient = None):
    if client:
        db = client.get_database("RealEstate")
        collection = pymongo.collection.Collection(db, "RealEstateRaw")
        data = collection.find(filter={})
        data = list(data)
        return data
    else:
        new_client = pymongo.MongoClient("mongodb+srv://nambn007:nambn007@cluster0.oki5a.mongodb.net/RealEstate?retryWrites=true&w=majority")
        db = new_client.get_database("RealEstate")
        collection = pymongo.collection.Collection(db, "RealEstateRaw")
        data = collection.find(filter={})
        new_client.close()
        data = list(data)
        return data

def get_item_by_id(id, client: pymongo.MongoClient = None):
    if client:
        db = client.get_database("RealEstate")
        collection = pymongo.collection.Collection(db, "RealEstateRaw")
        data = collection.find_one({'_id': ObjectId(id) })
        return data
    else:
        new_client = pymongo.MongoClient(
            "mongodb+srv://nambn007:nambn007@cluster0.oki5a.mongodb.net/RealEstate?retryWrites=true&w=majority")
        db = new_client.get_database("RealEstate")
        collection = pymongo.collection.Collection(db, "RealEstateRaw")
        data = collection.find_one({'_id': ObjectId(id)})
        new_client.close()
        return data

def get_data_by_ids(ids, client: pymongo.MongoClient = None):
    obj_ids = [ObjectId(id) for id in ids]
    if client:
        db = client.get_database("RealEstate")
        collection = pymongo.collection.Collection(db, "RealEstateRaw")
        data = collection.find({'_id': {"$in": obj_ids}})
        data = list(data)
        return data
    else:
        new_client = pymongo.MongoClient("mongodb+srv://nambn007:nambn007@cluster0.oki5a.mongodb.net/RealEstate?retryWrites=true&w=majority")
        db = new_client.get_database("RealEstate")
        collection = pymongo.collection.Collection(db, "RealEstateRaw")
        data = collection.find({'_id': {"$in": obj_ids}})
        data = list(data)
        new_client.close()
        return data

