from google.oauth2 import service_account
from googleapiclient.discovery import build
import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

def test_write():
    try:
        spreadsheet_id = os.getenv('GOOGLE_SPREADSHEET_ID')
        
        # Load service account credentials
        credentials_path = Path(__file__).parent / 'credentials' / 'credentials.json'
        credentials = service_account.Credentials.from_service_account_file(
            credentials_path,
            scopes=['https://www.googleapis.com/auth/spreadsheets']
        )
        
        # Build the Sheets service
        service = build('sheets', 'v4', credentials=credentials)
        
        # Prepare test data
        body = {
            'values': [
                ['Test Column 1', 'Test Column 2'],
                ['Hello', 'World']
            ]
        }
        
        # Write to spreadsheet
        result = service.spreadsheets().values().update(
            spreadsheetId=spreadsheet_id,
            range='A1',
            valueInputOption='RAW',
            body=body
        ).execute()
        
        print(f"Success! Updated {result.get('updatedCells')} cells")
        
    except Exception as e:
        print(f"Error: {str(e)}")

if __name__ == "__main__":
    test_write()
