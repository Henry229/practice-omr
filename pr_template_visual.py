import cv2
import matplotlib.pyplot as plt

def draw_bubble_block_on_image(image, field, details, bubble_dimensions):
    origin_x, origin_y = details["origin"]
    bubble_w, bubble_h = bubble_dimensions
    field_type = details["fieldType"]
    bubbles_gap = details["bubblesGap"]
    labels_gap = details["labelsGap"]
    
    # Determine the number of choices based on fieldType
    if "QTYPE_MCQ" in field_type:
        num_choices = int(field_type[-1])
    elif field_type == "QTYPE_INT":
        num_choices = 10

    # Determine the orientation (horizontal or vertical) based on fieldType
    if field_type == "QTYPE_INT":
        orientation = "vertical"
    else:
        orientation = "horizontal"
    
    # For blocks like "Math_Block_Q1", we should check the range in "fieldLabels" and iterate over it
    field_label = details["fieldLabels"][0]
    if ".." in field_label:
        start_label, end_label = field_label.split("..")
        start = int("".join([char for char in start_label if char.isdigit()]))
        end = int("".join([char for char in end_label if char.isdigit()]))
    else:
        start, end = 1, 1
    
    # Draw each bubble
    for question_num in range(start, end + 1):
        for choice_index in range(num_choices):
            if orientation == "horizontal":
                top_left = (
                    int(origin_x + choice_index * bubbles_gap),
                    int(origin_y + (question_num - start) * labels_gap)
                )
            else:  # vertical
                top_left = (
                    int(origin_x + (question_num - start) * labels_gap),
                    int(origin_y + choice_index * bubbles_gap)
                )
            bottom_right = (
                int(top_left[0] + bubble_w),
                int(top_left[1] + bubble_h)
            )
            cv2.rectangle(image, top_left, bottom_right, (0, 0, 255), 2)
                
    return image

# Visualize the blocks on the image
omr_image_with_blocks = omr_image.copy()

# Draw standard blocks
for field, details in template_data["fieldBlocks"].items():
    if "Math_Block" in field or "Thinking_Block" in field:
        omr_image_with_blocks = draw_bubble_block_on_image(omr_image_with_blocks, field, details, template_data["bubbleDimensions"])

plt.figure(figsize=(12, 20))
plt.imshow(cv2.cvtColor(omr_image_with_blocks, cv2.COLOR_BGR2RGB))
plt.axis('off')
plt.show()

# 새로 바꾼 소스 
# import cv2
# import matplotlib.pyplot as plt

# def draw_bubble_block_on_image_modified(image, field, details, bubble_dimensions):
#     origin_x, origin_y = details["origin"]
#     bubble_w, bubble_h = bubble_dimensions
#     field_type = details["fieldType"]
#     bubbles_gap = details["bubblesGap"]
#     labels_gap = details["labelsGap"]
    
#     # Determine the number of choices based on fieldType
#     if "QTYPE_MCQ" in field_type:
#         num_choices = int(field_type[-1])
#     elif field_type == "QTYPE_INT":
#         num_choices = 10

#     # Determine the orientation (horizontal or vertical) based on fieldType
#     if field_type == "QTYPE_INT":
#         orientation = "vertical"
#     else:
#         orientation = "horizontal"
    
#     # For blocks like "Math_Block_Q1", we should check the range in "fieldLabels" and iterate over it
#     field_label = details["fieldLabels"][0]
#     if ".." in field_label:
#         start_label, end_label = field_label.split("..")
#         start = int("".join([char for char in start_label if char.isdigit()]))
#         end = int("".join([char for char in end_label if char.isdigit()]))
#     else:
#         start, end = 1, len(details["fieldLabels"])
    
#     # Draw each bubble
#     for question_num in range(start, end + 1):
#         for choice_index in range(num_choices):
#             if orientation == "horizontal":
#                 top_left = (
#                     int(origin_x + choice_index * bubbles_gap),
#                     int(origin_y + (question_num - start) * labels_gap)
#                 )
#             else:  # vertical
#                 top_left = (
#                     int(origin_x + (question_num - start) * labels_gap),
#                     int(origin_y + choice_index * bubbles_gap)
#                 )
#             bottom_right = (
#                 int(top_left[0] + bubble_w),
#                 int(top_left[1] + bubble_h)
#             )
#             cv2.rectangle(image, top_left, bottom_right, (0, 0, 255), 2)
                
#     return image

# # Load the image
# omr_image = cv2.imread("/mnt/data/Math-Thinking-NSW.jpeg")

# # Visualize the blocks on the image using the modified function
# omr_image_with_blocks_modified = omr_image.copy()

# # Draw all blocks using the defined template_data
# for field, details in template_data["fieldBlocks"].items():
#     omr_image_with_blocks_modified = draw_bubble_block_on_image_modified(omr_image_with_blocks_modified, field, details, template_data["bubbleDimensions"])

# # Display the image
# plt.figure(figsize=(12, 20))
# plt.imshow(cv2.cvtColor(omr_image_with_blocks_modified, cv2.COLOR_BGR2RGB))
# plt.axis('off')
# plt.show()

