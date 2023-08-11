import cv2
import numpy as np
import matplotlib.pyplot as plt
from block_info_module import block_info

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
    answers = {}
    
    if block_info['marking_direction'] == 'V':
        expected_width = h // num_of_question
        expected_height = w // num_of_selection
        for q in range(num_of_question):
            start_x = q * expected_width
            bubbled = None
            for opt in range(num_of_selection):
                start_y = opt * expected_height
                option_region = morphed[start_y:start_y+expected_height, start_x:start_x+expected_width]
                total = cv2.countNonZero(option_region)
                if bubbled is None or total > bubbled[0]:
                    bubbled = (total, opt)
                    print('>> bubbled : ', bubbled, '/',  total)
            answers[q + 1] = bubbled[1]
    else:
        expected_height = h // num_of_question
        expected_width = w // num_of_selection
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

# 제공된 이미지 다시 로드
image_path = "/Users/henrychun/Downloads/Math-Thinking-NSW.jpeg"
# image_path = "/Users/henry/Downloads/Math-Thinking-NSW.jpeg"
        
# "student no" 블록을 처리하도록 함수를 업데이트 후 답안 추출
detected_answers_updated = {}
for block in block_info:
    detected_answers_updated[block['name']] = position_corrected_extract_answers(image_path, block)

# 결과 출력
output_results_updated = {}
for block in block_info:
    block_name = block['name']
    if 'StartingQuestion' in block:
        starting_question = int(block['StartingQuestion'])
        block_results = {}
        for local_q_num, ans in detected_answers_updated[block_name].items():
            global_q_num = local_q_num + starting_question - 1
            block_results[global_q_num] = ans
        output_results_updated[block_name] = block_results
    else:
        output_results_updated[block_name] = detected_answers_updated[block_name]

print(output_results_updated)

