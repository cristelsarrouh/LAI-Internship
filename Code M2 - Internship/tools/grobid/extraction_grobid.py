import re

def extract_body_content(xml_file_path):
    try:
        with open(xml_file_path, 'r', encoding='utf-8') as file:
            content = file.read()
    except FileNotFoundError:
        print(f"File '{xml_file_path}' not found.")
        return None

    # Use regular expressions to find and remove 'fig' and 'foot' elements
    content = re.sub(r'<figure.*?</figure>', '', content, flags=re.DOTALL)
    content = re.sub(r'<note.*?</note>', '', content, flags=re.DOTALL)

    # Find the start and end indices of the <body> tag
    start_tag = content.find('<body>')
    end_tag = content.find('</body>')

    if start_tag == -1 or end_tag == -1:
        return None

    # Extract content between start and end tags (excluding tags themselves)
    body_content = content[start_tag + len('<body>'): end_tag]

    return body_content.strip()

def extract_all_div_content(body_content):
    div_contents = []

    # Use regular expression to find content inside <div> tags
    div_content_matches = re.finditer(r'<div xmlns="http://www.tei-c.org/ns/1.0">(.*?)</div>', body_content, re.DOTALL)

    for match in div_content_matches:
        div_contents.append(match.group(1).strip())

    return div_contents

# Example usage
xml_file_path = r"C:\Users\phpue\Desktop\cristel\PycharmProjects\Internship\biophysical_journal\articles_xml\PIIS0006349514006249.grobid.tei.xml"
body_content = extract_body_content(xml_file_path)
if body_content:
    all_div_contents = extract_all_div_content(body_content)
    for div_content in all_div_contents:
        print(div_content)
else:
    print("No body content found.")
