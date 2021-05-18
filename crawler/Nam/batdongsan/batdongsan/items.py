# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

from scrapy.item import Item, Field
from itemloaders.processors import Identity

class BatDongSanItem(Item):

    title = Field() # Ok
    address = Field() # Ok
    wards = Field() # Ok
    district = Field() # Ok
    province = Field()  # Ok ~ city
    square = Field() # Ok
    type = Field() # Ok
    price = Field() # Ok
    description = Field() # Ok
    seller = Field() # Ok
    source = Field() # Ok
    time = Field()
    image = Field(output_processor=Identity())


class AlomuabannhadatItem(Item):
    title = Field() # Ok
    address = Field() # Ok
    wards = Field() # Ok
    district = Field() # Ok
    province = Field()  # Ok ~ city
    square = Field() # Ok
    type = Field() # Ok
    price = Field() # Ok
    description = Field() # Ok
    seller = Field() # Ok
    source = Field() # Ok
    time = Field()
    image = Field(output_processor=Identity())