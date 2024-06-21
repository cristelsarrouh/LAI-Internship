import requests
import time
import random
def get_papers_by_journal_and_year(year_range, output_file, publication_types=None):
    # Define the API endpoint URL
    url = 'https://api.semanticscholar.org/graph/v1/paper/search'

    # Your API key
    api_key = 'CTEt7pN9zh7P4eA3K15Ysa0lxxLySqN562N3nx6x'

    # Define headers with API key
    headers = {'x-api-key': api_key}

    # More specific query parameter
    query_params = {
        'query': 'biology',
        'journal': 'Journal of Immunology',  # Specify the journal from which to extract biophysical_journal
        'publicationTypes': publication_type,
        'fields': 'journal,title,externalIds',  # Include title and external IDs in the response
        'offset': random.randint(0, 1000),  # Random offset for starting position of biophysical_journal
    }
    # if year_range == '2000-2010':
    #     query_params['year'] = '2000-2010'
    # elif year_range == '2011-2015':
    #     query_params['year'] = '2011-2015'
    # elif year_range == '2016-2020':
    #     query_params['year'] = '2016-2020'
    # elif year_range == '2021-2024':
    #     query_params['year'] = '2021-2024'
    if year_range == '2002-2004':
        query_params['year'] = '2002-2004'
    elif year_range == '2005-2007':
        query_params['year'] = '2005-2007'
    elif year_range == '2008-2010':
        query_params['year'] = '2008-2010'
    elif year_range == '2011-2012':
        query_params['year'] = '2011-2012'
    elif year_range == '2013-2014':
        query_params['year'] = '2013-2014'
    elif year_range == '2015-2016':
        query_params['year'] = '2015-2016'
    elif year_range == '2017-2018':
        query_params['year'] = '2017-2018'
    elif year_range == '2019-2020':
        query_params['year'] = '2019-2020'
    elif year_range == '2021-2022':
        query_params['year'] = '2021-2022'
    elif year_range == '2023-2024':
        query_params['year'] = '2023-2024'
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
            print(f"Response data for ({year_range}): {response_data}")

            # Process and write DOIs to the output file
            count = 0
            with open(output_file, 'a') as f:
                for paper in response_data['data']:
                    if 'externalIds' in paper and 'DOI' in paper['externalIds']:
                        doi = paper['externalIds']['DOI']
                        f.write(doi + '\n')
                        print(f"DOI: {doi} - Journal: - Year Range: {year_range}")
                        count += 1
                        if count == 25:
                            break
            break  # Break out of the retry loop if successful
        elif response.status_code == 504:
            print(f"Request timed out for ({year_range}). Retrying...")
        else:
            print(
                f"Request failed for ({year_range}) with status code {response.status_code}: {response.text}")
            if attempt < retries - 1:
                # Wait for some time before retrying
                time.sleep(5)  # 5 seconds (adjust as needed)


# List of PDFs
# journal_names = ['Journal of Immunology']
#  year_ranges = ['2000-2010', '2011-2015', '2016-2020', '2021-2024']
year_ranges = ['2002-2004', '2005-2007', '2008-2010', '2011-2012', '2013-2014','2015-2016', '2017-2018', '2019-2020', '2021-2022','2023-2024']
publication_type = ['JournalArticle']


# Output file
output_file = r'C:\Users\phpue\Desktop\cristell\fetch_specific_articles\journal_articles_doi.txt'

# Open the output file in 'w' mode to overwrite it
with open(output_file, 'w') as f:
    pass  # Just to create an empty file

# Call the function for each journal and year range
# for journal_name in journal_names:
for year_range in year_ranges:
    get_papers_by_journal_and_year(year_range, output_file)

