import requests
import pandas as pd
import json
from pathlib import Path
import getpass
import time
from concurrent.futures import ThreadPoolExecutor
from tqdm import tqdm
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from datetime import datetime

CONFIG_DIR = Path.home() / '.attio'
CONFIG_FILE = CONFIG_DIR / 'config.json'
CREDENTIALS_FILE = CONFIG_DIR / 'credentials.json'

def setup_credentials():
    """Setup Attio credentials if they don't exist"""
    if not CONFIG_DIR.exists():
        CONFIG_DIR.mkdir(mode=0o700)  # Create directory with restricted permissions
    
    if not CONFIG_FILE.exists() or input("Existing credentials found. Reset? (y/N): ").lower() == 'y':
        api_key = getpass.getpass("Please enter your Attio API key: ")
        
        # Save credentials
        config = {'api_key': api_key}
        CONFIG_FILE.write_text(json.dumps(config))
        CONFIG_FILE.chmod(0o600)  # Restrict file permissions
        print("Credentials saved successfully!")
    
    return json.loads(CONFIG_FILE.read_text())['api_key']

def setup_google_auth():
    """Setup Google service account credentials and spreadsheet ID"""
    if not CREDENTIALS_FILE.exists():
        print("\nGoogle Sheets API setup required!")
        print("\nPlease place your service account JSON file at:")
        print(f"{CREDENTIALS_FILE}")
        raise FileNotFoundError(
            f"\nService account JSON file not found at: {CREDENTIALS_FILE}"
        )
    
    # Load or prompt for spreadsheet ID
    config_path = CONFIG_DIR / 'google_config.json'
    if not config_path.exists() or input("Existing Google config found. Reset? (y/N): ").lower() == 'y':
        print("\nPlease enter the ID of your Google Sheet.")
        print("(This is the long string of characters from the sheet's URL)")
        print("Example: 1GIWgo1kN0a-SnC7HndZH24zYz3eZr_FzcI8K7qFnjSE")
        spreadsheet_id = input("Spreadsheet ID: ").strip()
        
        # Save config
        config = {'spreadsheet_id': spreadsheet_id}
        config_path.write_text(json.dumps(config))
        config_path.chmod(0o600)
        print("Google config saved successfully!")
    else:
        config = json.loads(config_path.read_text())
        spreadsheet_id = config['spreadsheet_id']
    
    # Return both credentials and spreadsheet ID
    creds = service_account.Credentials.from_service_account_file(
        CREDENTIALS_FILE,
        scopes=['https://www.googleapis.com/auth/spreadsheets']
    )
    
    return creds, spreadsheet_id

def get_company_records(api_key, object_id, limit=25, offset=0):
    url = f"https://api.attio.com/v2/objects/{object_id}/records/query"
    
    headers = {
        "accept": "application/json",
        "content-type": "application/json",
        "authorization": f"Bearer {api_key}"
    }
    
    payload = {
        "limit": limit,
        "offset": offset,
        "sort": {
            "direction": "desc",
            "attribute": "created_at"
        }
    }

    print(f"\nFetching records from URL: {url}")
    print(f"With payload: {payload}")
    response = requests.post(url, json=payload, headers=headers)
    result = response.json()
    print(f"API Response: {result}")
    return result

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
        print(f"\nWarning: Unknown attribute type '{attribute_type}' for field '{field_name}'")
        return None

def get_list_records(api_key, list_id, limit=25, offset=0):
    """Fetch records from a specific list"""
    url = f"https://api.attio.com/v2/lists/{list_id}"
    
    headers = {
        "accept": "application/json",
        "authorization": f"Bearer {api_key}"
    }
    
    response = requests.get(url, headers=headers)
    return response.json()

def fetch_batch(params):
    """Helper function to fetch a single batch of records"""
    api_key, object_id, batch_size, offset = params
    print(f"\nFetching batch for object_id: {object_id}, offset: {offset}")
    
    max_retries = 3
    base_delay = 0.01  # 10ms delay
    
    for attempt in range(max_retries):
        try:
            result = get_company_records(api_key, object_id, limit=batch_size, offset=offset)
            print(f"Batch result: {result}")
            
            if 'error' in result:
                if result.get('status') == 429:  # Rate limit error
                    retry_after = float(result.get('retry_after', base_delay))
                    time.sleep(retry_after)
                    continue
                raise Exception(f"API Error: {result['error']}")
            
            if 'data' not in result:
                print(f"Unexpected response structure: {result}")
                raise Exception(f"Unexpected API response structure")
                
            records = []
            for record in result['data']:
                if 'values' not in record:
                    continue
                    
                try:
                    csv_data = {
                        'record_id': record['id']['record_id']
                    }
                    
                    for field_name, value_list in record['values'].items():
                        csv_data[field_name] = process_record_value(field_name, value_list)
                    
                    records.append(csv_data)
                    
                except Exception as e:
                    continue
            
            return records
            
        except Exception as e:
            if attempt == max_retries - 1:  # Last attempt
                raise
            time.sleep(base_delay)  # Exponential backoff
    
    return []  # If we somehow get here

