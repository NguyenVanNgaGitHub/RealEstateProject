import urllib.request, json , csv, base64, requests, time, re, html
import pandas as pd 
from pandas.io.json import json_normalize

     
def Chotot():
    set_id = set()
    len_link = 0
    try:
        with open("set_id_chotot1.txt","r") as f:
            for line in f.readlines():
                set_id.add(line.split('\n')[0])
        len_link = len(set_id)
    except:
        with open("set_id_chotot1.txt","w") as f:
            pass


    for i in range(800):
        homepage = "https://gateway.chotot.com/v1/public/ad-listing/"
        page = "https://gateway.chotot.com/v1/public/ad-listing?region_v2=12000&cg=1000&limit=20&o="+str(i*20)+"&st=s,k&page="+str(i+1)
        try:
            with urllib.request.urlopen(page) as url:
                data = json.loads(url.read().decode())
        except:
            continue

        if len(data['ads']) == 0:
            break

        for j in range(len(data['ads'])):
            if str(data['ads'][j]['list_id']) in set_id:
                continue
            print(data['ads'][j]['list_id'])

            try:
                with urllib.request.urlopen(homepage+str(data['ads'][j]['list_id'])) as url1:
                    data1 = json.loads(url1.read().decode())
            except:
                continue

            res = dict()
            res['image'], res['source'], res['title'], res['address'], res['wards'],res['datetime'], res['district'], res['province'], res['square'], res['type'], res['price'], res['description'], res['seller'] = ['UNKNOW']*13
            res['source'] = data1['ad']['list_id']
            res['title'] = data1['ad']['subject']
            try:
                res['address'] = data1['ad']['address']
            except:
                pass
            try:
                res['wards'] = data1['ad']['ward_name']
            except:
                continue
            res['district'] = data1['ad']['area_name']
            res['province'] = data1['ad']['region_name']
            res['square'] = data1['ad']['size']
            res['type'] = data1['ad']['category_name']
            res['price'] = data1['ad']['price']/1000000
            res['description'] = data1['ad']['body']
            res['seller'] = data1['ad']['account_name']
            res['datetime'] = data1['ad']['list_time']
            try: 
                res['image'] = [image for image in data1['ad']['images']]
            except:
                pass
            # print(res)
            
            columns = list(res.keys())
            df = pd.DataFrame([res],columns=columns)
            try:
                df1 = pd.read_csv("chotot1.csv")
                df = pd.concat([df1, df], ignore_index=True, sort = False)
            except:
                pass
            df.to_csv("chotot1.csv", index=False)
            set_id.add(str(data['ads'][j]['list_id']))
            with open("set_id_chotot1.txt","a") as f_id:
                f_id.write(str(data['ads'][j]['list_id'])+'\n')
            len_link += 1
            if len_link > 1100:
                return
            # return

Chotot()