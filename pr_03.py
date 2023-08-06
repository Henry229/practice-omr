
# import cv2
# import numpy as np

# # Define the function to recognize answers
# def recognize_answers(image, block_info, recognize_func):
#     answers = []
#     recognized_numbers = []
#     marking_images = []
#     for i in range(block_info['num_of_question']):
#         for j in range(block_info['num_of_selection']):
#             if block_info['marking_direction'] == 'V':
#                 x = i * (block_info['width'] // block_info['num_of_question'])
#                 y = j * (block_info['height'] // block_info['num_of_selection'])
#             else:
#                 x = j * (block_info['width'] // block_info['num_of_selection'])
#                 y = i * (block_info['height'] // block_info['num_of_question'])
#             width = block_info['width'] // block_info['num_of_question']
#             height = block_info['height'] // block_info['num_of_selection']
#             marking_area = image[y:y+height, x:x+width]
#             if recognize_func(marking_area):
#                 answers.append((i, j))
#                 recognized_numbers.append(j)
#                 marking_images.append(marking_area)
#                 break
#     return answers, recognized_numbers, marking_images

# # Define the function to recognize marking by finding circular objects
# def recognize_marking_circular(image):
#     if len(image.shape) == 3:
#         image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
#     thresholded = cv2.adaptiveThreshold(image, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 11, 2)
#     contours, _ = cv2.findContours(thresholded, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
#     min_contour_area = 50
#     for contour in contours:
#         if cv2.contourArea(contour) > min_contour_area:
#             return True
#     return False

# # The block_info data
# block_info = [
#     {
#         'name': 'Student No',
#         'type': 'STUDENT_NO',
#         'marking_direction': 'V',
#         'items': ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9'],
#         'x': 69,
#         'y': 338,
#         'width': 371,
#         'height': 280,
#         'num_of_question': 8,
#         'num_of_selection': 10,
#         'selection_starting_number': 0,
#         'Item type': 'num'
#     },
#     {
#     'name': 'Test Type',
#     'type': 'TEST_TYPE',
#     'marking_direction': 'V',
#     'items': ['Entrance', 'Selective_Trial_Test', 'Scholarship_Test', 'OC_Trial_Test', 'Class_Test', 'DUMMY', 'Blended_OCTT', 'Blended_STT'],
#     'x': 441,
#     'y': 350,
#     'width': 38,
#     'height': 133,
#     'num_of_question': 1,
#     'num_of_selection': 8,
#     'selection_starting_number': 0
#     },
#     {
#       'name': 'Test Subj',
#       'type': 'SUBJECT',
#       'marking_direction': 'V',
#       'items': ['Maths', 'GA', 'Reading', 'Voca', 'TextType', 'Part1', 'Part2', 'Science', 'Others'],
#       'x': 591,
#       'y': 345,
#       'width': 27,
#       'height': 246,
#       'num_of_question': 1,
#       'num_of_selection': 9,
#       'selection_starting_number': 0
#     },
#     {
#       'name': 'Test Level1',
#       'type': 'TEST_LEVEL1',
#       'marking_direction': 'V',
#       'items': ['Year1', 'Year2', 'Year3', 'Year4', 'Year5', 'Year6'],
#       'x': 688,
#       'y': 350,
#       'width': 27,
#       'height': 176,
#       'num_of_question': 1,
#       'num_of_selection': 6,
#       'selection_starting_number': 0
#     },
#     {
#       'name': 'Test Level2',
#       'type': 'TEST_LEVEL2',
#       'marking_direction': 'V',
#       'items': ['Year7', 'Year8', 'Year9', 'Year10', 'Year11', 'Year12'],
#       'x': 767,
#       'y': 350,
#       'width': 27,
#       'height': 176,
#       'num_of_question': 1,
#       'num_of_selection': 6,
#       'selection_starting_number': 0
#     },
#     {
#       'name': 'Test No',
#       'type': 'TEST_NO',
#       'marking_direction': 'V',
#       'items': ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9'],
#       'x': 854,
#       'y': 350,
#       'width': 82,
#       'height': 265,
#       'num_of_question': 2,
#       'num_of_selection': 10,
#       'selection_starting_number': 0
#     },
#     {
#       'name': 'Branch No',
#       'type': 'BRANCH_NO',
#       'marking_direction': 'V',
#       'items': ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9'],
#       'x': 952,
#       'y': 350,
#       'width': 82,
#       'height': 265,
#       'num_of_question': 2,
#       'num_of_selection': 10,
#       'selection_starting_number': 0
#     }
#   ]

