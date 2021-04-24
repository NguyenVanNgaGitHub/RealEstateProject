import pymongo
import pandas as pd
data = pd.read_csv("crawling_real_estate_alonhadat.com.vn.csv", names=['title', 'value', 'area', 'address',
                                                              'wards', 'district', 'province',
                                                              'type', 'description', 'sellerName',
                                                              'time', 'source', 'image'])
client = pymongo.MongoClient("mongodb+srv://nguyenvannga1507:nguyenvannga1507@cluster0.faxqo.mongodb.net/RealEstate?retryWrites=true&w=majority")
db = client.get_database("RealEstate")
collection = pymongo.collection.Collection(db, "RealEstateRaw")
for idx, row in data.iterrows():
    collection.insert_one({'title': row['title'],
                            'price': float(row['value']),
                            'square': float(row['area']),
                            'address': row['address'],
                            'wards': row['wards'],
                            'district': row['district'],
                            'province': row['province'],
                            'type': row['type'],
                            'description': row['description'],
                            'seller': row['sellerName'],
                            'time': row['time'],
                            'source': row['source'],
                            'image': str(row['image']).split(' ')})
client.close()
