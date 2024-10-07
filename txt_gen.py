import re
import os
import pandas as pd

# 파일 경로 설정
tsv_name = 'FallRisk_ko_No1_5000_modified'
file_path = f'FallRisk_Ko/FallRisk_Ko/{tsv_name}.tsv'

# 파일 읽기
with open(file_path, 'r', encoding='utf-8') as file:
    lines = file.readlines()

# 연속된 #Text= 블록을 하나의 문장으로 병합
current_text_block = ''
merged_texts = []
for line in lines:
    if line.startswith('#Text='):
        if current_text_block:  # 이전 텍스트 블록이 있으면 리스트에 추가
            merged_texts.append(current_text_block.strip())
        # 새로운 텍스트 블록 초기화 및 #Text= 제거
        current_text_block = re.sub(r'^#Text=', '', line.strip())
    else:
        # 태그가 아닌 경우는 무시하고 넘어감
        continue

# 마지막 텍스트 블록 추가
if current_text_block:
    merged_texts.append(current_text_block.strip())

# 추출된 병합된 텍스트들을 DataFrame으로 생성
df_text_lines = pd.DataFrame(merged_texts, columns=['Extracted Text'])

# 디렉토리 생성 (폴더가 없으면 생성)
output_dir = f'data/{tsv_name}'
os.makedirs(output_dir, exist_ok=True)

# DataFrame의 각 행을 별도의 텍스트 파일로 저장 (4자리로 패딩하여 파일 이름 생성)
for idx, row in df_text_lines.iterrows():
    # 파일명 설정 (숫자를 4자리로 패딩)
    file_name = f'{tsv_name}_{str(idx+1).zfill(4)}.txt'
    
    # 파일에 해당 행의 텍스트 저장
    with open(os.path.join(output_dir, file_name), 'w', encoding='utf-8') as f:
        f.write(row['Extracted Text'])

# 저장된 파일 목록을 확인하기 위한 결과 반환
output_files = [f'{tsv_name}_{str(idx+1).zfill(4)}.txt' for idx in range(len(df_text_lines))]
