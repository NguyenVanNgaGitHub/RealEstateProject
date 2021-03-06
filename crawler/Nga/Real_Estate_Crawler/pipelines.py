from itemadapter import ItemAdapter
from csv import writer
from scrapy.exceptions import DropItem
import re
from datetime import date, timedelta
import pymongo
from joblib import load
import os
from model.cleaner import cleanRealEstateDescription

class ExtractTime:
    def process_item(self, item, spider):
        today = date.today().strftime("%d/%m/%Y")
        yesterday = (date.today() - timedelta(days=1)).strftime("%d/%m/%Y")
        itemAdapter = ItemAdapter(item=item)
        if itemAdapter.get("time"):
            time = str(itemAdapter.get("time"))
            time = time.replace(" ", "").replace("ngàyđăng:","").replace("hômnay",today).replace("hômqua",yesterday)
            itemAdapter.update({"time": time})
            return itemAdapter.item
        else:
            return DropItem(f"Missing field in real estate at {itemAdapter.get('source')}")

class ExtractArea:
    def getSquare(self, area):
        area = area.replace(" ", "").replace(".","").replace(",",".").lower()
        square = re.findall(r"([0-9]+[.]?[0-9]*)m2", area)
        if square:
            return square[0]
        else:
            return None

    def process_item(self, item, spider):
        itemAdapter = ItemAdapter(item=item)
        if itemAdapter.get("area"):
            area = str(itemAdapter.get("area"))
            itemAdapter.update({"area": self.getSquare(area)})
            return itemAdapter.item
        else:
            return DropItem(f"Missing field in real estate at {itemAdapter.get('source')}")

class ExtractValue:
    def getPrice(self, value, area):
        price = 0
        value = value.replace(" ", "").replace(".","").replace(",",".").lower()
        billion = re.findall(r"([0-9]+[.]?[0-9]*)tỷ", value)
        if billion:
            price += float(billion[0])*1000
        million = re.findall(r"([0-9]+[.]?[0-9]*)triệu", value)
        if million:
            price += float(million[0])
        thousand = re.findall(r"([0-9]+[.]?[0-9]*)nghìn", value)
        if thousand:
            price += float(thousand[0]) / 1000
        if value.endswith("/m2"):
            if area:
                price = price*float(area)
            else:
                price = 0
        if price == 0:
            return None
        else:
            return "%.3f"%price

    def process_item(self, item, spider):
        itemAdapter = ItemAdapter(item=item)
        if itemAdapter.get("value"):
            value = str(itemAdapter.get("value"))
            area = str(itemAdapter.get("area"))
            itemAdapter.update({"value": self.getPrice(value, area)})
            return itemAdapter.item
        else:
            return DropItem(f"Missing real estate in paper at {itemAdapter.get('source')}")

class ExtractType:
    def open_spider(self, spider):
        self.classifier = load("model"+os.sep+"typeClassifier.joblib")
        self.type_mapping = {
            "Nhà đất": ["Mua bán nhà riêng", "nhà trong hẻm", "Mua bán nhà phố", "nhà mặt tiền", "Nhà ở",
                        "Mua bán nhà mặt phố", "Nhà riêng", "Nhà mặt phố"],
            "Đất nền": ["đất thổ cư, đất ở", "Đất", "đất nền, liền kề, đất dự án", "Mua bán đất", "Đất nền khu dân cư",
                        "mặt bằng", "Đất nền", "Đất nền dự án", "Mua bán đất nền dự án"],
            "Căn hộ": ["Mua bán căn hộ chung cư", "Căn hộ/Chung cư", "căn hộ chung cư", "Căn hộ chung cư",
                       "Căn hộ Cao cấp", "Căn hộ trung cấp", "Căn hộ mini", "Căn hộ Tập thể"],
            "Biệt thự": ["Mua bán biệt thự", "biệt thự, nhà liền kề", "Mua bán nhà biệt thự liền kề",
                         "Biệt thự liền kề", "Nhà biệt thự"],
            "Loại hình khác": ["Văn phòng, Mặt bằng kinh doanh", "kho, xưởng", "nhà hàng, khách sạn",
                               "đất nông, lâm nghiệp", "phòng trọ, nhà trọ", "Mua bán nhà hàng - khách sạn",
                               "Mua bán văn phòng", "trang trại", "Mua bán phòng trọ", "văn phòng",
                               "Mặt bằng bán lẻ", "các loại khác", "Mua bán trang trại khu nghỉ dưỡng"]
        }

    def get_refine_type(self, t):
        for x in self.type_mapping:
            if t in self.type_mapping[x]:
                return x
        return "UNKNOW"

    def process_item(self, item, spider):
        itemAdapter = ItemAdapter(item=item)
        if itemAdapter.get('title') and itemAdapter.get('description'):
            type = self.get_refine_type(str(itemAdapter.get("type")))
            if type=="UNKNOW":
                text = [str(itemAdapter.get('title'))+str(itemAdapter.get('description'))]
                prediction = self.classifier.predict(text)
                type = prediction[0]
            itemAdapter.update({'type': type})
            return itemAdapter.item
        else:
            return DropItem(f"Missing field in paper at {itemAdapter.get('source')}")

