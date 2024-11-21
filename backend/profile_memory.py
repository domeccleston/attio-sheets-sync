from memory_profiler import profile
import json
import time
from main import process_spreadsheet
import logging
from flask import Request

class MockRequest:
    def __init__(self, json_data):
        self._json = json_data

    def get_json(self):
        return self._json

@profile
def run_function():
    # Create mock request with real data
    mock_request = MockRequest({
        "attioApiKey": "your-api-key",
        "resourceId": "companies",
        "spreadsheetId": "your-spreadsheet-id"
    })

    # Process the request
    start_time = time.time()
    response = process_spreadsheet(mock_request)
    
    print(f"\nTime taken: {time.time() - start_time:.2f}s")
    print(f"\nFunction response: {json.dumps(response, indent=2)}")

if __name__ == "__main__":
    # Set up logging to match Cloud Function
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s'
    )
    
    run_function()