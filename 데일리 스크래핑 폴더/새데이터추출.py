# 중복 데이터.csv를 제거하는 코드----------------------------------->

import csv

# CSV 파일 읽기
def read_csv(file_path):
    with open(file_path, 'r', newline='', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        data = [row for row in reader]
    return data

# CSV 파일 쓰기
def write_csv(file_path, data, fieldnames):
    with open(file_path, 'w', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(data)

# 매일 경로명 바꿔서 저장하기------------------------------------------------------->
old_data_path = '1204community_post_event_pg1.csv'
new_data_path = '1205community_post_event_pg1.csv'
output_path = '1205_event_added_items.csv'
# 매일 경로명 바꿔서 저장하기------------------------------------------------------>


# CSV 파일 읽기
old_data = read_csv(old_data_path)
new_data = read_csv(new_data_path)

# 추가된 항목 찾기
added_items = [item for item in new_data if (item['title'], item['content'], item['major_id']) not in 
              {(row['title'], row['content'], row['major_id']) for row in old_data}]

# 결과를 새로운 CSV 파일로 저장
fieldnames = new_data[0].keys()  # 필드 이름은 new_data의 첫 번째 행에서 가져옵니다.
write_csv(output_path, added_items, fieldnames)
