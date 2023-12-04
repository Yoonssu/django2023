## 전공게시판 전체 1페이지 스크래핑 코드
# page를 지정하여 전공게시판 전체를 스크래핑할 수 있음.


import requests
import pandas as pd
from bs4 import BeautifulSoup
import re


# 학과 및 bsIdx 정보
majorname_bsInx_vector = [['korean', '1162'], ['japanese', '1166'], ['chinese', '1236'], ['english', '1240'], ['french','1170'], ['german', '1174'], ['spanish', '1244'], ['history', '1248'], ['philo', '1252'], ['hisart', '1256'], ['anthro', '1182'], ['business', '1186'], ['account', '1260'], ['econo', '1191'], ['law', '1195'], ['sociol', '1178'], ['lis', '1200'], ['psycho', '1204'], ['hdfs', '1208'], ['socwel', '1264'], ['poli', '1212'], ['fashion', '1220'], ['eced', '1216'], ['computer', '1224'], ['itmedia', '1228'], ['biotech', '1276'], ['cybersec', '1268'], ['software', '1272'], ['exercise', '1296'], ['fan', '1292'], ['staticstics', '1284'], ['chemi', '1288'], ['math', '1280'], ['oriental', '1304'], ['western', '1308'], ['interior', '1312'], ['visualcomm', '1316'], ['textile', '1320']]
majorname_vector = ['korean', 'japanese', 'chinese', 'english', 'french', 'german', 'spanish', 'history', 'philo', 'hisart', 'anthro', 'business', 'account', 'econo', 'law', 'sociol', 'lis', 'psycho', 'hdfs', 'socwel', 'poli', 'fashion', 'eced', 'computer', 'itmedia', 'biotech', 'cybersec', 'software', 'exercise', 'fan', 'staticstics', 'chemi', 'math', 'oriental', 'western', 'interior', 'visualcomm', 'textile']
bsIdx_vector = ['1162', '1166', '1236', '1240', '1170', '1174', '1244', '1248', '1252', '1256', '1182', '1186', '1260', '1191', '1195', '1178', '1200', '1204', '1208', '1264', '1212', '1220', '1216', '1224', '1228', '1276', '1268', '1272', '1296', '1292', '1284', '1288', '1280', '1304', '1308', '1312', '1316', '1320']

# 빈 DataFrame 생성
all_data = pd.DataFrame(columns=['title', 'content', 'img', 'time', 'isduksung', 'major_id'])

# 각 학과별로 스크래핑 수행
for i in range(len(majorname_vector)):
    majorname = majorname_vector[i]
    bsIdx = bsIdx_vector[i]

    print(f"Scraping {majorname}...")

    try:
        # 스크래핑 요청
        response = requests.post(f'https://www.duksung.ac.kr/{majorname}/bbs/ajax/boardList.do',
                                 cookies={}, 
                                 headers={
                                     'Accept': 'application/json, text/javascript, */*; q=0.01',
                                     'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Mobile Safari/537.36',
                                     'X-Requested-With': 'XMLHttpRequest',
                                 },
                                 data={
                                     'menuId': '1414',
                                     'bsIdx': bsIdx,
                                     'page': '1',  # 1페이지 스크래핑
                                     'bcIdx': '0',
                                     'searchCondition': 'SUBJECT',
                                     'searchKeyword': '',
                                     'categoryAllYn': 'Y',
                                 })

        # 스크래핑된 데이터 가져오기
        data = response.json()
        dataList = data['resultList']

        # 각 학과별로 DataFrame에 데이터 추가
        titles = []
        content_list = []
        for d in dataList:
            titles.append(d['SUBJECT'])

            # 각 게시물의 URL
            post_url = f"https://www.duksung.ac.kr/bbs/boardView.do?bsIdx={bsIdx}&bIdx={d['B_IDX']}&menuId=1414&bcIdx=0&searchCondition=SUBJECT&searchKeyword="
            url_list = []
            url_list.append(post_url)

            # 게시물의 내용 스크래핑
            post_response = requests.get(post_url)
            post_html = post_response.text
            post_soup = BeautifulSoup(post_html, 'html.parser')
            content_div = post_soup.find('div', class_='bbs_memo')
            
            # span 태그 내의 모든 텍스트 추출
            span_texts = [span.get_text(strip=True) for span in content_div.find_all('span')]

            # 텍스트를 줄바꿈으로 구분하여 하나의 문자열로 결합
            content_detail = '\n'.join(span_texts)

            
            content_detail = content_div.get_text()

            # URL 추가
            content_detail += f"\n\n해당 게시글 바로가기: {post_url}"

            cleaned_text = re.sub(r'\n|\\xa0|\r', ' ', content_detail)
            cleaned_text = re.sub(r'\s+', ' ', cleaned_text).strip()
            content_list.append(cleaned_text)

        # 각 학과의 DataFrame 생성
        major_data = pd.DataFrame(data={'title': titles,
                                         'content': content_list,
                                         'img': [None] * len(titles),
                                         'time': pd.to_datetime('now'),
                                         'isduksung': True,
                                         'major_id': [i + 1] * len(titles)})

        # 모든 학과의 DataFrame을 하나로 합치기
        all_data = pd.concat([all_data, major_data], ignore_index=True)

        print(f"Scraping {majorname} complete!")
    except Exception as e:
        print(f"Scraping {majorname} failed: {e}")
        continue

# CSV 파일로 저장 => 날짜별로 파일명을 바꿔서 저장할 것.
all_data.to_csv('1204_community_post_all_majors_pg1.csv', index=False)
print("Scraping complete!")
