import cv2
import numpy as np
from block_info_module import block_info

def recognize_answers(image_path, block_info):
    # 이미지를 불러옵니다.
    img = cv2.imread(image_path)
    # 각 블록에 대해 반복합니다.
    for block in block_info:
        # 블록의 좌표를 가져옵니다.
        x, y, w, h = block['x'], block['y'], block['width'], block['height']

        # 이미지에서 블록을 분리합니다.
        block_img = img[y:y+h, x:x+w]

        # 블록 이미지를 그레이스케일로 변환합니다.
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        # 이미지를 이진화합니다.
        _, binary = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY_INV)

        # 컨투어를 찾습니다.
        contours, _ = cv2.findContours(binary, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        # 각 컨투어에 대해 반복합니다.
        for contour in contours:
            # 컨투어의 영역을 계산합니다.
            area = cv2.contourArea(contour)

            # 영역이 일정 크기 이상인 경우, 해당 컨투어를 답안으로 판단합니다.
            if area > 50:
                # 답안의 위치를 계산합니다.
                M = cv2.moments(contour)
                cX = int(M["m10"] / M["m00"])
                cY = int(M["m01"] / M["m00"])

                # 답안의 번호를 계산합니다.
                answer = cY // (h // block['num_of_selection'])

                # 답안을 출력합니다.
                print(f"Block '{block['name']}' answer: {answer}")
                
def visualize_blocks(image_path, block_info):
    # 이미지를 불러옵니다.
    img = cv2.imread(image_path)

    # 각 블록에 대해 반복합니다.
    for block in block_info:
        # 블록의 좌표를 가져옵니다.
        x, y, w, h = block['x'], block['y'], block['width'], block['height']

        # 이미지에 블록의 영역을 그립니다.
        cv2.rectangle(img, (x, y), (x+w, y+h), (0, 255, 0), 2)

    # 블록이 그려진 이미지를 반환합니다.
    return img
  
def preprocess_image(image_path):
    # 이미지를 불러옵니다.
    img = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)

    # 노이즈를 제거합니다. (옵션)
    img = cv2.medianBlur(img, 5)

    # 이미지를 이진화합니다. adaptive thresholding을 사용합니다.
    img = cv2.adaptiveThreshold(img, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2)

    # 이진화된 이미지를 반환합니다.
    return img  

# 이미지 경로와 블록 정보를 제공합니다.
image_path = '/Users/henry/Downloads/Math-Thinking-NSW.jpeg'
# 블록 영역을 시각화하고 결과를 저장합니다.
# img = visualize_blocks(image_path, block_info)
# cv2.imshow('block', img)
# cv2.waitKey(0)
# cv2.destroyAllWindows()

preprocessed_img = preprocess_image(image_path)

recognize_answers(image_path, block_info)
