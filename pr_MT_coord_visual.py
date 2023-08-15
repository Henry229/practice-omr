import cv2
import numpy as np
from  pr_sel_MT_block_info import sel_MT_block_data
from matplotlib import pyplot as plt

# Load the image
image_path = "/Users/henry/Downloads/Math-Thinking-NSW.jpg"
image = cv2.imread(image_path)
image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

# Using the provided sel_MT_block_data to calculate bubble coordinates
bubble_coordinates = {}

for field, details in sel_MT_block_data["fieldBlocks"].items():
    field_coordinates = []
    
    bubble_w, bubble_h = sel_MT_block_data["bubbleDimensions"]
    origin_x, origin_y = details["origin"]
    field_type = details["marking_direction"]
    bubbles_gap = details["bubblesGap"]
    labels_gap = details["labelsGap"]
    num_choices = details["num_of_selection"]

    # Determine the orientation based on marking_direction
    orientation = "vertical" if field_type == "V" else "horizontal"
    
    # Check for the range in "fieldLabels" 
    field_label = details["num_of_question"]
    start = int(details.get('StartingQuestion', 1))
    end = int(details.get('EndingQuestion', field_label))
    
    # Calculate coordinates for each bubble
    for question_num in range(start, end + 1):
        for choice_index in range(num_choices):
            if orientation == "horizontal":
                top_left = (
                    int(origin_x + choice_index * bubbles_gap),
                    int(origin_y + (question_num - start) * labels_gap)
                )
            else:
                top_left = (
                    int(origin_x + (question_num - start) * labels_gap),
                    int(origin_y + choice_index * bubbles_gap)
                )
            bottom_right = (
                int(top_left[0] + bubble_w),
                int(top_left[1] + bubble_h)
            )
            field_coordinates.append({
                "top_left": top_left,
                "bottom_right": bottom_right
            })
    
    bubble_coordinates[field] = field_coordinates

# Draw the calculated coordinates on the image
for field, coords in bubble_coordinates.items():
    for coord in coords:
        top_left = tuple(coord["top_left"])
        bottom_right = tuple(coord["bottom_right"])
        cv2.rectangle(image, top_left, bottom_right, (255, 0, 0), 2)

# Display the image
plt.figure(figsize=(10, 15))
plt.imshow(image)
plt.axis('off')
plt.show()
