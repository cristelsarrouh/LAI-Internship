import os
from pdfminer.high_level import extract_text

def extract_text_from_pdf(pdf_path):
    txt_directory = "pdfminer_biophysical_journal_txt"
    os.makedirs(txt_directory, exist_ok=True)  # Create txt directory if it doesn't exist

    for pdf_file in os.listdir(pdf_path):
        if pdf_file.endswith('.pdf'):
            pdf_file_path = os.path.join(pdf_path, pdf_file)
            text = extract_text(pdf_file_path)
            txt_filename = os.path.splitext(pdf_file)[0] + '.txt'  # Use the same name as the PDF file
            txt_path = os.path.join(txt_directory, txt_filename)
            with open(txt_path, 'w', encoding='utf-8') as txt_file:
                txt_file.write(text)

# Example usage
pdf_directory = r"C:\Users\phpue\Desktop\cristel\PycharmProjects\Internship\journal\biophysical_journal"
extract_text_from_pdf(pdf_directory)
