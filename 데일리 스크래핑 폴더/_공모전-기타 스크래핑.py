## 덕성 공모전/기타

import requests
import pandas as pd
from bs4 import BeautifulSoup
import re

# <제목가져오기>
cookies = {
}

headers = {
    'Accept': 'application/json, text/javascript, */*; q=0.01',
    'Accept-Language': 'ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7',
    'Connection': 'keep-alive',
    'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
    # 'Cookie': '1_1184=$2a$10$XhzHJf2pu3Ko1tJQwlXkK.GCLPv76.VcTQHQJugL0pj7tEDwDS2NO; visit_1=$2a$10$gxEbT/lRSh33pEp9sjD6quqW.GfhkUM8Y8JrKN0O10b1rgB6pjHwO; WMONID=G17nQHVWbdu; _ga_5RHKJ7PGMP=GS1.1.1695019597.4.1.1695020068.0.0.0; _ga=GA1.1.206436419.1676889468; _ga_5SXG79EMJJ=GS1.1.1696917284.9.1.1696917572.0.0.0; _ga_76XV8MCQVJ=GS1.1.1700549232.309.1.1700549239.0.0.0; JSESSIONID=aaaIYkxy5tBy74zN2iOUyEArvPOOWcp-5uMKiKMAW9490ZVxLiXWkdCjsKx9',
    'Origin': 'https://www.duksung.ac.kr',
    'Referer': 'https://www.duksung.ac.kr/bbs/board.do?menuId=1184&bsIdx=45',
    'Sec-Fetch-Dest': 'empty',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Site': 'same-origin',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Whale/3.23.214.10 Safari/537.36',
    'X-Requested-With': 'XMLHttpRequest',
    'sec-ch-ua': '"Whale";v="3", "Not-A.Brand";v="8", "Chromium";v="118"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
}

data = {
    'menuId': '1184',
    'bsIdx': '45',
    'page': '1',
    'bcIdx': '0',
    'searchCondition': 'SUBJECT',
    'searchKeyword': '',
    'categoryAllYn': 'Y',
}

response = requests.post('https://www.duksung.ac.kr/bbs/ajax/boardList.do', cookies=cookies, headers=headers, data=data)

url = "https://www.duksung.ac.kr/bbs/board.do?menuId=1184&bsIdx=45"
session = requests.Session()

titles = []

data = response.json()
dataList = data['resultList']

for d in dataList:
    titles.append(d['SUBJECT'])

# <url 가져오기>
getData = response.json()

url_list = []  

dataList = getData['resultList']

for d in dataList:
    b_idx = d['B_IDX']
    post_url = f"https://www.duksung.ac.kr/bbs/boardView.do?bsIdx=45&bIdx={b_idx}&menuId=1184&bcIdx=0&searchCondition=SUBJECT&searchKeyword="
    url_list.append(post_url)

# <본문 내용 및 URL 가져오기>
content_list = []

for i in range(0, len(url_list)):
    post_url = url_list[i]

    response = requests.get(post_url)
    html = response.text

    soup = BeautifulSoup(html, 'html.parser')

    content_div = soup.find('div', class_='bbs_memo')
    content_detail = content_div.get_text()

    # URL 추가
    content_detail += f"\n\n해당 게시글 바로가기: {post_url}"

    cleaned_text = re.sub(r'\n|\\xa0|\r', ' ', content_detail)
    cleaned_text = re.sub(r'\s+', ' ', cleaned_text).strip()
    content_detail = cleaned_text

    content_list.append(content_detail)

# DataFrame 생성
data = {
    'title': titles,
    'content': content_list,
    'img': [None] * len(titles),  # 이미지는 현재 스크래핑 코드에서 가져오지 않았으므로 None으로 채워넣음
    'time': pd.to_datetime('now'),  # 현재 시간을 사용하거나 스크래핑한 데이터에 시간 정보가 있다면 해당 정보로 대체
    'isduksung': False,  # 대외활동이라 false
    'major_id': [None] * len(titles),  # major_id는 현재 스크래핑 코드에서 가져오지 않았으므로 None으로 채워넣음
}

df = pd.DataFrame(data=data, columns=['title', 'content', 'img', 'time', 'isduksung', 'major_id'])

# NaN으로 대체
df['img'] = df['img'].apply(lambda x: pd.NA)
df['major_id'] = df['major_id'].apply(lambda x: pd.NA)

# CSV 파일로 저장
df.to_csv('1202community_post_competition_pg1.csv', index=False)