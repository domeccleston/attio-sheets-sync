# Attio Sheets Sync

Proof of concept app for one-way sync between Attio and a Google Sheet. `/app` contains an Apps Script script which adds some UI to Google Sheets enabling you to add an API key and pull in Object or List
data. This script makes requests to v2 Cloud Function defined in `/backend` which fetches records
from the Attio in parallel and uploads them in batches to the Google Sheet. This handled a test
dataset of 50k records and 40 attributes, though this was quite slow (~8 minutes). More fleshed out
implementation would have the ability to run this on a schedule.

The use cases this is designed for are
- Giving contractors readonly access to Attio lists
- Giving finance or sales teams the ability to do data analysis in Sheets (or connected apps like Looker)

