import os
import re

# 원본 파일명 설정
src_file = 'FallRisk_ko_No1_5000_modified'

# 파일 경로 설정
file_path = f'FallRisk_Ko/FallRisk_Ko/{src_file}.tsv'

# 파일 읽기
with open(file_path, 'r', encoding='utf-8') as file:
    lines = file.readlines()

# ann 파일을 저장할 디렉토리 생성
output_dir = f'ann/{src_file}'
os.makedirs(output_dir, exist_ok=True)

# 초기 설정
current_text_idx = 0  # 텍스트 블록의 인덱스 (파일 번호 생성 시 사용)
start_offset = None  # 텍스트 블록 내 첫 번째 토큰의 시작 위치
current_text = None  # 현재 텍스트 블록의 내용을 저장
ann_lines = []  # 각 텍스트 블록에 대한 주석을 저장하는 리스트
ann_results = []  # 파일명을 포함한 최종 결과 리스트
token_counter = 1  # T1, T2, T3... 같은 형식의 태그 ID 카운터

# 각 Text 블록에 대한 처리
for line in lines:
    # Text가 시작되는 줄을 찾음
    if line.startswith('#Text='):
        # 현재 텍스트가 있으면 이전 텍스트에 대한 ann 파일을 저장
        if current_text:
            ann_results.append((f'{src_file}_{str(current_text_idx + 1).zfill(4)}.ann', ann_lines))
            ann_lines = []  # 새로운 텍스트 블록에 대한 주석 초기화
            token_counter = 1  # 태그 ID를 T1부터 다시 시작
            current_text_idx += 1  # 파일 인덱스를 증가
            start_offset = None  # 시작 오프셋 초기화

        # 새로운 텍스트 블록이 시작되면 모든 변수 초기화
        current_text = re.sub(r'^#Text=', '', line.strip())  # #Text= 제거하고 텍스트 추출

    
    # 주석이 포함된 토큰 줄을 처리
    elif line.strip() and not line.startswith('#'):
        columns = line.split('\t')
        if len(columns) > 2:
            token_start, token_end = map(int, columns[1].split('-'))  # 시작과 끝 인덱스 추출
            token = columns[2]  # 실제 토큰 값
            tags = columns[3:]  # 태그 정보 추출
            
            # 텍스트 블록의 첫 번째 토큰이면, 시작 위치를 기록
            if start_offset is None:
                start_offset = token_start
            
            # 각 태그 처리
            for tag in tags:
                tag = tag.strip()
                if tag != '_' and tag:  # 태그가 유효한 경우에만 처리
                    if '[' in tag:  # 예: Risk_Beh[125] 같은 태그 처리
                        tag = tag.split('[')[0]  # 태그명만 추출
                    
                    clean_tag = tag.replace('\\', '')  # 태그에서 백슬래시 제거
                    
                    # 상대적 오프셋 계산
                    adjusted_start = token_start - start_offset
                    adjusted_end = token_end - start_offset
                    
                    # T1, T2, T3... 형식으로 태그 ID 생성
                    ann_id = f'T{token_counter}'
                    
                    # .ann 파일에 저장할 한 줄 추가 (형식: T1\tTag값 시작idx 끝idx\t토큰)
                    ann_lines.append(f"{ann_id}\t{clean_tag} {adjusted_start} {adjusted_end}\t{token}")
                    token_counter += 1

# 마지막 텍스트 블록에 대한 처리
if ann_lines:
    ann_results.append((f'{src_file}_{str(current_text_idx + 1).zfill(4)}.ann', ann_lines))

# ann 파일 저장
for ann_file_name, ann_content in ann_results:
    ann_file_path = os.path.join(output_dir, ann_file_name)
    with open(ann_file_path, 'w', encoding='utf-8') as f:
        f.write('\n'.join(ann_content))

print(f".ann files have been saved in the '{output_dir}' directory.")
