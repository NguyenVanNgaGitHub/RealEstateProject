import scrapy
import logging
from scrapy.loader import ItemLoader
from scrapy import Selector
from batdongsan.items import BatDongSanItem
from itemloaders.processors import TakeFirst

class BatDongSanSpider(scrapy.Spider):
    name = 'batdongsan.vn'
    start_urls = [
        'http://batdongsan.vn/giao-dich/ban-nha-dat.html'
     #   'http://batdongsan.vn/ban-nha-%F0%9F%8F%98-12c-khu-do-thi-viet-hung-long-bien-ha-noi-doi-dien-chung-cu-y2-p581426.html'
    ]

    custom_settings = {
        'CLOSESPIDER_ITEMCOUNT' : 1000,
        'DOWNLOAD_DELAY' : 1
    }

    custom_settings = {
        'ITEM_PIPELINES': {
            'batdongsan.pipelines.BatDongSanPipeline': 300
        }
    }

    def parse(self, response, **kwargs):
        list_post = response.xpath("//li[contains(@class,'Product_List')]//h2[contains(@class,'P_Title')]//a/@href").getall()
        for post in list_post:
            url = 'http://' + self.name + post
            yield scrapy.Request(url=url, callback=self.parse_item)

        # For next page
        next_page = response.xpath("//a[contains(@class,'next btn')]/@href").get()
        next_page_url = 'http://' + self.name + next_page
        yield scrapy.Request(url=next_page_url, callback=self.parse)

    def parse_item(self, response, **kwargs):
        item_loader = ItemLoader(item=BatDongSanItem(), response=response)
        item_loader.default_output_processor = TakeFirst()
        title = response.css('.P_Title1').xpath('//h1//text()').get()
        item_loader.add_value('title', title)

        items = response.css('.details-warp-item').getall()
        sel_arr = []
        dict_item = {}
        for item in items:
            sel = Selector(text=item)
            sel_arr.append(sel)
            arr = sel.xpath('//text()').getall()
            dict_item[arr[0]] = arr[1:]

        try:
            _type = dict_item['Loại:']
            item_loader.add_value('type', _type)
        except KeyError:
            item_loader.add_value('type', 'UNKNOW')

        wards = response.xpath("//div[contains(@class,'details-warp-item')]//a[contains(@class,'wards-item')]//span/text()").get()
        if wards is not None:
            item_loader.add_value('wards', wards)

        district = response.xpath("//div[contains(@class,'details-warp-item')]//a[contains(@class,'district-item')]//span/text()").get()
        item_loader.add_value('district', district.strip())

        city = response.xpath("//div[contains(@class,'details-warp-item')]//a[contains(@class,'city-item')]//span/text()").get()
        item_loader.add_value('province', city.strip())

        address = dict_item['Địa chỉ:']
        item_loader.add_value('address', ' '.join(address).strip())

        square = response.xpath('//div[contains(@class,"details-warp-item")]//span[contains(@class,"product-area")]/text()').get().split(' ')[0].strip()
        item_loader.add_value('square', square.strip())

        price = response.xpath('//div[contains(@class,"details-warp-item")]//span[contains(@class,"button-price")]//span/text()').get()
        item_loader.add_value('price', price.strip())

        description = response.css('div.PD_Gioithieu::text').getall()
        description = '\n'.join(description)
        item_loader.add_value('description', description.strip())

        seller = response.css('div.name').xpath('./a/text()').get()
        item_loader.add_value('seller', seller.strip())

        source = response.url
        item_loader.add_value('source', source)

        images = response.css('a.changemedia::attr(href)').getall()
        item_loader.add_value('image', images)

        time = response.xpath('//span[contains(@class,"PostDate")]//span//text()').get()
        item_loader.add_value('time', time.strip())


        return item_loader.load_item()