class ExtractAddress:
    def extractLocationName(self, address):
        address = address.lower().strip()
        address = re.sub("\s+", " ", address)
        address = re.sub("([\s\S]*)(tỉnh|thành phố|huyện|quận|thị xã|phường|xã|thị trấn) ", "", address)
        address = address.title()
        return address

    def process_item(self, item, spider):
        itemAdapter = ItemAdapter(item=item)
        address = [x.strip() for x in str(itemAdapter.get('address')).split(',')]
        if len(address)>=3:
            itemAdapter.update({'ward': self.extractLocationName(address[-3]),
                                'district': self.extractLocationName(address[-2]),
                                'province': self.extractLocationName(address[-1])})
            if str(itemAdapter.get('province'))=="Hà Nội":
                return itemAdapter.item
            else:
                return DropItem(f"Missing field in paper at {itemAdapter.get('source')}")
        else:
            return DropItem(f"Missing field in paper at {itemAdapter.get('source')}")

class RemoveEmptyRealEstate:
    def process_item(self, item, spider):
        itemAdapter = ItemAdapter(item=item)
        if itemAdapter.get('title') and itemAdapter.get('value') and itemAdapter.get('area') \
                and itemAdapter.get('address') and itemAdapter.get('ward') and itemAdapter.get('district') and itemAdapter.get('province') \
                and itemAdapter.get('type') and itemAdapter.get('description') and itemAdapter.get('sellerName') \
                and itemAdapter.get('time') and itemAdapter.get('image'):
            return item
        else:
            return DropItem(f"Missing field in real estate at {itemAdapter.get('source')}")

class CsvWriter:
    def open_spider(self, spider):
        self.spider_name = spider.name
        self.file = open('crawling_real_estate_'+self.spider_name+'.csv', 'a', encoding="utf-8", newline='')
        self.writer_object = writer(self.file)

    def close_spider(self, spider):
        self.file.close()

    def process_item(self, item, spider):
        itemAdapter = ItemAdapter(item=item)
        self.writer_object.writerow([itemAdapter.get('title'), itemAdapter.get('value'), itemAdapter.get('area'),
                                     itemAdapter.get('address'), itemAdapter.get('ward'), itemAdapter.get('district'), itemAdapter.get('province'),
                                     itemAdapter.get('type'), itemAdapter.get('description'), itemAdapter.get('sellerName'),
                                     itemAdapter.get('time'), itemAdapter.get('source'), itemAdapter.get('image')
                                     ])
        return item

class MongoWriter:
    def open_spider(self, spider):
        try:
            self.client = pymongo.MongoClient("mongodb+srv://nambn007:nambn007@cluster0.oki5a.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")
            self.db = self.client.get_database("RealEstate")
            self.collection = pymongo.collection.Collection(self.db, "RealEstateRaw")
        except Exception as ex:
            print("Can't create connection to database", ex)

    def close_spider(self, spider):
        try:
            self.client.close()
        except Exception as ex:
            print("Can't close connection", ex)

    def addRealEstate(self, itemAdapter):
        try:
            self.collection.insert_one({'title': itemAdapter.get('title'),
                                        'price': float(itemAdapter.get('value')),
                                        'square': float(itemAdapter.get('area')),
                                        'address': itemAdapter.get('address'),
                                        'wards': itemAdapter.get('ward'),
                                        'district': itemAdapter.get('district'),
                                        'province': itemAdapter.get('province'),
                                        'type': itemAdapter.get('type'),
                                        'description': itemAdapter.get('description'),
                                        'seller': itemAdapter.get('sellerName'),
                                        'time': itemAdapter.get('time'),
                                        'source': itemAdapter.get('source'),
                                        'image': str(itemAdapter.get('image')).split(' ')})
        except Exception as ex:
            print("Exception while insert a Real Estate", ex)
            raise Exception from ex

    def process_item(self, item, spider):
        itemAdapter = ItemAdapter(item=item)
        self.addRealEstate(itemAdapter=itemAdapter)
        return item

