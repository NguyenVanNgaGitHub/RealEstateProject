import pymongo
from bson.objectid import ObjectId

def get_data():
    client = pymongo.MongoClient("mongodb+srv://nguyenvannga1507:nguyenvannga1507@cluster0.faxqo.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")
    db = client.get_database("RealEstate")
    collection = pymongo.collection.Collection(db, "RealEstateRaw")
    data = collection.find(filter={})
    client.close()
    data = list(data)
    return data

def get_item_by_id(id):
    client = pymongo.MongoClient("mongodb+srv://nguyenvannga1507:nguyenvannga1507@cluster0.faxqo.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")
    db = client.get_database("RealEstate")
    collection = pymongo.collection.Collection(db, "RealEstateRaw")
    data = collection.find_one({'_id': ObjectId(id) })
    client.close()
    return data

def get_data_by_ids(ids, client=None):
    obj_ids = [ObjectId(id) for id in ids]
    if client == None:
        client = pymongo.MongoClient("mongodb+srv://nguyenvannga1507:nguyenvannga1507@cluster0.faxqo.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")
        db = client.get_database("RealEstate")
        collection = pymongo.collection.Collection(db, "RealEstateRaw")
        data = collection.find({'_id': {"$in": obj_ids}})
        client.close()
    else:
        db = client.get_database("RealEstate")
        collection = pymongo.collection.Collection(db, "RealEstateRaw")
        data = collection.find({'_id': {"$in": obj_ids}})
    data = list(data)
    return data

