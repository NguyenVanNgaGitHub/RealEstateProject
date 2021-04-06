from scrapy import Field, Item
from scrapy.loader import ItemLoader
from itemloaders.processors import TakeFirst, MapCompose, Join

class RealEstateRaw(Item):
    title = Field()
    value = Field()
    area = Field()
    address = Field()
    ward = Field()
    district = Field()
    province = Field()
    type = Field()
    description = Field()
    sellerName = Field()
    time = Field()
    source = Field()
    image = Field()

class RealEstateRawLoader(ItemLoader):
    default_output_processor = TakeFirst()
    title_in = MapCompose(str.strip, str.capitalize)
    value_in = MapCompose(str.strip, str.lower)
    value_out = Join()
    area_in = MapCompose(str.strip, str.lower)
    area_out = Join()
    address_in = MapCompose(str.strip)
    ward_in = MapCompose(str.strip)
    district_in = MapCompose(str.strip)
    province_in = MapCompose(str.strip)
    type_in = MapCompose(str.strip, str.lower)
    description_in = MapCompose(str.strip)
    description_out = Join('\n')
    sellerName_in = MapCompose(str.strip, str.lower, str.title)
    time_in = MapCompose(str.strip, str.lower)
    image_in = MapCompose(str.strip)
    image_out = Join(' ')



