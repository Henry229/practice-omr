# Define the recognize_answers function with the additional parameters
def recognize_answers(image_path, block_info):
    # 이미지를 불러옵니다.
    img = cv2.imread(image_path)

    # 각 블록에 대해 반복합니다.
    for block in block_info:
        # 블록의 좌표를 가져옵니다.
        x, y, w, h = block['x'], block['y'], block['width'], block['height']

        # 이미지에서 블록을 분리합니다.
        block_img = img[y:y+h, x:x+w]

        # 블록을 처리할 2차원 배열을 생성합니다.
        answers = [[None for _ in range(block['num_of_selection'])] for _ in range(block['num_of_question'])]

        # 각 질문과 선택지에 대해 반복합니다.
        for i in range(block['num_of_question']):
            for j in range(block['num_of_selection']):
                # 질문과 선택지의 좌표를 계산합니다.
                if block['marking_direction'] == 'V':
                    x = i * (w // block['num_of_question'])
                    y = j * (h // block['num_of_selection'])
                else:
                    x = j * (w // block['num_of_selection'])
                    y = i * (h // block['num_of_question'])
                width = w // block['num_of_question']
                height = h // block['num_of_selection']

                # 이미지에서 질문과 선택지를 분리합니다.
                marking_area = block_img[y:y+height, x:x+width]

                # 질문과 선택지를 그레이스케일로 변환합니다.
                gray = cv2.cvtColor(marking_area, cv2.COLOR_BGR2GRAY)

                # 이미지를 이진화합니다.
                _, binary = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY_INV)

                # 컨투어를 찾습니다.
                contours, _ = cv2.findContours(binary, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

                # 각 컨투어에 대해 반복합니다.
                for contour in contours:
                    # 컨투어의 영역을 계산합니다.
                    area = cv2.contourArea(contour)

                    # 영역이 일정 크기 이상인 경우, 해당 컨투어를 답안으로 판단합니다.
                    if area > 50:
                        # 답안을 배열에 저장합니다.
                        answers[i][j] = 1

        # 답안을 출력합니다.
        print(f"Block '{block['name']}' answers: {answers}")

# Run the recognize_answers function with the updated block info
recognize_answers(image_path, new_block_info)
