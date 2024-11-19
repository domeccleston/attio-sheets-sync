function onOpen() {
  SpreadsheetApp.getUi()
    .createMenu("Sync")
    .addItem("Sync with Attio", "syncWithAttio")
    .addItem("Configure API Key", "promptForApiKey")
    .addItem("Show Available Lists", "showLists")
    .addToUi();
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

function fetchCompany(recordId) {
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
      `https://api.attio.com/v2/objects/companies/records/${recordId}`,
      options
    );
    return JSON.parse(response.getContentText());
  } catch (error) {
    console.error("Error fetching company:", error);
    return null;
  }
}

function extractCompanyValue(value) {
  if (!value || !value.length) return "";

  const firstValue = value[0];

  switch (firstValue.attribute_type) {
    case "domain":
      return firstValue.domain || "";
    case "select":
      return firstValue.option?.title || "";
    case "text":
      return firstValue.value || "";
    case "number":
      return firstValue.value || "";
    case "date":
      return firstValue.value || "";
    default:
      return firstValue.value || "";
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

function fetchListEntries(workspaceId, listId) {
  const apiKey = getApiKey();
  if (!apiKey) return null;

  const options = {
    method: "post",
    headers: {
      accept: "application/json",
      authorization: `Bearer ${apiKey}`,
      "content-type": "application/json",
    },
    muteHttpExceptions: true,
    payload: JSON.stringify({}),
  };

  try {
    const response = UrlFetchApp.fetch(
      `https://api.attio.com/v2/lists/${listId}/entries/query`,
      options
    );
    console.log(response.getContentText());
    return JSON.parse(response.getContentText());
  } catch (error) {
    SpreadsheetApp.getActive().toast(
      "Error fetching list entries: " + error.toString(),
      "Error",
      10
    );
    return null;
  }
}

function extractValue(value) {
  if (!value) return "";

  switch (value.attribute_type) {
    case "status":
      return value.status?.title || "";

    case "select":
      return value.option?.title || "";

    case "currency":
      return value.currency_value
        ? `${value.currency_value} ${value.currency_code}`
        : "";

    case "location":
      const parts = [
        value.line_1,
        value.line_2,
        value.locality,
        value.region,
        value.country_code,
      ].filter((part) => part);
      return parts.join(", ");

    case "record-reference":
      return value.target_record_id || "";

    case "actor-reference":
      return value.referenced_actor_id || "";

    case "timestamp":
    case "date":
    case "text":
    case "number":
    default:
      return value.value || "";
  }
}

function fetchWorkspaceMember(memberId) {
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
      `https://api.attio.com/v2/workspace_members/${memberId}`,
      options
    );
    return JSON.parse(response.getContentText());
  } catch (error) {
    console.error("Error fetching workspace member:", error);
    return null;
  }
}

