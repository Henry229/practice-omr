import cv2
import numpy as np
import matplotlib.pyplot as plt
from block_info_module import block_info

def extract_answers_from_block(image_path, block_info):
    image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    x, y, w, h = block_info['x'], block_info['y'], block_info['width'], block_info['height']
    block_image = image[y:y+h, x:x+w]
    blurred = cv2.GaussianBlur(block_image, (5, 5), 0)
    thresh = cv2.threshold(blurred, 0, 255, cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)[1]
    kernel = np.ones((2, 2), np.uint8)
    morphed = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel)
    contours, _ = cv2.findContours(morphed, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    questionCnts = [cnt for cnt in contours if cv2.contourArea(cnt) > 100]
    questionCnts.sort(key=lambda cnt: cv2.boundingRect(cnt)[1])
    answers = {}
    num_of_question = block_info['num_of_question']
    num_of_selection = block_info['num_of_selection']
    for i in range(0, len(questionCnts), num_of_selection):
        cnts = sorted(questionCnts[i:i + num_of_selection], key=lambda cnt: cv2.boundingRect(cnt)[0])
        bubbled = None
        for (j, c) in enumerate(cnts):
            mask = np.zeros(thresh.shape, dtype="uint8")
            cv2.drawContours(mask, [c], -1, 255, -1)
            mask = cv2.bitwise_and(thresh, thresh, mask=mask)
            total = cv2.countNonZero(mask)
            if bubbled is None or total > bubbled[0]:
                bubbled = (total, j)
        q_num = i // num_of_selection + 1
        answers[q_num] = bubbled[1] + 1
    return answers

def position_corrected_extract_answers(image_path, block_info):
    image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    x, y, w, h = block_info['x'], block_info['y'], block_info['width'], block_info['height']
    block_image = image[y:y+h, x:x+w]
    blurred = cv2.GaussianBlur(block_image, (5, 5), 0)
    thresh = cv2.threshold(blurred, 0, 255, cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)[1]
    kernel = np.ones((2, 2), np.uint8)
    morphed = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel)
    num_of_question = block_info['num_of_question']
    num_of_selection = block_info['num_of_selection']
    expected_height = h // num_of_question
    expected_width = w // num_of_selection
    answers = {}
    for q in range(num_of_question):
        start_y = q * expected_height
        bubbled = None
        for opt in range(num_of_selection):
            start_x = opt * expected_width
            option_region = morphed[start_y:start_y+expected_height, start_x:start_x+expected_width]
            total = cv2.countNonZero(option_region)
            if bubbled is None or total > bubbled[0]:
                bubbled = (total, opt)
        answers[q + 1] = bubbled[1] + 1
    return answers

def visualize_answers_on_block_updated(block_img, answers):
    num_of_question = len(answers)
    h, w = block_img.shape
    expected_height = h // num_of_question
    expected_width = w // 5
    for q_num, ans in answers.items():
        start_y = (q_num - 1) * expected_height
        start_x = (ans - 1) * expected_width
        end_y = start_y + expected_height
        end_x = start_x + expected_width
        cv2.rectangle(block_img, (start_x, start_y), (end_x, end_y), (200), 2)
    return block_img

# Define the block_info


# Extract answers using the position-corrected method
# detected_answers_corrected = {}
# for block in block_info:
#     detected_answers_corrected[block['name']] = position_corrected_extract_answers("/Users/henrychun/Downloads/Math-Thinking-NSW.jpeg", block)

# # 결과 출력
# for block_name, answers in detected_answers_corrected.items():
#     print(f"\n{block_name}:")
#     for q_num, ans in answers.items():
#         print(f"Question: {q_num}: Answer: {ans}")

# 제공된 이미지 다시 로드
image_path = "/Users/henrychun/Downloads/Math-Thinking-NSW.jpeg"
image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)

missing_starting_question_blocks = []

for block in block_info:
    if 'StartingQuestion' not in block:
        missing_starting_question_blocks.append(block['name'])

if missing_starting_question_blocks:
    print("The following blocks are missing the 'StartingQuestion' key:", missing_starting_question_blocks)
else:
    print("All blocks have the 'StartingQuestion' key.")
    
# 이미지가 제대로 로드되었는지 확인
if image is not None:
    loaded = True
else:
    loaded = False

# 로드가 성공했을 경우, 답안 추출 및 결과 출력
if loaded:
    # 각 블록에 대한 답안 추출
    detected_answers_corrected = {}
    for block in block_info:
        detected_answers_corrected[block['name']] = position_corrected_extract_answers(image_path, block)

    # 결과를 시작 문제 번호를 고려하여 출력
    output_results = {}
    for block in block_info:
        block_name = block['name']
        if 'StartingQuestion' in block:
          starting_question = int(block['StartingQuestion'])
          block_results = {}
          for local_q_num, ans in detected_answers_corrected[block_name].items():
              global_q_num = local_q_num + starting_question - 1
              block_results[global_q_num] = ans
          output_results[block_name] = block_results

print(output_results)

