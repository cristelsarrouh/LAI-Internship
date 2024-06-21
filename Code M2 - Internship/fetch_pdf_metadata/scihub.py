import os
from bs4 import BeautifulSoup
from tqdm import tqdm
from time import sleep
import requests
import wget

def download_pdfs_from_scihub_combined(doi_file_path, invalid_urls_file_path, txt_output_folder):
    print('\n')
    print('Writing pdf files from Sci-Hub...')

    # Read the list of DOIs from 'no_url_found.txt'
    with open(doi_file_path, 'r') as doi_file:
        dois_no_url_found = [line.strip() for line in doi_file.readlines()]

    # Read the list of DOIs from 'invalid_url.txt'
    with open(invalid_urls_file_path, 'r') as invalid_urls_file:
        dois_invalid_url = [line.strip() for line in invalid_urls_file.readlines()]

    # Combine the DOIs from both files
    combined_dois = set(dois_no_url_found + dois_invalid_url)

    # Ensure the absolute path for txt_output_folder
    txt_output_folder = os.path.abspath(txt_output_folder)

    # Create the output folder if it doesn't exist
    os.makedirs(txt_output_folder, exist_ok=True)

    # Create 'scihub_downloads' directory at the same level as 'txt_outputs'
    output_folder = os.path.join(os.path.dirname(txt_output_folder), 'scihub_downloads')
    os.makedirs(output_folder, exist_ok=True)

    for doi in tqdm(combined_dois):
        try:
            base_url = 'https://sci-hub.se/'
            response = requests.get(base_url + doi.strip())
            soup = BeautifulSoup(response.content, 'html.parser')
            content = soup.find('embed').get('src').replace('#navpanes=0&view=FitH', '').replace('//', '/')

            if content.startswith('/downloads'):
                pdf = 'https://sci-hub.se/' + content
            elif content.startswith('/tree'):
                pdf = 'https://sci-hub.se/' + content
            elif content.startswith('/uptodate'):
                pdf = 'https://sci-hub.se/' + content
            else:
                pdf = 'https:/' + content

            print(pdf)

            # Use os.path.join to create the full path for the PDF download in 'scihub_downloads'
            # Ensure that the filename is a valid one (e.g., removing characters like /)
            pdf_filename = f'{doi.strip().replace("/", "_")}.pdf'
            pdf_filename = "".join(c for c in pdf_filename if c.isalnum() or c in ('.', '_', '-'))
            pdf_path = os.path.join(output_folder, pdf_filename)

            # Download the PDF using wget
            wget.download(pdf, out=pdf_path)

            pdfs_found = open(os.path.join(txt_output_folder, 'PDFs_Found_scihub.txt'), 'a')
            pdfs_found.write(doi.strip() + '\t' + pdf_path + '\n')

        except:
            pdfs_not_found = open(os.path.join(txt_output_folder, 'PDFs_not_Found_scihub.txt'), 'a')
            pdfs_not_found.write(doi.strip() + '\n')

        sleep(3)

# Specify the path to the DOI files, the txt_output_folder, and call the function
doi_file_path_no_url_found = 'txt_outputs/no_url_found.txt'
doi_file_path_invalid_url = 'txt_outputs/invalid_url.txt'
txt_output_folder = 'txt_outputs'  # This is the txt output folder path

# Call the function for 'no_url_found.txt' and 'invalid_url.txt'
# download_pdfs_from_scihub_combined(doi_file_path_no_url_found, doi_file_path_invalid_url, txt_output_folder)