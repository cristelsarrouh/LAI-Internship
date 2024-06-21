import os
from llmsherpa.readers import LayoutPDFReader


def llama_processing(pdf_file_path, llmsherpa_api_url):
    pdf_reader = LayoutPDFReader(llmsherpa_api_url)
    doc = pdf_reader.read_pdf(pdf_file_path)

    output_text = ""
    for section in doc.sections():
        output_text += section.to_html(include_children=True, recurse=True) + "\n"

    return output_text


# Directory containing PDFs
pdfs_directory = "pdfs"
# Directory to save output
output_directory = "llama_txt"
# API URL
llmsherpa_api_url = "https://readers.llmsherpa.com/api/document/developer/parseDocument?renderFormat=all"

# Create output directory if it doesn't exist
if not os.path.exists(output_directory):
    os.makedirs(output_directory)

# Iterate over PDF files in the directory
for filename in os.listdir(pdfs_directory):
    if filename.endswith(".pdf"):
        pdf_file_path = os.path.join(pdfs_directory, filename)
        output_file_path = os.path.join(output_directory, os.path.splitext(filename)[0] + ".txt")

        print(f"Processing {pdf_file_path}...")
        output_text = llama_processing(pdf_file_path, llmsherpa_api_url)

        # Save output to .manually file
        with open(output_file_path, "w", encoding="utf-8") as txt_file:
            txt_file.write(output_text)

        print(f"Processing complete. Output saved to {output_file_path}")

print("All PDFs processed.")
