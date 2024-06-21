# from pyzotero import zotero
#
# # Replace these variables with your own Zotero library information
# library_id = '13461108'
# library_type = 'user'  # or 'group' if it's a group library
# api_key = 'qR2BvC3bgPsdbNUDAm6fp329'
# collection_key = 'ZRHZVYBC'
#
# # Connect to Zotero library
# zot = zotero.Zotero(library_id, library_type, api_key)
#
# # Retrieve collection information
# collection_info = zot.collection(collection_key)
#
# # Print the name of the collection
# print('Collection Name:', collection_info['data']['name'])
#
# # Retrieve items from the specified collection
# collection_items = zot.collection_items(collection_key)
#
# # Initialize a counter for items with authors
# items_with_authors_count = 0
#
# # Print title and authors for each item with authors in the collection
# for item in collection_items:
#     title = item['data'].get('title', 'Title not available')
#
#     # Extract authors
#     authors = ', '.join([creator['lastName'] for creator in item['data'].get('creators', [])])
#
#     # Check if authors are available
#     if authors:
#         print('Title:', title)
#         print('Authors:', authors)
#
#         # Increment the counter for items with authors
#         items_with_authors_count += 1
#
# # Print the total count of items with authors
# print('Total number of items with authors in the collection:', items_with_authors_count)
#

from pyzotero import zotero
import os
import requests

# Replace these variables with your own Zotero library information
library_id = '13461108'
library_type = 'user'  # or 'group' if it's a group library
api_key = 'qR2BvC3bgPsdbNUDAm6fp329'
collection_key = 'ZRHZVYBC'

# Connect to Zotero library
zot = zotero.Zotero(library_id, library_type, api_key)

# Retrieve collection information
collection_info = zot.collection(collection_key)

# Print the name of the collection
print('Collection Name:', collection_info['data']['name'])

# Retrieve items from the specified collection
collection_items = zot.collection_items(collection_key)

# Initialize a counter for items with authors
items_with_authors_count = 0


# Function to download PDF attachments for an item
def download_pdf(item):
    attachments = item['data'].get('attachments', [])
    for attachment in attachments:
        if attachment['data']['contentType'] == 'application/pdf':
            pdf_url = attachment['data']['url']
            response = requests.get(pdf_url, stream=True)

            # Check if the 'articles' directory exists, create it if not
            if not os.path.exists('articles'):
                os.makedirs('articles')

            # Save the PDF to the 'articles' directory
            with open(f'articles/{item["key"]}.pdf', 'wb') as pdf_file:
                for chunk in response.iter_content(chunk_size=128):
                    pdf_file.write(chunk)


# Print title and authors for each item with authors in the collection
for item in collection_items:
    title = item['data'].get('title', 'Title not available')

    # Extract authors
    authors = ', '.join([creator['lastName'] for creator in item['data'].get('creators', [])])

    # Check if authors are available
    if authors:
        print('Title:', title)
        print('Authors:', authors)

        # Download PDF attachments
        download_pdf(item)

        # Increment the counter for items with authors
        items_with_authors_count += 1

# Print the total count of items with authors
print('Total number of items with authors in the collection:', items_with_authors_count)
