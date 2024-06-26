from requests_html import HTMLSession
import requests
from requests.exceptions import ConnectionError

s = HTMLSession()

headers = {'User-Agent' : 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:122.0) Gecko/20100101 Firefox/122.0'}

file = open('pmcid.txt', 'r')
ids = file.readlines()
for pmc in ids:
    try:
        pmcid = pmc.strip()
        print(pmcid)
        base_url = 'https://www.ncbi.nlm.nih.gov/pmc/articles/'
        r = s.get(base_url + pmcid + '/', headers=headers, timeout=5)
        pdf_url = 'https://www.ncbi.nlm.nih.gov' + r.html.find('a.int-view', first=True).attrs['href']
        print(pdf_url)
        r = s.get(pdf_url, stream=True)
        with open(pmcid + '.pdf', 'wb') as f:
            for chunk in r.iter_content(chunk_size=1024):
                if chunk:
                    f.write(chunk)

    except ConnectionError as e:
        pass
        out = open('ConnectionError_pmcids.txt', 'a')
        out.write(pmcid + '\n')


