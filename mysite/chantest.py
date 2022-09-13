import requests
from bs4 import BeautifulSoup
import time

def get_bs_obj(com_code):
        url = "https://finance.naver.com/item/main.nhn?code=" + com_code
        result = requests.get(url)
        bs_obj = BeautifulSoup(result.content, "html.parser") #html.parser 로 파이썬에서 쓸 수 있는 형태로 변환
        return bs_obj

def get_price(com_code):
        bs_obj = get_bs_obj(com_code)
        no_today = bs_obj.find("p", {"class":"no_today"})
        blind_now = no_today.find("span", {"class":"blind"})
        return blind_now.text

def get_name(com_code):
        bs_obj = get_bs_obj(com_code)
        no_today = bs_obj.find("th", {"class":"no1"})
        blind_now = no_today.find("a")
        return blind_now.text

#삼성전자 005930
print("삼성전자 현제가")
print(get_price("005930"))
print(get_name("005930"))