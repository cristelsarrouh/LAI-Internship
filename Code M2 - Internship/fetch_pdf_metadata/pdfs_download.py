import os
import json
import requests

def extract_doi_and_url(directory_path, url_found_file, no_url_found_file):
    # Check if the directory exists
    if not os.path.exists(directory_path):
        print(f"Directory not found: {directory_path}")
        return

    # Create a directory called 'url' if it doesn't exist
    output_directory = 'txt_outputs'
    if not os.path.exists(output_directory):
        os.makedirs(output_directory)

    # Get a list of all files in the directory
    files = [f for f in os.listdir(directory_path) if f.endswith('.json')]

    # Open files for writing in the 'url' directory
    with open(os.path.join(output_directory, url_found_file), 'w') as url_found, \
         open(os.path.join(output_directory, no_url_found_file), 'w') as no_url_found:
        # Read and parse each JSON file
        for file_name in files:
            file_path = os.path.join(directory_path, file_name)
            with open(file_path, 'r') as file:
                try:
                    data = json.load(file)

                    # Extract DOI and openAccessPdf URL
                    doi = data['externalIds']['DOI']
                    open_access_pdf = data.get('openAccessPdf', {})
                    pdf_url = open_access_pdf.get('url') if open_access_pdf else None

                    # Write to the appropriate file
                    if pdf_url:
                        url_found.write(f"{pdf_url} doi: {doi}\n")
                    else:
                        no_url_found.write(f"{doi}\n")
                except json.JSONDecodeError as e:
                    print(f"Error reading {file_name}: {e}")

# Specify the directory path containing the JSON files
json_directory = 'json'

# Specify the output file names
url_found_file_path = 'url_found.txt'
no_url_found_file_path = 'no_url_found.txt'

# Call the function to extract DOI and URL information
extract_doi_and_url(json_directory, url_found_file_path, no_url_found_file_path)

def download_pdfs_and_extract_invalid_dois(url_file_path, download_directory, invalid_doi_file):
    # Create the download directory if it doesn't exist
    if not os.path.exists(download_directory):
        os.makedirs(download_directory)

    # Open the invalid DOI file for writing in the 'url' directory
    with open(os.path.join('txt_outputs', invalid_doi_file), 'w') as invalid_doi_file:
        # Read URLs from the file
        with open(url_file_path, 'r') as url_file:
            for line in url_file:
                parts = line.split(' doi: ')
                if len(parts) == 2:
                    pdf_url, doi = parts
                    pdf_url = pdf_url.strip()
                    doi = doi.strip()

                    # Generate a filename based on the DOI
                    filename = f"{doi.replace('/', '_')}.pdf"
                    filepath = os.path.join(download_directory, filename)

                    # Download the PDF
                    try:
                        response = requests.get(pdf_url, stream=True)
                        response.raise_for_status()

                        with open(filepath, 'wb') as pdf_file:
                            for chunk in response.iter_content(chunk_size=8192):
                                pdf_file.write(chunk)

                        print(f"Downloaded {filename}")
                    except requests.exceptions.RequestException as e:
                        print(f"Error downloading {pdf_url}: {e}")
                        # Write the DOI to the invalid DOI file in the 'url' directory
                        invalid_doi_file.write(f"{doi}\n")

# Specify the path to the URL file, the directory for PDF downloads, and the invalid DOI file
url_file_path = 'txt_outputs/url_found.txt'
download_directory = 'pdf_downloads'
invalid_doi_file_path = 'invalid_url.txt'

# Call the function to download PDFs and extract invalid DOIs
# download_pdfs_and_extract_invalid_dois(url_file_path, download_directory, invalid_doi_file_path)