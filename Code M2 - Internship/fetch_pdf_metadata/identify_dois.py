import os
import xml.etree.ElementTree as ET

def extract_and_write_dois(directory_paths, output_file):
    ns = {'ns0': 'http://www.tei-c.org/ns/1.0'}
    all_dois = set()

    def extract_dois_from_file(xml_file):
        try:
            tree = ET.parse(xml_file)
            root = tree.getroot()

            for doi_element in root.findall('.//ns0:idno[@type="DOI"]', namespaces=ns):
                doi = doi_element.text
                if doi:
                    all_dois.add(doi)

        except FileNotFoundError:
            print(f"Error: XML file not found - {xml_file}")
        except ET.ParseError:
            print(f"Error: Unable to parse the XML file - {xml_file}")

    for directory_path in directory_paths:
        for filename in os.listdir(directory_path):
            if filename.endswith(".xml"):
                xml_file_path = os.path.join(directory_path, filename)
                extract_dois_from_file(xml_file_path)

    with open(output_file, 'w') as f:
        for doi in all_dois:
            f.write(f"{doi}\n")

# Usage
xml_directory_paths = ['xml_scihub_downloads', 'xml_url_downloads']
output_file_path = 'new_dois.txt'
extract_and_write_dois(xml_directory_paths, output_file_path)
