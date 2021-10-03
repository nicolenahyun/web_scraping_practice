# 라이브러리 호출
from bs4 import BeautifulSoup
import requests
import pandas as pd
import csv
from selenium import webdriver
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# csv 파일 저장 세팅
filename = "마켓컬리_샐러드간편식.csv"
f = open(filename, 'w', encoding="utf-8-sig", newline="")
writer = csv.writer(f)

#컬럼명
cols = ['상품명', '상품설명', '가격', '할인정보', '판매단위', '중량/용량', '배송구분', '포장타입']
writer.writerow(cols)

# Webdriver 설정
options = webdriver.ChromeOptions()
options.add_argument('headless')
options.add_argument('window-size=1920x1080')
options.add_argument("disable-gpu")     # headless 설정 : 창없는 크롬으로 크롤링하기

browser = webdriver.Chrome('chromedriver', chrome_options=options)

# 마켓컬리 샐러드간편식 카테고리 상품 페이지 URL
browser.get("https://www.kurly.com/shop/goods/goods_list.php?category=912")
time.sleep(2)

# 웹 스크래이핑
items = browser.find_elements_by_class_name('item')
pages = browser.find_elements_by_class_name('pagediv>span>a')

for page in range(len(pages)) :

    for i in range(len(items)) :
        
        if page >= 1 :
            try :
                pages = browser.find_elements_by_class_name('pagediv>span>a')
                pages[page].click()
            except :
                pass

        items = browser.find_elements_by_class_name('item')
        items[i].click()
        
        time.sleep(5)
        
        req = browser.page_source
        soup = BeautifulSoup(req, 'html.parser')

        # 베스트 상품의 정보를 담아줄 리스트 item 생성
        item = []

        # 1. 상품명
        item.append(soup.find('strong', attrs={'class': 'name'}).get_text())

        # 2. 상품설명
        item.append(soup.find('span', attrs={'class': 'short_desc'}).get_text())

        # 3. 가격
        item.append(soup.find('span', attrs={'class': 'dc_price'}).get_text())

        # 4. 할인정보
        discount = soup.find('span', attrs={'class': 'dc_percent'})
        if discount:
            item.append(discount.get_text())  #할인O
        else:
            item.append('X')  #할인X

        # 상품정보
        info = soup.find('div', attrs={'class': 'goods_info'}).get_text().split()

        # 5. 판매단위
        if '판매단위' in info:
            item.append(info[info.index('판매단위') + 1])
        else:
            item.append('해당사항없음')

        # 6. 중량/용량
        if '중량/용량' in info:
            item.append(info[info.index('중량/용량') + 1])
        else:
            item.append('해당사항없음')        

        # 7. 배송구분
        if '배송구분' in info:
            item.append(info[info.index('배송구분') + 1])
        else:
            item.append('해당사항없음')   
            
        # 8. 포장타입
        if '포장타입' in info:
            item.append(info[info.index('포장타입')+ 1])
        else:
            item.append('해당사항없음')   
        
        browser.back()
        
        writer.writerow(item)
        
        time.sleep(5)

    time.sleep(2)
    pages = browser.find_elements_by_class_name('pagediv>span>a')
    print(pages, len(pages))
    pages[page].click()