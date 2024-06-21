import os
import xml.etree.ElementTree as ET

def extract_references(xml_file):
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

            if bibl_id in references_dict:
                references_dict[bibl_id].append({
                    'raw_reference': raw_reference,
                    'journal_title': journal_title,
                    'dois': dois
                })
            else:
                references_dict[bibl_id] = [{
                    'raw_reference': raw_reference,
                    'journal_title': journal_title,
                    'dois': dois
                }]

        return references_dict

    except FileNotFoundError:
        print(f"Error: XML file not found - {xml_file}")
        return {}
    except ET.ParseError:
        print(f"Error: Unable to parse the XML file - {xml_file}")
        return {}

def print_references(references_dict):
    for bibl_id, references in references_dict.items():
        print(f"ID: {bibl_id}")
        for reference in references:
            print(f"  Raw Reference: {reference['raw_reference']}")
            print(f"  DOI: {', '.join(reference['dois'])}")
            print(f"  Journal Title: {reference['journal_title']}")
            print()

# Usage for a single XML file
xml_file_path = "/home/php/PycharmProjects/Internship/xml_extractions/light_image/xml_references/10.1016_j.bpj.2014.10.044.pdf.tei.xml"
references_dict = extract_references(xml_file_path)
print_references(references_dict)