def update_spreadsheet(creds, spreadsheet_id, records_df):
    """Update the existing Google Sheet with records"""
    print(f"Using spreadsheet ID: {spreadsheet_id}")
    try:
        service = build('sheets', 'v4', credentials=creds)
        
        # Clean the data
        records_df = records_df.replace({float('nan'): None})
        records_df = records_df.map(lambda x: str(x) if x is not None else '')
        
        # Prepare data for upload
        headers = records_df.columns.tolist()
        values = [headers] + records_df.values.tolist()
        
        # Clear existing data
        service.spreadsheets().values().clear(
            spreadsheetId=spreadsheet_id,
            range='A1:ZZ'  # Clear all data
        ).execute()
        
        # Update the spreadsheet with new data
        service.spreadsheets().values().update(
            spreadsheetId=spreadsheet_id,
            range='A1',
            valueInputOption='RAW',
            body={'values': values}
        ).execute()
        
        print(f"\nSpreadsheet updated: https://docs.google.com/spreadsheets/d/{spreadsheet_id}")
        
    except HttpError as error:
        print(f"\nError updating spreadsheet: {error}")

def get_objects(api_key):
    """Fetch available objects from Attio"""
    url = "https://api.attio.com/v2/objects"
    headers = {
        "accept": "application/json",
        "authorization": f"Bearer {api_key}"
    }
    
    response = requests.get(url, headers=headers)
    return response.json().get('data', [])

def select_object(api_key):
    """Display objects and let user select one"""
    print("\nFetching available objects...")
    objects = get_objects(api_key)
    
    if not objects:
        raise Exception("No objects found in workspace")
    
    print("\nAvailable objects:")
    for i, obj in enumerate(objects, 1):
        print(f"{i}. {obj['plural_noun']} ({obj['api_slug']})")
    
    while True:
        try:
            choice = int(input("\nSelect an object (enter number): "))
            if 1 <= choice <= len(objects):
                selected = objects[choice - 1]
                print(f"\nSelected: {selected['plural_noun']}")
                return selected['api_slug']
            else:
                print("Invalid selection. Please try again.")
        except ValueError:
            print("Please enter a number.")

def get_lists(api_key):
    """Fetch available lists from Attio"""
    url = "https://api.attio.com/v2/lists"
    headers = {
        "accept": "application/json",
        "authorization": f"Bearer {api_key}"
    }
    
    response = requests.get(url, headers=headers)
    data = response.json()
    print("\nAPI Response:", data)  # Simple print to see the actual response
    return data.get('data', [])

def select_list(api_key):
    """Display lists and let user select one"""
    print("\nFetching available lists...")
    lists = get_lists(api_key)
    
    if not lists:
        raise Exception("No lists found in workspace")
    
    print("\nAvailable lists:")
    for i, lst in enumerate(lists, 1):
        parent = f" ({', '.join(lst['parent_object'])})" if lst['parent_object'] else ""
        print(f"{i}. {lst['name']}{parent}")
        print(f"Debug - List {i}:", lst)
    
    while True:
        try:
            choice = int(input("\nSelect a list (enter number): "))
            if 1 <= choice <= len(lists):
                selected = lists[choice - 1]
                print(f"\nSelected: {selected['name']}")
                # Return both the parent object and the list's api_slug
                return selected['parent_object'][0], selected['api_slug']
            else:
                print("Invalid selection. Please try again.")
        except ValueError:
            print("Please enter a number.")

def get_list_entries(api_key, list_id, record_ids=None):
    """Fetch entries for a specific list with optional filtering"""
    url = f"https://api.attio.com/v2/lists/{list_id}/entries/query"
    headers = {
        'accept': 'application/json',
        'authorization': f'Bearer {api_key}',
        'content-type': 'application/json'
    }
    
    # Build the query payload
    payload = {}
    if record_ids:
        payload["filter"] = {
            "path": [
                [list_id, "parent_record"]
            ],
            "constraints": {
                "record_id": {
                    "in": record_ids
                }
            }
        }
    
    print(f"\nFetching list entries...")
    print(f"Using payload: {json.dumps(payload, indent=2)}")
    
    response = requests.post(url, json=payload, headers=headers)
    result = response.json()
    
    if response.status_code == 200:
        entries = result['data']
        print(f"✓ Found {len(entries)} entries")
        
        # Log sample entry structure
        if entries:
            first_entry = entries[0]
            print("\nSample entry structure:")
            print(f"- Parent Record ID: {first_entry['parent_record_id']}")
            print(f"- Entry Values:")
            for key in first_entry['entry_values'].keys():
                print(f"  • {key}")
        return entries
    else:
        print(f"! Error {response.status_code}: {result}")
        return None

