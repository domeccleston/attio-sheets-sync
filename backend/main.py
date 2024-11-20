import functions_framework
import requests
import time
import logging
from concurrent.futures import ThreadPoolExecutor

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

def get_object_records(api_key, object_id, batch_size=500):
    """Fetch records with minimal parallelization"""
    total_count = 0
    offset = 0
    max_workers = 2  # Just 2 workers
    
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        while True:
            # Submit just 2 batches
            futures = [
                executor.submit(fetch_batch, (api_key, object_id, batch_size, offset)),
                executor.submit(fetch_batch, (api_key, object_id, batch_size, offset + batch_size))
            ]
            
            got_records = False
            for future in futures:
                try:
                    batch = future.result()
                    if batch:
                        total_count += len(batch)
                        got_records = True
                        logger.info(f"Fetched {total_count} records so far")
                except Exception as e:
                    logger.error(f"Error fetching batch: {e}")
            
            if not got_records:
                break
                
            offset += batch_size * max_workers
    
    return total_count

def process_record_value(field_name, value_list):
    """Extract the appropriate value based on field type"""
    if not value_list:
        return None
        
    first_value = value_list[0]
    attribute_type = first_value.get('attribute_type')
    
    if attribute_type == 'personal-name':
        return first_value.get('full_name')
    elif attribute_type == 'email-address':
        return first_value.get('email_address')
    elif attribute_type == 'location':
        parts = [
            first_value.get('locality'),
            first_value.get('region'),
            first_value.get('country_code')
        ]
        return ', '.join(filter(None, parts))
    elif attribute_type == 'record-reference':
        return first_value.get('target_record_id')
    elif attribute_type == 'text':
        return first_value.get('value')
    elif attribute_type == 'number':
        return first_value.get('value')
    elif attribute_type == 'timestamp':
        return first_value.get('value')
    elif attribute_type == 'select':
        return first_value.get('option', {}).get('title')
    elif attribute_type == 'domain':
        return first_value.get('domain')
    elif attribute_type == 'date':
        return first_value.get('value')
    elif attribute_type == 'currency':
        return first_value.get('value')
    elif attribute_type == 'interaction':
        return first_value.get('value')
    elif attribute_type == 'actor-reference':
        actor_type = first_value.get('referenced_actor_type')
        actor_id = first_value.get('referenced_actor_id')
        if actor_type == 'system':
            return 'system'
        return f"{actor_type}:{actor_id}" if actor_id else actor_type
    else:
        logger.warning(f"Unknown attribute type '{attribute_type}' for field '{field_name}'")
        return None

@functions_framework.http
def process_spreadsheet(request):
    # Add proper health check handling
    if request.method == 'GET':
        logger.info("Health check received")
        return {
            'status': 'healthy',
            'message': 'Service is ready'
        }
        
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
