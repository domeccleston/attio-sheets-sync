import os
from dotenv import load_dotenv
from main import process_spreadsheet
from flask import Request
import json

load_dotenv()

class MockRequest:
    def __init__(self, method="POST", json_data=None):
        self.method = method
        self._json = json_data

    def get_json(self):
        return self._json

# Test data
test_request = MockRequest(json_data={
    "attioApiKey": os.getenv('ATTIO_API_KEY'),
    "resourceType": "object",
    "resourceId": "companies"
})

# Process records and monitor memory
response = process_spreadsheet(test_request)
print(f"\nFinal response: {json.dumps(response, indent=2)}") 