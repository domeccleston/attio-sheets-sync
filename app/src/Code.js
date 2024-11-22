function onOpen(e) {
  const ui = SpreadsheetApp.getUi();
  const menu = ui.createMenu("Sync");

  if (e && e.authMode == ScriptApp.AuthMode.LIMITED) {
    menu.addItem("Setup Attio Sync", "authorize");
    menu.addToUi();
    return;
  }

  menu
    .addItem("Sync with Attio", "showSelector")
    .addItem("Configure API Key", "promptForApiKey")
    .addSeparator()
    .addItem("Refresh Google Token", "refreshGoogleToken");

  menu.addToUi();
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

function fetchAttioObjects() {
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
      "https://api.attio.com/v2/objects",
      options
    );
    return JSON.parse(response.getContentText());
  } catch (error) {
    SpreadsheetApp.getActive().toast(
      "Error fetching objects: " + error.toString(),
      "Error",
      10
    );
    return null;
  }
}

function showSelector() {
  const objects = fetchAttioObjects();
  const lists = fetchAttioLists();
  if (!objects || !lists) return;

  const html = HtmlService.createHtmlOutput(
    `
    <style>
      body { font-family: Arial, sans-serif; padding: 20px; }
      .selector-group {
        margin-bottom: 20px;
      }
      select { 
        width: 100%;
        padding: 8px;
        margin: 10px 0;
      }
      button {
        background: #4285f4;
        color: white;
        border: none;
        padding: 10px 20px;
        border-radius: 4px;
        cursor: pointer;
        width: 100%;
      }
      .type-select {
        margin-bottom: 15px;
      }
      #listSelect, #objectSelect {
        display: none;
      }
    </style>
    <h2>Select Data to Sync</h2>
    
    <div class="type-select">
      <select id="typeSelect" onchange="toggleSelectors()">
        <option value="">Select type...</option>
        <option value="object">Object</option>
        <option value="list">List</option>
      </select>
    </div>

    <div id="objectSelect" class="selector-group">
      <h3>Select Object</h3>
      <select id="objectDropdown">
        ${objects.data
          .map(
            (obj) => `
          <option value="${obj.api_slug}|">${obj.plural_noun}</option>
        `
          )
          .join("")}
      </select>
    </div>

    <div id="listSelect" class="selector-group">
      <h3>Select List</h3>
      <select id="listDropdown">
        ${lists.data
          .map(
            (list) => `
          <option value="${list.api_slug}|${list.parent_object[0]}">${list.name}</option>
        `
          )
          .join("")}
      </select>
    </div>

    <button onclick="startSync()" id="syncButton" disabled>Start Sync</button>

    <script>
      function toggleSelectors() {
        const type = document.getElementById('typeSelect').value;
        document.getElementById('objectSelect').style.display = type === 'object' ? 'block' : 'none';
        document.getElementById('listSelect').style.display = type === 'list' ? 'block' : 'none';
        document.getElementById('syncButton').disabled = !type;
      }

      function startSync() {
        const type = document.getElementById('typeSelect').value;
        const value = type === 'object' 
          ? document.getElementById('objectDropdown').value 
          : document.getElementById('listDropdown').value;
        
        google.script.run
          .withSuccessHandler(() => google.script.host.close())
          .startAttioSync(value, type);
      }
    </script>
  `
  )
    .setWidth(400)
    .setHeight(500);

  SpreadsheetApp.getUi().showModalDialog(html, "Select Data to Sync");
}

function startAttioSync(value, type) {
  const apiKey = getApiKey();
  if (!apiKey) return;

  const [apiSlug, parentObject] = value.split("|");

  const spreadsheet = SpreadsheetApp.getActiveSpreadsheet();

  const payload = {
    attioApiKey: apiKey,
    resourceName: apiSlug,
    parentObject: type === "list" ? parentObject : null,
    resourceType: type,
    spreadsheetId: spreadsheet.getId(),
  };

  UrlFetchApp.fetch("<DEPLOYED_FUNCTION_URL>", {
    method: "post",
    contentType: "application/json",
    payload: JSON.stringify(payload),
  });

  showSyncProgress();
}

function doGet(e) {
  return HtmlService.createHtmlOutput(
    "This add-on is meant to be used within Google Sheets."
  );
}

function authorize() {
  const ui = SpreadsheetApp.getUi();
  try {
    ScriptApp.getOAuthToken();
    onOpen();
  } catch (e) {
    ui.alert(
      "Authorization Required",
      "Please authorize this add-on to access your spreadsheet.",
      ui.ButtonSet.OK
    );
  }
}

function refreshGoogleToken() {
  const ui = SpreadsheetApp.getUi();
  try {
    const newToken = ScriptApp.getOAuthToken();
    ui.alert(
      "Success",
      "Token refreshed successfully. Please try your sync operation again.",
      ui.ButtonSet.OK
    );
    return newToken;
  } catch (e) {
    ui.alert(
      "Error",
      "Failed to refresh token: " + e.toString(),
      ui.ButtonSet.OK
    );
  }
}
