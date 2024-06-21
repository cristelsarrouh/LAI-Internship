from Bio import Entrez

def fetch_pubmed_articles_by_doi(doi):
    Entrez.email = "cristelsarrouh2001@hotmail.com"  # Set your email address

    # Use ESearch to get the PubMed ID (PMID) for the given DOI
    esearch_handle = Entrez.esearch(db="pubmed", term=doi)
    esearch_result = Entrez.read(esearch_handle)

    if "IdList" not in esearch_result or not esearch_result["IdList"]:
        print(f"No PubMed articles found for DOI: {doi}")
        return

    pmid = esearch_result["IdList"][0]

    # Use EFetch to retrieve the article information based on the PMID
    efetch_handle = Entrez.efetch(db="pubmed", id=pmid, retmode="xml")
    efetch_result = Entrez.read(efetch_handle)

    # Extract and print relevant information from the XML result
    for article in efetch_result["PubmedArticle"]:
        article_title = article["MedlineCitation"]["Article"]["ArticleTitle"]
        article_authors = ", ".join([author["LastName"] + " " + author["Initials"] for author in article["MedlineCitation"]["Article"]["AuthorList"]])
        article_abstract = article["MedlineCitation"]["Article"].get("Abstract", {}).get("AbstractText", "")

        print(f"Title: {article_title}")
        print(f"Authors: {article_authors}")
        print(f"Abstract: {article_abstract}\n")

if __name__ == "__main__":
    # Replace "your_doi_here" with the actual DOI you want to search for
    doi_to_search = '10.3390/ijms160818149'
    fetch_pubmed_articles_by_doi(doi_to_search)
