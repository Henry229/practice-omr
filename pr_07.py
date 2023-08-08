import cv2
import numpy as np

# def sortTopToBottom(lhs, rhs):
#     rectLhs = cv2.boundingRect(np.array(lhs))
#     rectRhs = cv2.boundingRect(np.array(rhs))
#     return rectLhs[1] < rectRhs[1]

# def sortLeftToRight(lhs, rhs):
#     rectLhs = cv2.boundingRect(np.array(lhs))
#     rectRhs = cv2.boundingRect(np.array(rhs))
#     return rectLhs[0] < rectRhs[0]

def sortTopToBottom(contour):
    return cv2.boundingRect(np.array(contour))[1]

def sortLeftToRight(contour):
    return cv2.boundingRect(np.array(contour))[0]


def sort_contour(contours, from_idx, to_idx, sortOrder):
    if sortOrder == "top-to-bottom":
        contours[from_idx:to_idx] = sorted(contours[from_idx:to_idx], key=sortTopToBottom)
    elif sortOrder == "left-to-right":
        contours[from_idx:to_idx] = sorted(contours[from_idx:to_idx], key=sortLeftToRight)

# 이미지 로드
image = cv2.imread('/Users/henrychun/Downloads/Math-Thinking-NSW.jpeg', cv2.IMREAD_GRAYSCALE)

# 이진화
_, thresh = cv2.threshold(image, 127, 255, cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)

# 윤곽선 검출
contours, hierarchy = cv2.findContours(thresh, cv2.RETR_CCOMP, cv2.CHAIN_APPROX_SIMPLE)

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

# 문서 윤곽선 찾기
for i in range(len(contours)):
    contours_poly[i] = cv2.approxPolyDP(contours[i], 0.1, True)
    rect = cv2.boundingRect(contours[i])
    w = rect[2]
    h = rect[3]
    ar = w / h

    if hierarchy[0][i][3] == -1 and w >= 13 and h >= 13 and 0.7 < ar < 1.3:
        questionCnt.append(contours_poly[i])

# 윤곽선 정렬
sort_contour(questionCnt, 0, len(questionCnt), "top-to-bottom")
for i in range(0, len(questionCnt), NoOfChoice):
    sort_contour(questionCnt, i, i + NoOfChoice, "left-to-right")

# 답안 판별
testerAnswer1 = {}
num_of_question = block_info['num_of_question']

for i in range(0, min(len(questionCnt), num_of_question * NoOfChoice ), NoOfChoice):
    maxPixel = 0
    answerKey = 0

    for j in range(NoOfChoice):
        idx = i + j
        if idx >= len(questionCnt):
            break
          
        mask = np.zeros(thresh.shape, dtype=np.uint8)
        cv2.drawContours(mask, questionCnt, i + j, 255, -1)
        mask = cv2.bitwise_and(mask, thresh)

        if cv2.countNonZero(mask) > maxPixel:
            maxPixel = cv2.countNonZero(mask)
            answerKey = j

    if maxPixel < recognitionValue:
        answerKey = NoOfChoice

    testerAnswer1[i // NoOfChoice] = answerKey + 1  # +1 to make it 1-indexed

# 인식한 답 출력
for question, answer in testerAnswer1.items():
    print(f"Question {question}: Answer {answer}")
