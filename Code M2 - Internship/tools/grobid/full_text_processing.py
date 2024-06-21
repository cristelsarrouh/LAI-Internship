import os
import pandas as pd
from bs4 import BeautifulSoup
import re
import sys

def read_tei(tei_file):
    with open(tei_file, 'r', encoding='utf-8') as tei:
        soup = BeautifulSoup(tei, 'xml')  # Use 'xml' parser for XML files
        return soup

def preprocess_paragraph(paragraph):
    # Remove text within angle brackets
    return re.sub(r'<[^>]*>', '', paragraph)

def count_words(paragraph):
    # Split paragraph into words and count
    words = paragraph.split()
    return len(words)

def process_xml_file(xml_file):
    try:
        # Read the XML file
        soup = read_tei(xml_file)

        # Extract all <div> elements inside the <body> element
        body_elem = soup.find('body')
        if body_elem:
            div_elements = body_elem.find_all('div')

            # Initialize dictionary to store data
            data_dict = {}
            total_word_count = 0  # Initialize total word count

            for div_element in div_elements:
                # Extract text from <head> element
                header_elem = div_element.find('head')
                header_text = header_elem.text if header_elem else None

                # Extract all content after the <head> tag within the <div> element
                paragraph = ''
                for element in div_element.children:
                    if element.name == 'p':
                        paragraph += str(element)

                # Preprocess paragraph
                cleaned_paragraph = preprocess_paragraph(paragraph)

                # Count words
                word_count = count_words(cleaned_paragraph)

                # Associate header with paragraph and word count
                if header_text:
                    data_dict[header_text] = {'Paragraph': paragraph, 'Word Count': word_count}
                    total_word_count += word_count  # Accumulate total word count

            # Print total word count
            print(f"Total Number of Words: {total_word_count}")

            return data_dict

    except Exception as e:
        print(f"Error processing '{xml_file}': {e}")
        return None

def print_and_write_to_file(text, output_file, is_first_paragraph=False):
    if not is_first_paragraph and text.strip():  # Check if it's not the first paragraph and if text is not empty
        print("")  # Print empty line to separate paragraphs in console
        with open(output_file, 'a', encoding='utf-8') as f:  # Append mode to not overwrite previous content
            f.write('\n')  # Write empty line to separate paragraphs in file
    if text.strip():  # Check if text is not empty
        print(text)  # Print to console
        with open(output_file, 'a', encoding='utf-8') as f:  # Append mode to not overwrite previous content
            f.write(text + '\n')  # Write to file

# Path of the XML file to process
xml_file_path = r'C:\Users\phpue\Desktop\cristel\PycharmProjects\Internship\xml_extractions\10.1016_j.bpj.2014.06.015.xml_extractions.tei.xml'

# Process the XML file
xml_data = process_xml_file(xml_file_path)
if xml_data:
    output_file = "grobid.txt"  # Define the output file path
    with open(output_file, 'w', encoding='utf-8') as f:  # Clear the file content
        pass  # Do nothing, just to clear the file content
    is_first_paragraph = True
    for header, info in xml_data.items():
        paragraph = info['Paragraph']
        word_count = info['Word Count']
        cleaned_paragraph = preprocess_paragraph(paragraph)  # Clean paragraph
        print_and_write_to_file(f"Word Count: {word_count}", output_file, is_first_paragraph)
        print_and_write_to_file(f"Header: {header}", output_file)
        print_and_write_to_file(f"Paragraph: {cleaned_paragraph}", output_file)  # Print cleaned paragraph
        is_first_paragraph = False
else:
    print("Failed to process XML file.")
