# -*- coding: utf-8 -*-
"""naver_movie_review.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/17xWMSVOBZG-vcxFme-yD8jg_tqRPPLXc

## 영화 리뷰 스크레이핑
"""

# 필요한 라이브러리 설치
import re
import requests
from bs4 import BeautifulSoup

BASE_URL = "https://movie.naver.com/movie"

# get_page 함수 : 페이지 URL을 받아 해당 페이지를 가져오고 파싱한 두 결과들을 리턴함
def get_page(page_url):
    page = requests.get(page_url)
    soup = BeautifulSoup(page.content, "html.parser")

    return soup, page

# get_avg_stars 함수 : 리뷰 리스트를 받아 평균 별점을 구해 리턴함
def get_avg_stars(reviews):
    stars = []      # 빈 평점 리스트 생성

    for i in range(len(reviews)):
        stars.append(reviews[i]['review_star'])

    avg = sum(stars) / len(stars)

    return avg

# get_movie_code 함수 : 영화 제목을 받으면 해당 영화 제목으로 검색했을 때, 가장 먼저 나오는 영화의 아이디를 리턴함
def get_movie_code(movie_title):
    search_url = f"{BASE_URL}/search/result.naver?query={movie_title}&section=all&ie=utf8"

    page = requests.get(search_url)
    soup = BeautifulSoup(page.content, 'html.parser')

    code_url = soup.dt.a.get('href')        # <dt> 태그 내의 <a href>
    movie_code = int(code_url.split('=')[-1])       # '='을 기준으로 끊고, 뒤에서 첫번째의 숫자 추출

    return movie_code

# get_reviews 함수 : 리뷰들이 담긴 리뷰 리스트를 리턴함
def get_reviews(movie_code, page_num=1):
    review_url = f"{BASE_URL}/point/af/list.naver?st=mcode&sword={movie_code}&target=after&page={page_num}"
    review_list = []        # 빈 리뷰 리스트 생성

    page = requests.get(review_url)
    soup = BeautifulSoup(page.content, 'html.parser')

    # review_text
    text_raw = soup.find_all('td', 'title')
    review_text = []

    for i in range(len(text_raw)):
        text = text_raw[i].text.split('\n')[5]
        review_text.append(text)

    # review_star
    star_raw = soup.find_all('div', 'list_netizen_score')
    review_star = []

    for i in range(len(star_raw)):
        star = star_raw[i].find('em').string
        review_star.append(star)

    # review_text와 review_star를 dictionary 형태로 바꾸기
    for i in ranfe(len(review_star)):
        dict = {'review_text' : review_text[i],
                'review_star' : review_star[i]}
        review_list.append(dict)

    return review_list

# scrape_by_review_num 함수 : 총 스크레이핑할 리뷰 개수를 받아 해당 개수만큼 리뷰 항목이 담긴 리뷰 리스트를 리턴함
def scrape_by_review_num(movie_title, review_num):

    reviews = []
    page_num = 1
    while len(reviews) < review_num:
        reviews += get_reviews(get_movie_code(movie_title), page_num)
        page_num += 1
    return reviews[:review_num]

# scrape_by_page_num 함수 : 페이지 수를 기준으로 리뷰를 스크레이핑
def scrape_by_page_num(movie_title, page_num=10):

    reviews = []
    for i in range(page_num):
        reviews += get_reviews(get_movie_code(movie_title), i)