function writeEntriesToSheet(entries, listName) {
  const sheet = SpreadsheetApp.getActiveSheet();

  if (!entries.data || entries.data.length === 0) {
    SpreadsheetApp.getActive().toast("No entries found in list", "Info");
    return;
  }

  // Find company references and fetch company data
  const companies = new Map();
  entries.data.forEach((entry) => {
    if (entry.parent_object === "companies" && entry.parent_record_id) {
      const companyId = entry.parent_record_id;
      if (!companies.has(companyId)) {
        const companyData = fetchCompany(companyId);
        console.log(
          "Company data for ID",
          companyId,
          ":",
          JSON.stringify(companyData)
        );
        if (companyData) {
          companies.set(companyId, companyData.data);
        }
      }
    }
  });

  // Define which company fields we want
  const companyFields = [
    "name",
    "domains",
    "description",
    "categories",
    "primary_location",
    "estimated_arr_usd",
    "funding_raised_usd",
    "employee_range",
  ];

  // Add cache for workspace members to avoid duplicate API calls
  const workspaceMembers = new Map();

  // Get all fields including company fields
  const fields = new Set();
  const metaFields = ["parent_record_id", "parent_object", "created_at"];

  // Add regular fields
  entries.data.forEach((entry) => {
    Object.keys(entry.entry_values).forEach((field) => fields.add(field));
  });

  // Add metadata fields
  metaFields.forEach((field) => fields.add(field));

  // Add company fields for each company field we want
  companyFields.forEach((field) => fields.add(`company_${field}`));

  // Add owner and creator names to the fields we track
  fields.add("owner");
  fields.add("created_by");

  const fieldNames = Array.from(fields).sort();

  // Clear and set headers
  sheet.clear();
  sheet.getRange(1, 1, 1, fieldNames.length).setValues([fieldNames]);

  // Prepare rows
  const rows = entries.data.map((entry) => {
    return fieldNames.map((field) => {
      // Handle owner
      if (field === "owner") {
        const ownerId = entry.entry_values.owner?.[0]?.referenced_actor_id;
        if (ownerId) {
          if (!workspaceMembers.has(ownerId)) {
            const memberData = fetchWorkspaceMember(ownerId);
            if (memberData?.data) {
              workspaceMembers.set(ownerId, memberData.data);
            }
          }
          const member = workspaceMembers.get(ownerId);
          return member ? `${member.first_name} ${member.last_name}` : "";
        }
        return "";
      }

      // Handle created_by
      if (field === "created_by") {
        const creatorId =
          entry.entry_values.created_by?.[0]?.referenced_actor_id;
        if (creatorId) {
          if (!workspaceMembers.has(creatorId)) {
            const memberData = fetchWorkspaceMember(creatorId);
            if (memberData?.data) {
              workspaceMembers.set(creatorId, memberData.data);
            }
          }
          const member = workspaceMembers.get(creatorId);
          return member ? `${member.first_name} ${member.last_name}` : "";
        }
        return "";
      }

      // Handle company fields
      if (field.startsWith("company_")) {
        const companyId = entry.parent_record_id;
        if (companyId && companies.has(companyId)) {
          const company = companies.get(companyId);
          const companyField = field.replace("company_", "");
          return extractCompanyValue(company.values[companyField]);
        }
        return "";
      }

      // Handle metadata fields
      if (metaFields.includes(field)) {
        return entry[field] || "";
      }

      // Handle entry_values fields
      const values = entry.entry_values[field];
      if (!values || values.length === 0) return "";

      if (values.length > 1) {
        return values
          .map((v) => extractValue(v))
          .filter((v) => v)
          .join("; ");
      }

      return extractValue(values[0]);
    });
  });

  // Write data
  if (rows.length > 0) {
    const dataRange = sheet.getRange(2, 1, rows.length, fieldNames.length);
    dataRange.setValues(rows);
    
    // Set column formats based on Attio attribute types
    fieldNames.forEach((field, columnIndex) => {
      const column = columnIndex + 1;
      const range = sheet.getRange(2, column, rows.length);
      
      // Get the attribute type from the field name or data
      const attributeType = getAttributeType(field); // You'll need to implement this

      switch (attributeType) {
        case 'timestamp':
          range.setNumberFormat('yyyy-mm-dd hh:mm:ss');
          break;
          
        case 'date':
          range.setNumberFormat('yyyy-mm-dd');
          break;
          
        case 'currency':
          range.setNumberFormat('$#,##0.00');
          break;
          
        case 'number':
          range.setNumberFormat('#,##0.00');
          break;
          
        case 'phone_number':
          range.setNumberFormat('@'); // Force text format
          break;
          
        case 'rating':
          range.setNumberFormat('0.0');
          break;
          
        case 'checkbox':
          range.setNumberFormat('boolean');
          break;
          
        case 'email_address':
        case 'domain':
        case 'text':
        case 'select':
        case 'status':
        case 'actor_reference':
        case 'record_reference':
        case 'personal_name':
        case 'location':
        case 'interaction':
          range.setNumberFormat('@'); // Force text format
          break;
      }
    });
  }

  // Format
  sheet.getRange(1, 1, 1, fieldNames.length).setFontWeight("bold");
  sheet.autoResizeColumns(1, fieldNames.length);

  SpreadsheetApp.getActive().toast(
    `✅ Written ${rows.length} entries with company data to sheet`,
    listName
  );
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
        cursor: pointer;
      }
      .list-item:hover { 
        background-color: #f5f5f5; 
      }
    </style>
    <script>
      function importList(workspaceId, listId, listName) {
        google.script.run
          .withSuccessHandler(() => {
            google.script.host.close();
          })
          .importListToSheet(workspaceId, listId, listName);
      }
    </script>
    <h2>Your Attio Lists</h2>
    <div id="lists">
      ${lists.data
        .map(
          (list) => `
        <div class="list-item" onclick="importList('${list.id.workspace_id}', '${list.id.list_id}', '${list.name}')">
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

function importListToSheet(workspaceId, listId, listName) {
  const entries = fetchListEntries(workspaceId, listId);
  if (!entries) return;

  writeEntriesToSheet(entries, listName);
}

function doGet(e) {
  return HtmlService.createHtmlOutput(
    "This add-on is meant to be used within Google Sheets."
  );
}

// Additional formatting options you could add
function applyVisualFormatting(range, attributeType) {
  switch (attributeType) {
    case 'email_address':
      range.setFontColor('#1155cc')  // Blue for emails
           .setTextStyle(SpreadsheetApp.newTextStyle().setUnderline(true).build());
      break;
      
    case 'status':
    case 'select':
      range.setBackground('#f3f3f3');  // Light gray for categorical data
      break;
      
    case 'currency':
      range.setHorizontalAlignment('right')  // Right-align numbers
           .setBackground('#eef6e6');  // Light green for currency
      break;
      
    case 'checkbox':
      range.setHorizontalAlignment('center');
      break;
  }
}
