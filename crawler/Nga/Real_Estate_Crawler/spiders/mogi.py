from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors.lxmlhtml import LxmlLinkExtractor
from Real_Estate_Crawler.items import RealEstateRawLoader, RealEstateRaw
from scrapy import Request

class Mogi(CrawlSpider):
    name = "mogi.vn"
    allowed_domains = ['mogi.vn']
    start_urls = ['https://mogi.vn/mua-nha-dat']

    rules = (
        # lay link cua cac bai vip, new
        Rule(
            link_extractor=LxmlLinkExtractor(allow=(), deny=(), allow_domains=(), deny_domains=(), deny_extensions=None,
                                             restrict_xpaths=('/html/body/div[@id="mogi-page-content"]/div[@id="property"]/div[@class="property-listing"]/div[@id="property-top"]//div[@class="property-top"]',
                                                              '/html/body/div[@id="mogi-page-content"]/div[@id="property"]/div[@class="property-listing"]/ul[@class="props"]/li'),
                                             restrict_css=(), tags=('a', 'area'), attrs=('href'),
                                             canonicalize=False, unique=True, process_value=None, strip=True),
            callback='parse_item',
            cb_kwargs=None,
            follow=None,
            process_links=None,
            process_request=None,
            errback=None
        ),
        # lay link cua cac muc bai
        Rule(
            link_extractor=LxmlLinkExtractor(allow=(), deny=('/ha-noi/thue-nha'), allow_domains=(), deny_domains=(), deny_extensions=None,
                                             restrict_xpaths=('/html/body/div[@id="mogi-page-content"]/div[@id="property"]/div[@class="property-listing"]/div[@class="paging"]/ul[@class="pagination"]/li',
                                                              '/html/body/div[@class="mogi-footer"]/div[@class="container"]/div[@class="footer-right"]/ul[1]/li[2]/ul[@id="footer21"]/li'),
                                             restrict_css=(), tags=('a', 'area'), attrs=('href'),
                                             canonicalize=False, unique=True, process_value=None, strip=True),
            callback='parse_list_and_extract',
            cb_kwargs=None,
            follow=False,
            process_links=None,
            process_request=None,
            errback=None
        ),
    )

    def parse_item(self, response):
        realEstateLoader = RealEstateRawLoader(item=RealEstateRaw(), response=response)
        contentLeftXpath = '/html/body/div[@id="mogi-page-content"]/div[@class="property-detail clearfix"]/div[@class="property-detail-main"]'
        contentRightXpath = '/html/body/div[@id="mogi-page-content"]/div[@class="property-detail clearfix"]/div[@class="side-bar"]/div[@class="agent-widget widget"]'
        realEstateLoader.add_xpath('title', contentLeftXpath+'/div[@class="main-info"]/div[@class="title"]/h1/text()')
        realEstateLoader.add_xpath('value', contentLeftXpath+'/div[@class="main-info"]/div[@class="price"]//text()')
        area = response.xpath(contentLeftXpath+'/div[@class="main-info"]/div[@class="info-attrs clearfix"]/div[@class="info-attr clearfix"]/span[text()="Diện tích đất"]/following-sibling::span//text()').getall()
        if not area:
            area = response.xpath(contentLeftXpath + '/div[@class="main-info"]/div[@class="info-attrs clearfix"]/div[@class="info-attr clearfix"]/span[text()="Diện tích sử dụng"]/following-sibling::span//text()').getall()
        realEstateLoader.add_value('area', area)
        realEstateLoader.add_xpath('address', contentLeftXpath+'/div[@class="main-info"]/div[@class="address"]/text()')
        realEstateLoader.add_value('type', 'UNKNOW')
        realEstateLoader.add_xpath('description', contentLeftXpath+'/div[@class="main-info"]/div[@class="info-content-body"]/text()')
        name = response.xpath(contentRightXpath+'/div[@class="agent-info"]/div[@class="agent-name"]/a/text()').get()
        if not name:
            name = response.xpath(contentRightXpath+'/div[@class="agent-info"]/div[@class="agent-name"]/text()').get()
        realEstateLoader.add_value('sellerName', name)
        realEstateLoader.add_xpath('time', contentLeftXpath+'/div[@class="main-info"]/div[@class="info-attrs clearfix"]/div[@class="info-attr clearfix"]/span[text()="Ngày đăng"]/following-sibling::span/text()')
        realEstateLoader.add_value('source', response.url)
        realEstateLoader.add_xpath('image', contentLeftXpath+'/div[@class="main-intro"]/div[@id="gallery"]/div[@id="top-media"]//div[@class="media-item"]/img/@src')
        return realEstateLoader.load_item()

    def parse_list(self, response):
        for request in self.rules[0].link_extractor.extract_links(response):
            yield Request(url=request.url, callback=self.parse_item)

    def parse_list_and_extract(self, response):
        for request in self.rules[1].link_extractor.extract_links(response):
            yield Request(url=request.url, callback=self.parse_list)
        for request in self.rules[0].link_extractor.extract_links(response):
            yield Request(url=request.url, callback=self.parse_item)

