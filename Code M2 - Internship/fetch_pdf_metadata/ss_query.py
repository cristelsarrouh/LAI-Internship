import requests
import time
import random

from PDF_downloads.ss_json import get_paper_details
from PDF_downloads.pdfs_download import *
from PDF_downloads.scihub import *
def get_papers_by_journal_and_year(journal_name, year_range, output_file, publication_types=None):
    # Define the API endpoint URL
    url = 'https://api.semanticscholar.org/graph/v1/paper/search'

    # Your API key
    api_key = 'CTEt7pN9zh7P4eA3K15Ysa0lxxLySqN562N3nx6x'

    # Define headers with API key
    headers = {'x-api-key': api_key}

    # More specific query parameter
    query_params = {
        'query': 'immunology',
        'journal': journal_name,  # Specify the journal from which to extract biophysical_journal
        'publicationTypes': publication_type,
        'fields': 'title,externalIds',  # Include title and external IDs in the response
        'offset': random.randint(0, 1000),  # Random offset for starting position of biophysical_journal
    }

    if year_range == '1990-1999':
        query_params['year'] = '1990-1999'
    elif year_range == '2000-2009':
        query_params['year'] = '2000-2009'
    elif year_range == '2010-2024':
        query_params['year'] = '2010-2024'
    else:
        print("Invalid year range specified.")
        return

    retries = 3
    for attempt in range(retries):
        # Send the API request
        response = requests.get(url, params=query_params, headers=headers)

        # Check response status
        if response.status_code == 200:
            response_data = response.json()
            # Print response data for debugging
            print(f"Response data for {journal_name} ({year_range}): {response_data}")

            # Process and write DOIs to the output file
            count = 0
            with open(output_file, 'a') as f:
                for paper in response_data['data']:
                    if 'externalIds' in paper and 'DOI' in paper['externalIds']:
                        doi = paper['externalIds']['DOI']
                        f.write(doi + '\n')
                        print(f"DOI: {doi} - Journal: {journal_name} - Year Range: {year_range}")
                        count += 1
                        if count == 10:
                            break
            break  # Break out of the retry loop if successful
        elif response.status_code == 504:
            print(f"Request timed out for {journal_name} ({year_range}). Retrying...")
        else:
            print(
                f"Request failed for {journal_name} ({year_range}) with status code {response.status_code}: {response.text}")
            if attempt < retries - 1:
                # Wait for some time before retrying
                time.sleep(5)  # 5 seconds (adjust as needed)


# List of PDFs
journal_names = ['Biophysical Journal']
year_ranges = ['1990-1999', '2000-2009', '2010-2024']
publication_type = ['JournalArticle']

# Output file
output_file = r'C:\Users\phpue\Desktop\cristel\PycharmProjects\Internship\fetch_pdf\journal_articles_doi.txt'

# Open the output file in 'w' mode to overwrite it
with open(output_file, 'w') as f:
    pass  # Just to create an empty file

# Call the function for each journal and year range
for journal_name in journal_names:
    for year_range in year_ranges:
        get_papers_by_journal_and_year(journal_name, year_range, output_file)

# api_key = 'CTEt7pN9zh7P4eA3K15Ysa0lxxLySqN562N3nx6x'
# doi_path = r'C:\Users\phpue\Desktop\cristel\PycharmProjects\Internship\fetch_pdf\journal_articles_doi.txt'
#
# # results = get_paper_details(api_key, doi_path, output_dir='json')
#
# # Specify the directory path containing the JSON files
# json_directory = 'json'
#
# # Specify the output file names
# url_found_file_path = 'url_found.txt'
# no_url_found_file_path = 'no_url_found.txt'
#
# # Call the function to extract DOI and URL information
# extract_doi_and_url(json_directory, url_found_file_path, no_url_found_file_path)
#
# # Specify the path to the URL file, the directory for PDF downloads, and the invalid DOI file
# url_file_path = 'txt_outputs/url_found.txt'
# download_directory = 'pdf_downloads'
# invalid_doi_file_path = 'invalid_url.txt'
#
# # Call the function to download PDFs and extract invalid DOIs
# download_pdfs_and_extract_invalid_dois(url_file_path, download_directory, invalid_doi_file_path)
#
# # Specify the path to the DOI files, the txt_output_folder, and call the function
# doi_file_path_no_url_found = 'txt_outputs/no_url_found.txt'
# doi_file_path_invalid_url = 'txt_outputs/invalid_url.txt'
# txt_output_folder = 'txt_outputs'  # This is the txt output folder path
#
# # Call the function for 'no_url_found.txt' and 'invalid_url.txt'
# download_pdfs_from_scihub_combined(doi_file_path_no_url_found, doi_file_path_invalid_url, txt_output_folder)