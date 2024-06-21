# To read the PDF
import PyPDF2
from pdfminer.high_level import extract_pages
from pdfminer.layout import LTTextContainer, LTChar, LTFigure
import pdfplumber
from PIL import Image
from pdf2image import convert_from_path
import pytesseract
import os

# Create function to extract text
def text_extraction(element):
    line_text = element.get_text()
    line_formats = []
    for text_line in element:
        if isinstance(text_line, LTTextContainer):
            for character in text_line:
                if isinstance(character, LTChar):
                    line_formats.append(character.fontname)
                    line_formats.append(character.size)
    format_per_line = list(set(line_formats))
    return (line_text, format_per_line)

# Extracting tables from the page
def extract_table(pdf_path, page_num, table_num):
    pdf = pdfplumber.open(pdf_path)
    table_page = pdf.pages[page_num]
    table = table_page.extract_tables()[table_num]
    return table

# Convert table into appropriate format
def table_converter(table):
    table_string = ''
    for row_num in range(len(table)):
        row = table[row_num]
        cleaned_row = [item.replace('\n', ' ') if item is not None and '\n' in item else 'None' if item is None else item for item in row]
        table_string += ('|' + '|'.join(cleaned_row) + '|' + '\n')
    table_string = table_string[:-1]
    return table_string

# Create a function to check if the element is in any tables present in the page
def is_element_inside_any_table(element, page, tables):
    x0, y0up, x1, y1up = element.bbox
    y0 = page.bbox[3] - y1up
    y1 = page.bbox[3] - y0up
    for table in tables:
        tx0, ty0, tx1, ty1 = table.bbox
        if tx0 <= x0 <= x1 <= tx1 and ty0 <= y0 <= y1 <= ty1:
            return True
    return False

# Function to find the table for a given element
def find_table_for_element(element, page, tables):
    x0, y0up, x1, y1up = element.bbox
    y0 = page.bbox[3] - y1up
    y1 = page.bbox[3] - y0up
    for i, table in enumerate(tables):
        tx0, ty0, tx1, ty1 = table.bbox
        if tx0 <= x0 <= x1 <= tx1 and ty0 <= y0 <= y1 <= ty1:
            return i  # Return the index of the table
    return None

# Create a function to crop the image elements from PDFs
def crop_image(element, pageObj):
    [image_left, image_top, image_right, image_bottom] = [element.x0, element.y0, element.x1, element.y1]
    pageObj.mediabox.lower_left = (image_left, image_bottom)
    pageObj.mediabox.upper_right = (image_right, image_top)
    cropped_pdf_writer = PyPDF2.PdfWriter()
    cropped_pdf_writer.add_page(pageObj)
    with open('cropped_image.pdf', 'wb') as cropped_pdf_file:
        cropped_pdf_writer.write(cropped_pdf_file)

# Create a function to convert the PDF to images
def convert_to_images(input_file):
    images = convert_from_path(input_file)
    image = images[0]
    output_file = 'PDF_image.png'
    image.save(output_file, 'PNG')

# Create a function to read text from images
def image_to_text(image_path):
    img = Image.open(image_path)
    text = pytesseract.image_to_string(img)
    return text

# Find the PDF path
pdf_path = '/home/cristel/PycharmProjects/M2 Internship/Download_papers/PMC9389945.pdf'
pdfFileObj = open(pdf_path, 'rb')
pdfReaded = PyPDF2.PdfReader(pdfFileObj)

# Directory to save text files
output_directory = '/home/cristel/PycharmProjects/M2 Internship/Extract text/combo results'

# Create the dictionary to extract text from each image
text_per_page = {}
# Create a boolean variable for image detection
image_flag = False

# We extract the pages from the PDF
for pagenum, page in enumerate(extract_pages(pdf_path)):

    pageObj = pdfReaded.pages[pagenum]
    page_text = []
    line_format = []
    text_from_images = []
    text_from_tables = []
    page_content = []
    table_in_page = -1
    pdf = pdfplumber.open(pdf_path)
    page_tables = pdf.pages[pagenum]
    tables = page_tables.find_tables()
    if len(tables) != 0:
        table_in_page = 0

    # Extracting the tables of the page
    for table_num in range(len(tables)):
        table = extract_table(pdf_path, pagenum, table_num)
        table_string = table_converter(table)
        text_from_tables.append(table_string)

    page_elements = [(element.y1, element) for element in page._objs]
    page_elements.sort(key=lambda a: a[0], reverse=True)

    for i, component in enumerate(page_elements):
        element = component[1]

        if table_in_page == -1:
            pass
        else:
            if is_element_inside_any_table(element, page, tables):
                table_found = find_table_for_element(element, page, tables)
                if table_found == table_in_page and table_found is not None:
                    page_content.append(text_from_tables[table_in_page])
                    page_text.append('table')
                    line_format.append('table')
                    table_in_page += 1
                continue

        if not is_element_inside_any_table(element, page, tables):
            if isinstance(element, LTTextContainer):
                (line_text, format_per_line) = text_extraction(element)
                page_text.append(line_text)
                line_format.append(format_per_line)
                page_content.append(line_text)

            if isinstance(element, LTFigure):
                crop_image(element, pageObj)
                convert_to_images('cropped_image.pdf')
                image_text = image_to_text('PDF_image.png')
                text_from_images.append(image_text)
                page_content.append(image_text)
                page_text.append('image')
                line_format.append('image')
                image_flag = True

    dctkey = 'Page_' + str(pagenum)
    text_per_page[dctkey] = [page_text, line_format, text_from_images, text_from_tables, page_content]

    # Save the content to a text file
    output_file_path = os.path.join(output_directory, f'Page_{pagenum + 1}_content.txt')
    with open(output_file_path, 'w', encoding='utf-8') as output_file:
        output_file.write(''.join(page_content))

# Close the pdf file object
pdfFileObj.close()

# Delete the additional files created if image is detected
# if image_flag:
#     os.remove('cropped_image.pdf')
#     os.remove('PDF_image.png')

print("Content has been exported to text files.")

