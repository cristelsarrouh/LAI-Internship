import fitz  # PyMuPDF
import spacy
import re

def extract_sections(pdf_path):
    # Load the spaCy English model
    nlp = spacy.load("en_core_web_sm")

    # Open the PDF file
    pdf_document = fitz.open(pdf_path)

    # Initialize variables to store section content
    introduction = ""
    material_and_methods = ""
    results = ""
    discussion = ""

    # Iterate through each page
    for page_number in range(pdf_document.page_count):
        # Extract text from the page
        page = pdf_document[page_number]
        page_text = page.get_text()

        # Process the text with spaCy
        doc = nlp(page_text)

        # Classify sentences into sections based on keywords or patterns
        for sentence in doc.sents:
            if re.search(r'\b(introduction|background)\b', sentence.text, re.IGNORECASE):
                introduction += sentence.text + "\n"
            elif re.search(r'\b(materials? and methods?)\b', sentence.text, re.IGNORECASE):
                material_and_methods += sentence.text + "\n"
            elif re.search(r'\b(results?)\b', sentence.text, re.IGNORECASE):
                results += sentence.text + "\n"
            elif re.search(r'\b(discussion)\b', sentence.text, re.IGNORECASE):
                discussion += sentence.text + "\n"

    # Return the extracted sections
    return {
        'introduction': introduction,
        'material_and_methods': material_and_methods,
        'results': results,
        'discussion': discussion
    }

# Example usage
pdf_path = '/home/cristel/PycharmProjects/M2 Internship/Download_papers/PMC9701611.pdf'
output_file_path = 'output_sections.txt'

sections = extract_sections(pdf_path)

# Write sections to a text file
with open(output_file_path, 'w', encoding='utf-8') as output_file:
    for section_name, section_content in sections.items():
        output_file.write(f"=== {section_name.upper()} ===\n\n")
        output_file.write(section_content)
        output_file.write('\n\n')

print(f"Sections extracted and saved to {output_file_path}")
