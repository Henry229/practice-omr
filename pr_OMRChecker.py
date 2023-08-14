import cv2
import numpy as np
import matplotlib.pyplot as plt
import json
from  pr_template import template_data

def preprocess_image_for_recognition(image):
     # Convert to grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    
    # 1. Gaussian blur
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)
    
    # 2. Thresholding using OTSU's method
    _, thresh = cv2.threshold(blurred, 0, 255, cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)
    
    # 3. Morphological operation: CLOSE, to close small gaps
    kernel = np.ones((2, 2), np.uint8)
    morphed = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel)
    
    return morphed

def recognize_marked_answers_using_pixel_ratio(image, bubble_coordinates, bubble_dimensions, threshold_ratio=0.5):
    recognized_answers = {}
    
    for field, coordinates in bubble_coordinates.items():
        field_answers = []
        for bubble in coordinates:
            top_left = tuple(bubble["top_left"])
            bottom_right = tuple(bubble["bottom_right"])
            bubble_area = image[top_left[1]:bottom_right[1], top_left[0]:bottom_right[0]]
            
            # Calculate the ratio of black pixels
            total_pixels = bubble_area.size
            black_pixels = total_pixels - cv2.countNonZero(bubble_area)
            black_pixel_ratio = black_pixels / total_pixels
            
            # Consider the bubble as marked if the black pixel ratio is above the threshold
            if black_pixel_ratio > threshold_ratio:
                field_answers.append(1) ???
            else:
                field_answers.append(0)
        
        recognized_answers[field] = field_answers
    
    return recognized_answers

def visualize_correct_marked_answers(image, bubble_coordinates, bubble_dimensions, answers):
    visualized_image = image.copy()
    
    for block_name, block_coords in bubble_coordinates.items():
        if block_name in answers:
            for idx, coord_dict in enumerate(block_coords):
                top_left = tuple(coord_dict["top_left"])
                bottom_right = tuple(coord_dict["bottom_right"])
                
                # Check if the bubble is NOT marked
                if answers[block_name][idx] == 0:
                    cv2.rectangle(visualized_image, top_left, bottom_right, (0, 0, 255), 2)
                    
    return visualized_image
  
# Load bubble coordinates from the saved JSON file
with open('py_template_codinate.json', 'r') as file:
    loaded_bubble_coordinates = json.load(file)

# Load image
omr_image = cv2.imread('/Users/henry/Downloads/Math-Thinking-NSW.jpeg')

# Preprocess the image
preprocessed_image = preprocess_image_for_recognition(omr_image)

# Recognize marked answers using the pre-processed image
marked_answers = recognize_marked_answers_using_pixel_ratio(preprocessed_image, loaded_bubble_coordinates, template_data["bubbleDimensions"], threshold_ratio=0.75)

# Visualize the correctly marked answers on the original image
visualized_image_with_correct_markings = visualize_correct_marked_answers(omr_image, loaded_bubble_coordinates, template_data["bubbleDimensions"], marked_answers)

# # Show the visualized image
# plt.figure(figsize=(12, 20))
# plt.imshow(cv2.cvtColor(visualized_image_with_correct_markings, cv2.COLOR_BGR2RGB))
# plt.axis('off')
# plt.show()
