import os
import requests
from playwright.sync_api import sync_playwright

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
                  "AppleWebKit/537.36 (KHTML, like Gecko) "
                  "Chrome/115.0.0.0 Safari/537.36",
    "Accept-Language": "en-US,en;q=0.9",
    "Accept": "text/html,application/pdf,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
    "Referer": "https://www.google.com/"
}

def save_page_as_pdf(playwright, url, output_path):
    browser = playwright.chromium.launch(headless=True)
    page = browser.new_page()
    try:
        print(f"Loading page for PDF rendering: {url}")
        page.goto(url, wait_until='networkidle')
        page.pdf(path=output_path, format="A4")
        print(f"Saved PDF: {output_path}")
    except Exception as e:
        print(f"Failed to save PDF for {url}: {e}")
    finally:
        browser.close()

def download_pdfs(urls, output_dir="downloads"):
    os.makedirs(output_dir, exist_ok=True)

    with sync_playwright() as playwright:
        for url in urls:
            print(f"Processing: {url}")
            filename = url.rstrip('/').split('/')[-1]
            if not filename.lower().endswith(".pdf"):
                filename += ".pdf"
            output_path = os.path.join(output_dir, filename)

            if "nysenate.gov" in url and url.endswith("/download"):
                fixed_url = url[:-len("/download")]
                print(f"Detected NY Senate /download URL, fixing to: {fixed_url}")
                save_page_as_pdf(playwright, fixed_url, output_path)
                continue

            if url.lower().endswith(".pdf"):
                try:
                    response = requests.get(url, headers=HEADERS)
                    if response.status_code == 200:
                        with open(output_path, "wb") as f:
                            f.write(response.content)
                        print(f"Downloaded: {output_path}")
                    else:
                        print(f"Failed to download {url} - Status code: {response.status_code}")
                except Exception as e:
                    print(f"Error downloading {url}: {e}")
                continue

            save_page_as_pdf(playwright, url, output_path)
