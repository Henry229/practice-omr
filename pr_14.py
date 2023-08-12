import cv2
import numpy as np

# def sort_contour(cnts, method="top-to-bottom"):
#     reverse = False
#     i = 0
#     if method == "right-to-left" or method == "bottom-to-top":
#         reverse = True
#     if method == "top-to-bottom" or method == "bottom-to-top":
#         i = 1
#     boundingBoxes = [cv2.boundingRect(c) for c in cnts]
#     cnts, _ = zip(*sorted(zip(cnts, boundingBoxes), key=lambda b: b[1][i], reverse=reverse))
#     return list(cnts)

def sort_contour(cnts, from_idx, to_idx, method="top-to-bottom"):
    """This function sorts contours similar to the provided C++ function."""
    sub_cnts = cnts[from_idx:to_idx]
    if method == "top-to-bottom":
        sub_cnts.sort(key=lambda c: cv2.boundingRect(c)[1])
    elif method == "left-to-right":
        sub_cnts.sort(key=lambda c: cv2.boundingRect(c)[0])
    cnts[from_idx:to_idx] = sub_cnts
    return cnts
  
# Load the image
image = cv2.imread('/Users/henrychun/Downloads/Math-Thinking-NSW.jpeg', cv2.IMREAD_GRAYSCALE)
roi = image[338:338+280, 69:69+376]

# Thresholding
_, thresh = cv2.threshold(roi, 127, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)

# Find contours
contours, hierarchy = cv2.findContours(thresh, cv2.RETR_CCOMP, cv2.CHAIN_APPROX_SIMPLE)


questionCnts = []
for i, c in enumerate(contours):
    peri = cv2.arcLength(c, True)
    approx = cv2.approxPolyDP(c, 0.1 * peri, True)
    w, h = cv2.boundingRect(approx)[2:]
    ar = w / float(h)
    if hierarchy[0][i][3] == -1 and w >= 7 and h >= 7 and ar >= 0.7 and ar <= 1.3:
        questionCnts.append(approx)

questionCnts = sort_contour(questionCnts, 0, len(questionCnts), "top-to-bottom")

for i in range(0, len(questionCnts), 8):
    questionCnts = sort_contour(questionCnts, i, i+8, "left-to-right")

num = 1
id = 0
recognitionValue = 50  # This value might need adjustment based on your OMR sheet

# 각 마킹된 동그라미에 대한 정보와 계산된 ID 값을 저장하는 리스트를 생성합니다.
marking_info = []

for i in range(len(questionCnts)):
    mask = np.zeros(thresh.shape, dtype=np.uint8)
    cv2.drawContours(mask, [questionCnts[i]], -1, 255, -1)
    mask = cv2.bitwise_and(thresh, thresh, mask=mask)
    total = cv2.countNonZero(mask)
    if total > recognitionValue:
        id += num * 10 ** (7 - (i % 8))
        x, y, w, h = cv2.boundingRect(questionCnts[i])
        marking_info.append({"x": x, "y": y, "i": i, "value": num, "id_contribution": num * 10 ** (7 - (i % 8))})
        num += 1

print("marking_info:", marking_info)
print("Recognized ID:", id)
    # questionCnts[i:i+8] = sort_contour(questionCnts[i:i+8], "left-to-right")
    # questionCnts[i:i+8] = sort_contour(questionCnts[i:i+8], "left-to-right")

# num = 0
# id = 0
# recognitionValue = 50  # This value might need adjustment based on your OMR sheet

# for i in range(len(questionCnts)):
#     mask = np.zeros(thresh.shape, dtype=np.uint8)
#     cv2.drawContours(mask, [questionCnts[i]], -1, 255, -1)
#     mask = cv2.bitwise_and(thresh, thresh, mask=mask)
#     total = cv2.countNonZero(mask)
#     if total > recognitionValue:
#         id += num * 10 ** (7 - (i % 8))
#         num += 1

# print("Recognized ID:", id)
