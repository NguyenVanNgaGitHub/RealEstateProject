import scrapy
import logging
from scrapy.loader import ItemLoader
from batdongsan.items import AlomuabannhadatItem
from itemloaders.processors import TakeFirst, Identity
from scrapy import Selector

class NhatDat24hSpider(scrapy.Spider):
    name = 'alomuabannhadat.vn'

    custom_settings = {
        'ITEM_PIPELINES': {
            'batdongsan.pipelines.AlomuabannhadatPipeline': 300
        }
    }

    start_urls = [
        'https://alomuabannhadat.vn/nha-ban/'
        #'https://alomuabannhadat.vn/chinh-chu-ban-can-ho-3-ngu-91m2-toa-a-housinco-phung-khoang-gia-236-ty-735368.html'
        #'https://nhadat24h.net/ban-chung-cu-binh-trung/ban-can-ho-chung-cu-the-krista-p-binh-trung-dong-q2-tp-ho-chi-minh-ID3867291'
    ]

    def parse(self, response, **kwargs):
        list_page = response.xpath('//div[contains(@class,"wrap-property")]//div[contains(@class,"info")]/a/@href').getall()

        for page in list_page:
            yield scrapy.Request(url=page, callback=self.parse_item)

        next_pages = response.xpath('((//ul[contains(@class,"pagination")])[2]//li)').getall()
        next_page = next_pages[-1]
        next_page = Selector(text=next_page).xpath('//a//@href').get()
        if next_page != None:
            yield scrapy.Request(url=next_page, callback=self.parse)

    def parse_item(self, response, **kwargs):
        item_loader = ItemLoader(item=AlomuabannhadatItem(), response=response)
        item_loader.default_output_processor = TakeFirst()

        item_loader.add_value('title', response.xpath('//header[contains(@class,"property-title")]/h1//text()').get().strip())

        content = response.xpath('//header[contains(@class,"property-title")]/figure//text()').getall()
        for i, c in enumerate(content):
            content[i] = c.strip()

        index_address = content.index('Vị trí:') + 1
        index_price = content.index('Giá:') + 1
        index_square = content.index('Diện tích:') + 1

        item_loader.add_value('type', response.xpath('(//ol[contains(@class,"breadcrumb")]//li)[3]//span/text()').get().strip())
        item_loader.add_value('address', content[index_address])

        quick_summary = response.xpath('//section[contains(@id,"quick-summary")]//dl//text()').getall()
        for i, c in enumerate(quick_summary):
            quick_summary[i] = c.strip()
        total_address = quick_summary[quick_summary.index('Vị trí:') + 2]
        total_address = total_address.split(',')

        if len(total_address) <= 2:
            district = total_address[-2].strip()
            province = total_address[-1].strip()
        else:
            wards = total_address[-3].strip()
            district = total_address[-2].strip()
            province = total_address[-1].strip()

        item_loader.add_value('wards', wards)
        item_loader.add_value('district', district)
        item_loader.add_value('province', province)

        content2 = response.xpath('//section[contains(@id,"quick-summary")]//text()').getall()
        for i, c in enumerate(content2):
            content2[i] = c.strip()
        index_time = content2.index('Ngày đăng:') + 2


        item_loader.add_value('price', content[index_price].strip())
        item_loader.add_value('square', content[index_square].strip())
        item_loader.add_value('time', content2[index_time].strip())
        item_loader.add_value('description', ' '.join(response.xpath('//section[contains(@id,"description")]//p//text()').getall()))
        item_loader.add_value('seller', response.xpath('//aside[contains(@class,"agent-info")]//strong//text()').get().strip())
        item_loader.add_value('source', response.url)
        item_loader.add_value('image', response.xpath('//div[contains(@class,"property-slide")]//img//@src').getall())


        # item_loader.add_value('title', response.xpath('//a[contains(@id,"txtcontenttieudetin")]//text()').get())
        #
        # address = response.xpath('//label[contains(@id,"ContentPlaceHolder1_ctl00_lbTinhThanh")]//text()').get()
        # item_loader.add_value('address', address)
        #
        # detail_address = address.split(', ')
        # item_loader.add_value('province', detail_address[-1].strip())
        # if len(detail_address) <= 2:
        #     item_loader.add_value('district', detail_address[-2].strip())
        # else:
        #     item_loader.add_value('district', detail_address[-2].strip())
        #     item_loader.add_value('wards', detail_address[-3].strip())
        #
        # item_loader.add_value('price', response.xpath('//label[contains(@id,"ContentPlaceHolder1_ctl00_lbGiaDienTich")]//label[contains(@class,"strong1")]//text()').get())
        # item_loader.add_value('square', response.xpath('//label[contains(@id,"ContentPlaceHolder1_ctl00_lbGiaDienTich")]//label[contains(@class,"strong2")]//text()').get())
        # item_loader.add_value('type', response.xpath('//label[contains(@id,"ContentPlaceHolder1_ctl00_lbLoaiBDS")]//text()').get())
        # item_loader.add_value('description', response.xpath('//div[contains(@id,"ContentPlaceHolder1_ctl00_divContent")]//text()').get())
        # item_loader.add_value('seller', response.xpath('//div[contains(@class,"detailUserName")]//label[contains(@id,"lbHoTen")]//a//text()').get())
        # item_loader.add_value('source', response.url)
        #
        # images = response.xpath('//ul[contains(@id, "ContentPlaceHolder1_ctl00_viewImage1_divLi")]//li//a//@href').getall()
        # for index in range(len(images)):
        #     if 'http' not in images[index]:
        #         images[index] = 'http://' + self.name + images[index]
        # item_loader.add_value('images', images)

        return item_loader.load_item()