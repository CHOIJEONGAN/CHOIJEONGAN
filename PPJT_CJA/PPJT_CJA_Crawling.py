#네이버 증권(코스피 시가총액 순위)

import re # 정규 표현식(regular expression)을 지원하는 파이썬 라이브러리
import requests # HTTP 요청을 보내는 파이썬 라이브러리
from bs4 import BeautifulSoup # HTML과 XML 등의 마크업 언어에서 데이터를 추출하기 위한 파이썬 라이브러리

# 네이버 증권 시가총액 페이지 URL 가져오기
url="https://finance.naver.com/sise/sise_market_sum.naver?&page="
# page=1
for page in range(1,2): #50가지 3이면 100개
    res=requests.get(url+str(page))
    soup=BeautifulSoup(res.content,"lxml")
    
    data_rows=soup.find("table",{"class":"type_2"}).find("tbody").find_all("tr")
    for row in data_rows:
        columns=row.find_all("td")
        if len(columns)<=1:
            continue
        data=[column.get_text().strip() for column in columns]
        # i for i in list : 한줄 for문
        print(data)

#위의 네이버 증권(코스피 시가총액 순위) 코드를 판다스 데이터 프레임으로 정리
import os # 운영체제와 상호작용하기 위한 기능을 제공하는 파이썬 내장 라이브러리
import pandas as pd # 데이터프레임을 다루기 위한 모듈
from selenium import webdriver # 웹 브라우저를 자동화하는 라이브러리
from selenium.webdriver.common.by import By # 웹 요소를 검색하기 위한 라이브러

browser = webdriver.Chrome()
browser.maximize_window() # 창 최대화

# 네이버 증권 시가총액 페이지 URL 가져오기
url = 'https://finance.naver.com/sise/sise_market_sum.naver?&page='
browser.get(url)

# 조회 항목 초기화 (체크되어 있는 항목 체크 해제)
checkboxes = browser.find_elements(By.NAME, 'fieldIds')
for checkbox in checkboxes:
    if checkbox.is_selected(): # 체크된 상태라면?
        checkbox.click() # 클릭 (체크 해제)

# 원하는 조회 항목 설정
items_to_select = ['거래량', '전일거래량', 'PER', 'PBR', '외국인비율']
for checkbox in checkboxes:
    parent = checkbox.find_element(By.XPATH, '..') # 부모 element
    label = parent.find_element(By.TAG_NAME, 'label')
    # print(label.text) # 이름 확인
    if label.text in items_to_select: # 선택 항목과 일치한다면
        checkbox.click() # 체크

# 적용하기 클릭
btn_apply = browser.find_element(By.XPATH, '//a[@href="javascript:fieldSubmit()"]')
btn_apply.click()

for idx in range(1, 40): # 1 이상 40 미만 페이지 반복
    # 사전 작업 : 페이지 이동
    browser.get(url + str(idx)) # http://naver.com....&page=2

    # 데이터 추출
    df = pd.read_html(browser.page_source)[1]
    df.dropna(axis='index', how='all', inplace=True)
    df.dropna(axis='columns', how='all', inplace=True)
    if len(df) == 0: # 더 이상 가져올 데이터가 없으면?
        break

    # 결과를 csv 파일로 저장
    f_name = 'sise.csv'
    if os.path.exists(f_name): # 파일이 있다면? 헤더 제외
        df.to_csv(f_name, encoding='utf-8-sig', index=False, mode='a', header=False)
    else: # 파일이 없다면? 헤더 포함
        df.to_csv(f_name, encoding='utf-8-sig', index=False)
    print(f'{idx} 페이지 완료')

# 브라우저 종료
browser.quit()

#네이버 증권 주요뉴스 크롤링

import requests # HTTP 요청을 보내기 위한 모듈
from bs4 import BeautifulSoup # HTML 파싱을 위한 모듈
import csv # csv 파일을 만들기 위한 모듈
import pandas as pd # 데이터프레임을 다루기 위한 모듈

# 네이버 금융 시장지표 페이지에서 HTML을 가져와 BeautifulSoup 객체 생성
url = 'https://finance.naver.com/marketindex/'
response = requests.get(url)
soup = BeautifulSoup(response.text, 'html.parser')

# CSV 파일 생성 후 'Title', 'Link' 열을 가지는 첫번째 행 추가
with open('market_news.csv', 'w', encoding='utf-8', newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(['Title', 'Link'])
    
# section_news 클래스의 li 태그에서 제목과 링크 정보 추출하여 CSV 파일로 저장    
    section_news = soup.find('div', class_='section_news')
    for li in section_news.find_all('li'):
        title = li.text.strip()
        link = li.a['href']
        writer.writerow([title, link])
        
# 저장된 CSV 파일을 불러와서 데이터프레임으로 저장        
news = pd.read_csv("market_news.csv", encoding="utf-8")
# 저장된 데이터 프레임 출력
news.head()

#네이버 증권 환율,시세 텍스트 크롤링

import requests # HTTP 요청을 보내기 위한 모듈
from bs4 import BeautifulSoup # HTML 파싱을 위한 모듈
import csv # csv 파일을 만들기 위한 모듈
import pandas as pd # 데이터프레임을 다루기 위한 모듈

url = 'https://finance.naver.com/'
response = requests.get(url)
# BeautifulSoup 객체를 생성, 위에서 가져온 html 문서를 파싱
soup = BeautifulSoup(response.text, 'html.parser')

# 금융 뉴스 목록이 있는 table의 article2 class 선택
article2 = soup.select('.article2')

# table의 모든 tr 태그에 대해 각각의 td 태그에서 텍스트 정보를 추출하여 csv 파일로 저장
rows = []
for tr in article2[0].select('tr'):
    row = []
    for td in tr.select('td, th'):
        row.append(td.text.strip())
    rows.append(row)

with open('naver_finance.csv', 'w', newline='', encoding='utf-8') as csvfile:
    writer = csv.writer(csvfile)
    for row in rows:
        writer.writerow(row)


#저장된 CSV 파일을 불러와서 데이터프레임으로 저장
currency = pd.read_csv("naver_finance.csv", encoding="utf-8")
# 상위 26개의 데이터를 출력
currency.head(27)
currency.style.hide(axis='index')

#네이버 증권 가장 많이 본 리포트
import requests #HTTP 요청을 보내기 위한 모듈
from bs4 import BeautifulSoup #HTML 파싱을 위한 모듈
import csv # csv 파일을 만들기 위한 모듈
import pandas as pd # 데이터프레임을 다루기 위한 모듈

url = 'https://finance.naver.com/research/'
response = requests.get(url)
soup = BeautifulSoup(response.content, 'html.parser')

# 결과를 저장할 리스트 생성
results = []

# div class="box_type_r"에서 ul class="right_list_1" 선택
right_list_1 = soup.select_one('div.box_type_r ul.right_list_1')

# ul 태그 안에 있는 li 태그들 선택
for li in right_list_1.select('li'):
    # li 태그 안에 있는 a 태그와 span 태그에서 텍스트와 url 추출
    title = li.select_one('a').get_text(strip=True)
    link = li.select_one('a')['href']

    # 추출한 결과를 리스트에 저장
    results.append([title, link])

# 결과를 csv 파일로 저장
with open('naver_research.csv', 'w', newline='', encoding='utf-8') as f:
    writer = csv.writer(f)
    writer.writerow(['Title', 'Link'])
    writer.writerows(results)

# pandas로 csv 파일 읽기
most_viewed = pd.read_csv('naver_research.csv', encoding='utf-8')

#데이터프레임 출력
most_viewed.head()
