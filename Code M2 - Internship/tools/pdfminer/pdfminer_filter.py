import os
import re

def process_text(text):
    # Split the text into paragraphs
    paragraphs = text.split('\n\n')

    # Iterate through paragraphs
    delete_flag = False
    new_paragraphs = []
    for paragraph in paragraphs:
        # If the delete flag is set, skip this paragraph
        if delete_flag:
            # Check if the paragraph has at least four lines
            if paragraph.strip().count('\n') >= 3:
                delete_flag = False
            continue

        # Check if the paragraph contains the trigger phrase
        if 'TABLE ' in paragraph and any(char.isdigit() for char in paragraph):
            # Set the delete flag to True
            delete_flag = True
            continue

        # Check if the paragraph contains the stop phrase
        if paragraph.strip().startswith('the highest resolution structure was used.'):
            # Reset the delete flag
            delete_flag = False

        # Append the paragraph to new_paragraphs
        new_paragraphs.append(paragraph)

    # Join the remaining paragraphs
    result = '\n\n'.join(new_paragraphs)
    return result

def count_words(text):
    # Split the text into words
    words = re.findall(r'\b\w+\b', text)
    # Count the total number of words
    word_count = len(words)
    return word_count

def extract_material_and_methods(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        material_and_methods_section = []
        capturing = False
        skip_paragraph = False
        for line in file:
            line_lower = line.strip().lower()  # Convert line to lowercase for case-insensitive comparison
            # Check if "et al." is in the line and it's a short sentence
            words = line_lower.split()
            if "et al." in line_lower and len(words) < 5:  # Adjust the threshold as needed
                continue  # Skip this line and move to the next iteration
            # Remove lines containing only digits
            if re.match(r'^\d+$', line_lower):
                continue
            # Remove lines containing "biophysical journal"
            if "biophysical journal" in line_lower:
                continue
            # Remove lines matching the pattern like "Volume 75 November 1998"
            if re.search(r'volume\s+\d+\s+[a-zA-Z]+\s+\d+', line_lower):
                continue
            # Check for lines containing "FIGURE" followed by a number
            if re.search(r'figure\s+\d+', line_lower):
                skip_paragraph = True
                continue
            # Stop skipping paragraphs when reaching an empty line
            if skip_paragraph and not line.strip():
                skip_paragraph = False
                continue
            # Add a regular expression pattern to match all three patterns
            if "materials and methods" in line_lower and line_lower.strip() == "materials and methods":
                capturing = True
            elif ("results and discussion" in line_lower and line_lower.strip() == "results and discussion") or ("results" in line_lower and line_lower.strip() == "results"):
                capturing = False
                break  # Stop capturing when "Results" or "Results and Discussion" is found
            if capturing and not skip_paragraph:
                material_and_methods_section.append(line)
    # Process the extracted material and methods section
    processed_text = process_text(''.join(material_and_methods_section))
    return processed_text

def extract_from_directory(directory_path):
    extracted_texts = {}
    for file_name in os.listdir(directory_path):
        if file_name.endswith('.manually'):
            file_path = os.path.join(directory_path, file_name)
            extracted_text = extract_material_and_methods(file_path)
            extracted_texts[file_name] = extracted_text
    return extracted_texts

# Example usage:
directory_path = '../journals/biophysical journal/pdfminer_txt'  # Provide the path to your directory containing the manually files
extracted_texts = extract_from_directory(directory_path)
for file_name, text in extracted_texts.items():
    word_count = count_words(text)
    print(f"Extracted text from '{file_name}':\n{text}\n")
    print(f"Total number of words in '{file_name}': {word_count}\n")
