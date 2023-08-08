import cv2
import numpy as np

def sortTopToBottom(contour):
    return cv2.boundingRect(np.array(contour))[1]

def sortLeftToRight(contour):
    return cv2.boundingRect(np.array(contour))[0]

def sort_contour(contours, from_idx, to_idx, sortOrder):
    if sortOrder == "top-to-bottom":
        contours[from_idx:to_idx] = sorted(contours[from_idx:to_idx], key=sortTopToBottom)
    elif sortOrder == "left-to-right":
        contours[from_idx:to_idx] = sorted(contours[from_idx:to_idx], key=sortLeftToRight)

image_path = '/mnt/data/Math-Thinking-NSW.jpeg'
image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)

# Image preprocessing
blurred = cv2.GaussianBlur(image, (5, 5), 0)
thresh = cv2.adaptiveThreshold(blurred, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 11, 2)
kernel = np.ones((2, 2), np.uint8)
morphed = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel)

contours, hierarchy = cv2.findContours(morphed, cv2.RETR_CCOMP, cv2.CHAIN_APPROX_SIMPLE)

contours_poly = [None] * len(contours)
questionCnt = []

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

NoOfChoice = block_info['num_of_selection']
recognitionValue = 100

for i in range(len(contours)):
    contours_poly[i] = cv2.approxPolyDP(contours[i], 0.1, True)
    rect = cv2.boundingRect(contours[i])
    w = rect[2]
    h = rect[3]
    ar = w / h

    if hierarchy[0][i][3] == -1 and w >= 13 and h >= 13 and 0.7 < ar < 1.3:
        questionCnt.append(contours_poly[i])

sort_contour(questionCnt, 0, len(questionCnt), "top-to-bottom")
for i in range(0, len(questionCnt), NoOfChoice):
    sort_contour(questionCnt, i, i + NoOfChoice, "left-to-right")

x, y, w, h = block_info['x'], block_info['y'], block_info['width'], block_info['height']
block_image = image[y:y+h, x:x+w]
block_thresh = cv2.adaptiveThreshold(block_image, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 11, 2)
block_morphed = cv2.morphologyEx(block_thresh, cv2.MORPH_CLOSE, kernel)
block_contours, _ = cv2.findContours(block_morphed, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

block_questionCnt = []
for contour in block_contours:
    rect = cv2.boundingRect(contour)
    w, h = rect[2], rect[3]
    ar = w / h

    if w >= 13 and h >= 13 and 0.7 < ar < 1.3:
        block_questionCnt.append(contour)

sort_contour(block_questionCnt, 0, len(block_questionCnt), "top-to-bottom")
for i in range(0, len(block_questionCnt), NoOfChoice):
    sort_contour(block_questionCnt, i, i + NoOfChoice, "left-to-right")

testerAnswer1 = {}
num_of_question = block_info['num_of_question']

for i in range(0, min(len(block_questionCnt), num_of_question * NoOfChoice), NoOfChoice):
    maxPixel = 0
    answerKey = 0

    for j in range(NoOfChoice):
        idx = i + j
        if idx >= len(block_questionCnt):
            break
          
        mask = np.zeros(block_morphed.shape, dtype=np.uint8)
        cv2.drawContours(mask, block_questionCnt, i + j, 255, -1)
        mask = cv2.bitwise_and(mask, block_morphed)

        if cv2.countNonZero(mask) > maxPixel:
            maxPixel = cv2.countNonZero(mask)
            answerKey = j

    if maxPixel < recognitionValue:
      answerKey = NoOfChoice

    testerAnswer1[i // NoOfChoice] = answerKey + 1  # +1 to make it 1-indexed

visualized_block_image = cv2.cvtColor(block_image, cv2.COLOR_GRAY2BGR)
for i, contour in enumerate(block_questionCnt):
    if i // NoOfChoice in testerAnswer1:
        if testerAnswer1[i // NoOfChoice] == (i % NoOfChoice) + 1:
            cv2.drawContours(visualized_block_image, [contour], -1, (0, 255, 0), 2)

h, w = visualized_block_image.shape[:2]
visualized_image_combined = cv2.cvtColor(image, cv2.COLOR_GRAY2BGR)
visualized_image_combined[y:y+h, x:x+w] = visualized_block_image
