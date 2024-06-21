# import os
#
# # Replace 'path_to_storage' with the actual path to the 'storage' directory
# storage_directory = '/home/cristel/snap/zotero-snap/common/Zotero/storage'
#
# # List all directories in the 'storage' directory
# for directory_name in os.listdir(storage_directory):
#     directory_path = os.path.join(storage_directory, directory_name)
#
#     # Check if it's a directory
#     if os.path.isdir(directory_path):
#         print(f"Key: {directory_name}")
#         print(f"Directory Path: {directory_path}")
#
#         # List all PDF files in the key directory
#         pdf_files = [file for file in os.listdir(directory_path) if file.lower().endswith('.pdf')]
#
#         if pdf_files:
#             print("PDF Files:")
#             for pdf_file in pdf_files:
#                 pdf_file_path = os.path.join(directory_path, pdf_file)
#                 print(f"  - {pdf_file}")
#         else:
#             print("No PDF files found.")
#
#         print("---")

import os
import shutil
from pathlib import Path

def list_pdf_files(directory_path):
    return [file for file in os.listdir(directory_path) if file.lower().endswith('.pdf')]

def copy_pdfs(source_directory, destination_directory):
    for directory_path in source_directory.iterdir():
        if directory_path.is_dir():
            pdf_files = list_pdf_files(directory_path)

            for pdf_file in pdf_files:
                source_pdf_path = directory_path / pdf_file
                destination_pdf_path = destination_directory / pdf_file

                # Copy the PDF file to the destination directory
                shutil.copy2(source_pdf_path, destination_pdf_path)
                print(f"Copied: {pdf_file} from {source_pdf_path} to {destination_pdf_path}")

def main():
    # Replace 'path_to_storage' with the actual path to the 'storage' directory
    storage_directory = Path('/home/cristel/snap/zotero-snap/common/Zotero/storage')

    # Replace 'path_to_destination' with the actual path to the destination directory
    destination_directory = Path('/home/cristel/Desktop/Stage/Articles')

    # Check if the storage directory and destination directory exist
    if not storage_directory.exists() or not storage_directory.is_dir():
        print(f"Error: The specified storage directory '{storage_directory}' does not exist or is not a directory.")
        return
    if not destination_directory.exists() or not destination_directory.is_dir():
        print(f"Error: The specified destination directory '{destination_directory}' does not exist or is not a directory.")
        return

    copy_pdfs(storage_directory, destination_directory)

if __name__ == "__main__":
    main()
