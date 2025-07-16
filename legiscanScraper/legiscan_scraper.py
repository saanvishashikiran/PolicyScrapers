import requests
import json
import time
from dotenv import load_dotenv
import os

load_dotenv()

API_KEY = os.getenv("API_KEY")
BASE_URL = "https://api.legiscan.com/"
REQUEST_DELAY = 1  

def get_json(url, params):
    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        data = response.json()
        if data["status"] == "OK":
            return data
        else:
            print(f"API Error: {data.get('alert', {}).get('message')}")
            return None
    except Exception as e:
        print(f"Request failed: {e}")
        return None

def get_sessions(state):
    params = {"key": API_KEY, "op": "getSessionList", "state": state}
    data = get_json(BASE_URL, params)
    return data["sessions"] if data else []

def get_bills(session_id):
    params = {"key": API_KEY, "op": "getMasterList", "id": session_id}
    data = get_json(BASE_URL, params)
    return list(data["masterlist"].values())[1:] if data else []

def get_bill_details(bill_id):
    params = {"key": API_KEY, "op": "getBill", "id": bill_id}
    data = get_json(BASE_URL, params)
    return data["bill"] if data else None

def extract_document_urls(bill):
    return {
        "bill_number": bill.get("bill_number"),
        "session": bill.get("session", {}).get("session_name"),
        "passed": bill.get("passed"),
        "texts": [t.get("url") for t in bill.get("texts", [])],
        "amendments": [a.get("url") for a in bill.get("amendments", [])],
        "supplements": [s.get("url") for s in bill.get("supplements", [])],
    }

def collect_bills(state, start_year):
    output_file = f"{state}_legiscan_documents.json"
    all_documents = []

    sessions = get_sessions(state)
    recent_sessions = [s for s in sessions if s.get("year_start", 0) >= start_year]
    print(f"Found {len(recent_sessions)} sessions for {state} from {start_year} onward.")

    for session in recent_sessions:
        session_id = session["session_id"]
        session_name = session["session_name"]
        print(f"Processing session: {session_name} (ID {session_id})")

        bills = get_bills(session_id)
        print(f"  Found {len(bills)} bills.")

        for bill in bills:
            bill_id = bill.get("bill_id")
            bill_detail = get_bill_details(bill_id)
            if bill_detail and bill_detail.get("passed") == 1: 
                doc_urls = extract_document_urls(bill_detail)
                all_documents.append(doc_urls)
            time.sleep(REQUEST_DELAY)

    with open(output_file, "w") as f:
        json.dump(all_documents, f, indent=2)

    print(f"\nSaved {len(all_documents)} passed bill documents to {output_file}")

def main():
    state = "NY"
    start_year = 2023
    collect_bills(state, start_year)

if __name__ == "__main__":
    main()
