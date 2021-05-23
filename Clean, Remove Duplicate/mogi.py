import requests, codecs, re, ast, json
from bs4 import BeautifulSoup
def getPage(href):
    bs = BeautifulSoup(requests.get(href).text, 'html.parser')
    while bs is None:
        bs = BeautifulSoup(requests.get(href).text, 'html.parser')
    return bs

def findStreetWard(district, idDistrict):
    address[district] = dict()
    data = json.loads(""+getPage("https://mogi.vn/MarketPrice/GetByDistrict?districtId="+idDistrict).prettify(), strict=False)
    for i in range(len(data['Data'])):
        ward = data['Data'][i]['WardName'].lower().replace("phường","").replace("xã","").replace("thị trấn","").strip()
        street = data['Data'][i]['StreetName'].lower().replace('đường','').replace('phố','').replace('quốc lộ','').strip()
        try:
            if ward not in address[district]['ward']:
                address[district]['ward'].append(ward)
        except:
            address[district]['ward'] = [ward]
        try:
            address[district]['street'].append(street)
        except:
            address[district]['street'] = [street]
    # address[district]['ward'] = list(address[district]['ward'])
    # address[district]['st'] = list(address[district]['ward'])
def findDistrict(bs):
    province = bs.find_all("div",{"class":"district"})[-1]
    districts = province.find_all("a",{"class":"link-overlay"})
    for dis in districts:
        district = dis.text.lower().replace("quận","").replace("huyện","").replace("thị xã","").strip()
        address[district] = dict()
        print((district))
        findStreetWard(district, dis['href'].rsplit("-qd")[-1])
    json.dump((address), codecs.open("address_HN1.txt",'w','utf8'), ensure_ascii=False)
    
    
address = dict()
findDistrict(getPage("https://mogi.vn/gia-nha-dat"))