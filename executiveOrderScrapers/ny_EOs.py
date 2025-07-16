from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import json
import time
import re

# URLs
BASE_URL = "https://www.governor.ny.gov"
CURRENT_PAGE = f"{BASE_URL}/executiveorders"
PAST_PAGE = f"{BASE_URL}/past-executive-orders"

# output locations
CURRENT_OUTPUT_FILE = "ny_executive_orders.json" #renamed for simpler download script
PAST_OUTPUT_FILE = "ny_past_executive_orders.json"

# initializes a headless Chrome browser to run in the background
def init_driver():
    options = Options()
    options.headless = True
    return webdriver.Chrome(options=options)

"""
scrapes pdf links from the current executive orders page
"""
def scrape_current_orders(output_file):
    driver = init_driver() # starts a headless Chrome session
    orders = [] 
    page = 0

    try:
        while True:
            # constructs the current page's URL and tells the browser to navigate to it
            url = f"{CURRENT_PAGE}?page={page}"
            print(f" Loading CURRENT orders page {page}: {url}")
            driver.get(url)

            # waits for page to lowk .view-rows blocks, the format of the page, and stops
            # scraping if not found in 10 secs
            try:
                WebDriverWait(driver, 10).until(
                    EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".views-row"))
                )
            except TimeoutException:
                print(f" No content on page {page}. Ending current scrape.")
                break
            
            # collects all EO blocks on the page
            blocks = driver.find_elements(By.CSS_SELECTOR, ".views-row")
            print(f" Found {len(blocks)} blocks on page {page}")
            if not blocks:
                break
            
            # iterating through the blocks to extract titles, links, and dates
            for block in blocks:
                try:
                    title_elem = block.find_element(By.CSS_SELECTOR, ".content-title a")
                    title = title_elem.text.strip()

                    try:
                        link_elem = block.find_element(By.CSS_SELECTOR, ".content-document a")
                        pdf_link = link_elem.get_attribute("href")
                    except NoSuchElementException:
                        pdf_link = None

                    try:
                        date_elem = block.find_element(By.CSS_SELECTOR, ".date")
                        date = date_elem.text.strip()
                    except NoSuchElementException:
                        date = None

                    print(f" {title} -> {pdf_link}")
                    orders.append({
                        "title": title,
                        "pdf_link": pdf_link,
                        "date": date
                    })

                except NoSuchElementException as e:
                    print(f" Skipping block due to missing data: {e}")
                    continue

            page += 1
            time.sleep(1)

    finally:
        driver.quit()

    with open(output_file, "w") as f:
        json.dump(orders, f, indent=2)

    print(f"\n Saved {len(orders)} current executive orders to {output_file}")

"""
scrapes pdf links from the past executive orders page,
which has a different format that warrents a separate function
"""
def scrape_past_orders(output_file):
    driver = init_driver() # starting a browser
    orders = []

    try:
        print(f"\n Loading PAST executive orders page: {PAST_PAGE}")
        driver.get(PAST_PAGE) # navigating to the page
        time.sleep(3)

        # grabbing all <a> tags in <p> linking to pdfs 
        links = driver.find_elements(By.CSS_SELECTOR, "p a[href$='.pdf']") 
        print(f" Found {len(links)} past executive order links.")

        # extracting title text, link, and date
        for link in links:
            title = link.text.strip()
            href = link.get_attribute("href")

            match = re.search(r"issued\s+([A-Za-z]+\s+\d{1,2},\s+\d{4})", title)
            date = match.group(1) if match else None

            # if a date was found, check if it's 2015 or later
            include = True
            if date:
                try:
                    from datetime import datetime
                    parsed_date = datetime.strptime(date, "%B %d, %Y")
                    if parsed_date.year < 2015:
                        include = False
                except ValueError:
                    print(f" Could not parse date: {date}")

            if include and href and href.endswith(".pdf"):
                orders.append({
                    "title": title,
                    "pdf_link": href,
                    "date": date
                })

    finally:
        driver.quit()

    with open(output_file, "w") as f:
        json.dump(orders, f, indent=2)

    print(f" Saved {len(orders)} past executive orders to {output_file}")

def main():
    scrape_current_orders(CURRENT_OUTPUT_FILE)
    scrape_past_orders(PAST_OUTPUT_FILE)

if __name__ == "__main__":
    main()
