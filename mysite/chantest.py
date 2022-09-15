import json
from bs4 import BeautifulSoup   
import requests
from urllib.request import urlopen
import config

def savedata(date):
        data = get_obj(date)
        file_path = "./data/" + date + ".json"

        with open(file_path, 'w', encoding='utf-8') as file:
                json.dump(data, file)

def get_obj(date):
    url = "https://apis.data.go.kr/1160100/service/GetStockSecuritiesInfoService/getStockPriceInfo?serviceKey="+ config.APT_KEY +"&numOfRows=10000&resultType=json&basDt=" + date
    result = requests.get(url,verify=False).text
    data = json.loads(result)
    datalist = data.get("response").get("body").get("items").get("item")
    print(len(datalist))
    return data

def get_json(date):
        with open ("data/" + date + ".json", "r") as f:
                data = json.load(f)
                datalist = data.get("response").get("body").get("items").get("item")
                for i in datalist:
                        print(i.get("itmsNm") + " " + i.get("mrktCtg") + " " + i.get("srtnCd"))

#get_json("20220908")
get_obj("20220915")



