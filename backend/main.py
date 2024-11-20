import functions_framework
import requests
import time
from concurrent.futures import ThreadPoolExecutor
from flask import Response
import sys
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Log startup time
start_time = time.time()
logger.info(f"Starting import of dependencies")

def fetch_batch(params):
    """Helper function to fetch a single batch of records"""
    api_key, object_id, batch_size, offset = params
    url = f"https://api.attio.com/v2/objects/{object_id}/records/query"
    headers = {
        'accept': 'application/json',
        'authorization': f'Bearer {api_key}',
        'content-type': 'application/json'
    }
    
    payload = {
        "limit": batch_size,
        "offset": offset,
        "sort": {
            "direction": "desc",
            "attribute": "created_at"
        }
    }
    
    max_retries = 3
    base_delay = 0.01  # 10ms delay
    
    for attempt in range(max_retries):
        try:
            response = requests.post(url, json=payload, headers=headers)
            result = response.json()
            
            if response.status_code != 200:
                print(f"Error response: {response.status_code} - {result}")  # More detailed error logging
                raise Exception(f"API returned status {response.status_code}")
            
            if 'error' in result:
                if result.get('status') == 429:  # Rate limit error
                    retry_after = float(result.get('retry_after', base_delay))
                    time.sleep(retry_after)
                    continue
                raise Exception(f"API Error: {result['error']}")
            
            return result.get('data', [])
            
        except Exception as e:
            if attempt == max_retries - 1:  # Last attempt
                raise
            time.sleep(base_delay * (2 ** attempt))  # Exponential backoff
    
    return []

def get_object_records(api_key, object_id, batch_size=100):
    """Fetch all records for an object in parallel batches"""
    # First get total count
    try:
        initial_batch = fetch_batch((api_key, object_id, 1, 0))
        if not initial_batch or 'total_count' not in initial_batch[0]:
            raise Exception("Failed to get total record count")
    except Exception as e:
        print(f"Error getting initial count: {e}")
        return []
    
    total_records = initial_batch[0].get('total_count', 0)
    print(f"Total records to fetch: {total_records}")
    
    # Calculate batches
    offsets = range(0, total_records, batch_size)
    params = [(api_key, object_id, batch_size, offset) for offset in offsets]
    
    # Fetch in parallel
    all_records = []
    completed = 0
    total_batches = len(params)
    
    with ThreadPoolExecutor(max_workers=10) as executor:
        futures = [executor.submit(fetch_batch, p) for p in params]
        for future in futures:
            try:
                batch_records = future.result()
                all_records.extend(batch_records)
                completed += 1
                print(f"Completed {completed}/{total_batches} batches")
            except Exception as e:
                print(f"Error fetching batch: {e}")
    
    return all_records

@functions_framework.http
def process_spreadsheet(request):
    # Add health check handling
    if request.method == 'GET':
        return Response(status=200)
        
    try:
        data = request.get_json()
        
        # Extract the parameters
        attio_api_key = data['attioApiKey']
        resource_type = data['resourceType']
        resource_id = data['resourceId']
        
        if resource_type != 'object':
            return {
                'status': 'error',
                'message': 'Only object type is supported'
            }, 400
            
        records = get_object_records(attio_api_key, resource_id)
        
        if not records:
            return {
                'status': 'error',
                'message': f'No records found for object {resource_id}'
            }, 400
            
        print(f"Fetched {len(records)} records from object {resource_id}")
        
        return {
            'status': 'success',
            'message': f'Successfully fetched {len(records)} records',
            'record_count': len(records)
        }

    except KeyError as e:
        return {
            'status': 'error',
            'message': f'Missing required parameter: {str(e)}'
        }, 400
    except Exception as e:
        return {
            'status': 'error',
            'message': str(e)
        }, 400

logger.info(f"Dependencies imported in {time.time() - start_time:.2f}s")
