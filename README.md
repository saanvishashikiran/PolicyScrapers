##  Components

### `documentScraper/`

This folder includes:
- Scripts that use AI readiness and digital infrastructure-related keyword prompts
- Calls to the OpenAI API to pull related policy documents
- Tools for categorizing and saving documents in a structured format

#### Requirements
- OpenAI API key (stored in `.env` as `OPENAI_API_KEY`)
- `openai`, `python-dotenv`, and other supporting libraries

---

### `legiscanScraper/`

This folder includes:
- Scripts that interact with the [LegiScan API](https://legiscan.com)
- Downloads JSON records for **all bills, resolutions, and policy documents** for a given state
- Includes filters for date ranges 

#### Requirements
- LegiScan API key (stored in `.env` as `API_KEY`)
- `requests`, `python-dotenv`, and `json`

---

### `executiveOrderScrapers/`

This folder contains web scrapers tailored to each state’s public records system. Currently supported states:
- **New York**: Pulls EOs from the NY Governor's website
- **Texas**: Scrapes past and current EOs from the Texas Governor’s executive order archive
- **California**: Extracts EOs from the CA Governor’s public executive order page

Each scraper:
- Collects PDF URLs, metadata (title, date), and stores structured output as JSON
- Handles unique HTML layouts and access patterns per state

#### Requirements
- `requests`, `beautifulsoup4`, `selenium` (if applicable)
- Browser drivers (for Selenium-based scrapers)

---
