from django.http import HttpResponse
from django.shortcuts import render
from urllib.request import urlopen
from bs4 import BeautifulSoup   
import requests
import json
import os.path 
from datetime import datetime, timedelta



def get_json(date, num):
    file_path = "2022data/" + date + ".json"
    if os.path.exists(file_path):
        with open (file_path, "r") as f:
                data = json.load(f)
                datalist = data.get("response").get("body").get("items").get("item")
                for i in datalist:
                    if(i.get("srtnCd") == num):
                        return i.get("fltRt")
    else:
        return 999


def get_bs_obj(com_code):
    url = "https://finance.naver.com/item/main.nhn?code=" + com_code
    result = requests.get(url)
    bs_obj = BeautifulSoup(result.content, "html.parser") #html.parser 로 파이썬에서 쓸 수 있는 형태로 변환
    # print(bs_obj)
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

# def index(request):
#     if request.method == 'GET':
#         if(request.GET.get("idnum", None) != None):
#             # num = request.GET.get("idnum", None)
#             # html = urlopen("https://finance.naver.com/item/main.naver?code=" + request.GET.get("idnum", None))  
#             # bsObject = BeautifulSoup(html, "html.parser") 
#             # temp1 = bsObject .find('div',"wrap_company")
#             # temp2 = temp1.find_all('a')
#             # name = temp2[0].get_text()
#             # price = bsObject.select_one('#content > div.section.invest_trend > div.sub_section.right > table > tbody > tr:nth-child(2) > td:nth-child(2) > em').text
#             num = request.GET.get("idnum", None)
#             name = get_name(num)
#             price = get_price(num)
#             context = {'num' : num, 'name' : name, 'price' : price,}
#             return render(request, 'search/index.html', context)
#     return render(request, 'search/index.html')

def index(request):
    if request.method == 'GET':
        if(request.GET.get("idnum", None) != None):
            num = request.GET.get("idnum", None)
            name = get_name(num)
            price = []
            start = "20220901"
            last = "20220915"
            start_date = datetime.strptime(start, "%Y%m%d")
            last_date = datetime.strptime(last, "%Y%m%d")
            while start_date <= last_date:
                dates = start_date.strftime("%Y%m%d")
                # print(dates)
                if get_json(dates, num) != 999:
                    price.append(get_json(dates, num))
                # 하루 더하기
                start_date += timedelta(days=1)

            print(price)
            context = {'num' : num, 'name' : name, 'price' : price,}
            return render(request, 'search/index.html', context)
    return render(request, 'search/index.html')

def results(request):
    #response = "You're looking at the results of question."
    context = {'num' : request.GET.get('idnum'), }
    #return render(request, 'search/index.html', context)
    return HttpResponse(request.GET.get('idnum'))

