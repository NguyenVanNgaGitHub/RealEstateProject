from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors.lxmlhtml import LxmlLinkExtractor
from Real_Estate_Crawler.items import RealEstateRawLoader, RealEstateRaw
from scrapy import Request

class AloNhaDat(CrawlSpider):
    name = "alonhadat.com.vn"
    allowed_domains = ['alonhadat.com.vn']
    start_urls = ['https://alonhadat.com.vn/nha-dat/can-ban/nha-dat/1/ha-noi.html']

    rules = (
        # lay link cua cac bai vip, new
        Rule(
            link_extractor=LxmlLinkExtractor(allow=(), deny=(), allow_domains=(), deny_domains=(), deny_extensions=None,
                                             restrict_xpaths=("/html/body/div[@id='wrapper']/div[@class='body']/div[@class='home-page']/div[@id='content']/div[@class='content-left']/div[@class='vip-property-box']/div[@class='vip-properties']/div[@class='item']",
                                                              "/html/body/div[@id='wrapper']/div[@class='body']/div[@class='home-page']/div[@id='content']/div[@class='content-left']/div[@class='new-property-box']/div[@class='items']/div[@class='item']",
                                                              "/html/body/div[@id='wrapper']/div[@class='body']/div[@id='ctl00_content_pc_content']/div[@id='content-body']/div[@id='left']/div[@class='content-items']/div[@class='content-item']/div[1]/div[@class='ct_title']"),
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
            link_extractor=LxmlLinkExtractor(allow=(), deny=(), allow_domains=(), deny_domains=(), deny_extensions=None,
                                             restrict_xpaths=("/html/body/div[@id='wrapper']/div[@id='ctl00_pc_footer']/div[@class='house-bottom-navigation']/ul/li[1]",
                                                              "/html/body/div[@id='wrapper']/div[@class='body']/div[@id='ctl00_content_pc_content']/div[@id='content-body']/div[@id='right']/div[@class='right-navigation-box']/div[@class='item']/ul/li",
                                                              "/html/body/div[@id='wrapper']/div[@class='body']/div[@id='ctl00_content_pc_content']/div[@id='content-body']/div[@id='left']/div[@class='page']"),
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
        contentLeftXpath = '/html/body/div[@id="wrapper"]/div[@class="body"]/div[@id="ctl00_content_pc_content"]/div[@id="left"]/div[@class="property"]'
        contentRightXpath = '/html/body/div[@id="wrapper"]/div[@class="body"]/div[@id="ctl00_content_pc_content"]/div[@id="right"]'
        realEstateLoader.add_xpath('title', contentLeftXpath + '/div[@class="title"]/h1/text()')
        realEstateLoader.add_xpath('value', contentLeftXpath + '/div[@class="moreinfor"]/span[@class="price"]/span[@class="value"]//text()')
        realEstateLoader.add_xpath('area', contentLeftXpath + '/div[@class="moreinfor"]/span[@class="square"]/span[@class="value"]//text()')
        realEstateLoader.add_xpath('address', contentLeftXpath + '/div[@class="address"]/span[@class="value"]/text()')
        realEstateLoader.add_xpath('type', contentLeftXpath + '/div[@class="moreinfor1"]/div[@class="infor"]/table/tr[3]/td[2]/text()')
        realEstateLoader.add_xpath('description', contentLeftXpath + '/div[@class="detail text-content"]/text()')
        realEstateLoader.add_xpath('sellerName', contentRightXpath + '/div[@class="contact"]/div[@class="contact-info"]/div[@class="content"]/div[@class="name"]/text()')
        realEstateLoader.add_xpath('time', contentLeftXpath + '/div[@class="title"]/span[@class="date"]/text()')
        realEstateLoader.add_value('source', response.url)
        realEstateLoader.add_xpath('image', contentLeftXpath +'/div[@class="images"]/div[@class="image-list"]/span/img/@src')
        return realEstateLoader.load_item()

    def parse_list(self, response):
        for request in self.rules[0].link_extractor.extract_links(response):
            yield Request(url=request.url, callback=self.parse_item)

    def parse_list_and_extract(self, response):
        for request in self.rules[1].link_extractor.extract_links(response):
            yield Request(url=request.url, callback=self.parse_list)
        for request in self.rules[0].link_extractor.extract_links(response):
            yield Request(url=request.url, callback=self.parse_item)

