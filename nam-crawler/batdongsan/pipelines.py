# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import pymongo


class BatDongSanPipeline:

    collection_name = 'RealEstateRaw'

    def __init__(self, mongo_uri, mongo_db):
        self.mongo_uri = mongo_uri
        self.mongo_db = mongo_db

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            mongo_uri=crawler.settings.get('MONGO_URI'),
            mongo_db=crawler.settings.get('MONGO_DATABASE')
        )

    def open_spider(self, spider):
        self.client = pymongo.MongoClient(self.mongo_uri)
        self.db = self.client[self.mongo_db]

    def close_spider(self, spider):
        self.client.close()

    def process_item(self, item, spider):
        if item['province'].lower() == 'hà nội' or item['province'].lower() == 'ha noi':
            for field in item.fields:
                item.setdefault(field, 'UNKNOW')

            if item['square'] != 'UNKNOW':
                item['square'] = float(item['square'].replace(',', '.'))

            if 'Tỷ' in item['price']:
                item['price'] = float(item['price'].split(' ')[0].strip().replace(',', '.')) * 1000
            elif 'Triệu/m²' in item['price']:
                item['price'] = float(item['price'].split(' ')[0].strip()) * float(item['square'])
            else:
                item['price'] = float(item['price'].split(' ')[0].strip())

            self.db[self.collection_name].insert_one(ItemAdapter(item).asdict())
            return item

class AlomuabannhadatPipeline:

    collection_name = 'RealEstateRaw'

    def __init__(self, mongo_uri, mongo_db):
        self.mongo_uri = mongo_uri
        self.mongo_db = mongo_db

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            mongo_uri=crawler.settings.get('MONGO_URI'),
            mongo_db=crawler.settings.get('MONGO_DATABASE')
        )

    def open_spider(self, spider):
        self.client = pymongo.MongoClient(self.mongo_uri)
        self.db = self.client[self.mongo_db]

    def close_spider(self, spider):
        self.client.close()

    def process_item(self, item, spider):
        if item['province'].lower() == 'hà nội' or item['province'].lower() == 'ha noi':
            for field in item.fields:
                item.setdefault(field, 'UNKNOW')

            if item['square'] != 'UNKNOW':
                item['square'] = abs(float(item['square'].replace(',', '.')))

            if 'tỷ' in item['price'] and 'triệu' in item['price']:
                money = item['price'].split(' ')
                item['price'] = float(money[0]) * 1000 + float(money[2])
            elif 'tỷ' in item['price']:
                item['price'] = float(item['price'].split(' ')[0].strip()) * 1000
            else:
                item['price'] = float(item['price'].split(' ')[0].strip())

            item['time'] = item['time'].replace('-', '/')
            self.db[self.collection_name].insert_one(ItemAdapter(item).asdict())
            return item

        return None