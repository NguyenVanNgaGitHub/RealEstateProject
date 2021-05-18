"""
    # title: tiêu đề
    # address: địa chỉ cụ thể
    # wards: xã phường
    # district: quận huyện
    # province: tỉnh
    # square: diện tích
    # type: loai bất động sản
    # price: giá
    # description: mô tả
    # seller: người bán
    # source: link
    # image: danh sách URL của ảnh 
"""
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from urllib.parse import urlparse, quote # use the urllib.parse.quote function on the non-ascii string
from urllib.request import urlopen
from urllib.error import HTTPError, URLError
import ssl, os, codecs, re
import base64, requests, bs4
import pandas as pd 

class Crawler:
    def __init__(self, homePage, url):
        self.homePage = homePage
        self.pages = set()
        self.nPages = 0
        self.path = os.path.abspath(os.getcwd())

        try:
            setPages = codecs.open(self.path+'/'+self.homePage+'1.txt', 'r', 'utf-8')
            self.pages = set(line[:-1] for line in setPages.readlines())
            setPages.close()
            self.nPages = len(self.pages)
        except:

            os.makedirs(self.path+'/'+ self.homePage, exist_ok = True)
                    
    def getPages(self, url):
        bs = None
        while bs is None:
            html = requests.get(url).text
            bs = BeautifulSoup(html, 'html.parser')
            # with open("tt.html","w") as f:
            #     f.write(bs.prettify())
            # print(type(bs))
        return bs
        
    def savePages(self, contents):
        for content in contents:
            page = content['href']
            # print(page)
            if page not in self.pages:
                info = self.parse_page(self.getPages(page), str(self.nPages+1), page)
                # with codecs.open('./'+self.homePage+'/'+str(self.nPages)+'.html', 'w', 'utf-8') as f:
                #     f.wri••••••••••te(bs.prettify())
                # print(info)
                # return
                columns = list(info.keys())
                df = pd.DataFrame([info],columns=columns)
                try:
                    df1 = pd.read_csv("bds1.csv")
                    df = pd.concat([df1, df], ignore_index=True, sort = False)
                except:
                    pass
                df.to_csv("bds1.csv", index=False)
                
                with codecs.open(self.path+'/'+self.homePage+'1.txt', 'a', 'utf-8') as filePage:
                    filePage.write(page+'\n')
                self.nPages += 1
                if self.nPages > 1100:
                    return
                self.pages.add(page)
                print(self.nPages)
                print(page)
    def parse_page(self, bs, filename, url):
        info = dict()
        info['source'] = url
        # title-product
        try:
            element = bs.find("h1",{"class":"title-product"})
            info['title']= element.text.strip()
        except:
            print(filename)
            os.remove(self.path+'/'+filename)
            return
        # # address
        # elements = bs.find("ul",{"class":"list-attr-hot clearfix"})
        # print(len(elements))
        # for element in elements:
        #     print(element)
        # list-attr-hot clearfix
        elements = bs.find_all("ul",{"class":"list-attr-hot clearfix"})

        for element in elements:
            for item in element.findChildren(recursive=False):
                key = None
                for chil in item.find_all(text=lambda text: not isinstance(text, bs4.element.Comment), recursive=True):
                    if chil.strip() !='':
                        if key is None:
                            # print(chil.strip())
                            info[chil.strip()]=None
                            key = chil.strip()
                        # print(chil.strip())
                        else:
                            info[key] = chil.strip()
                            key = None
                            # info.append(chil.strip())
        # print(info)
        features = list(info.keys())
        info['image'],info['address'], info['wards'],info['datetime'], info['district'], info['province'], info['square'], info['type'], info['price'], info['description'], info['seller'] = ['UNKNOW']*11

        info['type'] = features[2]
        info['province'] = features[3]
        info['district'] = features[4]
        info['wards'] = features[5]
        info['price'] = info['Giá :']
        try:
            if 'tỷ' in info['price']:
                info['price'] = float(re.search('\d+\.*\,*\d*', info['price'])[0].replace(',','.'))*1000
            elif 'triệu' in info['price']:
                info['price'] = float(re.search('\d+\.*\,*\d*', info['price'])[0].replace(',','.'))
        except:
            pass
        info['datetime'] = info['Ngày đăng :']
        
        info['square'] = info['Diện tích :']
        try:
            if ('m2' in info['square']) or ('m²' in info['square']):
                info['square'] = float(re.search('\d+\.*\,*\d*', info['square'])[0].replace(',','.'))
        except:
            pass

        info['image'] = [img['src'] for img in bs.find("div",{"class":"box-slide-detail clearfix"}).find_all("img")]
        list_keys = ['source','title','address','wards','district','province','square','type','price','description','image','datetime','seller']
        for key in list(info.keys()):
            if key not in list_keys:
                del info[key]
        # thong tin mo ta
        info['description']=[]
        element = bs.find("div",{"class":"ct-pr-sum"})
        for chil in element.find_all(text=lambda text: not isinstance(text, bs4.element.Comment), recursive=True):
            if chil.strip() !='':
                if chil.strip() == 'Tìm kiếm theo từ khóa:':
                    break
                # print(chil.strip())
                info['description'].append(chil.strip())

        # lien he nguoi ban
        info['seller'] = bs.find("div",{"class":"col-md-8 col-sm-8 pr-info-it-2"}).text.strip()
        # elements = bs.find(lambda tag: tag.name == 'div' and tag.get('class') == ['row-cl']).find_all("div", {"class":"col-item-info row-cl"})
        # # print(len(elements), elements)
        # for element in elements:
        #     items = element.find_all(text=lambda text: (not isinstance(text, bs4.element.Comment)) and (text.strip() != ''), recursive=True)
        #     key = None
        #     for item in items:
        #         if key is None:
        #             key = item.strip()
        #             info[key] = None
        #         else:
        #             info[key] = item.strip()
        #             key = None
        for key in info.keys():
            if info[key] is None:
                info[key]= 'UNKNOW'
        # print(info)
        return info
    def crawl(self, url, page_idx):
        # print(url+str(page_idx))
        bs = self.getPages(url+str(page_idx))
        if bs is not None:
            print('\n\n-----------------------------------------------\n\n')
            print(page_idx, )
            self.savePages(bs.find_all("a",{"class":"image-item-nhadat"}))
            page_idx+=1
            self.crawl(url, page_idx)

url = 'https://bds.com.vn/mua-ban-nha-dat-ha-noi-page'
c = Crawler('bds',url)         
c.crawl(url, 27)