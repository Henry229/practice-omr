import json
from  pr_sel_MT_block_info import sel_MT_block_data

# Calculate the coordinates for each bubble based on the template.json

bubble_coordinates = {}

for field, details in sel_MT_block_data["fieldBlocks"].items():
    field_coordinates = []
    
    bubble_w, bubble_h = sel_MT_block_data["bubbleDimensions"]
    origin_x, origin_y = details["origin"]
    field_type = details["marking_direction"]
    bubbles_gap = details["bubblesGap"]
    labels_gap = details["labelsGap"]
    
    # Determine the number of choices based on fieldType
    num_choices = details["num_of_selection"]

    # Determine the orientation (horizontal or vertical) based on fieldType
    if field_type == "V":
        orientation = "vertical"
    else:
        orientation = "horizontal"
    
    # Check for the range in "fieldLabels" and iterate over it for blocks like "Math_Block_Q1"
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