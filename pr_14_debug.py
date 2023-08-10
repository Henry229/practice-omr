import cv2
import numpy as np
from block_info_module import block_info

def visualize_student_no_block(image_path, block_info):
    image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    x, y, w, h = block_info['x'], block_info['y'], block_info['width'], block_info['height']
    block_image = image[y:y+h, x:x+w]
    cv2.imshow('Student No Block', block_image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

# Visualizing 'Student No' block
block_to_visualize = [block for block in block_info if block['name'] == 'Student No'][0]
visualize_student_no_block("/Users/henry/Downloads/Math-Thinking-NSW.jpeg", block_to_visualize)