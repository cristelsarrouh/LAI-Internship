# # pdfminer
# from pdfminer.high_level import extract_text
#
# text = extract_text("/home/cristel/PyCharmProjects/M2 Internship/Download_papers/PMC9389945.pdf")
# print(text)

import pdfplumber

with pdfplumber.open("/home/cristel/PyCharmProjects/M2 Internship/Download_papers/PMC9389945.pdf") as pdf:
    p0 = pdf.pages[0]
    im = p0.to_image()
    im.reset().draw_rects(p0.chars)

    text = p0.extract_text(keep_blank_chars=True)

# Define the output file path
output_file_path = '/home/cristel/PyCharmProjects/M2 Internship/Paper Pipeline/output.txt'

# Write the extracted text to the output file
with open(output_file_path, 'w', encoding='utf-8') as output_file:
    output_file.write(text)
