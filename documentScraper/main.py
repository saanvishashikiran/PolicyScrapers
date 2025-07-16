from search import search_policy_links
from downloader import download_pdfs

if __name__ == "__main__":
    category = "Data"
    state = "New York"

    print(f"Searching for policy PDFs in {state} under the {category} category...")
    pdf_links = search_policy_links(category, state)

    print(f"Found {len(pdf_links)} PDF(s). Starting download...")
    download_pdfs(pdf_links)