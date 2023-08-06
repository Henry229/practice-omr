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
    min_contour_area = 50  # This value might need to be adjusted depending on the specific marking method
    for contour in contours:
        if cv2.contourArea(contour) > min_contour_area:
            return True
    return False

# Define the block_info
block_info = {
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
    'ActualWidth': 1122,
    'ActualHeight': 1636
}

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

# Crop the block from the image
block_image = final_block_image[block_info['y']:block_info['y']+block_info['height'], block_info['x']:block_info['x']+block_info['width']]

# Recognize the answers in the block with the new method
answers, recognized_numbers, marking_images = recognize_answers(block_image, block_info, recognize_func=recognize_marking_circular)

print('Recognized answers:', answers)
print('Recognized numbers:', recognized_numbers)

{
  'name': 'Test Level1',
  'type': 'TEST_LEVEL1',
  'marking_direction': 'V',
  'items': ['Year1', 'Year2', 'Year3', 'Year4', 'Year5', 'Year6'],
  'x': 707,
  'y': 295,
  'width': 37,
  'height': 176,
  'num_of_question': 1,
  'num_of_selection': 6,
  'selection_starting_number': 0
},
{
  'name': 'Test Level2',
  'type': 'TEST_LEVEL2',
  'marking_direction': 'V',
  'items': ['Year7', 'Year8', 'Year9', 'Year10', 'Year11', 'Year12'],
  'x': 791,
  'y': 295,
  'width': 38,
  'height': 176,
  'num_of_question': 1,
  'num_of_selection': 6,
  'selection_starting_number': 0
},
{
  'name': 'Test No',
  'type': 'TEST_NO',
  'marking_direction': 'V',
  'items': ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9'],
  'x': 894,
  'y': 295,
  'width': 87,
  'height': 293,
  'num_of_question': 2,
  'num_of_selection': 10,
  'selection_starting_number': 0
},
{
  'name': 'Branch No',
  'type': 'BRANCH_NO',
  'marking_direction': 'V',
  'items': ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9'],
  'x': 1001,
  'y': 295,
  'width': 89,
  'height': 293,
  'num_of_question': 2,
  'num_of_selection': 10,
  'selection_starting_number': 0
}
]