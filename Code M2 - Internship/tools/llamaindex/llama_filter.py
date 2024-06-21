import os
import re

def extract_section(text, start_headers, end_headers):
    if isinstance(start_headers, str):
        start_headers = [start_headers]

    start_pattern = "|".join(re.escape(header) for header in start_headers)

    end_pattern = "|".join(re.escape(header) for header in end_headers)

    # Construct the regular expression pattern to find the section
    pattern = re.compile(
        rf"(?s)<(?:h\d+|p)>(?:{start_pattern})<\/(?:h\d+|p)>(.*?)"
        rf"(?=<(?:h\d+|p)>(?:{end_pattern})<\/(?:h\d+|p)>|$)",
        re.IGNORECASE | re.DOTALL
    )

    match = pattern.search(text)

    if match:
        section_content = match.group(1)
        section_content = re.sub(r"<table[^>]*>.*?<\/table>", "", section_content, flags=re.IGNORECASE | re.DOTALL)
        section_content = re.sub(r"<p[^>]*>\s*Figure.*?<\/p>", "", section_content, flags=re.IGNORECASE | re.DOTALL)
        return section_content.strip()

    return None

def count_words(text):
    text_without_tags = re.sub(r"<[^>]+>", "", text)
    words = re.findall(r"\b\w+\b", text_without_tags)
    return len(words)

# Define possible start headers
# possible_start_headers = ["Experimental procedures", "STAR+METHODS", "EXPERIMENTAL MODEL AND SUBJECT DETAILS", "METHOD DETAILS","EXPERIMENTAL MODEL AND SUBJECT DETAILS"]
possible_start_headers = ["Methods", "Materials and Methods","Materials and Methods", "Experimental section", "Experimental" ]

# Define the directory containing the text files
input_directory = r'C:\Users\phpue\Desktop\cristel\PycharmProjects\Text_extraction\llama_txt'
output_directory = r'C:\Users\phpue\Desktop\cristel\PycharmProjects\Text_extraction'

# Create the output directory if it doesn't exist
os.makedirs(output_directory, exist_ok=True)

# Iterate over each file in the input directory
for filename in os.listdir(input_directory):
    if filename.endswith('.txt'):
        file_path = os.path.join(input_directory, filename)
        with open(file_path, 'r', encoding='utf-8') as file:
            text_content = file.read()

        # Extract section from any of the possible start headers to "<p> REFERENCES AND NOTES"
        materials_and_methods_section = extract_section(text_content, possible_start_headers, ["Results and discussion", "results", "Acknowledgements" ])

        if materials_and_methods_section:
            word_count = count_words(materials_and_methods_section)

            output_filename = f"{os.path.splitext(filename)[0]}_output.txt"
            output_file_path = os.path.join(output_directory, output_filename)

            with open(output_file_path, 'w', encoding='utf-8') as output_file:
                output_file.write(f"File: {filename}\n")
                output_file.write("Content of MATERIALS AND METHODS section:\n")
                output_file.write(materials_and_methods_section + "\n")
                output_file.write(f"\nWord count (excluding HTML tags): {word_count}\n")

            print(f"Processed and saved output for {filename}")
        else:
            print(f"MATERIALS AND METHODS section not found in {filename}")
