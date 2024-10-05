import re
import pandas as pd

# 파일 경로 설정
# file_path = 'FallRisk_En/FallRisk_En/FallRisk_En_No6.tsv'  # 업로드된 파일 경로
file_path = 'FallRisk_Ko/FallRisk_Ko/FallRisk_ko_No5_4361.tsv'  # 업로드된 파일 경로

# 파일 읽기
with open(file_path, 'r', encoding='utf-8') as file:
    lines = file.readlines()

# '#Text='로 시작하는 행만 추출 (정규표현식을 사용해 '#Text=' 제거)
text_lines = [re.sub(r'^#Text=', '', line.strip()) for line in lines if line.startswith('#Text=')]

# 추출된 행들을 DataFrame으로 생성
df_text_lines = pd.DataFrame(text_lines, columns=['Extracted Text'])

# DataFrame의 각 행을 별도의 텍스트 파일로 저장 (4자리로 패딩하여 파일 이름 생성)
for idx, row in df_text_lines.iterrows():
    # 파일명 설정 (숫자를 4자리로 패딩)
    file_name = f'FallRisk_ko_No5_4361_{str(idx+1).zfill(4)}.txt'
    
    # 파일에 해당 행의 텍스트 저장
    with open(f'data/FallRisk_ko_No5_4361/{file_name}', 'w', encoding='utf-8') as f:
        f.write(row['Extracted Text'])

# 저장된 파일 목록을 확인하기 위한 결과 반환
[f'FallRisk_ko_No5_4361_{str(idx+1).zfill(4)}.txt' for idx in range(len(df_text_lines))]
