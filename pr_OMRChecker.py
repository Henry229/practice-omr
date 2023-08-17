import cv2
import numpy as np
import matplotlib.pyplot as plt
import json
from  pr_sel_MT_block_info import sel_MT_block_data

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
        num_of_selection = sel_MT_block_data["fieldBlocks"][field]["num_of_selection"]
        # Only for blocks starting with Math_Answer_ or Think_Answer_
        if field.startswith("Math_Answer_") or field.startswith("Think_Answer_"):
            starting_question = sel_MT_block_data["fieldBlocks"][field].get("StartingQuestion", 1)
        else:
            starting_question = None

        for idx, bubble in enumerate(coordinates):
            top_left = tuple(bubble["top_left"])
            bottom_right = tuple(bubble["bottom_right"])
            bubble_area = image[top_left[1]:bottom_right[1], top_left[0]:bottom_right[0]]
            
            # Calculate the ratio of black pixels
            total_pixels = bubble_area.size
            black_pixels = total_pixels - cv2.countNonZero(bubble_area)
            black_pixel_ratio = black_pixels / total_pixels
            
            # Determine the marked choice index
            choice_index = idx % num_of_selection
            question_number = "Q" + str(int(starting_question) + idx // num_of_selection) if starting_question is not None else None
            
            # Consider the bubble as marked if the black pixel ratio is above the threshold
            answer_data = {
                "block_name": field,
                "is_marked": 1 if black_pixel_ratio < threshold_ratio else 0,
                "marked_choice_index": choice_index if black_pixel_ratio < threshold_ratio else None,
                "question_number": question_number
            }

            field_answers.append(answer_data)
            
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
                if answers[block_name][idx]["is_marked"] == 1:
                    cv2.rectangle(visualized_image, top_left, bottom_right, (0, 255, 0), 2)  # Green rectangle for marked answers
                else:
                    cv2.rectangle(visualized_image, top_left, bottom_right, (0, 0, 255), 2)  # Red rectangle for unmarked answers
                    
    return visualized_image

# Load bubble coordinates from the saved JSON file
with open('selective_Math_Thinking_coordinates.json', 'r') as file:
    loaded_bubble_coordinates = json.load(file)

# Load image
omr_image = cv2.imread('/Users/henry/Downloads/Math-Thinking-NSW.jpeg')

# Preprocess the image
preprocessed_image = preprocess_image_for_recognition(omr_image)

# Recognize marked answers using the pre-processed image
marked_answers = recognize_marked_answers_using_pixel_ratio(preprocessed_image, loaded_bubble_coordinates, sel_MT_block_data["bubbleDimensions"], threshold_ratio=0.75)
filtered_answers = {block: [answer for answer in answers if answer["is_marked"] == 1] for block, answers in marked_answers.items()}
print('>>> recognized_answers:', filtered_answers)

# Visualize the correctly marked answers on the original image
visualized_image_with_correct_markings = visualize_correct_marked_answers(omr_image, loaded_bubble_coordinates, sel_MT_block_data["bubbleDimensions"], marked_answers)

# Show the visualized image
plt.figure(figsize=(12, 20))
plt.imshow(cv2.cvtColor(visualized_image_with_correct_markings, cv2.COLOR_BGR2RGB))
plt.axis('off')
plt.show()
