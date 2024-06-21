import os
import json
import shutil

def author_in_article(data, author_name):
    authors = data.get("authors", [])
    for author in authors:
        if author.get("name", "").lower() == author_name.lower():
            return True
    return False

def process_json_file(file_path, dest_directory, author_name):
    with open(file_path, 'r', encoding='utf-8') as file:
        data = json.load(file)

        # Check if "publicationTypes" exists in data and it is not None
        publication_types = data.get("publicationTypes")
        if publication_types is None:
            print(f"Skipping file {file_path} because it does not contain 'publicationTypes'.")
            return

        # Check if "Review" is in publicationTypes
        if "Review" in publication_types:
            print(f"Skipping file {file_path} because it contains 'Review' in publicationTypes.")
            return

        # Check if the year is less than 2000
        year = data.get("year")
        if year is not None and year < 2000:
            print(f"Skipping file {file_path} because its year is less than 2000.")
            return

        # Check if the specified author is in the list of authors
        if not author_in_article(data, author_name):
            print(f"Skipping file {file_path} because '{author_name}' is not an author.")
            return

        # If all conditions are met, copy the file to the new directory
        dest_path = os.path.join(dest_directory, os.path.basename(file_path))
        shutil.copy(file_path, dest_path)
        print(f"Copied file to {dest_path}")

def process_json_directory(source_directory, dest_directory, author_name):
    if not os.path.exists(dest_directory):
        os.makedirs(dest_directory)

    for filename in os.listdir(source_directory):
        if filename.endswith(".json"):
            file_path = os.path.join(source_directory, filename)
            process_json_file(file_path, dest_directory, author_name)

# Example usage
source_directory = r'C:\Users\phpue\Desktop\cristell\LLM application\PHP\Third\json_4'
dest_directory = r'C:\Users\phpue\Desktop\cristell\LLM application\PHP\Third\json_4\json_filter_4'
author_name = 'Pierre-henri Puech'
process_json_directory(source_directory, dest_directory, author_name)
