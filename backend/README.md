# Requirements

1. Google Cloud CLI
2. PDM to manage Python virtual environments and packages (`brew install pdm`)
3. A service account set up with authorization to read from and write to the Google Sheets API

After deploying, you should add the URL as the path in `./app/src/Code.js`.

This also contains a script `cli.py` that allows you to handle syncing data from the CLI, rather than 
installing an Apps Script app.