# # Load and preprocess the image
# image_path = "/Users/henry/Downloads/Math-Thinking-NSW.jpeg"
# image = cv2.imread(image_path)

# gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
# blurred = cv2.GaussianBlur(gray, (5, 5), 0)
# _, thresholded_otsu = cv2.threshold(blurred, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
# kernel = np.ones((3, 3), np.uint8)
# opened_otsu = cv2.morphologyEx(thresholded_otsu, cv2.MORPH_OPEN, kernel, iterations=2)
# closed_otsu = cv2.morphologyEx(opened_otsu, cv2.MORPH_CLOSE, kernel, iterations=2)
# final_block_image = cv2.GaussianBlur(closed_otsu, (3, 3), 0)

# # Rest of the code for processing and visualizations...


import cv2
import numpy as np

# Define the function to recognize answers
def recognize_answers(image, block_info, recognize_func):
    answers = []
    recognized_numbers = []
    marking_images = []
    for i in range(block_info['num_of_question']):
        for j in range(block_info['num_of_selection']):
            if block_info['marking_direction'] == 'V':
                x = i * (block_info['width'] // block_info['num_of_question'])
                y = j * (block_info['height'] // block_info['num_of_selection'])
            else:
                x = j * (block_info['width'] // block_info['num_of_selection'])
                y = i * (block_info['height'] // block_info['num_of_question'])
            width = block_info['width'] // block_info['num_of_question']
            height = block_info['height'] // block_info['num_of_selection']
            marking_area = image[y:y+height, x:x+width]
            if recognize_func(marking_area):
                answers.append((i, j))
                recognized_numbers.append(j)
                marking_images.append(marking_area)
                break
    return answers, recognized_numbers, marking_images

# Define the function to recognize marking by finding circular objects
def recognize_marking_circular(image):
    if len(image.shape) == 3:
        image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    thresholded = cv2.adaptiveThreshold(image, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 11, 2)
    contours, _ = cv2.findContours(thresholded, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    min_contour_area = 50
    for contour in contours:
        if cv2.contourArea(contour) > min_contour_area:
            return True
    return False

# The block_info data
block_info = [
  {
      'name': 'Student No',
      'type': 'STUDENT_NO',
      'marking_direction': 'V',
      'items': ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9'],
      'x': 69,
      'y': 338,
      'width': 376,
      'height': 280,
      'num_of_question': 8,
      'num_of_selection': 10,
      'selection_starting_number': 0,
      'Item_type': 'combo'
  },
  {
      'name': 'Test Type',
      'type': 'TEST_TYPE',
      'marking_direction': 'V',
      'items': ['Entrance', 'Selective_Trial_Test', 'Scholarship_Test', 'OC_Trial_Test', 'Class_Test', 'DUMMY', 'Blended_OCTT', 'Blended_STT'],
      'x': 441,
      'y': 350,
      'width': 38,
      'height': 236,
      'num_of_question': 1,
      'num_of_selection': 8,
      'selection_starting_number': 0,
      'Item_type': 'combo'
  },
  {
      'name': 'Test Subj',
      'type': 'SUBJECT',
      'marking_direction': 'V',
      'items': ['Maths', 'GA', 'Reading', 'Voca', 'TextType', 'Part1', 'Part2', 'Science', 'Others'],
      'x': 601,
      'y': 350,
      'width': 36,
      'height': 261,
      'num_of_question': 1,
      'num_of_selection': 9,
      'selection_starting_number': 0,
      'Item_type': 'multi'
  },
  {
      'name': 'Test Level1',
      'type': 'TEST_LEVEL1',
      'marking_direction': 'V',
      'items': ['Year1', 'Year2', 'Year3', 'Year4', 'Year5', 'Year6'],
      'x': 685,
      'y': 350,
      'width': 27,
      'height': 176,
      'num_of_question': 1,
      'num_of_selection': 6,
      'selection_starting_number': 0,
      'Item_type': 'combo'
  },
  {
      'name': 'Test Level2',
      'type': 'TEST_LEVEL2',
      'marking_direction': 'V',
      'items': ['Year7', 'Year8', 'Year9', 'Year10', 'Year11', 'Year12'],
      'x': 767,
      'y': 350,
      'width': 27,
      'height': 176,
      'num_of_question': 1,
      'num_of_selection': 6,
      'selection_starting_number': 0,
      'Item_type': 'combo'
  },
  {
      'name': 'Test No',
      'type': 'TEST_NO',
      'marking_direction': 'V',
      'items': ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9'],
      'x': 854,
      'y': 350,
      'width': 82,
      'height': 265,
      'num_of_question': 2,
      'num_of_selection': 10,
      'selection_starting_number': 0,
      'Item_type': 'num'
  },
  {
      'name': 'Branch No',
      'type': 'BRANCH_NO',
      'marking_direction': 'V',
      'items': ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9'],
      'x': 952,
      'y': 350,
      'width': 82,
      'height': 265,
      'num_of_question': 2,
      'num_of_selection': 10,
      'selection_starting_number': 0,
      'Item_type': 'num'
  },
  {
      'name': 'Answer_1',
      'type': 'ANSWER',
      'marking_direction': 'V',
      'Group': 'Math',
      'StartingQuestion': '1',
      'items': ['1', '2', '3', '4', '5'],
      'x': 131,
      'y': 675,
      'width': 175,
      'height': 410,
      'num_of_question': 15,
      'num_of_selection': 5,
      'selection_starting_number': 1,
      'Item_type': 'num'
  },
  {
      'name': 'Answer_2',
      'type': 'ANSWER',
      'marking_direction': 'V',
      'Group': 'Math',
      'StartingQuestion': '16',
      'items': ['1', '2', '3', '4', '5'],
      'x': 372,
      'y': 675,
      'width': 175,
      'height': 410,
      'num_of_question': 15,
      'num_of_selection': 5,
      'selection_starting_number': 1,
      'Item_type': 'num'
  },
  {
      'name': 'Answer_3',
      'type': 'ANSWER',
      'marking_direction': 'V',
      'Group': 'Math',
      'StartingQuestion': '31',
      'items': ['1', '2', '3', '4', '5'],
      'x': 612,
      'y': 675,
      'width': 175,
      'height': 410,
      'num_of_question': 15,
      'num_of_selection': 5,
      'selection_starting_number': 1,
      'Item_type': 'num'
  },
  {
      'name': 'Answer_4',
      'type': 'ANSWER',
      'marking_direction': 'V',
      'Group': 'Math',
      'StartingQuestion': '46',
      'items': ['1', '2', '3', '4', '5'],
      'x': 852,
      'y': 675,
      'width': 175,
      'height': 410,
      'num_of_question': 15,
      'num_of_selection': 5,
      'selection_starting_number': 1,
      'Item_type': 'num'
  },
  {
      'name': 'Answer_5',
      'type': 'ANSWER',
      'marking_direction': 'V',
      'Group': 'Thinking Skills',
      'StartingQuestion': '1',
      'items': ['1', '2', '3', '4', '5'],
      'x': 131,
      'y': 1143,
      'width': 175,
      'height': 410,
      'num_of_question': 15,
      'num_of_selection': 5,
      'selection_starting_number': 1,
      'Item_type': 'num'
  },
]

# The rest of the code remains unchanged
# ...

# Load and preprocess the image
image_path = "/Users/henry/Downloads/Math-Thinking-NSW.jpeg"
image = cv2.imread(image_path)

gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
blurred = cv2.GaussianBlur(gray, (5, 5), 0)
_, thresholded_otsu = cv2.threshold(blurred, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
kernel = np.ones((3, 3), np.uint8)
opened_otsu = cv2.morphologyEx(thresholded_otsu, cv2.MORPH_OPEN, kernel, iterations=2)
closed_otsu = cv2.morphologyEx(opened_otsu, cv2.MORPH_CLOSE, kernel, iterations=2)
final_block_image = cv2.GaussianBlur(closed_otsu, (3, 3), 0)

# Rest of the code for processing and visualizations...

