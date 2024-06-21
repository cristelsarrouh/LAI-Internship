import os
import requests

# Define the API endpoint URL
url = 'https://api.semanticscholar.org/graph/v1/paper/search'

# Define the query parameters
query = 'immunology'  # Example query
journal = 'Journal of Immunology'  # Example journal name
years = ['2000-2005', '2006-2010', '2011-2015', '2016-2020']  # Example list of years
query_params = {
    'query': query,
    'venue': journal,
    'publicationTypes': 'JournalArticle',
    'fields': 'title,externalIds,publicationTypes',  # Example fields
}

# Securely retrieve the API key from environment variables
api_key = 'CTEt7pN9zh7P4eA3K15Ysa0lxxLySqN562N3nx6x'

if not api_key:
    raise ValueError("API key not found. Please set the SEMANTIC_SCHOLAR_API_KEY environment variable.")

# Define headers with API key
headers = {'x-api-key': api_key}

try:
    for year in years:
        query_params['year'] = year  # Update the query parameters with the current year

        # Define the output file for the current year
        output_file = f'dois_{year}.txt'

        # Loop to handle pagination and fetch 20 articles
        count = 0  # Count the number of articles fetched
        offset = 0  # Initialize offset
        with open(output_file, 'w') as f:
            while count < 25:
                # Update the offset for the next request
                query_params['offset'] = offset

                # Send the API request
                response = requests.get(url, params=query_params, headers=headers)

                # Check response status
                response.raise_for_status()  # Raise an HTTPError for bad responses (4xx or 5xx)

                # Process and print the response data as needed
                response_data = response.json()
                papers = response_data.get('data', [])
                print(f"Results for year {year}:")
                filtered_papers = [paper for paper in papers if 'Review' not in paper['publicationTypes']]
                print(filtered_papers)

                # Write the DOIs to the output file
                for paper in filtered_papers:
                    if 'externalIds' in paper and 'DOI' in paper['externalIds']:
                        doi = paper['externalIds']['DOI']
                        f.write(doi + '\n')
                        count += 1  # Increment count

                        # Break the loop if we've fetched 20 articles
                        if count == 25:
                            break

                # Update the offset for the next request
                offset += len(papers)

                # Break the loop if no more papers are returned
                if not papers:
                    break

except requests.exceptions.HTTPError as http_err:
    print(f"HTTP error occurred: {http_err}")
except Exception as err:
    print(f"An error occurred: {err}")

