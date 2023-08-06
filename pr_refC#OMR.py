import cv2
import numpy as np

def recognize_answers(image, block_info, recognize_func):
    answers = []
    recognized_numbers = []
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
                break
    return answers, recognized_numbers

def recognize_marking_otsu(image):
    if len(image.shape) == 3:
        image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    _, thresholded = cv2.threshold(image, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    total_pixels = image.shape[0] * image.shape[1]
    dark_pixels = (thresholded == 255).sum()
    ratio = dark_pixels / total_pixels
    return ratio > 0.1

# Define the block_info
block_info = {
    'name': 'Student No',
    'type': 'STUDENT_NO',
    'marking_direction': 'V',
    'items': ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9'],
    'x': 69, #원래 29
    'y': 338, # 원래 295
    'width': 376, # 원래 394
    'height': 280, # 원래 293
    'num_of_question': 8,
    'num_of_selection': 10,
    'selection_starting_number': 0,
    'ActualWidth': 1122,
    'ActualHeight': 1636
}
# {'name': 'Student No',
#  'type': 'STUDENT_NO',
#  'marking_direction': 'V',
#  'items': ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9'],
#  'x': 67,
#  'y': 345,
#  'width': 357,
#  'height': 269,
#  'num_of_question': 8,
#  'num_of_selection': 10,
#  'selection_starting_number': 0,
#  'ActualWidth': 1122,
#  'ActualHeight': 1636}

# Load and preprocess the image
image_path = "/Users/henry/Downloads/Math-Thinking-NSW.jpeg"  
image = cv2.imread(image_path)

# Adjustments
# block_info['x'] = block_info['x'] * block_info['ActualWidth'] // image.shape[1] + 20
# block_info['y'] = block_info['y'] * block_info['ActualHeight'] // image.shape[0] + 24
# block_info['width'] = (block_info['width'] - 10) * block_info['ActualWidth'] // image.shape[1]
# block_info['height'] = (block_info['height'] - 10) * block_info['ActualHeight'] // image.shape[0]

gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
blurred = cv2.GaussianBlur(gray, (5, 5), 0)
_, thresholded_otsu = cv2.threshold(blurred, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
kernel = np.ones((3, 3), np.uint8)
opened_otsu = cv2.morphologyEx(thresholded_otsu, cv2.MORPH_OPEN, kernel, iterations=2)
closed_otsu = cv2.morphologyEx(opened_otsu, cv2.MORPH_CLOSE, kernel, iterations=2)
final_block_image = cv2.GaussianBlur(closed_otsu, (3, 3), 0)

# Crop the block from the image
block_image = final_block_image[block_info['y']:block_info['y']+block_info['height'], block_info['x']:block_info['x']+block_info['width']]

# Recognize the answers in the block
answers, recognized_numbers = recognize_answers(block_image, block_info, recognize_func=recognize_marking_otsu)
print('Recognized answers:', answers)
print('Recognized numbers:', recognized_numbers)



# import cv2
# import numpy as np
# from PIL import Image

# # Define the function to recognize answers
# def recognize_answers(image, block_info):
#     # This function should be implemented based on the specific marking method of the OMR sheet.
#     # Here is a simple example of how it can be implemented.
#     answers = []
#     recognized_numbers = []  # 마킹된 숫자를 저장할 리스트
#     for i in range(block_info['num_of_question']):
#         for j in range(block_info['num_of_selection']):
#             # Calculate the position of the marking area for the current question and selection
#             if block_info['marking_direction'] == 'V':
#                 x = i * (block_info['width'] // block_info['num_of_question'])
#                 y = j * (block_info['height'] // block_info['num_of_selection'])
#             else:
#                 x = j * (block_info['width'] // block_info['num_of_selection'])
#                 y = i * (block_info['height'] // block_info['num_of_question'])
#             width = block_info['width'] // block_info['num_of_question']
#             height = block_info['height'] // block_info['num_of_selection']

#             # Crop the marking area from the image
#             marking_area = image[y:y+height, x:x+width]
#             # print('>>> marking area:', marking_area.shape)
#             # Show the marking area
#             # cv2.imshow('Marking Area', marking_area)
#             # cv2.waitKey(0) # Wait for a key press

#             # Recognize the answer in the marking area
#             # answer = recognize_marking(marking_area)
#             # if answer is not None:
#             #     answers.append((i, answer))
#             if recognize_marking(marking_area): # 마킹이 인식된 경우
#                 answers.append((i, j)) # 문제 인덱스와 선택지 인덱스를 추가
#                 recognized_numbers.append(j)  # 마킹된 숫자를 리스트에 추가
#                 break  # 다음 문제로 넘어가기
                
#     return answers, recognized_numbers
  
# def recognize_marking(image):
#     # This function should be implemented based on the specific marking method of the OMR sheet.
#     # Here is a more sophisticated example of how it can be implemented.	
#     # Apply adaptive thresholding to the image	
#     # thresholded = cv2.adaptiveThreshold(image, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 11, 2)	
#     # Find contours in the thresholded image	
#     # contours, _ = cv2.findContours(thresholded, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)	
#      # Define a minimum area for the contour
#     # min_contour_area = 44
#     # If any contour is found with area greater than minimum area, return True
#     # for contour in contours:
#         # if cv2.contourArea(contour) > min_contour_area:
#             # return True
#     # return False
#     # Define the threshold value
#     threshold = 127

#     # Convert the image to grayscale if it's not
#     if len(image.shape) == 3:
#         image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
#     # Apply thresholding to the image
#     _, thresholded = cv2.threshold(image, threshold, 255, cv2.THRESH_BINARY_INV)
    
#     # Calculate the total number of pixels and the number of dark pixels
#     total_pixels = image.shape[0] * image.shape[1]
#     dark_pixels = (thresholded == 255).sum()
#     # dark_pixels = (image < threshold).sum()

#     # Define a ratio to determine if the area is marked
#     ratio = dark_pixels / total_pixels

#     # If the ratio of dark pixels is greater than a certain value, consider it as marked
#     if ratio > 0.1: # You can adjust this value based on the specific marking method
#         return True
#     return False
  
  
# # Define the block information
# block_info = {
#     'name': 'Student No',
#     'type': 'STUDENT_NO',
#     'marking_direction': 'V',
#     'items': ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9'],
#     'x': 29,
#     'y': 295,
#     'width': 394,
#     'height': 293,
#     'num_of_question': 8,
#     'num_of_selection': 10,
#     'selection_starting_number': 0,
#     'ActualWidth': 1122,	
#     'ActualHeight': 1636
# }

# # Load the image
# image = cv2.imread("/Users/henry/Downloads/Math-Thinking-NSW.jpeg")

# # # Preprocess the image
# # image = cv2.medianBlur(image, 5)
# # ret, image = cv2.threshold(image, 127, 255, cv2.THRESH_BINARY)

# # Convert the image to grayscale
# gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# # Apply Gaussian blur to remove noise
# blurred = cv2.GaussianBlur(gray, (5, 5), 0)

# # Apply Canny edge detection to the image
# edged = cv2.Canny(blurred, 50, 200, 255)

# # Find contours in the edged image
# contours, _ = cv2.findContours(edged.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

# # Sort the contours from left-to-right
# contours = sorted(contours, key=cv2.contourArea, reverse=True)

# # Loop over the contours
# # for contour in contours:
# #     # Compute the bounding rectangle of the contour
# #     x, y, w, h = cv2.boundingRect(contour)

# #     # Draw a green rectangle around the contour
# #     cv2.rectangle(image, (x, y), (x+w, y+h), (0, 255, 0), 2)

# # Compute the bounding rectangle of the largest contour	
# x, y, width, height = cv2.boundingRect(contours[0])

		
# # Adjust the block_info	
# block_info['x'] = block_info['x'] * block_info['ActualWidth'] // image.shape[1] + 30	
# block_info['y'] = block_info['y'] * block_info['ActualHeight']  // image.shape[0] + 34	
# block_info['width'] = block_info['width'] * block_info['ActualWidth'] // image.shape[1]	
# block_info['height'] = block_info['height'] * block_info['ActualHeight'] // image.shape[0]

# # Apply adaptive thresholding for binarization
# thresholded = cv2.adaptiveThreshold(blurred, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2)

# # Apply morphological transformations to remove small noise
# kernel = np.ones((3, 3), np.uint8)
# opended = cv2.morphologyEx(thresholded, cv2.MORPH_OPEN, kernel, iterations=2)

# # Crop the block from the image
# block_image = opended[block_info['y']:block_info['y']+block_info['height'], block_info['x']:block_info['x']+block_info['width']]
# # print('*** Block_image', block_image)

# # Recognize the answers in the block
# answers, recognized_numbers = recognize_answers(block_image, block_info)

# # Print the recognized answers
# print('Recognized answers:', answers)
# print('Recognized numbers:', recognized_numbers)

# # Draw a green rectangle around the block
# # cv2.rectangle(image, (block_info['x'], block_info['y']), (block_info['x']+block_info['width'], block_info['y']+block_info['height']), (0, 255, 0), 2)
# # for contour in contours:	
#     # cv2.drawContours(image, [contour], -1, (0, 255, 0), 2)
# # Draw a green rectangle around the block
# cv2.rectangle(image, (block_info['x'], block_info['y']), (block_info['x']+block_info['width'], block_info['y']+block_info['height']), (0, 255, 0), 2)

# # Show the image
# cv2.imshow('OMR Sheet', image)

# # Wait for a key press and close the window
# cv2.waitKey(0)

# cv2.destroyAllWindows()