def process_records_to_csv(api_key, google_creds, spreadsheet_id, object_id, list_id=None):
    """Process records and upload to Google Sheets"""
    print("\nStarting record processing...")
    
    def process_list_value(value_obj):
        """Extract the appropriate value from a list entry value object"""
        if not value_obj:
            return None
            
        attr_type = value_obj.get("attribute_type")
        
        if attr_type == "status":
            return value_obj.get("status", {}).get("title")
        elif attr_type == "select":
            return value_obj.get("option", {}).get("title")
        elif attr_type == "currency":
            return value_obj.get("currency_value")
        elif attr_type == "rating":
            return value_obj.get("value")
        elif attr_type == "date":
            return value_obj.get("value")
        elif attr_type == "text":
            return value_obj.get("value")
        elif attr_type == "timestamp":
            return value_obj.get("value")
        elif attr_type == "record-reference":
            return value_obj.get("target_record_id")
        elif attr_type == "actor-reference":
            return value_obj.get("referenced_actor_id")
        else:
            return None

    if list_id:
        # Get list entries
        entries = get_list_entries(api_key, list_id)
        if not entries:
            print("No entries found in list")
            return
            
        # Get all parent record IDs
        parent_record_ids = [entry['parent_record_id'] for entry in entries]
        
        # Fetch all parent records
        print(f"\nFetching {len(parent_record_ids)} parent records...")
        result = get_company_records(api_key, object_id, limit=len(parent_record_ids))
        parent_records = result.get('data', [])
        
        # Create a map of record_id to record values
        parent_record_map = {
            record['id']['record_id']: record['values']
            for record in parent_records
        }
        
        # Process both parent records and list entries
        rows = []
        for entry in entries:
            row = {}
            parent_record_id = entry['parent_record_id']
            
            # Add parent record values
            if parent_record_id in parent_record_map:
                for attr_name, values in parent_record_map[parent_record_id].items():
                    row[attr_name] = process_record_value(attr_name, values)
            
            # Add list entry values with 'list_' prefix
            for attr_name, values in entry['entry_values'].items():
                if isinstance(values, list) and values:
                    row[f"list_{attr_name}"] = process_list_value(values[0])
            
            # Add list entry metadata
            row['list_entry_id'] = entry['id']['entry_id']
            row['list_created_at'] = entry['created_at']
            
            rows.append(row)
    else:
        # Handle regular records (existing code)
        result = get_company_records(api_key, object_id)
        records = result.get('data', [])
        
        if not records:
            print("No records found")
            return
            
        rows = []
        for record in records:
            row = {}
            for attr_name, values in record['values'].items():
                row[attr_name] = process_record_value(attr_name, values)
            rows.append(row)

    # Convert rows to DataFrame and upload
    print("\nConverting records to DataFrame...")
    df = pd.DataFrame(rows)
    print(f"Created DataFrame with {len(df)} rows and {len(df.columns)} columns")
    
    print("\nUploading to Google Sheets...")
    update_spreadsheet(google_creds, spreadsheet_id, df)

def get_record(api_key, object_id, record_id):
    """Fetch a single record by ID"""
    url = f"https://api.attio.com/v2/objects/{object_id}/records/{record_id}"
    headers = {
        'accept': 'application/json',
        'authorization': f'Bearer {api_key}'
    }
    
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()  # Raise an exception for bad status codes
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error fetching record {record_id}: {e}")
        return None

# For local script execution
if __name__ == "__main__":
    print("Attio Records Exporter")
    print("--------------------")
    
    while True:
        export_type = input("\nDo you want to export (1) objects or (2) lists? Enter 1 or 2: ").strip()
        if export_type in ['1', '2']:
            break
        print("Invalid selection. Please enter 1 or 2.")
    
    api_key = setup_credentials()
    google_creds, spreadsheet_id = setup_google_auth()
    
    if export_type == '1':
        object_id = select_object(api_key)
        process_records_to_csv(api_key, google_creds, spreadsheet_id, object_id)
    else:
        parent_object, list_id = select_list(api_key)
        process_records_to_csv(api_key, google_creds, spreadsheet_id, parent_object, list_id)
