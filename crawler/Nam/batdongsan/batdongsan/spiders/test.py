import scrapy
import logging


class TestSpider(scrapy.Spider):
    name = 'test'
    start_urls = [
        "https://cloud.google.com/translate/docs/languages"
    ]


    def parse(self, response, **kwargs):

        table_lang = response.xpath("//div[contains(@class, 'devsite-table-wrapper')]").get()

        logging.info(table_lang)

