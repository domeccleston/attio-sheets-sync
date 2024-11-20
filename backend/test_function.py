import requests
import json
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

def test_function(payload, expected_status=200):
    url = "http://localhost:8080"
    response = requests.post(
        url,
        headers={"Content-Type": "application/json"},
        json=payload
    )
    
    print(f"Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    assert response.status_code == expected_status

# Test object fetch
test_function({
    "attioApiKey": os.getenv('ATTIO_API_KEY'),
    "resourceType": "object",
    "resourceId": "companies"  # replace with your object ID
})

# # Test missing parameter
test_function({
    "attioApiKey": os.getenv('ATTIO_API_KEY'),
    "resourceType": "object"
    # resourceId missing
}, expected_status=400)
