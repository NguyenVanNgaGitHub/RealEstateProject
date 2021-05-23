import pymongo


class DataBase(object):
    MONGO_URI = 'mongodb+srv://nambn007:nambn007@cluster0.faxqo.mongodb.net/RealEstate?retryWrites=true&w=majority'
    MONGO_DATABASE = 'RealEstate'
    COLLECTION_REAL_ESTATE_NAME = 'RealEstateClean'
    COLLECTION_TIME_DISTRICT = 'TimeVisualize'
    COLLECTION_TIME_MEAN = 'TimeMean'

    @staticmethod
    def connect_to_database():
        client = pymongo.MongoClient(DataBase.MONGO_URI)
        db = client[DataBase.MONGO_DATABASE]
        return db

    @staticmethod
    def convert_price_to_float():
        db = DataBase.connect_to_database()
        bds_collection = db[DataBase.COLLECTION_REAL_ESTATE_NAME]
        result = bds_collection.update_many(filter={}, update=[
            {"$set": {"price": {"$convert": {"input": "$price", "to": "double", "onError": 0, "onNull": 0}}}}])
        print(result.modified_count)

    @staticmethod
    def convert_square_to_float():
        db = DataBase.connect_to_database()
        bds_collection = db[DataBase.COLLECTION_REAL_ESTATE_NAME]
        result = bds_collection.update_many(filter={}, update=[
            {"$set": {"square": {"$convert": {"input": "$square", "to": "double", "onError": 0, "onNull": 0}}}}])
        print(result.modified_count)

    @staticmethod
    def find_real_estate_document(filter=None, projection=None):
        db = DataBase.connect_to_database()
        bds_collection = db[DataBase.COLLECTION_REAL_ESTATE_NAME]

        print(filter)
        print(projection)

        if projection:
            result = bds_collection.find(filter=filter, projection=projection)
        else:
            result = bds_collection.find(filter=filter)
        print(result)
        return list(result)

    @staticmethod
    def create_indexes_search(field_names, orders=None):
        DEFAULT_ORDER = pymongo.ASCENDING # ascending
        keys = []
        if orders is None:
            orders = [DEFAULT_ORDER for i in range(len(field_names))]

        for field_name, order in zip(field_names, orders):
            keys.append((field_name, order))

        db = DataBase.connect_to_database()
        bds_collection = db[DataBase.COLLECTION_REAL_ESTATE_NAME]
        result = bds_collection.create_index(keys=keys)
        print(result)

    @staticmethod
    def get_field_values(field_name):
        db = DataBase.connect_to_database()
        bds_collection = db[DataBase.COLLECTION_REAL_ESTATE_NAME]
        field_values = []
        result = bds_collection.find(filter={}, projection=[field_name])
        count = 0
        print(result.count())
        while count < result.count():
            field_values.append(result.next()[field_name])
            count += 1
            print(count)
        return field_values

    @staticmethod
    def get_all_data(field_names):
        db = DataBase.connect_to_database()
        bds_collection = db[DataBase.COLLECTION_REAL_ESTATE_NAME]
        data = []
        result = bds_collection.find(filter={}, projection=field_names)
        return list(result)

from bson import ObjectId
if __name__ == '__main__':
    for c in DataBase.find_real_estate_document(filter={
        '_id': ObjectId('60955ae180686f1c9e310041')
    })[0]['district']:
        print(c)