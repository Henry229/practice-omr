import cv2
import numpy as np

# Define the function to recognize answers for blocks with single markings
def recognize_answers_single(image, block_info, recognize_func):
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

# Define the function to recognize answers for blocks with multiple markings
def recognize_answers_multi(image, block_info, recognize_func):
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
    return answers, recognized_numbers, marking_images

# Define the function to recognize marking by finding circular objects
def recognize_marking_circular(image):
    if len(image.shape) == 3:
        image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    thresholded = cv2.adaptiveThreshold(image, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 11, 2)
    contours, _ = cv2.findContours(thresholded, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    min_contour_area = 50  # This value might need to be adjusted depending on the specific marking method
    for contour in contours:
        if cv2.contourArea(contour) > min_contour_area:
            return True
    return False

# Define the block_info
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
        'Item type': 'combo'
    },
    {
        'name': 'Test Type',
        'type': 'TEST_TYPE',
        'marking_direction': 'V',
        'items': ['Entrance', 'Selective_Trial_Test', 'Scholarship_Test', 'OC_Trial_Test', 'Class_Test', 'DUMMY', 'Blended_OCTT', 'Blended_STT'],
        'x': 441,
        'y': 295,
        'width': 38,
        'height': 236,
        'num_of_question': 1,
        'num_of_selection': 8,
        'selection_starting_number': 0,
        'Item type': 'combo'
    },
    {
        'name': 'Test Subj',
        'type': 'SUBJECT',
        'marking_direction': 'V',
        'items': ['Maths', 'GA', 'Reading', 'Voca', 'TextType', 'Part1', 'Part2', 'Science', 'Others'],
        'x': 601,
        'y': 295,
        'width': 36,
        'height': 261,
        'num_of_question': 1,
        'num_of_selection': 9,
        'selection_starting_number': 0,
        'Item type': 'multi'
    },
    {
        'name': 'Test
