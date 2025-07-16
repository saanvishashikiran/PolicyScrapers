import requests
from bs4 import BeautifulSoup
import csv
import json
from io import StringIO
import re

BASE_URL = "https://www.library.ca.gov"

"""
find the downloadable csv from the main executive orders and proclamations page
"""
def find_csv_url(page_url):
    # headers to mimic a real browser
    headers = {
        "User-Agent": (
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/114.0.0.0 Safari/537.36"
        )
    }

    # fetching and parsing the webpage
    response = requests.get(page_url, headers=headers)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, "html.parser")

    # looking for a link that contains 'download-csv-executive-order.php'
    link_tag = soup.find("a", href=re.compile("download-csv-executive-order\\.php"))
    if not link_tag:
        raise ValueError("Could not find CSV download link on the page.")

    # constructing full URL
    relative_path = link_tag.get("href")
    full_url = BASE_URL + relative_path if relative_path.startswith("/") else relative_path
    return full_url

"""
downloads the csv and returns it as decoded text
"""
def download_csv(csv_url):
    headers = {
        "User-Agent": (
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/114.0.0.0 Safari/537.36"
        )
    }
    response = requests.get(csv_url, headers=headers)
    response.raise_for_status()
    return response.content.decode("utf-8")

"""
parses the csv content and extracting executive orders/metadata
"""
def extract_executive_orders(csv_text):
    reader = csv.DictReader(StringIO(csv_text))
    executive_orders = []

    for row in reader:
        # extracting all EO tags into a single field
        tags = [
                row.get(f"Tag {i}", "").strip()
                for i in range(1, 15)
                if row.get(f"Tag {i}", "").strip()
            ]
        combined_tags = ", ".join(tags)

        # only included EOs
        if "Executive Order" in row.get("Type", ""):
            executive_orders.append({
                "executive_order_number": row.get("Executive Order Number", "").strip(),
                "governor": row.get("Last Name", "").strip(),
                "date_signed": row.get("Date Signed", "").strip(),
                "date_filed": row.get("Date Filed", "").strip(),
                "pdf_link": row.get("Link", "").strip(),
                "tags": combined_tags
            })

    return executive_orders

"""
saves data to file
"""
def save_to_json(data, filename):
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)

"""
runs the scraping and saving pipeline
"""
def run_pipeline():
    page_url = "https://www.library.ca.gov/government-publications/executive-orders/"
    csv_url = find_csv_url(page_url)
    csv_text = download_csv(csv_url)
    executive_orders = extract_executive_orders(csv_text)
    save_to_json(executive_orders, "ca_executive_orders.json")

def main():
    run_pipeline()

if __name__ == "__main__":
    main()
