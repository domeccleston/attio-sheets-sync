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
  const token = ScriptApp.getOAuthToken();
  const sheetId = SpreadsheetApp.getActiveSpreadsheet().getId();

  const cloudFunctionUrl = "YOUR_CLOUD_FUNCTION_URL";

  UrlFetchApp.fetch(cloudFunctionUrl, {
    method: "post",
    contentType: "application/json",
    payload: JSON.stringify({
      token,
      sheetId,
      apiKey: getApiKey(),
    }),
  });
}

function doGet(e) {
  return HtmlService.createHtmlOutput(
    "This add-on is meant to be used within Google Sheets."
  );
}
