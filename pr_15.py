import cv2
import numpy as np
from block_info_module import block_info

# Define constants
recognitionValue = 50 # This value might need adjustment based on your OMR sheet

def sort_contour(cnts, from_idx, to_idx, method="top-to-bottom"):
    """Sort contours."""
    sub_cnts = cnts[from_idx:to_idx]
    if method == "top-to-bottom":
        sub_cnts.sort(key=lambda c: cv2.boundingRect(c)[1])
    elif method == "left-to-right":
        sub_cnts.sort(key=lambda c: cv2.boundingRect(c)[0])
    cnts[from_idx:to_idx] = sub_cnts
    return cnts

def process_block_for_direction_V(block):
    """Process block without converting the indices to array."""
    x, y, width, height = block['x'], block['y'], block['width'], block['height']
    roi = image[y:y+height, x:x+width]
    _, thresh = cv2.threshold(roi, 127, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)
    contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    questionCnts = []
    
    for c in contours:
        peri = cv2.arcLength(c, True)
        approx = cv2.approxPolyDP(c, 0.1 * peri, True)
        w, h = cv2.boundingRect(approx)[2:]
        ar = w / float(h)
        if w >= 7 and h >= 7 and ar >= 0.7 and ar <= 1.3:
            questionCnts.append(approx)
            
    questionCnts = sort_contour(questionCnts, 0, len(questionCnts), "top-to-bottom")

    for i in range(0, len(questionCnts), block['num_of_question']):
        questionCnts = sort_contour(questionCnts, i, i+block['num_of_question'], "left-to-right")

    marking_info = []
    for i in range(len(questionCnts)):
        mask = np.zeros(thresh.shape, dtype=np.uint8)
        cv2.drawContours(mask, [questionCnts[i]], -1, 255, -1)
        mask = cv2.bitwise_and(thresh, thresh, mask=mask)
        total = cv2.countNonZero(mask)
        if total > recognitionValue:
            x, y, w, h = cv2.boundingRect(questionCnts[i])
            marking_info.append({"x": x, "y": y, "i": i})
            
    # recognized_indices = [mark["i"] for mark in marking_info]
    return marking_info
    # return recognized_indices, marking_info

image_path = "/Users/henry/Downloads/Math-Thinking-NSW.jpeg"
image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)

# Process blocks
results = []
for block in block_info:
    if block['marking_direction'] == 'V':
        marking_info = process_block_for_direction_V(block)
        results.append({
            "block_name": block['name'],
            "xxxxx": marking_info
        })
    else:
      print('block_name : ', block['name'])
      
      
# Extracting the entire code for display
code_content = """
import cv2
import numpy as np
from block_info_module import block_info

# Define constants
recognitionValue = 50

def sort_contour(cnts, from_idx, to_idx, method="top-to-bottom"):
    sub_cnts = cnts[from_idx:to_idx]
    if method == "top-to-bottom":
        sub_cnts.sort(key=lambda c: cv2.boundingRect(c)[1])
    elif method == "left-to-right":
        sub_cnts.sort(key=lambda c: cv2.boundingRect(c)[0])
    cnts[from_idx:to_idx] = sub_cnts
    return cnts

def process_block_for_direction_V(block):
    x, y, width, height = block['x'], block['y'], block['width'], block['height']
    roi = image[y:y+height, x:x+width]
    _, thresh = cv2.threshold(roi, 127, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)
    contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    questionCnts = []
    
    for c in contours:
        peri = cv2.arcLength(c, True)
        approx = cv2.approxPolyDP(c, 0.1 * peri, True)
        w, h = cv2.boundingRect(approx)[2:]
        ar = w / float(h)
        if w >= 7 and h >= 7 and ar >= 0.7 and ar <= 1.3:
            questionCnts.append(approx)
            
    questionCnts = sort_contour(questionCnts, 0, len(questionCnts), "top-to-bottom")

    for i in range(0, len(questionCnts), block['num_of_question']):
        questionCnts = sort_contour(questionCnts, i, i+block['num_of_question'], "left-to-right")

    marking_info = []
    for i in range(len(questionCnts)):
        mask = np.zeros(thresh.shape, dtype=np.uint8)
        cv2.drawContours(mask, [questionCnts[i]], -1, 255, -1)
        mask = cv2.bitwise_and(thresh, thresh, mask=mask)
        total = cv2.countNonZero(mask)
        if total > recognitionValue:
            x, y, w, h = cv2.boundingRect(questionCnts[i])
            marking_info.append({"x": x, "y": y, "i": i})
            
    return marking_info

def get_recognized_items(block, marking_info):
    recognized_items = []
    interval = block['height'] / block['num_of_selection']
    for mark in marking_info:
        idx = int(mark['y'] / interval)
        if idx < len(block['items']):
            recognized_items.append(block['items'][idx])
    return recognized_items

def get_recognized_items_for_student_no(block, marking_info):
    recognized_items = ['x'] * block['num_of_question'] 
    interval = block['height'] / block['num_of_selection']
    for mark in marking_info:
        item_idx = int(mark['y'] / interval)
        question_idx = mark['i'] // block['num_of_selection']
        if item_idx < len(block['items']):
            recognized_items[question_idx] = block['items'][item_idx]
    return recognized_items

def indices_to_arr_final(indices):
    arr = [-1] * 8
    for index in indices:
        col = index % 8
        value = index // 8
        arr[col] = value
    return arr

def get_recognized_items_for_student_no_updated(block, marking_info):
    indices = [mark['i'] for mark in marking_info]
    arr_final = indices_to_arr_final(indices)
    recognized_items = [block['items'][idx] if idx != -1 else 'x' for idx in arr_final]
    return recognized_items

image_path = "/mnt/data/Math-Thinking-NSW.jpeg"
image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)

results = []
for block in block_info:
    if block['marking_direction'] == 'V':
        marking_info = process_block_for_direction_V(block)
        results.append({
            "block_name": block['name'],
            "marking_info": marking_info
        })

final_results = {}
for result in results:
    block_name = result['block_name']
    marking_info = result['marking_info']
    block_data = next((block for block in block_info if block['name'] == block_name), None)
    if block_data:
        if block_name == "Student No":
            recognized_items = get_recognized_items_for_student_no_updated(block_data, marking_info)
        else:
            recognized_items = get_recognized_items(block_data, marking_info)
        final_results[block_name] = recognized_items
"""

code_content
