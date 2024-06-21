import os
import csv
import xml.etree.ElementTree as ET
from collections import Counter


def extract_journals(xml_file):
    ns = {'ns0': 'http://www.tei-c.org/ns/1.0'}
    journals = []

    try:
        tree = ET.parse(xml_file)
        root = tree.getroot()

        for biblStruct in root.findall('.//ns0:biblStruct', namespaces=ns):
            journal_title_element = biblStruct.find('.//ns0:monogr/ns0:title[@level="j"]', namespaces=ns)
            journal_title = journal_title_element.text if journal_title_element is not None else None

            if journal_title:
                journals.append(journal_title)

        return journals

    except FileNotFoundError:
        print(f"Error: XML file not found - {xml_file}")
        return []
    except ET.ParseError:
        print(f"Error: Unable to parse the XML file - {xml_file}")
        return []


def count_and_save_journals(directory_paths):
    all_journals = []
    individual_occurrences = {}

    # Create the 'journal_occurrences' directory if it doesn't exist
    output_directory = 'journal_occurrences'
    os.makedirs(output_directory, exist_ok=True)

    for directory_path in directory_paths:
        for filename in os.listdir(directory_path):
            if filename.endswith(".xml"):
                xml_file_path = os.path.join(directory_path, filename)
                journals = extract_journals(xml_file_path)
                all_journals.extend(journals)

                # Count occurrences for each individual XML file
                individual_occurrences[filename] = Counter(journals)

    # Count total occurrences across all XML files
    total_occurrences = Counter(all_journals)

    # Sort occurrences in descending order
    sorted_total_occurrences = dict(sorted(total_occurrences.items(), key=lambda item: item[1], reverse=True))

    # Save total occurrences to CSV file
    total_output_csv = os.path.join(output_directory, 'total_journal_occurrences.csv')
    with open(total_output_csv, 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['Journal Title', 'Occurrences']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()

        for journal, count in sorted_total_occurrences.items():
            writer.writerow({'Journal Title': journal, 'Occurrences': count})

    print(f"Total CSV file '{total_output_csv}' created successfully.")

    # Save individual occurrences to CSV files
    for filename, occurrences in individual_occurrences.items():
        sorted_individual_occurrences = dict(sorted(occurrences.items(), key=lambda item: item[1], reverse=True))
        individual_output_csv = os.path.join(output_directory,
                                             f'individual_journal_occurrences_{os.path.splitext(filename)[0]}.csv')

        with open(individual_output_csv, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()

            for journal, count in sorted_individual_occurrences.items():
                writer.writerow({'Journal Title': journal, 'Occurrences': count})

        print(f"Individual CSV file '{individual_output_csv}' created successfully.")


# Example usage for two directories
xml_directory_paths = [r'C:\Users\phpue\Desktop\cristel\PycharmProjects\Internship\grobid\xml_references']
count_and_save_journals(xml_directory_paths)
