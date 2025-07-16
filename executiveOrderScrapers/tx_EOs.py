import requests
from bs4 import BeautifulSoup
import json

# currently scrapes only greg abbott's EOs, need to make it scrape all governor's EOs
URL = "https://lrl.texas.gov/legeLeaders/governors/searchproc.cfm?govdoctypeID=5&governorID=45"
OUTPUT_FILE = "executiveOrders/downloads/tx_executive_orders.json" #changed name for consistency with other states


"""
scrapes all executive orders/metadata from the input page
"""
def scrape_executive_orders(url):
    # sending a get request to the webpage and parsing the HTML content of the response
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")

    # finding the first table on the page and getting all table rows besides the header row
    table = soup.find("table")
    rows = table.find_all("tr")[1:]  

    results = []
    # iterating through table rows extracting metadata
    for row in rows:
        cols = row.find_all("td")
        if len(cols) < 6: 
            continue   # skipping rows that don't have all expected columns
        
        #finding pdf link from third column
        title_link = cols[2].find("a")

        # extracting metadata
        results.append({
            "date": cols[0].get_text(strip=True),
            "session": cols[1].get_text(strip=True),
            "title": title_link.get_text(strip=True) if title_link else cols[2].get_text(strip=True),
            "pdf_url": f"https://lrl.texas.gov{title_link['href']}" if not title_link['href'].startswith("http") else f"{title_link['href'].replace('http://www.lrl.state.tx.us', 'https://lrl.texas.gov')}",
            "author": cols[3].get_text(strip=True),
            "type": cols[4].get_text(strip=True),
            "document_number": cols[5].get_text(strip=True),
        })

    return results

def run():
    orders = scrape_executive_orders(URL)
    with open(OUTPUT_FILE, "w") as f:
        json.dump(orders, f, indent=2)

def main():
    run()


if __name__ == "__main__":
    main()
