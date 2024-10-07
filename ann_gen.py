import re,os

tag_map = {
    'Restraint': 'Tx_Restraint',
    'RiskMed': 'Tx_RiskMed',
    'DisOT': 'Cog_DisOT',
    'LOC': 'Cog_LOC',
    'Aids': 'Mob_Aids',
    'Confusion': 'Cog_Confusion',
    'Hearing\\_Imp': 'Sen_Hearing_Imp',   # 백슬래시 없음
    'Slp\\_\\_Imp': 'Slp_Imp',
    'Visual\\_Imp': 'Sen_Visual_Imp',     # 백슬래시 없음
    'Non\\_cooper': 'Beh_Non_cooper',     # 백슬래시 없음
    'Alone': 'Beh_Alone',
    'RiskPro': 'Tx_RiskPro',
    'Weak': 'Mob_Weak',
    'P\\_limit': 'Mob_P_limit',           # 백슬래시 없음
    'Dizz': 'Mob_Dizz',
    'Sedatives': 'Slp_Sedatives'
}
# 파일 경로 설정
file_name='FallRisk_ko_No5_4361_modified'
file_path = f'FallRisk_Ko/FallRisk_Ko/{file_name}.tsv'

# 파일 읽기
with open(file_path, 'r', encoding='utf-8') as file:
    lines = file.readlines()
# 각 ann_results가 정확히 오프셋이 적용되도록 다시 수정

# ann 파일을 저장할 디렉토리 생성
output_dir = f'ann/{file_name}'
os.makedirs(output_dir, exist_ok=True)

ann_lines = []
current_text = None
current_text_idx = 0
token_counter = 1  # T1부터 시작하는 토큰 번호
start_offset = None  # 시작 위치를 저장하는 변수

# 결과를 저장할 리스트
ann_results = []

# Extracting lines related to each #Text=
for line in lines:
    # Text가 시작되는 줄
    if line.startswith('#Text='):
        if current_text:  # 이전에 있던 Text가 있으면 .ann 파일로 저장
            ann_results.append((f'{file_name}_{str(current_text_idx+1).zfill(4)}.ann', ann_lines))
            ann_lines = []  # 초기화
            current_text_idx += 1
            token_counter = 1  # T1부터 다시 시작
            start_offset = None  # 오프셋 초기화
        
        # 새로운 Text 시작
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
                start_offset = token_start
            
            # 태그가 있는지 확인하고 처리
            for tag in tags:
                if tag != '_':  # 유효한 태그가 있을 때만 처리
                    # tag_map에 태그가 존재하면 변환
                    if '[' in tag:  # 예: Hearing_Imp[125] 같은 형태 처리
                        tag = tag.split('[')[0]
                    mapped_tag = tag_map.get(tag, None)  # tag_map에 있으면 변환, 없으면 None
                    
                    # tag_map에 존재하는 모든 태그를 저장, UNK로 매핑된 것도 저장
                    if mapped_tag:  # mapped_tag가 존재하면 저장
                        ann_id = f'T{token_counter}'  # T1, T2, T3... 형식으로 태그 ID
                        # 첫 번째 태그의 시작 위치만큼 빼서 상대적 위치로 변환
                        adjusted_start = token_start - start_offset
                        adjusted_end = token_end - start_offset
                        ann_lines.append(f"{ann_id}\t{mapped_tag} {adjusted_start} {adjusted_end}\t{token}")
                        token_counter += 1

# 마지막 Text에 대한 처리
if current_text:
    ann_results.append((f'{file_name}_{str(current_text_idx+1).zfill(4)}.ann', ann_lines))


# ann 파일을 ann 디렉토리에 저장
for ann_file_name, ann_content in ann_results:
    ann_file_path = os.path.join(output_dir, ann_file_name)
    with open(ann_file_path, 'w', encoding='utf-8') as f:
        f.write('\n'.join(ann_content))

print(f".ann files have been saved in the '{output_dir}' directory.")