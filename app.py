# import cv2
# import numpy as np

# # 이미지 로드
# image = cv2.imread('/Users/henry/Downloads/Math-Thinking-NSW.jpeg')

# # 이미지를 그레이스케일로 변환
# gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# # 블러링
# blurred = cv2.GaussianBlur(gray, (5, 5), 0)

# # 적응형 이진화
# binary = cv2.adaptiveThreshold(blurred, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 11, 2)

# # 윤곽선 찾기
# contours, _ = cv2.findContours(binary, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

# # 윤곽선을 y 좌표에 따라 정렬
# contours = sorted(contours, key=lambda contour: cv2.boundingRect(contour)[1])

# # 각 윤곽선에 대해
# for contour in contours:
#     # 윤곽선의 경계 상자를 얻음
#     x, y, w, h = cv2.boundingRect(contour)

#     # 경계 상자의 면적을 계산
#     area = cv2.contourArea(contour)

#     # 경계 상자의 면적이 일정 크기 이상인 경우만 선택
#     if area > 500:
#         # 경계 상자를 이미지에 그림
#         cv2.rectangle(image, (x, y), (x+w, y+h), (0, 255, 0), 2)

#         # 경계 상자 내부의 ROI를 추출
#         roi = binary[y:y+h, x:x+w]

#         # ROI의 평균 픽셀 강도를 계산
#         mean_intensity = np.mean(roi)

#         # 평균 픽셀 강도가 특정 임계값보다 낮은 경우, 마킹된 것으로 판단
#         if mean_intensity < 128:
#             print(f'Box at {(x, y)} is marked.')
#             # 마킹된 부분을 빨간색으로 표시
#             image[y:y+h, x:x+w] = (0, 0, 255)

# cv2.imshow('OMR Sheet', image)
# cv2.waitKey(0)
# cv2.destroyAllWindows()

# ----------------------------------------------------------------

# import cv2
# import numpy as np

# # 이미지 로드
# image = cv2.imread('/Users/henry/Downloads/Math-Thinking-NSW.jpeg')

# # 이미지를 그레이스케일로 변환
# gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# # 블러링
# blurred = cv2.GaussianBlur(gray, (5, 5), 0)

# # 적응형 이진화
# binary = cv2.adaptiveThreshold(blurred, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 11, 2)

# # 윤곽선 찾기
# contours, _ = cv2.findContours(binary, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

# # 윤곽선을 y 좌표에 따라 정렬
# contours = sorted(contours, key=lambda contour: cv2.boundingRect(contour)[1])

# # 각 윤곽선에 대해
# for contour in contours:
#     # 윤곽선의 경계 상자를 얻음
#     x, y, w, h = cv2.boundingRect(contour)

#     # 경계 상자의 면적을 계산
#     area = cv2.contourArea(contour)

#     # 경계 상자의 면적이 일정 크기 이상인 경우만 선택
#     if area > 500:
#         # 경계 상자를 이미지에 그림
#         cv2.rectangle(image, (x, y), (x+w, y+h), (0, 255, 0), 2)

#         # 경계 상자 내부의 ROI를 추출
#         roi = gray[y:y+h, x:x+w]

#         # ROI의 평균 픽셀 강도를 계산
#         mean_intensity = np.mean(roi)

#         # 평균 픽셀 강도가 특정 임계값보다 낮은 경우, 마킹된 것으로 판단
#         if mean_intensity < 150:
#             print(f'Box at {(x, y)} is marked.')
#             # 마킹된 부분을 빨간색으로 표시
#             image[y:y+h, x:x+w] = (0, 0, 255)

# cv2.imshow('OMR Sheet', image)
# cv2.waitKey(0)
# cv2.destroyAllWindows()

# ________________________________________________________________


# import cv2
# import numpy as np

# # 이미지 로드
# image = cv2.imread('/Users/henry/Downloads/Math-Thinking-NSW.jpeg')

