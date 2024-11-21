import requests
import json
from dotenv import load_dotenv
import os
import sys

# Load environment variables
load_dotenv()

def test_function(payload, use_cache=None):
    if use_cache:
        payload['cacheFile'] = use_cache
        
    url = "https://europe-west1-attio-sheets-sync.cloudfunctions.net/process-spreadsheet-large-v2"
    try:
        response = requests.post(
            url,
            headers={"Content-Type": "application/json"},
            json=payload,
            timeout=600
        )
        
        print(f"Status: {response.status_code}")
        
        try:
            response_json = response.json()
            print(f"Response: {json.dumps(response_json, indent=2)}")
        except json.JSONDecodeError:
            print(f"Raw response: {response.text}")
            
        assert response.status_code == 200
        
    except requests.exceptions.Timeout:
        print("ERROR: Request timed out after 600s")
        sys.exit(1)
    except requests.exceptions.RequestException as e:
        print(f"ERROR: Request failed: {e}")
        sys.exit(1)

# First run - will download and cache
test_function({
    "attioApiKey": os.getenv('ATTIO_API_KEY'),
    "googleToken": os.getenv('GOOGLE_OAUTH_TOKEN'),
    "spreadsheetId": os.getenv('GOOGLE_SPREADSHEET_ID'),
    "resourceId": "companies"
})

# test_function({
#     "attioApiKey": os.getenv('ATTIO_API_KEY'),
#     "googleToken": os.getenv('GOOGLE_TOKEN'),
#     "spreadsheetId": os.getenv('SPREADSHEET_ID'),
#     "resourceId": "people"
# }, use_cache="cache/records_<timestamp>.json") 
