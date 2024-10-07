import re
import pandas as pd

# 파일 경로 설정
file_path = 'FallRisk_Ko/FallRisk_Ko/FallRisk_ko_No1_5000.tsv'  # 원본 TSV 파일 경로
new_file_path = 'FallRisk_Ko/FallRisk_Ko/FallRisk_ko_No1_5000_modified.tsv'  # 수정된 TSV 파일 경로

# 파일 읽기
with open(file_path, 'r', encoding='utf-8') as file:
    lines = file.readlines()

# 새로 생성할 TSV의 내용을 담을 리스트
new_tsv_content = []
current_text = ""

for line in lines:
    line = line.strip()
    
    # #Text=로 시작하는 부분을 처리
    if line.startswith('#Text='):
        # 현재 텍스트가 비어있지 않다면 이전 텍스트를 공백 2개로 이어 붙이기
        if current_text:
            current_text += "" + re.sub(r'^#Text=', '', line)
        else:
            current_text = re.sub(r'^#Text=', '', line)
    else:
        # 단어 위치 정보가 있는 경우, 현재까지 이어진 텍스트를 기록하고 초기화
        if current_text:
            # 합쳐진 텍스트를 새로운 TSV 파일의 첫 열로 추가
            new_tsv_content.append(f"#Text={current_text}\r")
            current_text = ""
        
        # 나머지 줄은 그대로 추가 (단어 위치 정보)
        new_tsv_content.append(line + "\r")

# 마지막으로 남아있는 텍스트 블록을 처리
if current_text:
    new_tsv_content.append(f"#Text={current_text}\r")

# 수정된 내용을 새 TSV 파일로 저장
with open(new_file_path, 'w', encoding='utf-8') as new_file:
    new_file.writelines(new_tsv_content)

# 저장된 새로운 TSV 파일 확인 메시지 출력
print(f"Modified TSV file saved to: {new_file_path}")
