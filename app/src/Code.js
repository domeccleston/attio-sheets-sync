function onOpen(e) {
  // Note: add 'e' parameter
  const ui = SpreadsheetApp.getUi();
  const menu = ui.createMenu("Sync");

  // Check if we're in LIMITED auth mode
  if (e && e.authMode == ScriptApp.AuthMode.LIMITED) {
    menu.addItem("Setup Attio Sync", "authorize");
    menu.addToUi();
    return;
  }

  const isReset =
    PropertiesService.getUserProperties().getProperty("resetRequested") ===
    "true";

  if (isReset) {
    menu.addItem("Setup Attio Sync", "authorize");
  } else {
    menu
      .addItem("Sync with Attio", "syncWithAttio")
      .addItem("Configure API Key", "promptForApiKey")
      .addItem("Show Available Lists", "showLists")
      .addSeparator()
      .addItem("Reset Authorization", "resetAuth");
  }

  menu.addToUi();
}

function resetAuth() {
  const ui = SpreadsheetApp.getUi();

  PropertiesService.getUserProperties().setProperty("resetRequested", "true");
  PropertiesService.getUserProperties().deleteProperty("ATTIO_API_KEY");

  ui.alert(
    "Authorization Reset",
    "To complete reset, please open:\nGoogle Account Settings > Security > Third-party apps with account access\n\nFind this script and remove access.",
    ui.ButtonSet.OK
  );

  onOpen();
}

function authorize() {
  const ui = SpreadsheetApp.getUi();

  // Clear reset state before starting auth
  PropertiesService.getUserProperties().deleteProperty("resetRequested");

  // Trigger auth flow
  ScriptApp.getOAuthToken();

  // After auth, rebuild menu
  onOpen();

  ui.alert(
    "Setup Complete",
    "Authorization successful! You can now use Attio Sync features.",
    ui.ButtonSet.OK
  );
}

function promptForApiKey() {
  const ui = SpreadsheetApp.getUi();
  const response = ui.prompt(
    "Attio API Key Configuration",
    "Please enter your Attio API key:",
    ui.ButtonSet.OK_CANCEL
  );

  if (response.getSelectedButton() == ui.Button.OK) {
    const apiKey = response.getResponseText().trim();
    if (apiKey) {
      PropertiesService.getUserProperties().setProperty(
        "ATTIO_API_KEY",
        apiKey
      );
      ui.alert("API Key saved successfully!");
    } else {
      ui.alert("Error", "API key cannot be empty", ui.ButtonSet.OK);
    }
  }
}

function getApiKey() {
  const apiKey =
    PropertiesService.getUserProperties().getProperty("ATTIO_API_KEY");
  if (!apiKey) {
    const ui = SpreadsheetApp.getUi();
    ui.alert(
      "API Key Required",
      'Please configure your Attio API key first using the "Configure API Key" menu option.',
      ui.ButtonSet.OK
    );
    return null;
  }
  return apiKey;
}

function fetchAttioLists() {
  const apiKey = getApiKey();
  if (!apiKey) return null;

  const options = {
    method: "get",
    headers: {
      accept: "application/json",
      authorization: `Bearer ${apiKey}`,
    },
    muteHttpExceptions: true,
  };

  try {
    const response = UrlFetchApp.fetch(
      "https://api.attio.com/v2/lists",
      options
    );
    return JSON.parse(response.getContentText());
  } catch (error) {
    SpreadsheetApp.getActive().toast(
      "Error fetching lists: " + error.toString(),
      "Error",
      10
    );
    return null;
  }
}

function showLists() {
  const lists = fetchAttioLists();
  if (!lists) return;

  const html = HtmlService.createHtmlOutput(
    `
    <style>
      body { font-family: Arial, sans-serif; padding: 20px; }
      .list-item { 
        padding: 10px; 
        border-bottom: 1px solid #eee; 
      }
      .list-item:hover { 
        background-color: #f5f5f5; 
      }
    </style>
    <h2>Your Attio Lists</h2>
    <div id="lists">
      ${lists.data
        .map(
          (list) => `
        <div class="list-item">
          ${list.name}
        </div>
      `
        )
        .join("")}
    </div>
  `
  )
    .setWidth(400)
    .setHeight(500);

  SpreadsheetApp.getUi().showModalDialog(html, "Available Attio Lists");
}

function syncWithAttio() {
  const apiKey = getApiKey();
  if (!apiKey) return; // Already handles UI alert
  const html = HtmlService.createHtmlOutput(`
  <div class="container">
    <div class="spinner"></div>
    <div id="status">
      <p>Starting sync...</p>
      <p class="detail">This may take a few minutes</p>
    </div>
  </div>

  <style>
    .container {
      text-align: center;
      padding: 20px;
      font-family: Arial, sans-serif;
    }
    .spinner {
      border: 3px solid #f3f3f3;
      border-top: 3px solid #3498db;
      border-radius: 50%;
      width: 30px;
      height: 30px;
      margin: 20px auto;
      animation: spin 1s linear infinite;
    }
    .detail {
      color: #666;
      font-size: 0.9em;
      margin-top: 8px;
    }
    @keyframes spin {
      0% { transform: rotate(0deg); }
      100% { transform: rotate(360deg); }
    }
    p {
      margin: 8px 0;
    }
  </style>

  <script>
    setTimeout(() => {
      document.getElementById('status').innerHTML = 
        '<p>Sync started!</p><p class="detail">Your sheet will update shortly.</p>';
      setTimeout(() => google.script.host.close(), 1000);
    }, 3000);
  </script>
`);

  // Get required data
  const token = ScriptApp.getOAuthToken();
  const spreadsheet = SpreadsheetApp.getActiveSpreadsheet();

  const payload = {
    attioApiKey: apiKey,
    googleToken: token,
    spreadsheetId: spreadsheet.getId(),
    spreadsheetName: spreadsheet.getName(),
    userEmail: Session.getEffectiveUser().getEmail(),
    timestamp: new Date().toISOString(),
  };

  // Call Cloud Function
  UrlFetchApp.fetch("YOUR_CLOUD_FUNCTION_URL", {
    method: "post",
    contentType: "application/json",
    payload: JSON.stringify(payload),
  });

  SpreadsheetApp.getUi().showModalDialog(html, "Syncing with Attio");
}

function doGet(e) {
  return HtmlService.createHtmlOutput(
    "This add-on is meant to be used within Google Sheets."
  );
}
