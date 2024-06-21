import requests
import json
import os
from metapub import PubMedFetcher
import logging


def fetch_abstract_by_pmid(pmid):
    fetch = PubMedFetcher()
    try:
        # Fetch article details from PubMed using the provided PMID
        article = fetch.article_by_pmid(pmid)
        # Retrieve the abstract from the fetched article
        abstract = article.abstract

        return abstract
    except Exception as e:
        # Handle exceptions when fetching abstract and log the error
        logging.error(f"Error fetching abstract for PMID {pmid}: {e}")
        return None

def get_paper_details(api_key, doi_path, output_dir):
    # Create the output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)

    print("Reading DOIs from file...")
    with open(doi_path, 'r') as file:
        dois = file.read().splitlines()

    results = []
    for doi in dois:
        url = f'https://api.semanticscholar.org/graph/v1/paper/{doi}'
        headers = {'x-api-key': api_key}
        params = {'fields': 'title,year,abstract,authors,openAccessPdf,externalIds,referenceCount,citationCount,publicationTypes,fieldsOfStudy,journal'}

        print(f"Fetching paper details for DOI: {doi}")
        response = requests.get(url, params=params, headers=headers)
        print(f"Response status code: {response.status_code}")
        result = response.json()

        # Keep only "DOI" and "PubMed" entries in "externalIds"
        result['externalIds'] = {key: value for key, value in result.get('externalIds', {}).items() if key in ['DOI', 'PubMed']}

        # If "PubMed" is not present, add it with a value of null
        if 'PubMed' not in result['externalIds']:
            result['externalIds']['PubMed'] = None

        # Fetch abstract from PubMed if available
        pubmed_id = result['externalIds'].get('PubMed')
        if pubmed_id:
            print(f"Fetching abstract for PubMed ID: {pubmed_id}")
            abstract = fetch_abstract_by_pmid(pubmed_id)
            result['abstract'] = abstract

        results.append(result)

        # Replace slash with underscore in the DOI for the filename
        doi_filename = doi.replace('/', '_')
        output_path = os.path.join(output_dir, f'{doi_filename}.json')
        print(f"Writing paper details to file: {output_path}")
        with open(output_path, 'w') as output_file:
            json.dump(result, output_file, indent=2)

    print("Processing completed.")
    return results

# Example usage
api_key = 'CTEt7pN9zh7P4eA3K15Ysa0lxxLySqN562N3nx6x'
# doi_path = 'dois.txt'  # Replace with the actual path to your dois.txt file
# doi_path = r'C:\Users\phpue\Desktop\cristel\PycharmProjects\Internship\fetch_pdf\journal_articles_doi.txt'
# results = get_paper_details(api_key, doi_path, output_dir='json')
