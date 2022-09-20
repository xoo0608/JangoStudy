import json
from xmlrpc.server import DocCGIXMLRPCRequestHandler
from bs4 import BeautifulSoup   
import requests
from urllib.request import urlopen
import config
import time
from datetime import datetime, timedelta


def savedata(date):
        data = get_obj(date)
        file_path = "./2022data/" + date + ".json"
        datalist = data.get("response").get("body").get("items").get("item")
        if len(datalist) > 1:
                print("yes!")
                with open(file_path, 'w', encoding='utf-8') as file:
                        json.dump(data, file)
        else:
                print("no!")

def get_obj(date):
        time.sleep(0.3)
        url = "https://apis.data.go.kr/1160100/service/GetStockSecuritiesInfoService/getStockPriceInfo?serviceKey="+ config.APT_KEY +"&numOfRows=10000&resultType=json&basDt=" + date
        result = requests.get(url,verify=False).text
        data = json.loads(result)
        return data

def get_json(date):
        with open ("data/" + date + ".json", "r") as f:
                data = json.load(f)
                datalist = data.get("response").get("body").get("items").get("item")
                for i in datalist:
                        print(i.get("itmsNm") + " " + i.get("mrktCtg") + " " + i.get("srtnCd"))

#get_json("20220908")
#get_obj("20220908")
savedata("20220916")


# start = "20211213"
# last = "20211231"

# # 시작일, 종료일 datetime 으로 변환
# start_date = datetime.strptime(start, "%Y%m%d")
# last_date = datetime.strptime(last, "%Y%m%d")



# 종료일 까지 반복
# while start_date <= last_date:
#     dates = start_date.strftime("%Y%m%d")
#     # print(dates)
#     savedata(str(dates))
#     # 하루 더하기
#     start_date += timedelta(days=1)