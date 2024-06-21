import PyPDF2
import re

def extract_sections(pdf_path):
    # Open the PDF file
    with open(pdf_path, 'rb') as file:
        # Create a PDF reader object
        pdf_reader = PyPDF2.PdfReader(file)

        # Initialize variables to store section content
        introduction = ""
        material_and_methods = ""
        results = ""
        discussion = ""

        # Iterate through each page
        for page_number in range(len(pdf_reader.pages)):
            # Extract text from the page
            page_text = pdf_reader.pages[page_number].extract_text()

            # Use regular expressions to identify section headings and content
            if re.search(r'\b(introduction|background)\b', page_text, re.IGNORECASE):
                introduction += page_text
            elif re.search(r'\b(materials? and methods?)\b', page_text, re.IGNORECASE):
                material_and_methods += page_text
            elif re.search(r'\b(results?)\b', page_text, re.IGNORECASE):
                results += page_text
            elif re.search(r'\b(discussion)\b', page_text, re.IGNORECASE):
                discussion += page_text

        # Return the extracted sections
        return {
            'introduction': introduction,
            'material_and_methods': material_and_methods,
            'results': results,
            'discussion': discussion
        }

# Example usage
pdf_path = 'PMC9389945.pdf'
output_file_path = 'output_sections.txt'

sections = extract_sections(pdf_path)

# Write sections to a text file
with open(output_file_path, 'w', encoding='utf-8') as output_file:
    for section_name, section_content in sections.items():
        output_file.write(f"=== {section_name.upper()} ===\n\n")
        output_file.write(section_content)
        output_file.write('\n\n')

print(f"Sections extracted and saved to {output_file_path}")