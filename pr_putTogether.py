import cv2
import numpy as np
from block_info_module import block_info

def vertical_preprocess(image):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)
    _, thresholded_otsu = cv2.threshold(blurred, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    kernel = np.ones((3, 3), np.uint8)
    opened_otsu = cv2.morphologyEx(thresholded_otsu, cv2.MORPH_OPEN, kernel, iterations=2)
    closed_otsu = cv2.morphologyEx(opened_otsu, cv2.MORPH_CLOSE, kernel, iterations=2)
    final_block_image = cv2.GaussianBlur(closed_otsu, (3, 3), 0)
    return final_block_image
    
def recognize_test_info(image, block, recognize_func):
    answers = []
    recognized_numbers = []
    marking_images = []
    
    for i in range(block['num_of_question']):
        for j in range(block['num_of_selection']):
            x = i * (block['width'] // block['num_of_question'])
            y = j * (block['height'] // block['num_of_selection'])
            width = block['width'] // block['num_of_question']
            height = block['height'] // block['num_of_selection']
            marking_area = image[y:y+height, x:x+width]
            if recognize_func(marking_area):
                answers.append((i, j))
                recognized_numbers.append(j)
                marking_images.append(marking_area)
                break
    return answers, recognized_numbers, marking_images
    
def recogize_marking_circular(image):
    if len(image.shape) == 3:
        image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    thresholded = cv2.adaptiveThreshold(image, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 11, 2)
    contours, _ = cv2.findContours(thresholded, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    min_contour_area = 50  # This value might need to be adjusted depending on the specific marking method
    for contour in contours:
        if cv2.contourArea(contour) > min_contour_area:
            return True
    return False
  
def horizontal_block_image(image_path, block_info):
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
    
# Load and preprocess the image
image_path = "/Users/henrychun/Downloads/Math-Thinking-NSW.jpeg"
# image_path = "/Users/henry/Downloads/Math-Thinking-NSW.jpeg" 
image = cv2.imread(image_path)

vertical_block_image = vertical_preprocess(image)

# Aggregate results from all blocks
all_answers = []
all_recognized_numbers = []
all_marking_images = []
 
output_results =  {}
detected_answers_updated = {}

for block in block_info:
    block_making_direction = block['marking_direction']
    
    if block_making_direction == 'V':
        block_image = vertical_block_image[block['y']:block['y']+block['height'], block['x']:block['x']+block['width']]
        answers, recognized_numbers, marking_images = recognize_test_info(block_image, block, recognize_func = recogize_marking_circular)
        all_answers.extend(answers)
        all_recognized_numbers.extend(recognized_numbers)
        all_marking_images.extend(marking_images)
    else:
        detected_answers_updated[block['name']] = horizontal_block_image(image_path, block)
        print('block name:', block['name'])
        # answers, recognized_numbers = recognize_answer_info(image, block)

print('Recognized answers:', all_answers)
print('Recognized numbers:', all_recognized_numbers)

# 결과 출력
output_results_updated = {}
for block in block_info:
    block_name = block['name']
    block_making_direction = block['marking_direction']
    
    if block_making_direction == 'H':
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