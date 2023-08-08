import cv2
import numpy as np

# Function to extract answers from a specified block
def extract_answers_from_block(image_path, block_info):
    # Load the image
    image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    
    # Extract block from the image
    x, y, w, h = block_info['x'], block_info['y'], block_info['width'], block_info['height']
    block_image = image[y:y+h, x:x+w]
    
    # Preprocess the block
    blurred = cv2.GaussianBlur(block_image, (5, 5), 0)
    thresh = cv2.threshold(blurred, 0, 255, cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)[1]
    kernel = np.ones((2, 2), np.uint8)
    morphed = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel)
    
    # Find contours in the block
    contours, _ = cv2.findContours(morphed, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    questionCnts = [cnt for cnt in contours if cv2.contourArea(cnt) > 100]
    
    # Sort contours
    questionCnts.sort(key=lambda cnt: cv2.boundingRect(cnt)[1])
    
    answers = {}
    num_of_question = block_info['num_of_question']
    num_of_selection = block_info['num_of_selection']

    # Loop over the questions and identify the bubbled answer
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

        # Store the answer for the current question
        q_num = i // num_of_selection + 1  # 1-indexed
        answers[q_num] = bubbled[1] + 1  # Answer options are also 1-indexed

    return answers

# Define the block_info
block_info = {
    'name': 'Answer_1',
    'type': 'ANSWER',
    'marking_direction': 'H',
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
}

# Extracting answers using the provided block_info
image_path = "/Users/henry/Downloads/Math-Thinking-NSW.jpeg"
detected_answers = extract_answers_from_block(image_path, block_info)

# Printing the detected answers
for question, answer in detected_answers.items():
    print(f"Question {question}: Answer {answer}")
