import os
import xml.etree.ElementTree as ET
import re

def extract_references_from_xml(xml_file):
    ns = {'ns0': 'http://www.tei-c.org/ns/1.0'}
    references_dict = {}

    try:
        tree = ET.parse(xml_file)
        root = tree.getroot()

        for biblStruct in root.findall('.//ns0:biblStruct', namespaces=ns):
            bibl_id = biblStruct.get('{http://www.w3.org/XML/1998/namespace}id')  # Extract xml:id
            raw_reference_element = biblStruct.find('.//ns0:note[@type="raw_reference"]', namespaces=ns)
            raw_reference = raw_reference_element.text if raw_reference_element is not None else None

            journal_title_element = biblStruct.find('.//ns0:monogr/ns0:title[@level="j"]', namespaces=ns)
            journal_title = journal_title_element.text if journal_title_element is not None else None

            doi_elements = biblStruct.findall('.//ns0:idno[@type="DOI"]', namespaces=ns)
            dois = [doi_element.text for doi_element in doi_elements]

            references_dict[bibl_id] = {
                'raw_reference': raw_reference,
                'journal_title': journal_title,
                'dois': dois
            }

        return references_dict

    except FileNotFoundError:
        print(f"Error: XML file not found - {xml_file}")
        return {}
    except ET.ParseError:
        print(f"Error: Unable to parse the XML file - {xml_file}")
        return {}

def extract_references_from_text(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()
    except FileNotFoundError:
        print(f"File '{file_path}' not found.")
        return None

    # Extract all <ref> tags and their content
    references = re.findall(r'<ref.*?</ref>', content, re.DOTALL)
    return references

def match_references(text_references, xml_references):
    matched_references = []

    for ref in text_references:
        # Extract the ID from the reference tag
        match = re.search(r'target="#(b\d+)"', ref)
        if match:
            ref_id = match.group(1)
            if ref_id in xml_references:
                matched_references.append((ref_id, xml_references[ref_id], ref))

    return matched_references

def print_matched_references(matched_references):
    reference_numbers = {}

    with open("PHP/Third/doi/dois_4.txt", "w") as doi_file:
        for index, (ref_id, xml_ref, text_ref) in enumerate(matched_references, start=1):
            # Extract the reference number (ID number + First)
            reference_number = str(int(ref_id[1:]) + 1)  # Assuming ID format like bXX
            reference_numbers[ref_id] = reference_number

            print(f"This is what the matched reference {index} looks like:")
            print(f"Text Reference: {text_ref}")
            print(f"Reference Number: {reference_number}")
            print(f"  ID: {ref_id}")
            print(f"  Raw Reference: {xml_ref['raw_reference']}")
            print(f"  DOI: {', '.join(xml_ref['dois'])}")
            print(f"  Journal Title: {xml_ref['journal_title']}")
            print()

            # Write DOIs to file, each on a new line
            for doi in xml_ref['dois']:
                doi_file.write(f"{doi}\n")

    print("DOIs extracted and saved to dois_1.txt.")
    print(f"Total number of matched references: {len(matched_references)}")
    return reference_numbers

def identify_duplicate_references(matched_references, reference_numbers):
    reference_counts = {}
    duplicate_references = {}

    # Count occurrences of each reference ID
    for ref_id, _, _ in matched_references:
        if ref_id in reference_counts:
            reference_counts[ref_id] += 1
        else:
            reference_counts[ref_id] = 1

    # Identify references cited more than once
    for ref_id, count in reference_counts.items():
        reference_number = reference_numbers.get(ref_id, "Unknown")
        if count > 1:
            duplicate_references[reference_number] = count

    return duplicate_references

def main():
    # xml_file_path = r"C:\Users\phpue\Desktop\cristell\LLM application\First\10.1529_biophysj.108.135491.pdf.tei.xml"
    # text_file_path = r"C:\Users\phpue\Desktop\cristell\LLM application\First\outputs\10.1529_biophysj.108.135491.pdf.tei_with_tags.txt"

    xml_file_path = r"C:\Users\phpue\Desktop\cristell\LLM application\PHP\Second\grobid_output\10.1126_stke.4062007pl5.pdf.tei.xml"
    text_file_path = r"C:\Users\phpue\Desktop\cristell\LLM application\PHP\Second\grobid_txt\10.1126_stke.4062007pl5.pdf.tei_with_tags.txt"

    # Process XML file
    xml_references = extract_references_from_xml(xml_file_path)

    # Process text file
    text_references = extract_references_from_text(text_file_path)

    # Match references
    matched_references = match_references(text_references, xml_references)

    # Print matched references to a text file and get reference numbers
    reference_numbers = print_matched_references(matched_references)

    # Identify duplicate references and print their reference numbers and counts
    duplicate_references = identify_duplicate_references(matched_references, reference_numbers)
    if duplicate_references:
        print("Reference numbers of citations cited more than once and how many times:")
        for ref_number, count in duplicate_references.items():
            print(f"- Reference number {ref_number}: {count} times")
    else:
        print("No citations cited more than once.")

if __name__ == "__main__":
    main()
