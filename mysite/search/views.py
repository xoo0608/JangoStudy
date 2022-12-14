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

def get_json2(date, name):
    file_path = "2022data/" + date + ".json"
    if os.path.exists(file_path):
        with open (file_path, "r") as f:
                data = json.load(f)
                datalist = data.get("response").get("body").get("items").get("item")
                for i in datalist:
                    if(i.get("itmsNm") == name):
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
        # no_today = bs_obj.find("th", {"class":"no1"})
        # blind_now = no_today.find("a")
        return bs_obj.select_one('#middle > div.h_company > div.wrap_company > h2 > a').string

def get_num(com_code):
    file_path = "2022data/" + "20220915" + ".json"
    if os.path.exists(file_path):
        with open (file_path, "r") as f:
                data = json.load(f)
                datalist = data.get("response").get("body").get("items").get("item")
                for i in datalist:
                    if(i.get("itmsNm") == com_code):
                        return i.get("srtnCd")
    else:
        return 999

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
            if '0' <= num[0] and num[0] <= '9':
                name = get_name(num)
            else:
                name = num
                num = get_num(name)

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
            context = {'num' : num, 'name' : name, 'price' : price,}
            return render(request, 'search/index.html', context)
            
    return render(request, 'search/index.html')

def results(request):
    #response = "You're looking at the results of question."
    context = {'num' : request.GET.get('idnum'), }
    #return render(request, 'search/index.html', context)
    return HttpResponse(request.GET.get('idnum'))

def searchtwo(request):
    if request.method == 'GET':
        if(request.GET.get("idnum1", None) != None and request.GET.get("idnum2", None) != None):
            num1 = request.GET.get("idnum1", None)
            num2 = request.GET.get("idnum2", None)
            if '0' <= num1[0] and num1[0] <= '9':
                name1 = get_name(num1)
            else:
                name1 = num1
                num1 = get_num(name1)

            if '0' <= num2[0] and num2[0] <= '9':
                name2 = get_name(num2)
            else:
                name2 = num2
                num2 = get_num(name2)

            price1 = []
            price2 = []
            start = "20220901"
            last = "20220915"
            start_date = datetime.strptime(start, "%Y%m%d")
            last_date = datetime.strptime(last, "%Y%m%d")
            while start_date <= last_date:
                dates = start_date.strftime("%Y%m%d")
                # print(dates)
                if get_json(dates, num1) != 999:
                    price1.append(get_json(dates, num1))
                    price2.append(get_json(dates, num2))
                # 하루 더하기
                start_date += timedelta(days=1)
            context = {'num1' : num1, 'name1' : name1, 'price1' : price1,
            'num2' : num2, 'name2' : name2, 'price2' : price2,}
            return render(request, 'search/searchtwo.html', context)
            
    return render(request, 'search/searchtwo.html')