# # 이미지를 그레이스케일로 변환
# gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# # 블러링
# blurred = cv2.GaussianBlur(gray, (5, 5), 0)

# # 적응형 이진화
# binary = cv2.adaptiveThreshold(blurred, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 11, 2)

# # 윤곽선 찾기
# contours, _ = cv2.findContours(binary, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

# # 각 윤곽선에 대해
# for contour in contours:
#     # 윤곽선의 경계 상자를 얻음
#     x, y, w, h = cv2.boundingRect(contour)

#     # 경계 상자의 면적을 계산
#     area = cv2.contourArea(contour)

#     # 경계 상자의 면적이 일정 크기 이상인 경우만 선택
#     if 100 < area < 1000:  # Adjust these values based on the size of the circles
#         # 경계 상자 내부의 ROI를 추출
#         roi = binary[y:y+h, x:x+w]

#         # ROI의 평균 픽셀 강도를 계산
#         mean_intensity = np.mean(roi)

#         # 평균 픽셀 강도가 특정 임계값보다 높은 경우, 마킹된 것으로 판단 
#         if mean_intensity > 0.9:  # Adjusted threshold
#             # 마킹된 부분을 빨간색으로 표시
#             center_x = x + w // 2
#             center_y = y + h // 2
#             radius = max(w, h) // 2
#             cv2.circle(image, (center_x, center_y), radius, (0, 0, 255), 2)

# cv2.imshow('OMR Sheet', image)
# cv2.waitKey(0)
# cv2.destroyAllWindows()

import cv2
import numpy as np
import imutils
from imutils.perspective import four_point_transform
from imutils import contours

# 이미지 로드
image = cv2.imread('/Users/henry/Downloads/Math-Thinking-NSW.jpeg')

# 그레이스케일로 변환
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# 가우시안 블러를 사용하여 노이즈 제거
blurred = cv2.GaussianBlur(gray, (5, 5), 0)

# 캐니 엣지 검출을 사용하여 이미지의 엣지를 찾음
edged = cv2.Canny(blurred, 75, 200)

# 윤곽선을 찾음
cnts = cv2.findContours(edged.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
cnts = imutils.grab_contours(cnts)

# 문서의 윤곽선을 찾음
docCnt = None
if len(cnts) > 0:
    cnts = sorted(cnts, key=cv2.contourArea, reverse=True)
    for c in cnts:
        peri = cv2.arcLength(c, True)
        approx = cv2.approxPolyDP(c, 0.02 * peri, True)
        if len(approx) == 4:
            docCnt = approx
            break

# 문서의 윤곽선을 기반으로 투시 변환을 적용
paper = four_point_transform(image, docCnt.reshape(4, 2))
warped = four_point_transform(gray, docCnt.reshape(4, 2))

# 이진화
thresh = cv2.threshold(warped, 0, 255, cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)[1]

# 문제의 윤곽선을 찾음
cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
cnts = imutils.grab_contours(cnts)

# 문제의 윤곽선을 정렬
questionCnts = contours.sort_contours(cnts, method="top-to-bottom")[0]

# 각 문제에 대해 가장 많은 픽셀이 마킹된 영역을 찾음
for (q, i) in enumerate(np.arange(0, len(questionCnts), 5)):
    tmp = contours.sort_contours(questionCnts[i:i + 5])[0]
    bubbled = None
    for (j, c) in enumerate(tmp):
        mask = np.zeros(thresh.shape, dtype="uint8")
        cv2.drawContours(mask, [c], -1, 255, -1)
        mask = cv2.bitwise_and(thresh, thresh, mask=mask)
        total = cv2.countNonZero(mask)
        if bubbled is None or total > bubbled[0]:
            bubbled = (total, j)
    color = (0, 0, 255)
    cv2.drawContours(paper, [tmp[bubbled[1]]], -1, color, 3)

# 결과를 출력
cv2.imshow("OMR Test", paper)
cv2.waitKey(0)





