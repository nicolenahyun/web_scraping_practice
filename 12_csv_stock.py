# 시가총액 1위부터 200위까지 csv 파일로 뽑아오기
import csv
import requests
from bs4 import BeautifulSoup

url = "https://finance.naver.com/sise/sise_market_sum.nhn?sosok=0&page="

filename = "시가총액1-200.csv"
f = open(filename, "w", encoding="utf-8-sig", newline="") # newline="" : 한 줄 하고, 다음 정보를 출력하기 위함(엔터를 공백처리)
# utf8로 csv 파일을 열었을 때, 한글이 깨진다면 utf-8-sig로 변경하면 해결됨
writer = csv.writer(f) # writer를 통해 파일을 읽을 수 있음

for page in range(1, 5):
    res = requests.get(url + str(page)) # page를 문자열로 바꿔주기
    res.raise_for_status
    soup = BeautifulSoup(res.text, "html.parser")

    data_rows = soup.find("table", attrs={"class":"type_2"}).find("tbody").find_all("tr")
    for row in data_rows:
        columns = row.find_all("td")
        if len(columns) <= 1: # 의미 없는 데이터는 skip
            continue
        data = [column.get_text().strip() for column in columns] # strip() : 불필요한 공백 제거
        # print(data)
        writer.writerow(data) # 데이터가 리스트 형태로 저장됨