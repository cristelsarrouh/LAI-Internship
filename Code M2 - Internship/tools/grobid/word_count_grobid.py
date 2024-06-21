import os
import pandas as pd
from bs4 import BeautifulSoup

def calculate_word_count(csv_file):
    try:
        # Read the CSV file
        df = pd.read_csv(csv_file)

        # Initialize total word count
        total_word_count = 0

        # Calculate word count for each section
        for index, row in df.iterrows():
            header = row['Header'] if pd.notna(row['Header']) else ''
            paragraph = row['Paragraph'] if pd.notna(row['Paragraph']) else ''
            section_text = header + ' ' + paragraph

            # Remove HTML tags
            section_text = BeautifulSoup(section_text, 'html.parser').get_text()

            words = section_text.split()
            section_word_count = len(words)
            total_word_count += section_word_count

        return total_word_count

    except Exception as e:
        print(f"Error processing '{csv_file}': {e}")
        return 0

def count_words_in_sections(directory):
    total_word_count_all_files = 0

    # Iterate over CSV files in the directory
    for filename in os.listdir(directory):
        if filename.endswith('.csv'):
            csv_file_path = os.path.join(directory, filename)
            total_word_count_file = calculate_word_count(csv_file_path)
            total_word_count_all_files += total_word_count_file
            print(f"Total word count in '{filename}': {total_word_count_file}")

    print(f"Total word count in all files: {total_word_count_all_files}")

# Directory containing CSV files
csv_directory = r'C:\Users\phpue\Desktop\cristel\PycharmProjects\Internship\grobid\xml_section_extraction'

# Call the function to count words in sections
count_words_in_sections(csv_directory)
