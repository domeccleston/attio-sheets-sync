import functions_framework
import requests
import time
import logging
from concurrent.futures import ThreadPoolExecutor
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
import pandas as pd
import json
import os

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
logger = logging.getLogger(__name__)

# Log startup time
start_time = time.time()
logger.info(f"Starting import of dependencies")

def fetch_batch(params):
    """Helper function to fetch a single batch of records"""
    api_key, object_id, batch_size, offset = params
    logger.info(f"Fetching batch: size={batch_size}, offset={offset}")
    
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
            logger.debug(f"Attempt {attempt + 1}/{max_retries} for batch offset={offset}")
            response = requests.post(url, json=payload, headers=headers)
            result = response.json()
            
            if response.status_code != 200:
                logger.error(f"API Error: Status={response.status_code}, Response={result}")
                raise Exception(f"API returned status {response.status_code}")
            
            if 'error' in result:
                if result.get('status') == 429:
                    retry_after = float(result.get('retry_after', base_delay))
                    logger.warning(f"Rate limit hit, waiting {retry_after}s before retry")
                    time.sleep(retry_after)
                    continue
                logger.error(f"API Error: {result['error']}")
                raise Exception(f"API Error: {result['error']}")
            
            records = result.get('data', [])
            logger.info(f"Successfully fetched {len(records)} records from offset {offset}")
            return records
            
        except Exception as e:
            if attempt == max_retries - 1:
                logger.error(f"Failed all {max_retries} attempts for batch offset={offset}: {str(e)}")
                raise
            logger.warning(f"Attempt {attempt + 1} failed: {str(e)}. Retrying...")
            time.sleep(base_delay * (2 ** attempt))
    
    return []

def get_object_records(api_key, object_id, batch_size=500):
    """Fetch records with minimal parallelization"""
    all_records = []
    offset = 0
    max_workers = 2  # Just 2 workers
    
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        while True:
            futures = [
                executor.submit(fetch_batch, (api_key, object_id, batch_size, offset)),
                executor.submit(fetch_batch, (api_key, object_id, batch_size, offset + batch_size))
            ]
            
            got_records = False
            for future in futures:
                try:
                    batch = future.result()
                    if batch:
                        all_records.extend(batch)
                        got_records = True
                        logger.info(f"Fetched {len(all_records)} records so far")
                except Exception as e:
                    logger.error(f"Error fetching batch: {e}")
            
            if not got_records:
                break
                
            offset += batch_size * max_workers
    
    return all_records

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

def update_spreadsheet(google_token, spreadsheet_id, records_df):
    """Update the Google Sheet with records"""
    try:
        logger.info(f"Starting spreadsheet update with {len(records_df)} records")
        
        # Create credentials from the token
        logger.debug("Creating Google credentials")
        creds = Credentials(
            token=google_token,
            scopes=['https://www.googleapis.com/auth/spreadsheets']
        )
        
        service = build('sheets', 'v4', credentials=creds)
        
        # Clean the data
        logger.debug("Cleaning DataFrame")
        records_df = records_df.replace({float('nan'): None})
        records_df = records_df.map(lambda x: str(x) if x is not None else '')
        
        # Prepare data for upload
        headers = records_df.columns.tolist()
        values = [headers] + records_df.values.tolist()
        logger.info(f"Prepared {len(values)} rows (including headers) for upload")
        
        # Add size logging
        total_cells = records_df.size  # rows * columns
        logger.info(f"Attempting to write {total_cells} cells to spreadsheet")
        logger.info(f"DataFrame dimensions: {records_df.shape[0]} rows x {records_df.shape[1]} columns")
        
        try:
            # Clear existing data
            logger.info("Clearing existing spreadsheet data")
            service.spreadsheets().values().clear(
                spreadsheetId=spreadsheet_id,
                range='A1:ZZ'
            ).execute()
            
            # Update the spreadsheet with new data
            logger.info("Uploading new data to spreadsheet")
            update_result = service.spreadsheets().values().update(
                spreadsheetId=spreadsheet_id,
                range='A1',
                valueInputOption='RAW',
                body={'values': values}
            ).execute()
            
            logger.info(f"Spreadsheet updated successfully: {update_result.get('updatedCells')} cells updated")
            return True
        except Exception as e:
            # Get the actual error details
            if hasattr(e, 'resp') and hasattr(e.resp, 'status'):
                if e.resp.status == 429:
                    logger.error("Google Sheets API rate limit exceeded!")
                    logger.error(f"Response headers: {e.resp.headers}")  # May contain quota info
                else:
                    logger.error(f"Google Sheets API error: Status {e.resp.status}")
            logger.error(f"Full error details: {str(e)}")
            raise
        
    except Exception as e:
        logger.error(f"Error updating spreadsheet: {str(e)}", exc_info=True)
        raise

def save_records_to_file(records, request_id):
    """Save records to a local cache file"""
    cache_dir = "cache"
    os.makedirs(cache_dir, exist_ok=True)
    
    filepath = os.path.join(cache_dir, f"records_{request_id}.json")
    logger.info(f"Saving {len(records)} records to {filepath}")
    
    with open(filepath, 'w') as f:
        json.dump(records, f)
    
    return filepath

def load_records_from_file(filepath):
    """Load records from a cache file"""
    logger.info(f"Loading records from {filepath}")
    with open(filepath, 'r') as f:
        return json.load(f)

@functions_framework.http
def process_spreadsheet(request):
    request_id = f"req_{int(time.time())}"
    start_time = time.time()
    logger.info(f"[{request_id}] New request received")
    
    try:
        data = request.get_json()
        
        # Check if we should use cached data
        cache_file = data.get('cacheFile')
        
        if cache_file:
            logger.info(f"[{request_id}] Using cached records from {cache_file}")
            records = load_records_from_file(cache_file)
        else:
            # Fetch new records
            logger.info(f"[{request_id}] Fetching new records from Attio")
            records = get_object_records(data['attioApiKey'], data['resourceId'])
            # Save to cache
            cache_file = save_records_to_file(records, request_id)
        
        logger.info(f"[{request_id}] Processing {len(records)} records")
        
        # Process records into a format suitable for the spreadsheet
        processed_records = []
        for record in records:
            if 'values' not in record:
                continue
                
            csv_data = {
                'record_id': record['id']['record_id']
            }
            
            for field_name, value_list in record['values'].items():
                csv_data[field_name] = process_record_value(field_name, value_list)
            
            processed_records.append(csv_data)
        
        # Convert to DataFrame
        df = pd.DataFrame(processed_records)
        
        # Update the spreadsheet
        update_spreadsheet(data['googleToken'], data['spreadsheetId'], df)
        
        logger.info(f"[{request_id}] Successfully processed {len(processed_records)} records")
        
        return {
            'status': 'success',
            'message': f'[{request_id}] Successfully uploaded {len(processed_records)} records to spreadsheet',
            'record_count': len(processed_records)
        }

    except KeyError as e:
        return {
            'status': 'error',
            'message': f'[{request_id}] Missing required parameter: {str(e)}'
        }, 400
    except Exception as e:
        return {
            'status': 'error',
            'message': f'[{request_id}] Error: {str(e)}'
        }, 400

logger.info(f"Dependencies imported in {time.time() - start_time:.2f}s")
