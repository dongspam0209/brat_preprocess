import os
import re

src_file='FallRisk_ko_No5_4361'
# 파일 경로 설정
file_path = f'FallRisk_Ko/FallRisk_Ko/{src_file}.tsv'

# 파일 읽기
with open(file_path, 'r', encoding='utf-8') as file:
    lines = file.readlines()

# ann 파일을 저장할 디렉토리 생성
output_dir = f'ann/{src_file}'
os.makedirs(output_dir, exist_ok=True)

# 각 Text마다 누적되지 않도록 token_counter 초기화
current_text_idx = 0
ann_lines = []
start_offset = None  # 시작 오프셋을 저장하는 변수
current_text = None
# 결과를 저장할 리스트
ann_results = []
token_counter = 1


# 각 Text에 대한 처리
for line in lines:
    # Text가 시작되는 줄
    if line.startswith('#Text='):
        # 이전 텍스트에 대한 ann 파일을 저장
        # if ann_lines:
        #     ann_results.append((f'{src_file}_{str(current_text_idx+1).zfill(4)}.ann', ann_lines))
        if current_text:
            ann_results.append((f'{src_file}_{str(current_text_idx+1).zfill(4)}.ann', ann_lines))
        # 새로운 텍스트가 시작될 때마다 token_counter와 ann_lines 초기화
            ann_lines = []
            token_counter = 1  # T1부터 다시 시작
            current_text_idx += 1
            start_offset = None  # 각 텍스트 블록마다 시작 오프셋을 초기화

        
        # 새로운 텍스트 내용 처리 및 오프셋 초기화
        current_text = re.sub(r'^#Text=', '', line.strip())
        
    # 태그 정보가 있는 줄 처리
    elif line.strip() and not line.startswith('#'):
        columns = line.split('\t')
        if len(columns) > 2:
            token_start, token_end = map(int, columns[1].split('-'))
            token = columns[2]
            tags = columns[3:]
            
            # 첫 번째 태그의 시작 위치를 저장
            if start_offset is None:
                start_offset = token_start  # 텍스트 블록 내 첫 번째 토큰의 시작 위치
            
            # 유효한 태그가 있는지 확인하고 처리
            for tag in tags:
                if tag != '_' and tag.strip():  # 유효한 태그가 있을 때만 처리
                    if '[' in tag:  # 예: Hearing_Imp[125] 같은 형태 처리
                        tag = tag.split('[')[0]
                    
                    # 백슬래시 제거
                    clean_tag = tag.replace('\\', '')
                    
                    # 상대적 위치 정보 적용 (start_offset을 기준으로 변환)
                    adjusted_start = token_start - start_offset
                    adjusted_end = token_end - start_offset
                    
                    ann_id = f'T{token_counter}'  # T1, T2, T3... 형식으로 태그 ID
                    ann_lines.append(f"{ann_id}\t{clean_tag} {adjusted_start} {adjusted_end}\t{token}")
                    token_counter += 1

# 마지막 Text에 대한 처리
if ann_lines:
    ann_results.append((f'{src_file}_{str(current_text_idx+1).zfill(4)}.ann', ann_lines))

# ann 파일을 저장
for ann_file_name, ann_content in ann_results:
    ann_file_path = os.path.join(output_dir, ann_file_name)
    with open(ann_file_path, 'w', encoding='utf-8') as f:
        f.write('\n'.join(ann_content))

print(f".ann files have been saved in the '{output_dir}' directory.")
