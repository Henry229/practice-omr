def extract_block_from_image(image, block):
    """Extracts a specific block region from the given image."""
    return image[block['y']:block['y']+block['height'], block['x']:block['x']+block['width']]

def recognize_block_data(image, block, direction):
    """Recognizes data from the given block in the image."""
    if direction == 'V':
        return recognize_test_info(image, block, recognize_func=recogize_marking_circular)
    else:
        return horizontal_block_image(image_path, block), None, None

def update_test_data(block, answers, recognized_numbers, test_data):
    """Updates the test data dictionary based on recognized block data."""
    block_name = block['name']
    direction = block['marking_direction']
    
    if direction == 'V':
        if block_name in ['Student No', 'Test Type', 'Test Subj', 'Test Level1', 'Test Level2', 'Test No', 'Branch No']:
            concatenated_value = ''.join([str(recognized_numbers[answers.index(answer)]) for answer in answers if answer[0] < block['num_of_question']])
            test_data[block_name] = concatenated_value
        else:
            answers_list = []
            if 'StartingQuestion' in block:
                starting_question = int(block['StartingQuestion'])
                for local_q_num, ans in answers.items():
                    global_q_num = local_q_num + starting_question - 1
                    answers_list.append((global_q_num, ans))
            test_data[f'Answer_{block_name}'] = answers_list
    else:
        if block_name in ['Student No', 'Test Type', 'Test Subj', 'Test Level1', 'Test Level2', 'Test No', 'Branch No']:
            test_data[block_name] = str(answers.get(1, ''))
        else:
            answers_list = []
            if 'StartingQuestion' in block:
                starting_question = int(block['StartingQuestion'])
                for local_q_num, ans in answers.items():
                    global_q_num = local_q_num + starting_question - 1
                    answers_list.append((global_q_num, ans))
            test_data[f'Answer_{block_name}'] = answers_list

def process_image(image_path):
    """Processes the given image and returns the recognized test data."""
    image = cv2.imread(image_path)
    preprocessed_image = general_preprocess(image)
    
    test_data = {}
    
    for block in block_info:
        block_image = extract_block_from_image(preprocessed_image, block)
        answers, recognized_numbers, _ = recognize_block_data(block_image, block, block['marking_direction'])
        update_test_data(block, answers, recognized_numbers, test_data)
    
    return test_data

# Process the image using the refactored code
refactored_output = process_image(image_path)
refactored_output
