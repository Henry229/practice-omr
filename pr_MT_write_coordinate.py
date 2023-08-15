import json
from  pr_sel_MT_block_info import sel_MT_block_data

# Calculate the coordinates for each bubble based on the template.json

bubble_coordinates = {}

for field, details in sel_MT_block_data["fieldBlocks"].items():
    field_coordinates = []
    
    origin_x, origin_y = details["origin"]
    bubble_w, bubble_h = sel_MT_block_data["bubbleDimensions"]
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
    
    # Check for the range in "fieldLabels" and iterate over it for blocks like "Math_Block_Q1"
    field_label = details["fieldLabels"][0]
    if ".." in field_label:
        start_label, end_label = field_label.split("..")
        start = int("".join([char for char in start_label if char.isdigit()]))
        end = int("".join([char for char in end_label if char.isdigit()]))
    else:
        start, end = 1, len(details["fieldLabels"])
    
    # Calculate coordinates for each bubble
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
            field_coordinates.append({
                "top_left": top_left,
                "bottom_right": bottom_right
            })
    
    bubble_coordinates[field] = field_coordinates

# Save the calculated coordinates to a JSON file
bubble_coordinates_filepath = "/Users/henrychun/Downloads/selective_Math_Thinking_coordinates.json"
with open(bubble_coordinates_filepath, 'w') as file:
    json.dump(bubble_coordinates, file, indent=4)

bubble_coordinates_filepath