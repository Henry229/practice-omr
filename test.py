# import cv2
# import numpy as np

# def recognize_omr(image_path, omr_definition):
#     # 이미지 읽기
#     image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)

#     # 전처리: GaussianBlur
#     pre_processor = omr_definition['preProcessors'][0]
#     if pre_processor['name'] == 'GaussianBlur':
#         kSize = tuple(pre_processor['options']['kSize'])
#         sigmaX = pre_processor['options']['sigmaX']
#         image = cv2.GaussianBlur(image, kSize, sigmaX)

#     # 결과를 저장할 딕셔너리
#     results = {}

#     # 각 필드 블록에 대한 버블 인식
#     for field, details in omr_definition['fieldBlocks'].items():
#         origin_x, origin_y = details['origin']
#         bubbles_gap = details['bubblesGap']
#         bubble_width, bubble_height = omr_definition['bubbleDimensions']

#         field_results = []

#         for idx, label in enumerate(details['fieldLabels']):
#             x = origin_x + idx * details['labelsGap']
#             y = origin_y

#             # 버블 영역 추출
#             bubble_area = image[y:y+bubble_height, x:x+bubble_width]

#             # 버블 내부의 픽셀 값 평균 계산
#             mean_val = np.mean(bubble_area)

#             # 픽셀 값 평균이 임계값보다 낮으면 마킹으로 판단 (임계값은 조정이 필요)
#             if mean_val < 128:
#                 field_results.append(label)

#         results[field] = field_results

#     return results

# # 주어진 JSON 파일을 파이썬 딕셔너리로 변환
# omr_definition = {
#     "pageDimensions": [1169, 1654],
#     "bubbleDimensions": [18, 18],
#     "preProcessors": [
#         {
#             "name": "GaussianBlur",
#             "options": {
#                 "kSize": [3, 3],
#                 "sigmaX": 0
#             }
#         }
#     ],
#     # ... (나머지 JSON 내용)
# }

# # 예제 사용
# image_path = "path_to_your_image.jpg"
# print(recognize_omr(image_path, omr_definition))

import cv2
import numpy as np
import matplotlib.pyplot as plt

def preprocess_image_for_recognition(image):
    # 1. Gaussian blur
    blurred = cv2.GaussianBlur(image, (5, 5), 0)
    
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
                field_answers.append(1)
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

# Load image
omr_image = cv2.imread('/mnt/data/Math-Thinking-NSW.jpeg')

# Preprocess the image
preprocessed_image = preprocess_image_for_recognition(omr_image)

# Recognize marked answers using the pre-processed image
marked_answers = recognize_marked_answers_using_pixel_ratio(preprocessed_image, loaded_bubble_coordinates, template_data["bubbleDimensions"], threshold_ratio=0.75)

# Visualize the correctly marked answers on the original image
visualized_image_with_correct_markings = visualize_correct_marked_answers(omr_image, loaded_bubble_coordinates, template_data["bubbleDimensions"], marked_answers)

# Show the visualized image
plt.figure(figsize=(12, 20))
plt.imshow(cv2.cvtColor(visualized_image_with_correct_markings, cv2.COLOR_BGR2RGB))
plt.axis('off')
plt.show()


[
    {
        "student": "15990005",
        "Test_Type": "Selective_Trial_Test",
        "Test_Subj": ["Maths", "GA"],
        "Test_Level1": "Year5",
        "Test_Level2": "",
        "Test_No": "07",
        "Brnach_No": "22"
     }
]

0100000000
0000010000
0000000001
0000000001
1000000000
1000000000
1000000000
0000010000
