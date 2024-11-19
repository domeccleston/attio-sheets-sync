Brain dumping some thoughts here

- The goal of this is to recreate Attio views in Google Sheets
- I will start with Lists, then move on to Objects
- There are a few distinctions between the two. Firstly, Lists are
  subsets of some of the records of some object type. Secondly they don't have 
  relationship attributes, just record references, which are one-way: don't think
  this matters in our case since we aren't dealing with live data sync. Third, 
  lists have a different API for retrieving records than objects do.

I'm starting with Lists primarily because the initial customer request for this
came from someone who needed to share a list with a single contractor. However,
since then I got a lot of interest internally from sales and finance people that
want to export data to a Google Sheet in order to use it for reporting etc. This
is now the primary driver of interest in the tool so I want to pivot to that.

The way this works currently is that the user will add an API key, and then
click a button which will sync a list to the sheet. 
I will load what appears to be all of the attributes defined
on that list, as well as all of the company attributes linked. So currently I'm
assuming that we're dealing with a list of companies, but that's not a safe
assumption, it could be any kind of list. I load the linked company attributes
and preface them with company_-. This will be written to the current page in the
spreadsheet. It's then possible for users to create other pages that query the first.

After I can support any list type I'd like to support objects. This would mean:

- Add new option in UI to select object rather than list
- Add new flow within to query objectss API rather than list entries API
- This will require handling of different data shape

A second question is how to handle showing the right attributes to the user. My
preferred approach is to just load all of the data, and then handle attribute
selection via filters in other pages of the sheet. This means that there's no need
for the user to manually select attributes up front which is a pain, especially
if they realize later that they need more data. It does mean that they need to figure out how to create views with the relevant data but that's a solvable problem.

You could even have an option for attribute selection but rather than being for
deciding what to query, it just generates the query syntax for you. But that's for later. 

One issue here is dealing with lots of records. From the website:

Attio's API rate limits are 100 requests per second for read requests and 25 requests per second for write requests. Attio may temporarily or permanently reduce the rate limit for certain APIs or during an incident to protect the platform. 

That's pretty generous. For 50,0000 list entries, as it stands I'm doing 3 reqs per entry (entry, company, user) so this would be 150,000 reqs. That would take 1500
seconds or 25 minutes – which is quite slow actually. However, you would only need
to do this once. For very large lists like that you would probably want a different
approach with a CSV export first, then 'enriching' it from Attio. It's unlikely
we'd want to work with such large numbers in reality. For a check:

- Attio's Deals object has 2,225 active Deals
- Attio's Workspaces object has 9,311 Workspaces in Active or Trial

This isn't going to be suitable for historical data analysis, you'd need BigQuery
for that. However in sales or finance you're mostly interested in the last quarter
or the last year. I need to meet with Roberto and understand what kind of filters
he needs.

## Lists API response

{
  "data": [
    {
      "id": {
        "workspace_id": "515117c4-5fd1-4bfd-bc63-58f639d3f357",
        "list_id": "030f5287-761d-42ef-9feb-7d2e9a1ba52b",
        "entry_id": "05ed19c6-381c-4593-b1cf-fb298549781f"
      },
      "parent_record_id": "f99c571b-3b2f-4059-a1b7-5ce3324a5dec",
      "parent_object": "companies",
      "created_at": "2024-11-12T12:01:10.798000000Z",
      "entry_values": {
        "stage": [
          {
            "active_from": "2024-11-12T12:01:10.798000000Z",
            "active_until": null,
            "created_by_actor": {
              "type": "workspace-member",
              "id": "bbe415be-7a1d-45c7-9a8b-2af7b3cc962a"
            },
            "status": {
              "id": {
                "workspace_id": "515117c4-5fd1-4bfd-bc63-58f639d3f357",
                "object_id": "030f5287-761d-42ef-9feb-7d2e9a1ba52b",
                "attribute_id": "1a04f7e7-9392-40cb-9071-b1024f2eec73",
                "status_id": "10e0b809-893f-438a-a6a4-d69153c38ddc"
              },
              "title": "Prospecting",
              "is_archived": false,
              "target_time_in_status": null,
              "celebration_enabled": false
            },
            "attribute_type": "status"
          }
        ],
        "entry_id": [
          {
            "active_from": "2024-11-12T12:01:10.798000000Z",
            "active_until": null,
            "created_by_actor": {
              "type": "workspace-member",
              "id": "bbe415be-7a1d-45c7-9a8b-2af7b3cc962a"
            },
            "value": "05ed19c6-381c-4593-b1cf-fb298549781f",
            "attribute_type": "text"
          }
        ],
        "main_point_of_contact": [],
        "owner": [
          {
            "active_from": "2024-11-12T12:01:10.798000000Z",
            "active_until": null,
            "created_by_actor": {
              "type": "workspace-member",
              "id": "bbe415be-7a1d-45c7-9a8b-2af7b3cc962a"
            },
            "referenced_actor_type": "workspace-member",
            "referenced_actor_id": "bbe415be-7a1d-45c7-9a8b-2af7b3cc962a",
            "attribute_type": "actor-reference"
          }
        ],
        "priority": [],
        "estimated_contract_value": [],
        "projected_close_date": [
          {
            "active_from": "2024-11-12T12:01:10.798000000Z",
            "active_until": null,
            "created_by_actor": {
              "type": "workspace-member",
              "id": "bbe415be-7a1d-45c7-9a8b-2af7b3cc962a"
            },
            "value": "2024-11-26",
            "attribute_type": "date"
          }
        ],
        "close_confidence": [],
        "close_lost_reason": [],
        "notes": [],
        "created_at": [
          {
            "active_from": "2024-11-12T12:01:10.798000000Z",
            "active_until": null,
            "created_by_actor": {
              "type": "workspace-member",
              "id": "bbe415be-7a1d-45c7-9a8b-2af7b3cc962a"
            },
            "value": "2024-11-12T12:01:10.831000000Z",
            "attribute_type": "timestamp"
          }
        ],
        "created_by": [
          {
            "active_from": "2024-11-12T12:01:10.798000000Z",
            "active_until": null,
            "created_by_actor": {
              "type": "workspace-member",
              "id": "bbe415be-7a1d-45c7-9a8b-2af7b3cc962a"
            },
            "referenced_actor_type": "workspace-member",
            "referenced_actor_id": "bbe415be-7a1d-45c7-9a8b-2af7b3cc962a",
            "attribute_type": "actor-reference"
          }
        ],
        "deal_name": [],
        "company": []
      }
    },
    {
      "id": {
        "workspace_id": "515117c4-5fd1-4bfd-bc63-58f639d3f357",
        "list_id": "030f5287-761d-42ef-9feb-7d2e9a1ba52b",
        "entry_id": "14382145-26a5-4258-a6c5-ed11cf448b9b"
      },
      "parent_record_id": "8d8934b4-6545-4a6e-bdb8-ae9593458982",
      "parent_object": "companies",
      "created_at": "2024-11-12T12:01:08.261000000Z",
      "entry_values": {
        "stage": [
          {
            "active_from": "2024-11-12T12:01:08.261000000Z",
            "active_until": null,
            "created_by_actor": {
              "type": "workspace-member",
              "id": "bbe415be-7a1d-45c7-9a8b-2af7b3cc962a"
            },
            "status": {
              "id": {
                "workspace_id": "515117c4-5fd1-4bfd-bc63-58f639d3f357",
                "object_id": "030f5287-761d-42ef-9feb-7d2e9a1ba52b",
                "attribute_id": "1a04f7e7-9392-40cb-9071-b1024f2eec73",
                "status_id": "10e0b809-893f-438a-a6a4-d69153c38ddc"
              },
              "title": "Prospecting",
              "is_archived": false,
              "target_time_in_status": null,
              "celebration_enabled": false
            },
            "attribute_type": "status"
          }
        ],
        "entry_id": [
          {
            "active_from": "2024-11-12T12:01:08.261000000Z",
            "active_until": null,
            "created_by_actor": {
              "type": "workspace-member",
              "id": "bbe415be-7a1d-45c7-9a8b-2af7b3cc962a"
            },
            "value": "14382145-26a5-4258-a6c5-ed11cf448b9b",
            "attribute_type": "text"
          }
        ],
        "main_point_of_contact": [],
        "owner": [
          {
            "active_from": "2024-11-12T12:01:08.261000000Z",
            "active_until": null,
            "created_by_actor": {
              "type": "workspace-member",
              "id": "bbe415be-7a1d-45c7-9a8b-2af7b3cc962a"
            },
            "referenced_actor_type": "workspace-member",
            "referenced_actor_id": "bbe415be-7a1d-45c7-9a8b-2af7b3cc962a",
            "attribute_type": "actor-reference"
          }
        ],
        "priority": [],
        "estimated_contract_value": [],
        "projected_close_date": [
          {
            "active_from": "2024-11-12T12:01:08.261000000Z",
            "active_until": null,
            "created_by_actor": {
              "type": "workspace-member",
              "id": "bbe415be-7a1d-45c7-9a8b-2af7b3cc962a"
            },
            "value": "2024-11-26",
            "attribute_type": "date"
          }
        ],
        "close_confidence": [],
        "close_lost_reason": [],
        "notes": [],
        "created_at": [
          {
            "active_from": "2024-11-12T12:01:08.261000000Z",
            "active_until": null,
            "created_by_actor": {
              "type": "workspace-member",
              "id": "bbe415be-7a1d-45c7-9a8b-2af7b3cc962a"
            },
            "value": "2024-11-12T12:01:08.297000000Z",
            "attribute_type": "timestamp"
          }
        ],
        "created_by": [
          {
            "active_from": "2024-11-12T12:01:08.261000000Z",
            "active_until": null,
            "created_by_actor": {
              "type": "workspace-member",
              "id": "bbe415be-7a1d-45c7-9a8b-2af7b3cc962a"
            },
            "referenced_actor_type": "workspace-member",
            "referenced_actor_id": "bbe415be-7a1d-45c7-9a8b-2af7b3cc962a",
            "attribute_type": "actor-reference"
          }
        ],
        "deal_name": [],
        "company": []
      }
    },
    {
      "id": {
        "workspace_id": "515117c4-5fd1-4bfd-bc63-58f639d3f357",
        "list_id": "030f5287-761d-42ef-9feb-7d2e9a1ba52b",
        "entry_id": "147d6f4c-022f-424d-8194-02255b2eb99c"
      },
      "parent_record_id": "8c524b10-0af6-4c8e-8c6f-894bc9da9c9b",
      "parent_object": "companies",
      "created_at": "2024-11-12T12:01:08.259000000Z",
      "entry_values": {
        "stage": [
          {
            "active_from": "2024-11-12T12:01:08.259000000Z",
            "active_until": null,
            "created_by_actor": {
              "type": "workspace-member",
              "id": "bbe415be-7a1d-45c7-9a8b-2af7b3cc962a"
            },
            "status": {
              "id": {
                "workspace_id": "515117c4-5fd1-4bfd-bc63-58f639d3f357",
                "object_id": "030f5287-761d-42ef-9feb-7d2e9a1ba52b",
                "attribute_id": "1a04f7e7-9392-40cb-9071-b1024f2eec73",
                "status_id": "10e0b809-893f-438a-a6a4-d69153c38ddc"
              },
              "title": "Prospecting",
              "is_archived": false,
              "target_time_in_status": null,
              "celebration_enabled": false
            },
            "attribute_type": "status"
          }
        ],
        "entry_id": [
          {
            "active_from": "2024-11-12T12:01:08.259000000Z",
            "active_until": null,
            "created_by_actor": {
              "type": "workspace-member",
              "id": "bbe415be-7a1d-45c7-9a8b-2af7b3cc962a"
            },
            "value": "147d6f4c-022f-424d-8194-02255b2eb99c",
            "attribute_type": "text"
          }
        ],
        "main_point_of_contact": [],
        "owner": [
          {
            "active_from": "2024-11-12T12:01:08.259000000Z",
            "active_until": null,
            "created_by_actor": {
              "type": "workspace-member",
              "id": "bbe415be-7a1d-45c7-9a8b-2af7b3cc962a"
            },
            "referenced_actor_type": "workspace-member",
            "referenced_actor_id": "bbe415be-7a1d-45c7-9a8b-2af7b3cc962a",
            "attribute_type": "actor-reference"
          }
        ],
        "priority": [],
        "estimated_contract_value": [],
        "projected_close_date": [
          {
            "active_from": "2024-11-12T12:01:08.259000000Z",
            "active_until": null,
            "created_by_actor": {
              "type": "workspace-member",
              "id": "bbe415be-7a1d-45c7-9a8b-2af7b3cc962a"
            },
            "value": "2024-11-26",
            "attribute_type": "date"
          }
        ],
        "close_confidence": [],
        "close_lost_reason": [],
        "notes": [],
        "created_at": [
          {
            "active_from": "2024-11-12T12:01:08.259000000Z",
            "active_until": null,
            "created_by_actor": {
              "type": "workspace-member",
              "id": "bbe415be-7a1d-45c7-9a8b-2af7b3cc962a"
            },
            "value": "2024-11-12T12:01:08.295000000Z",
            "attribute_type": "timestamp"
          }
        ],
        "created_by": [
          {
            "active_from": "2024-11-12T12:01:08.259000000Z",
            "active_until": null,
            "created_by_actor": {
              "type": "workspace-member",
              "id": "bbe415be-7a1d-45c7-9a8b-2af7b3cc962a"
            },
            "referenced_actor_type": "workspace-member",
            "referenced_actor_id": "bbe415be-7a1d-45c7-9a8b-2af7b3cc962a",
            "attribute_type": "actor-reference"
          }
        ],
        "deal_name": [],
        "company": []
      }
    },
    {
      "id": {
        "workspace_id": "515117c4-5fd1-4bfd-bc63-58f639d3f357",
        "list_id": "030f5287-761d-42ef-9feb-7d2e9a1ba52b",
        "entry_id": "16eb9d0b-b8af-48c0-b69e-d284415c92ea"
      },
      "parent_record_id": "d8207d1f-5bba-4127-b41d-48b078a82122",
      "parent_object": "companies",
      "created_at": "2024-11-12T12:01:10.422000000Z",
      "entry_values": {
        "stage": [
          {
            "active_from": "2024-11-12T12:01:10.422000000Z",
            "active_until": null,
            "created_by_actor": {
              "type": "workspace-member",
              "id": "bbe415be-7a1d-45c7-9a8b-2af7b3cc962a"
            },
            "status": {
              "id": {
                "workspace_id": "515117c4-5fd1-4bfd-bc63-58f639d3f357",
                "object_id": "030f5287-761d-42ef-9feb-7d2e9a1ba52b",
                "attribute_id": "1a04f7e7-9392-40cb-9071-b1024f2eec73",
                "status_id": "10e0b809-893f-438a-a6a4-d69153c38ddc"
              },
              "title": "Prospecting",
              "is_archived": false,
              "target_time_in_status": null,
              "celebration_enabled": false
            },
            "attribute_type": "status"
          }
        ],
        "entry_id": [
          {
            "active_from": "2024-11-12T12:01:10.422000000Z",
            "active_until": null,
            "created_by_actor": {
              "type": "workspace-member",
              "id": "bbe415be-7a1d-45c7-9a8b-2af7b3cc962a"
            },
            "value": "16eb9d0b-b8af-48c0-b69e-d284415c92ea",
            "attribute_type": "text"
          }
        ],
        "main_point_of_contact": [],
        "owner": [
          {
            "active_from": "2024-11-12T12:01:10.422000000Z",
            "active_until": null,
            "created_by_actor": {
              "type": "workspace-member",
              "id": "bbe415be-7a1d-45c7-9a8b-2af7b3cc962a"
            },
            "referenced_actor_type": "workspace-member",
            "referenced_actor_id": "bbe415be-7a1d-45c7-9a8b-2af7b3cc962a",
            "attribute_type": "actor-reference"
          }
        ],
        "priority": [],
        "estimated_contract_value": [],
        "projected_close_date": [
          {
            "active_from": "2024-11-12T12:01:10.422000000Z",
            "active_until": null,
            "created_by_actor": {
              "type": "workspace-member",
              "id": "bbe415be-7a1d-45c7-9a8b-2af7b3cc962a"
            },
            "value": "2024-11-26",
            "attribute_type": "date"
          }
        ],
        "close_confidence": [],
        "close_lost_reason": [],
        "notes": [],
        "created_at": [
          {
            "active_from": "2024-11-12T12:01:10.422000000Z",
            "active_until": null,
            "created_by_actor": {
              "type": "workspace-member",
              "id": "bbe415be-7a1d-45c7-9a8b-2af7b3cc962a"
            },
            "value": "2024-11-12T12:01:10.453000000Z",
            "attribute_type": "timestamp"
          }
        ],
        "created_by": [
          {
            "active_from": "2024-11-12T12:01:10.422000000Z",
            "active_until": null,
            "created_by_actor": {
              "type": "workspace-member",
              "id": "bbe415be-7a1d-45c7-9a8b-2af7b3cc962a"
            },
            "referenced_actor_type": "workspace-member",
            "referenced_actor_id": "bbe415be-7a1d-45c7-9a8b-2af7b3cc962a",
            "attribute_type": "actor-reference"
          }
        ],
        "deal_name": [],
        "company": []
      }
    },
    {
      "id": {
        "workspace_id": "515117c4-5fd1-4bfd-bc63-58f639d3f357",
        "list_id": "030f5287-761d-42ef-9feb-7d2e9a1ba52b",
        "entry_id": "1ea51d57-e008-4e1d-b627-0685818e13db"
      },
      "parent_record_id": "504283ad-59e4-45d4-a6b7-cf46c9eb0887",
      "parent_object": "companies",
      "created_at": "2024-11-12T12:01:07.162000000Z",
      "entry_values": {
        "stage": [
          {
            "active_from": "2024-11-12T12:01:07.162000000Z",
            "active_until": null,
            "created_by_actor": {
              "type": "workspace-member",
              "id": "bbe415be-7a1d-45c7-9a8b-2af7b3cc962a"
            },
            "status": {
              "id": {
                "workspace_id": "515117c4-5fd1-4bfd-bc63-58f639d3f357",
                "object_id": "030f5287-761d-42ef-9feb-7d2e9a1ba52b",
                "attribute_id": "1a04f7e7-9392-40cb-9071-b1024f2eec73",
                "status_id": "10e0b809-893f-438a-a6a4-d69153c38ddc"
              },
              "title": "Prospecting",
              "is_archived": false,
              "target_time_in_status": null,
              "celebration_enabled": false
            },
            "attribute_type": "status"
          }
        ],
        "entry_id": [
          {
            "active_from": "2024-11-12T12:01:07.162000000Z",
            "active_until": null,
            "created_by_actor": {
              "type": "workspace-member",
              "id": "bbe415be-7a1d-45c7-9a8b-2af7b3cc962a"
            },
            "value": "1ea51d57-e008-4e1d-b627-0685818e13db",
            "attribute_type": "text"
          }
        ],
        "main_point_of_contact": [],
        "owner": [
          {
            "active_from": "2024-11-12T12:01:07.162000000Z",
            "active_until": null,
            "created_by_actor": {
              "type": "workspace-member",
              "id": "bbe415be-7a1d-45c7-9a8b-2af7b3cc962a"
            },
            "referenced_actor_type": "workspace-member",
            "referenced_actor_id": "bbe415be-7a1d-45c7-9a8b-2af7b3cc962a",
            "attribute_type": "actor-reference"
          }
        ],
        "priority": [],
        "estimated_contract_value": [],
        "projected_close_date": [
          {
            "active_from": "2024-11-12T12:01:07.162000000Z",
            "active_until": null,
            "created_by_actor": {
              "type": "workspace-member",
              "id": "bbe415be-7a1d-45c7-9a8b-2af7b3cc962a"
            },
            "value": "2024-11-26",
            "attribute_type": "date"
          }
        ],
        "close_confidence": [],
        "close_lost_reason": [],
        "notes": [],
        "created_at": [
          {
            "active_from": "2024-11-12T12:01:07.162000000Z",
            "active_until": null,
            "created_by_actor": {
              "type": "workspace-member",
              "id": "bbe415be-7a1d-45c7-9a8b-2af7b3cc962a"
            },
            "value": "2024-11-12T12:01:07.205000000Z",
            "attribute_type": "timestamp"
          }
        ],
        "created_by": [
          {
            "active_from": "2024-11-12T12:01:07.162000000Z",
            "active_until": null,
            "created_by_actor": {
              "type": "workspace-member",
              "id": "bbe415be-7a1d-45c7-9a8b-2af7b3cc962a"
            },
            "referenced_actor_type": "workspace-member",
            "referenced_actor_id": "bbe415be-7a1d-45c7-9a8b-2af7b3cc962a",
            "attribute_type": "actor-reference"
          }
        ],
        "deal_name": [],
        "company": []
      }
    },
    {
      "id": {
        "workspace_id": "515117c4-5fd1-4bfd-bc63-58f639d3f357",
        "list_id": "030f5287-761d-42ef-9feb-7d2e9a1ba52b",
        "entry_id": "1ed43ebf-878d-4e21-a70b-921cda32ef77"
      },
      "parent_record_id": "572ae30b-c253-4b4d-bc51-259238e4b128",
      "parent_object": "companies",
      "created_at": "2024-11-12T12:01:07.276000000Z",
      "entry_values": {
        "stage": [
          {
            "active_from": "2024-11-12T12:01:07.276000000Z",
            "active_until": null,
            "created_by_actor": {
              "type": "workspace-member",
              "id": "bbe415be-7a1d-45c7-9a8b-2af7b3cc962a"
            },
            "status": {
              "id": {
                "workspace_id": "515117c4-5fd1-4bfd-bc63-58f639d3f357",
                "object_id": "030f5287-761d-42ef-9feb-7d2e9a1ba52b",
                "attribute_id": "1a04f7e7-9392-40cb-9071-b1024f2eec73",
                "status_id": "10e0b809-893f-438a-a6a4-d69153c38ddc"
              },
              "title": "Prospecting",
              "is_archived": false,
              "target_time_in_status": null,
              "celebration_enabled": false
            },
            "attribute_type": "status"
          }
        ],
        "entry_id": [
          {
            "active_from": "2024-11-12T12:01:07.276000000Z",
            "active_until": null,
            "created_by_actor": {
              "type": "workspace-member",
              "id": "bbe415be-7a1d-45c7-9a8b-2af7b3cc962a"
            },
            "value": "1ed43ebf-878d-4e21-a70b-921cda32ef77",
            "attribute_type": "text"
          }
        ],
        "main_point_of_contact": [],
        "owner": [
          {
            "active_from": "2024-11-12T12:01:07.276000000Z",
            "active_until": null,
            "created_by_actor": {
              "type": "workspace-member",
              "id": "bbe415be-7a1d-45c7-9a8b-2af7b3cc962a"
            },
            "referenced_actor_type": "workspace-member",
            "referenced_actor_id": "bbe415be-7a1d-45c7-9a8b-2af7b3cc962a",
            "attribute_type": "actor-reference"
          }
        ],
        "priority": [],
        "estimated_contract_value": [],
        "projected_close_date": [
          {
            "active_from": "2024-11-12T12:01:07.276000000Z",
            "active_until": null,
            "created_by_actor": {
              "type": "workspace-member",
              "id": "bbe415be-7a1d-45c7-9a8b-2af7b3cc962a"
            },
            "value": "2024-11-26",
            "attribute_type": "date"
          }
        ],
        "close_confidence": [],
        "close_lost_reason": [],
        "notes": [],
        "created_at": [
          {
            "active_from": "2024-11-12T12:01:07.276000000Z",
            "active_until": null,
            "created_by_actor": {
              "type": "workspace-member",
              "id": "bbe415be-7a1d-45c7-9a8b-2af7b3cc962a"
            },
            "value": "2024-11-12T12:01:07.311000000Z",
            "attribute_type": "timestamp"
          }
        ],
        "created_by": [
          {
            "active_from": "2024-11-12T12:01:07.276000000Z",
            "active_until": null,
            "created_by_actor": {
              "type": "workspace-member",
              "id": "bbe415be-7a1d-45c7-9a8b-2af7b3cc962a"
            },
            "referenced_actor_type": "workspace-member",
            "referenced_actor_id": "bbe415be-7a1d-45c7-9a8b-2af7b3cc962a",
            "attribute_type": "actor-reference"
          }
        ],
        "deal_name": [],
        "company": []
      }
    },
    {
      "id": {
        "workspace_id": "515117c4-5fd1-4bfd-bc63-58f639d3f357",
        "list_id": "030f5287-761d-42ef-9feb-7d2e9a1ba52b",
        "entry_id": "20aee50a-8ec3-4943-88f5-3ab612114ec5"
      },
      "parent_record_id": "1acb0275-969f-4fa6-951d-b99a5a24d601",
      "parent_object": "companies",
      "created_at": "2024-11-12T12:01:06.050000000Z",
      "entry_values": {
        "stage": [
          {
            "active_from": "2024-11-12T12:01:06.050000000Z",
            "active_until": null,
            "created_by_actor": {
              "type": "workspace-member",
              "id": "bbe415be-7a1d-45c7-9a8b-2af7b3cc962a"
            },
            "status": {
              "id": {
                "workspace_id": "515117c4-5fd1-4bfd-bc63-58f639d3f357",
                "object_id": "030f5287-761d-42ef-9feb-7d2e9a1ba52b",
                "attribute_id": "1a04f7e7-9392-40cb-9071-b1024f2eec73",
                "status_id": "10e0b809-893f-438a-a6a4-d69153c38ddc"
              },
              "title": "Prospecting",
              "is_archived": false,
              "target_time_in_status": null,
              "celebration_enabled": false
            },
            "attribute_type": "status"
          }
        ],
        "entry_id": [
          {
            "active_from": "2024-11-12T12:01:06.050000000Z",
            "active_until": null,
            "created_by_actor": {
              "type": "workspace-member",
              "id": "bbe415be-7a1d-45c7-9a8b-2af7b3cc962a"
            },
            "value": "20aee50a-8ec3-4943-88f5-3ab612114ec5",
            "attribute_type": "text"
          }
        ],
        "main_point_of_contact": [],
        "owner": [
          {
            "active_from": "2024-11-12T12:01:06.050000000Z",
            "active_until": null,
            "created_by_actor": {
              "type": "workspace-member",
              "id": "bbe415be-7a1d-45c7-9a8b-2af7b3cc962a"
            },
            "referenced_actor_type": "workspace-member",
            "referenced_actor_id": "bbe415be-7a1d-45c7-9a8b-2af7b3cc962a",
            "attribute_type": "actor-reference"
          }
        ],
        "priority": [],
        "estimated_contract_value": [],
        "projected_close_date": [
          {
            "active_from": "2024-11-12T12:01:06.050000000Z",
            "active_until": null,
            "created_by_actor": {
              "type": "workspace-member",
              "id": "bbe415be-7a1d-45c7-9a8b-2af7b3cc962a"
            },
            "value": "2024-11-26",
            "attribute_type": "date"
          }
        ],
        "close_confidence": [],
        "close_lost_reason": [],
        "notes": [],
        "created_at": [
          {
            "active_from": "2024-11-12T12:01:06.050000000Z",
            "active_until": null,
            "created_by_actor": {
              "type": "workspace-member",
              "id": "bbe415be-7a1d-45c7-9a8b-2af7b3cc962a"
            },
            "value": "2024-11-12T12:01:06.079000000Z",
            "attribute_type": "timestamp"
          }
        ],
        "created_by": [
          {
            "active_from": "2024-11-12T12:01:06.050000000Z",
            "active_until": null,
            "created_by_actor": {
              "type": "workspace-member",
              "id": "bbe415be-7a1d-45c7-9a8b-2af7b3cc962a"
            },
            "referenced_actor_type": "workspace-member",
            "referenced_actor_id": "bbe415be-7a1d-45c7-9a8b-2af7b3cc962a",
            "attribute_type": "actor-reference"
          }
        ],
        "deal_name": [],
        "company": []
      }
    },
    {
      "id": {
        "workspace_id": "515117c4-5fd1-4bfd-bc63-58f639d3f357",
        "list_id": "030f5287-761d-42ef-9feb-7d2e9a1ba52b",
        "entry_id": "2241aa2e-b528-4b07-ab30-623826fd829c"
      },
      "parent_record_id": "7d4201bd-3c7f-40b9-b24b-23b735a9974d",
      "parent_object": "companies",
      "created_at": "2024-11-12T12:01:07.773000000Z",
      "entry_values": {
        "stage": [
          {
            "active_from": "2024-11-12T12:01:07.773000000Z",
            "active_until": null,
            "created_by_actor": {
              "type": "workspace-member",
              "id": "bbe415be-7a1d-45c7-9a8b-2af7b3cc962a"
            },
            "status": {
              "id": {
                "workspace_id": "515117c4-5fd1-4bfd-bc63-58f639d3f357",
                "object_id": "030f5287-761d-42ef-9feb-7d2e9a1ba52b",
                "attribute_id": "1a04f7e7-9392-40cb-9071-b1024f2eec73",
                "status_id": "10e0b809-893f-438a-a6a4-d69153c38ddc"
              },
              "title": "Prospecting",
              "is_archived": false,
              "target_time_in_status": null,
              "celebration_enabled": false
            },
            "attribute_type": "status"
          }
        ],
        "entry_id": [
          {
            "active_from": "2024-11-12T12:01:07.773000000Z",
            "active_until": null,
            "created_by_actor": {
              "type": "workspace-member",
              "id": "bbe415be-7a1d-45c7-9a8b-2af7b3cc962a"
            },
            "value": "2241aa2e-b528-4b07-ab30-623826fd829c",
            "attribute_type": "text"
          }
        ],
        "main_point_of_contact": [],
        "owner": [
          {
            "active_from": "2024-11-12T12:01:07.773000000Z",
            "active_until": null,
            "created_by_actor": {
              "type": "workspace-member",
              "id": "bbe415be-7a1d-45c7-9a8b-2af7b3cc962a"
            },
            "referenced_actor_type": "workspace-member",
            "referenced_actor_id": "bbe415be-7a1d-45c7-9a8b-2af7b3cc962a",
            "attribute_type": "actor-reference"
          }
        ],
        "priority": [],
        "estimated_contract_value": [],
        "projected_close_date": [
          {
            "active_from": "2024-11-12T12:01:07.773000000Z",
            "active_until": null,
            "created_by_actor": {
              "type": "workspace-member",
              "id": "bbe415be-7a1d-45c7-9a8b-2af7b3cc962a"
            },
            "value": "2024-11-26",
            "attribute_type": "date"
          }
        ],
        "close_confidence": [],
        "close_lost_reason": [],
        "notes": [],
        "created_at": [
          {
            "active_from": "2024-11-12T12:01:07.773000000Z",
            "active_until": null,
            "created_by_actor": {
              "type": "workspace-member",
              "id": "bbe415be-7a1d-45c7-9a8b-2af7b3cc962a"
            },
            "value": "2024-11-12T12:01:07.807000000Z",
            "attribute_type": "timestamp"
          }
        ],
        "created_by": [
          {
            "active_from": "2024-11-12T12:01:07.773000000Z",
            "active_until": null,
            "created_by_actor": {
              "type": "workspace-member",
              "id": "bbe415be-7a1d-45c7-9a8b-2af7b3cc962a"
            },
            "referenced_actor_type": "workspace-member",
            "referenced_actor_id": "bbe415be-7a1d-45c7-9a8b-2af7b3cc962a",
            "attribute_type": "actor-reference"
          }
        ],
        "deal_name": [],
        "company": []
      }
    },
    {
      "id": {
        "workspace_id": "515117c4-5fd1-4bfd-bc63-58f639d3f357",
        "list_id": "030f5287-761d-42ef-9feb-7d2e9a1ba52b",
        "entry_id": "2a91eaaf-5843-439d-a3d0-564ab88a12fc"
      },
      "parent_record_id": "d9574ad9-8107-4bbe-9577-b1a62f7c01cc",
      "parent_object": "companies",
      "created_at": "2024-11-12T12:01:10.616000000Z",
      "entry_values": {
        "stage": [
          {
            "active_from": "2024-11-12T12:01:10.616000000Z",
            "active_until": null,
            "created_by_actor": {
              "type": "workspace-member",
              "id": "bbe415be-7a1d-45c7-9a8b-2af7b3cc962a"
            },
            "status": {
              "id": {
                "workspace_id": "515117c4-5fd1-4bfd-bc63-58f639d3f357",
                "object_id": "030f5287-761d-42ef-9feb-7d2e9a1ba52b",
                "attribute_id": "1a04f7e7-9392-40cb-9071-b1024f2eec73",
                "status_id": "10e0b809-893f-438a-a6a4-d69153c38ddc"
              },
              "title": "Prospecting",
              "is_archived": false,
              "target_time_in_status": null,
              "celebration_enabled": false
            },
            "attribute_type": "status"
          }
        ],
        "entry_id": [
          {
            "active_from": "2024-11-12T12:01:10.616000000Z",
            "active_until": null,
            "created_by_actor": {
              "type": "workspace-member",
              "id": "bbe415be-7a1d-45c7-9a8b-2af7b3cc962a"
            },
            "value": "2a91eaaf-5843-439d-a3d0-564ab88a12fc",
            "attribute_type": "text"
          }
        ],
        "main_point_of_contact": [],
        "owner": [
          {
            "active_from": "2024-11-12T12:01:10.616000000Z",
            "active_until": null,
            "created_by_actor": {
              "type": "workspace-member",
              "id": "bbe415be-7a1d-45c7-9a8b-2af7b3cc962a"
            },
            "referenced_actor_type": "workspace-member",
            "referenced_actor_id": "bbe415be-7a1d-45c7-9a8b-2af7b3cc962a",
            "attribute_type": "actor-reference"
          }
        ],
        "priority": [],
        "estimated_contract_value": [],
        "projected_close_date": [
          {
            "active_from": "2024-11-12T12:01:10.616000000Z",
            "active_until": null,
            "created_by_actor": {
              "type": "workspace-member",
              "id": "bbe415be-7a1d-45c7-9a8b-2af7b3cc962a"
            },
            "value": "2024-11-26",
            "attribute_type": "date"
          }
        ],
        "close_confidence": [],
        "close_lost_reason": [],
        "notes": [],
        "created_at": [
          {
            "active_from": "2024-11-12T12:01:10.616000000Z",
            "active_until": null,
            "created_by_actor": {
              "type": "workspace-member",
              "id": "bbe415be-7a1d-45c7-9a8b-2af7b3cc962a"
            },
            "value": "2024-11-12T12:01:10.671000000Z",
            "attribute_type": "timestamp"
          }
        ],
        "created_by": [
          {
            "active_from": "2024-11-12T12:01:10.616000000Z",
            "active_until": null,
            "created_by_actor": {
              "type": "workspace-member",
              "id": "bbe415be-7a1d-45c7-9a8b-2af7b3cc962a"
            },
            "referenced_actor_type": "workspace-member",
            "referenced_actor_id": "bbe415be-7a1d-45c7-9a8b-2af7b3cc962a",
            "attribute_type": "actor-reference"
          }
        ],
        "deal_name": [],
        "company": []
      }
    },
    {
      "id": {
        "workspace_id": "515117c4-5fd1-4bfd-bc63-58f639d3f357",
        "list_id": "030f5287-761d-42ef-9feb-7d2e9a1ba52b",
        "entry_id": "324a34d5-7331-4ed6-9ea3-a6fe0cc9ac6b"
      },
      "parent_record_id": "e317ba2f-f3d6-46ab-a4df-47940f510e74",
      "parent_object": "companies",
      "created_at": "2024-11-12T12:01:10.588000000Z",
      "entry_values": {
        "stage": [
          {
            "active_from": "2024-11-12T12:01:10.588000000Z",
            "active_until": null,
            "created_by_actor": {
              "type": "workspace-member",
              "id": "bbe415be-7a1d-45c7-9a8b-2af7b3cc962a"
            },
            "status": {
              "id": {
                "workspace_id": "515117c4-5fd1-4bfd-bc63-58f639d3f357",
                "object_id": "030f5287-761d-42ef-9feb-7d2e9a1ba52b",
                "attribute_id": "1a04f7e7-9392-40cb-9071-b1024f2eec73",
                "status_id": "10e0b809-893f-438a-a6a4-d69153c38ddc"
              },
              "title": "Prospecting",
              "is_archived": false,
              "target_time_in_status": null,
              "celebration_enabled": false
            },
            "attribute_type": "status"
          }
        ],
        "entry_id": [
          {
            "active_from": "2024-11-12T12:01:10.588000000Z",
            "active_until": null,
            "created_by_actor": {
              "type": "workspace-member",
              "id": "bbe415be-7a1d-45c7-9a8b-2af7b3cc962a"
            },
            "value": "324a34d5-7331-4ed6-9ea3-a6fe0cc9ac6b",
            "attribute_type": "text"
          }
        ],
        "main_point_of_contact": [],
        "owner": [
          {
            "active_from": "2024-11-12T12:01:10.588000000Z",
            "active_until": null,
            "created_by_actor": {
              "type": "workspace-member",
              "id": "bbe415be-7a1d-45c7-9a8b-2af7b3cc962a"
            },
            "referenced_actor_type": "workspace-member",
            "referenced_actor_id": "bbe415be-7a1d-45c7-9a8b-2af7b3cc962a",
            "attribute_type": "actor-reference"
          }
        ],
        "priority": [],
        "estimated_contract_value": [],
        "projected_close_date": [
          {
            "active_from": "2024-11-12T12:01:10.588000000Z",
            "active_until": null,
            "created_by_actor": {
              "type": "workspace-member",
              "id": "bbe415be-7a1d-45c7-9a8b-2af7b3cc962a"
            },
            "value": "2024-11-26",
            "attribute_type": "date"
          }
        ],
        "close_confidence": [],
        "close_lost_reason": [],
        "notes": [],
        "created_at": [
          {
            "active_from": "2024-11-12T12:01:10.588000000Z",
            "active_until": null,
            "created_by_actor": {
              "type": "workspace-member",
              "id": "bbe415be-7a1d-45c7-9a8b-2af7b3cc962a"
            },
            "value": "2024-11-12T12:01:10.614000000Z",
            "attribute_type": "timestamp"
          }
        ],
        "created_by": [
          {
            "active_from": "2024-11-12T12:01:10.588000000Z",
            "active_until": null,
            "created_by_actor": {
              "type": "workspace-member",
              "id": "bbe415be-7a1d-45c7-9a8b-2af7b3cc962a"
            },
            "referenced_actor_type": "workspace-member",
            "referenced_actor_id": "bbe415be-7a1d-45c7-9a8b-2af7b3cc962a",
            "attribute_type": "actor-reference"
          }
        ],
        "deal_name": [],
        "company": []
      }
    },
    {
      "id": {
        "workspace_id": "515117c4-5fd1-4bfd-bc63-58f639d3f357",
        "list_id": "030f5287-761d-42ef-9feb-7d2e9a1ba52b",
        "entry_id": "348a69a2-9805-4de8-a219-02c1f607f61e"
      },
      "parent_record_id": "469546b3-9ea6-4f7c-9525-13d6650abb50",
      "parent_object": "companies",
      "created_at": "2024-11-12T12:01:06.795000000Z",
      "entry_values": {
        "stage": [
          {
            "active_from": "2024-11-12T12:01:06.795000000Z",
            "active_until": null,
            "created_by_actor": {
              "type": "workspace-member",
              "id": "bbe415be-7a1d-45c7-9a8b-2af7b3cc962a"
            },
            "status": {
              "id": {
                "workspace_id": "515117c4-5fd1-4bfd-bc63-58f639d3f357",
                "object_id": "030f5287-761d-42ef-9feb-7d2e9a1ba52b",
                "attribute_id": "1a04f7e7-9392-40cb-9071-b1024f2eec73",
                "status_id": "10e0b809-893f-438a-a6a4-d69153c38ddc"
              },
              "title": "Prospecting",
              "is_archived": false,
              "target_time_in_status": null,
              "celebration_enabled": false
            },
            "attribute_type": "status"
          }
        ],
        "entry_id": [
          {
            "active_from": "2024-11-12T12:01:06.795000000Z",
            "active_until": null,
            "created_by_actor": {
              "type": "workspace-member",
              "id": "bbe415be-7a1d-45c7-9a8b-2af7b3cc962a"
            },
            "value": "348a69a2-9805-4de8-a219-02c1f607f61e",
            "attribute_type": "text"
          }
        ],
        "main_point_of_contact": [],
        "owner": [
          {
            "active_from": "2024-11-12T12:01:06.795000000Z",
            "active_until": null,
            "created_by_actor": {
              "type": "workspace-member",
              "id": "bbe415be-7a1d-45c7-9a8b-2af7b3cc962a"
            },
            "referenced_actor_type": "workspace-member",
            "referenced_actor_id": "bbe415be-7a1d-45c7-9a8b-2af7b3cc962a",
            "attribute_type": "actor-reference"
          }
        ],
        "priority": [],
        "estimated_contract_value": [],
        "projected_close_date": [
          {
            "active_from": "2024-11-12T12:01:06.795000000Z",
            "active_until": null,
            "created_by_actor": {
              "type": "workspace-member",
              "id": "bbe415be-7a1d-45c7-9a8b-2af7b3cc962a"
            },
            "value": "2024-11-26",
            "attribute_type": "date"
          }
        ],
        "close_confidence": [],
        "close_lost_reason": [],
        "notes": [],
        "created_at": [
          {
            "active_from": "2024-11-12T12:01:06.795000000Z",
            "active_until": null,
            "created_by_actor": {
              "type": "workspace-member",
              "id": "bbe415be-7a1d-45c7-9a8b-2af7b3cc962a"
            },
            "value": "2024-11-12T12:01:06.834000000Z",
            "attribute_type": "timestamp"
          }
        ],
        "created_by": [
          {
            "active_from": "2024-11-12T12:01:06.795000000Z",
            "active_until": null,
            "created_by_actor": {
              "type": "workspace-member",
              "id": "bbe415be-7a1d-45c7-9a8b-2af7b3cc962a"
            },
            "referenced_actor_type": "workspace-member",
            "referenced_actor_id": "bbe415be-7a1d-45c7-9a8b-2af7b3cc962a",
            "attribute_type": "actor-reference"
          }
        ],
        "deal_name": [],
        "company": []
      }
    },
    {
      "id": {
        "workspace_id": "515117c4-5fd1-4bfd-bc63-58f639d3f357",
        "list_id": "030f5287-761d-42ef-9feb-7d2e9a1ba52b",
        "entry_id": "36266987-d727-4698-9fc2-7c002bdc0275"
      },
      "parent_record_id": "2e53312c-0cf6-401e-ab57-2f6d40d428cc",
      "parent_object": "companies",
      "created_at": "2024-11-12T12:01:06.042000000Z",
      "entry_values": {
        "stage": [
          {
            "active_from": "2024-11-12T12:01:06.042000000Z",
            "active_until": null,
            "created_by_actor": {
              "type": "workspace-member",
              "id": "bbe415be-7a1d-45c7-9a8b-2af7b3cc962a"
            },
            "status": {
              "id": {
                "workspace_id": "515117c4-5fd1-4bfd-bc63-58f639d3f357",
                "object_id": "030f5287-761d-42ef-9feb-7d2e9a1ba52b",
                "attribute_id": "1a04f7e7-9392-40cb-9071-b1024f2eec73",
                "status_id": "10e0b809-893f-438a-a6a4-d69153c38ddc"
              },
              "title": "Prospecting",
              "is_archived": false,
              "target_time_in_status": null,
              "celebration_enabled": false
            },
            "attribute_type": "status"
          }
        ],
        "entry_id": [
          {
            "active_from": "2024-11-12T12:01:06.042000000Z",
            "active_until": null,
            "created_by_actor": {
              "type": "workspace-member",
              "id": "bbe415be-7a1d-45c7-9a8b-2af7b3cc962a"
            },
            "value": "36266987-d727-4698-9fc2-7c002bdc0275",
            "attribute_type": "text"
          }
        ],
        "main_point_of_contact": [],
        "owner": [
          {
            "active_from": "2024-11-12T12:01:06.042000000Z",
            "active_until": null,
            "created_by_actor": {
              "type": "workspace-member",
              "id": "bbe415be-7a1d-45c7-9a8b-2af7b3cc962a"
            },
            "referenced_actor_type": "workspace-member",
            "referenced_actor_id": "bbe415be-7a1d-45c7-9a8b-2af7b3cc962a",
            "attribute_type": "actor-reference"
          }
        ],
        "priority": [],
        "estimated_contract_value": [],
        "projected_close_date": [
          {
            "active_from": "2024-11-12T12:01:06.042000000Z",
            "active_until": null,
            "created_by_actor": {
              "type": "workspace-member",
              "id": "bbe415be-7a1d-45c7-9a8b-2af7b3cc962a"
            },
            "value": "2024-11-26",
            "attribute_type": "date"
          }
        ],
        "close_confidence": [],
        "close_lost_reason": [],
        "notes": [],
        "created_at": [
          {
            "active_from": "2024-11-12T12:01:06.042000000Z",
            "active_until": null,
            "created_by_actor": {
              "type": "workspace-member",
              "id": "bbe415be-7a1d-45c7-9a8b-2af7b3cc962a"
            },
            "value": "2024-11-12T12:01:06.073000000Z",
            "attribute_type": "timestamp"
          }
        ],
        "created_by": [
          {
            "active_from": "2024-11-12T12:01:06.042000000Z",
            "active_until": null,
            "created_by_actor": {
              "type": "workspace-member",
              "id": "bbe415be-7a1d-45c7-9a8b-2af7b3cc962a"
            },
            "referenced_actor_type": "workspace-member",
            "referenced_actor_id": "bbe415be-7a1d-45c7-9a8b-2af7b3cc962a",
            "attribute_type": "actor-reference"
          }
        ],
        "deal_name": [],
        "company": []
      }
    },
    {
      "id": {
        "workspace_id": "515117c4-5fd1-4bfd-bc63-58f639d3f357",
        "list_id": "030f5287-761d-42ef-9feb-7d2e9a1ba52b",
        "entry_id": "3aac5a78-4464-4264-aa33-1196d3add907"
      },
      "parent_record_id": "c1b840cb-86ed-444b-b044-126e347bceda",
      "parent_object": "companies",
      "created_at": "2024-11-12T12:01:09.768000000Z",
      "entry_values": {
        "stage": [
          {
            "active_from": "2024-11-12T12:01:09.768000000Z",
            "active_until": null,
            "created_by_actor": {
              "type": "workspace-member",
              "id": "bbe415be-7a1d-45c7-9a8b-2af7b3cc962a"
            },
            "status": {
              "id": {
                "workspace_id": "515117c4-5fd1-4bfd-bc63-58f639d3f357",
                "object_id": "030f5287-761d-42ef-9feb-7d2e9a1ba52b",
                "attribute_id": "1a04f7e7-9392-40cb-9071-b1024f2eec73",
                "status_id": "10e0b809-893f-438a-a6a4-d69153c38ddc"
              },
              "title": "Prospecting",
              "is_archived": false,
              "target_time_in_status": null,
              "celebration_enabled": false
            },
            "attribute_type": "status"
          }
        ],
        "entry_id": [
          {
            "active_from": "2024-11-12T12:01:09.768000000Z",
            "active_until": null,
            "created_by_actor": {
              "type": "workspace-member",
              "id": "bbe415be-7a1d-45c7-9a8b-2af7b3cc962a"
            },
            "value": "3aac5a78-4464-4264-aa33-1196d3add907",
            "attribute_type": "text"
          }
        ],
        "main_point_of_contact": [],
        "owner": [
          {
            "active_from": "2024-11-12T12:01:09.768000000Z",
            "active_until": null,
            "created_by_actor": {
              "type": "workspace-member",
              "id": "bbe415be-7a1d-45c7-9a8b-2af7b3cc962a"
            },
            "referenced_actor_type": "workspace-member",
            "referenced_actor_id": "bbe415be-7a1d-45c7-9a8b-2af7b3cc962a",
            "attribute_type": "actor-reference"
          }
        ],
        "priority": [],
        "estimated_contract_value": [],
        "projected_close_date": [
          {
            "active_from": "2024-11-12T12:01:09.768000000Z",
            "active_until": null,
            "created_by_actor": {
              "type": "workspace-member",
              "id": "bbe415be-7a1d-45c7-9a8b-2af7b3cc962a"
            },
            "value": "2024-11-26",
            "attribute_type": "date"
          }
        ],
        "close_confidence": [],
        "close_lost_reason": [],
        "notes": [],
        "created_at": [
          {
            "active_from": "2024-11-12T12:01:09.768000000Z",
            "active_until": null,
            "created_by_actor": {
              "type": "workspace-member",
              "id": "bbe415be-7a1d-45c7-9a8b-2af7b3cc962a"
            },
            "value": "2024-11-12T12:01:09.824000000Z",
            "attribute_type": "timestamp"
          }
        ],
        "created_by": [
          {
            "active_from": "2024-11-12T12:01:09.768000000Z",
            "active_until": null,
            "created_by_actor": {
              "type": "workspace-member",
              "id": "bbe415be-7a1d-45c7-9a8b-2af7b3cc962a"
            },
            "referenced_actor_type": "workspace-member",
            "referenced_actor_id": "bbe415be-7a1d-45c7-9a8b-2af7b3cc962a",
            "attribute_type": "actor-reference"
          }
        ],
        "deal_name": [],
        "company": []
      }
    },
    {
      "id": {
        "workspace_id": "515117c4-5fd1-4bfd-bc63-58f639d3f357",
        "list_id": "030f5287-761d-42ef-9feb-7d2e9a1ba52b",
        "entry_id": "40e42099-8c5e-489f-b135-ef0a7deb7f1d"
      },
      "parent_record_id": "98f8b682-b89e-4fe1-a434-fbfcaa834d31",
      "parent_object": "companies",
      "created_at": "2024-11-12T12:01:08.969000000Z",
      "entry_values": {
        "stage": [
          {
            "active_from": "2024-11-12T12:01:08.969000000Z",
            "active_until": null,
            "created_by_actor": {
              "type": "workspace-member",
              "id": "bbe415be-7a1d-45c7-9a8b-2af7b3cc962a"
            },
            "status": {
              "id": {
                "workspace_id": "515117c4-5fd1-4bfd-bc63-58f639d3f357",
                "object_id": "030f5287-761d-42ef-9feb-7d2e9a1ba52b",
                "attribute_id": "1a04f7e7-9392-40cb-9071-b1024f2eec73",
                "status_id": "10e0b809-893f-438a-a6a4-d69153c38ddc"
              },
              "title": "Prospecting",
              "is_archived": false,
              "target_time_in_status": null,
              "celebration_enabled": false
            },
            "attribute_type": "status"
          }
        ],
        "entry_id": [
          {
            "active_from": "2024-11-12T12:01:08.969000000Z",
            "active_until": null,
            "created_by_actor": {
              "type": "workspace-member",
              "id": "bbe415be-7a1d-45c7-9a8b-2af7b3cc962a"
            },
            "value": "40e42099-8c5e-489f-b135-ef0a7deb7f1d",
            "attribute_type": "text"
          }
        ],
        "main_point_of_contact": [],
        "owner": [
          {
            "active_from": "2024-11-12T12:01:08.969000000Z",
            "active_until": null,
            "created_by_actor": {
              "type": "workspace-member",
              "id": "bbe415be-7a1d-45c7-9a8b-2af7b3cc962a"
            },
            "referenced_actor_type": "workspace-member",
            "referenced_actor_id": "bbe415be-7a1d-45c7-9a8b-2af7b3cc962a",
            "attribute_type": "actor-reference"
          }
        ],
        "priority": [],
        "estimated_contract_value": [],
        "projected_close_date": [
          {
            "active_from": "2024-11-12T12:01:08.969000000Z",
            "active_until": null,
            "created_by_actor": {
              "type": "workspace-member",
              "id": "bbe415be-7a1d-45c7-9a8b-2af7b3cc962a"
            },
            "value": "2024-11-26",
            "attribute_type": "date"
          }
        ],
        "close_confidence": [],
        "close_lost_reason": [],
        "notes": [],
        "created_at": [
          {
            "active_from": "2024-11-12T12:01:08.969000000Z",
            "active_until": null,
            "created_by_actor": {
              "type": "workspace-member",
              "id": "bbe415be-7a1d-45c7-9a8b-2af7b3cc962a"
            },
            "value": "2024-11-12T12:01:09.006000000Z",
            "attribute_type": "timestamp"
          }
        ],
        "created_by": [
          {
            "active_from": "2024-11-12T12:01:08.969000000Z",
            "active_until": null,
            "created_by_actor": {
              "type": "workspace-member",
              "id": "bbe415be-7a1d-45c7-9a8b-2af7b3cc962a"
            },
            "referenced_actor_type": "workspace-member",
            "referenced_actor_id": "bbe415be-7a1d-45c7-9a8b-2af7b3cc962a",
            "attribute_type": "actor-reference"
          }
        ],
        "deal_name": [],
        "company": []
      }
    },
    {
      "id": {
        "workspace_id": "515117c4-5fd1-4bfd-bc63-58f639d3f357",
        "list_id": "030f5287-761d-42ef-9feb-7d2e9a1ba52b",
        "entry_id": "42912a45-964d-4e2e-b797-7d84a614ee29"
      },
      "parent_record_id": "b1953b3b-e40b-4ae9-b2fc-244a9b9eb321",
      "parent_object": "companies",
      "created_at": "2024-11-12T12:01:09.618000000Z",
      "entry_values": {
        "stage": [
          {
            "active_from": "2024-11-12T12:01:09.618000000Z",
            "active_until": null,
            "created_by_actor": {
              "type": "workspace-member",
              "id": "bbe415be-7a1d-45c7-9a8b-2af7b3cc962a"
            },
            "status": {
              "id": {
                "workspace_id": "515117c4-5fd1-4bfd-bc63-58f639d3f357",
                "object_id": "030f5287-761d-42ef-9feb-7d2e9a1ba52b",
                "attribute_id": "1a04f7e7-9392-40cb-9071-b1024f2eec73",
                "status_id": "10e0b809-893f-438a-a6a4-d69153c38ddc"
              },
              "title": "Prospecting",
              "is_archived": false,
              "target_time_in_status": null,
              "celebration_enabled": false
            },
            "attribute_type": "status"
          }
        ],
        "entry_id": [
          {
            "active_from": "2024-11-12T12:01:09.618000000Z",
            "active_until": null,
            "created_by_actor": {
              "type": "workspace-member",
              "id": "bbe415be-7a1d-45c7-9a8b-2af7b3cc962a"
            },
            "value": "42912a45-964d-4e2e-b797-7d84a614ee29",
            "attribute_type": "text"
          }
        ],
        "main_point_of_contact": [],
        "owner": [
          {
            "active_from": "2024-11-12T12:01:09.618000000Z",
            "active_until": null,
            "created_by_actor": {
              "type": "workspace-member",
              "id": "bbe415be-7a1d-45c7-9a8b-2af7b3cc962a"
            },
            "referenced_actor_type": "workspace-member",
            "referenced_actor_id": "bbe415be-7a1d-45c7-9a8b-2af7b3cc962a",
            "attribute_type": "actor-reference"
          }
        ],
        "priority": [],
        "estimated_contract_value": [],
        "projected_close_date": [
          {
            "active_from": "2024-11-12T12:01:09.618000000Z",
            "active_until": null,
            "created_by_actor": {
              "type": "workspace-member",
              "id": "bbe415be-7a1d-45c7-9a8b-2af7b3cc962a"
            },
            "value": "2024-11-26",
            "attribute_type": "date"
          }
        ],
        "close_confidence": [],
        "close_lost_reason": [],
        "notes": [],
        "created_at": [
          {
            "active_from": "2024-11-12T12:01:09.618000000Z",
            "active_until": null,
            "created_by_actor": {
              "type": "workspace-member",
              "id": "bbe415be-7a1d-45c7-9a8b-2af7b3cc962a"
            },
            "value": "2024-11-12T12:01:09.682000000Z",
            "attribute_type": "timestamp"
          }
        ],
        "created_by": [
          {
            "active_from": "2024-11-12T12:01:09.618000000Z",
            "active_until": null,
            "created_by_actor": {
              "type": "workspace-member",
              "id": "bbe415be-7a1d-45c7-9a8b-2af7b3cc962a"
            },
            "referenced_actor_type": "workspace-member",
            "referenced_actor_id": "bbe415be-7a1d-45c7-9a8b-2af7b3cc962a",
            "attribute_type": "actor-reference"
          }
        ],
        "deal_name": [],
        "company": []
      }
    },
    {
      "id": {
        "workspace_id": "515117c4-5fd1-4bfd-bc63-58f639d3f357",
        "list_id": "030f5287-761d-42ef-9feb-7d2e9a1ba52b",
        "entry_id": "463222d4-5af6-4857-92e9-dbfba6fb2e12"
      },
      "parent_record_id": "82d9f5f5-1eba-433a-83a2-c9a454d37ee4",
      "parent_object": "companies",
      "created_at": "2024-11-12T12:01:07.831000000Z",
      "entry_values": {
        "stage": [
          {
            "active_from": "2024-11-12T12:01:07.831000000Z",
            "active_until": null,
            "created_by_actor": {
              "type": "workspace-member",
              "id": "bbe415be-7a1d-45c7-9a8b-2af7b3cc962a"
            },
            "status": {
              "id": {
                "workspace_id": "515117c4-5fd1-4bfd-bc63-58f639d3f357",
                "object_id": "030f5287-761d-42ef-9feb-7d2e9a1ba52b",
                "attribute_id": "1a04f7e7-9392-40cb-9071-b1024f2eec73",
                "status_id": "10e0b809-893f-438a-a6a4-d69153c38ddc"
              },
              "title": "Prospecting",
              "is_archived": false,
              "target_time_in_status": null,
              "celebration_enabled": false
            },
            "attribute_type": "status"
          }
        ],
        "entry_id": [
          {
            "active_from": "2024-11-12T12:01:07.831000000Z",
            "active_until": null,
            "created_by_actor": {
              "type": "workspace-member",
              "id": "bbe415be-7a1d-45c7-9a8b-2af7b3cc962a"
            },
            "value": "463222d4-5af6-4857-92e9-dbfba6fb2e12",
            "attribute_type": "text"
          }
        ],
        "main_point_of_contact": [],
        "owner": [
          {
            "active_from": "2024-11-12T12:01:07.831000000Z",
            "active_until": null,
            "created_by_actor": {
              "type": "workspace-member",
              "id": "bbe415be-7a1d-45c7-9a8b-2af7b3cc962a"
            },
            "referenced_actor_type": "workspace-member",
            "referenced_actor_id": "bbe415be-7a1d-45c7-9a8b-2af7b3cc962a",
            "attribute_type": "actor-reference"
          }
        ],
        "priority": [],
        "estimated_contract_value": [],
        "projected_close_date": [
          {
            "active_from": "2024-11-12T12:01:07.831000000Z",
            "active_until": null,
            "created_by_actor": {
              "type": "workspace-member",
              "id": "bbe415be-7a1d-45c7-9a8b-2af7b3cc962a"
            },
            "value": "2024-11-26",
            "attribute_type": "date"
          }
        ],
        "close_confidence": [],
        "close_lost_reason": [],
        "notes": [],
        "created_at": [
          {
            "active_from": "2024-11-12T12:01:07.831000000Z",
            "active_until": null,
            "created_by_actor": {
              "type": "workspace-member",
              "id": "bbe415be-7a1d-45c7-9a8b-2af7b3cc962a"
            },
            "value": "2024-11-12T12:01:07.883000000Z",
            "attribute_type": "timestamp"
          }
        ],
        "created_by": [
          {
            "active_from": "2024-11-12T12:01:07.831000000Z",
            "active_until": null,
            "created_by_actor": {
              "type": "workspace-member",
              "id": "bbe415be-7a1d-45c7-9a8b-2af7b3cc962a"
            },
            "referenced_actor_type": "workspace-member",
            "referenced_actor_id": "bbe415be-7a1d-45c7-9a8b-2af7b3cc962a",
            "attribute_type": "actor-reference"
          }
        ],
        "deal_name": [],
        "company": []
      }
    },
    {
      "id": {
        "workspace_id": "515117c4-5fd1-4bfd-bc63-58f639d3f357",
        "list_id": "030f5287-761d-42ef-9feb-7d2e9a1ba52b",
        "entry_id": "464125ee-0299-4fa8-870a-52491fd9ff09"
      },
      "parent_record_id": "522eed0e-c9dc-4b10-bada-533f427a7b5b",
      "parent_object": "companies",
      "created_at": "2024-11-12T12:01:07.524000000Z",
      "entry_values": {
        "stage": [
          {
            "active_from": "2024-11-12T12:01:07.524000000Z",
            "active_until": null,
            "created_by_actor": {
              "type": "workspace-member",
              "id": "bbe415be-7a1d-45c7-9a8b-2af7b3cc962a"
            },
            "status": {
              "id": {
                "workspace_id": "515117c4-5fd1-4bfd-bc63-58f639d3f357",
                "object_id": "030f5287-761d-42ef-9feb-7d2e9a1ba52b",
                "attribute_id": "1a04f7e7-9392-40cb-9071-b1024f2eec73",
                "status_id": "10e0b809-893f-438a-a6a4-d69153c38ddc"
              },
              "title": "Prospecting",
              "is_archived": false,
              "target_time_in_status": null,
              "celebration_enabled": false
            },
            "attribute_type": "status"
          }
        ],
        "entry_id": [
          {
            "active_from": "2024-11-12T12:01:07.524000000Z",
            "active_until": null,
            "created_by_actor": {
              "type": "workspace-member",
              "id": "bbe415be-7a1d-45c7-9a8b-2af7b3cc962a"
            },
            "value": "464125ee-0299-4fa8-870a-52491fd9ff09",
            "attribute_type": "text"
          }
        ],
        "main_point_of_contact": [],
        "owner": [
          {
            "active_from": "2024-11-12T12:01:07.524000000Z",
            "active_until": null,
            "created_by_actor": {
              "type": "workspace-member",
              "id": "bbe415be-7a1d-45c7-9a8b-2af7b3cc962a"
            },
            "referenced_actor_type": "workspace-member",
            "referenced_actor_id": "bbe415be-7a1d-45c7-9a8b-2af7b3cc962a",
            "attribute_type": "actor-reference"
          }
        ],
        "priority": [],
        "estimated_contract_value": [],
        "projected_close_date": [
          {
            "active_from": "2024-11-12T12:01:07.524000000Z",
            "active_until": null,
            "created_by_actor": {
              "type": "workspace-member",
              "id": "bbe415be-7a1d-45c7-9a8b-2af7b3cc962a"
            },
            "value": "2024-11-26",
            "attribute_type": "date"
          }
        ],
        "close_confidence": [],
        "close_lost_reason": [],
        "notes": [],
        "created_at": [
          {
            "active_from": "2024-11-12T12:01:07.524000000Z",
            "active_until": null,
            "created_by_actor": {
              "type": "workspace-member",
              "id": "bbe415be-7a1d-45c7-9a8b-2af7b3cc962a"
            },
            "value": "2024-11-12T12:01:07.560000000Z",
            "attribute_type": "timestamp"
          }
        ],
        "created_by": [
          {
            "active_from": "2024-11-12T12:01:07.524000000Z",
            "active_until": null,
            "created_by_actor": {
              "type": "workspace-member",
              "id": "bbe415be-7a1d-45c7-9a8b-2af7b3cc962a"
            },
            "referenced_actor_type": "workspace-member",
            "referenced_actor_id": "bbe415be-7a1d-45c7-9a8b-2af7b3cc962a",
            "attribute_type": "actor-reference"
          }
        ],
        "deal_name": [],
        "company": []
      }
    },
    {
      "id": {
        "workspace_id": "515117c4-5fd1-4bfd-bc63-58f639d3f357",
        "list_id": "030f5287-761d-42ef-9feb-7d2e9a1ba52b",
        "entry_id": "4907c085-decf-4de3-bb50-f620620c2182"
      },
      "parent_record_id": "9bd0cffb-f162-4656-b3a3-9e58d3ae9630",
      "parent_object": "companies",
      "created_at": "2024-11-12T12:01:08.996000000Z",
      "entry_values": {
        "stage": [
          {
            "active_from": "2024-11-12T12:01:08.996000000Z",
            "active_until": null,
            "created_by_actor": {
              "type": "workspace-member",
              "id": "bbe415be-7a1d-45c7-9a8b-2af7b3cc962a"
            },
            "status": {
              "id": {
                "workspace_id": "515117c4-5fd1-4bfd-bc63-58f639d3f357",
                "object_id": "030f5287-761d-42ef-9feb-7d2e9a1ba52b",
                "attribute_id": "1a04f7e7-9392-40cb-9071-b1024f2eec73",
                "status_id": "10e0b809-893f-438a-a6a4-d69153c38ddc"
              },
              "title": "Prospecting",
              "is_archived": false,
              "target_time_in_status": null,
              "celebration_enabled": false
            },
            "attribute_type": "status"
          }
        ],
        "entry_id": [
          {
            "active_from": "2024-11-12T12:01:08.996000000Z",
            "active_until": null,
            "created_by_actor": {
              "type": "workspace-member",
              "id": "bbe415be-7a1d-45c7-9a8b-2af7b3cc962a"
            },
            "value": "4907c085-decf-4de3-bb50-f620620c2182",
            "attribute_type": "text"
          }
        ],
        "main_point_of_contact": [],
        "owner": [
          {
            "active_from": "2024-11-12T12:01:08.996000000Z",
            "active_until": null,
            "created_by_actor": {
              "type": "workspace-member",
              "id": "bbe415be-7a1d-45c7-9a8b-2af7b3cc962a"
            },
            "referenced_actor_type": "workspace-member",
            "referenced_actor_id": "bbe415be-7a1d-45c7-9a8b-2af7b3cc962a",
            "attribute_type": "actor-reference"
          }
        ],
        "priority": [],
        "estimated_contract_value": [],
        "projected_close_date": [
          {
            "active_from": "2024-11-12T12:01:08.996000000Z",
            "active_until": null,
            "created_by_actor": {
              "type": "workspace-member",
              "id": "bbe415be-7a1d-45c7-9a8b-2af7b3cc962a"
            },
            "value": "2024-11-26",
            "attribute_type": "date"
          }
        ],
        "close_confidence": [],
        "close_lost_reason": [],
        "notes": [],
        "created_at": [
          {
            "active_from": "2024-11-12T12:01:08.996000000Z",
            "active_until": null,
            "created_by_actor": {
              "type": "workspace-member",
              "id": "bbe415be-7a1d-45c7-9a8b-2af7b3cc962a"
            },
            "value": "2024-11-12T12:01:09.029000000Z",
            "attribute_type": "timestamp"
          }
        ],
        "created_by": [
          {
            "active_from": "2024-11-12T12:01:08.996000000Z",
            "active_until": null,
            "created_by_actor": {
              "type": "workspace-member",
              "id": "bbe415be-7a1d-45c7-9a8b-2af7b3cc962a"
            },
            "referenced_actor_type": "workspace-member",
            "referenced_actor_id": "bbe415be-7a1d-45c7-9a8b-2af7b3cc962a",
            "attribute_type": "actor-reference"
          }
        ],
        "deal_name": [],
        "company": []
      }
    },
    {
      "id": {
        "workspace_id": "515117c4-5fd1-4bfd-bc63-58f639d3f357",
        "list_id": "030f5287-761d-42ef-9feb-7d2e9a1ba52b",
        "entry_id": "49c887ad-3668-41f7-8021-f756e1c2f3b8"
      },
      "parent_record_id": "3e4f67e1-d0d2-491d-baa2-55a0eb55d131",
      "parent_object": "companies",
      "created_at": "2024-11-12T12:01:06.679000000Z",
      "entry_values": {
        "stage": [
          {
            "active_from": "2024-11-12T12:01:06.679000000Z",
            "active_until": null,
            "created_by_actor": {
              "type": "workspace-member",
              "id": "bbe415be-7a1d-45c7-9a8b-2af7b3cc962a"
            },
            "status": {
              "id": {
                "workspace_id": "515117c4-5fd1-4bfd-bc63-58f639d3f357",
                "object_id": "030f5287-761d-42ef-9feb-7d2e9a1ba52b",
                "attribute_id": "1a04f7e7-9392-40cb-9071-b1024f2eec73",
                "status_id": "10e0b809-893f-438a-a6a4-d69153c38ddc"
              },
              "title": "Prospecting",
              "is_archived": false,
              "target_time_in_status": null,
              "celebration_enabled": false
            },
            "attribute_type": "status"
          }
        ],
        "entry_id": [
          {
            "active_from": "2024-11-12T12:01:06.679000000Z",
            "active_until": null,
            "created_by_actor": {
              "type": "workspace-member",
              "id": "bbe415be-7a1d-45c7-9a8b-2af7b3cc962a"
            },
            "value": "49c887ad-3668-41f7-8021-f756e1c2f3b8",
            "attribute_type": "text"
          }
        ],
        "main_point_of_contact": [],
        "owner": [
          {
            "active_from": "2024-11-12T12:01:06.679000000Z",
            "active_until": null,
            "created_by_actor": {
              "type": "workspace-member",
              "id": "bbe415be-7a1d-45c7-9a8b-2af7b3cc962a"
            },
            "referenced_actor_type": "workspace-member",
            "referenced_actor_id": "bbe415be-7a1d-45c7-9a8b-2af7b3cc962a",
            "attribute_type": "actor-reference"
          }
        ],
        "priority": [],
        "estimated_contract_value": [],
        "projected_close_date": [
          {
            "active_from": "2024-11-12T12:01:06.679000000Z",
            "active_until": null,
            "created_by_actor": {
              "type": "workspace-member",
              "id": "bbe415be-7a1d-45c7-9a8b-2af7b3cc962a"
            },
            "value": "2024-11-26",
            "attribute_type": "date"
          }
        ],
        "close_confidence": [],
        "close_lost_reason": [],
        "notes": [],
        "created_at": [
          {
            "active_from": "2024-11-12T12:01:06.679000000Z",
            "active_until": null,
            "created_by_actor": {
              "type": "workspace-member",
              "id": "bbe415be-7a1d-45c7-9a8b-2af7b3cc962a"
            },
            "value": "2024-11-12T12:01:06.718000000Z",
            "attribute_type": "timestamp"
          }
        ],
        "created_by": [
          {
            "active_from": "2024-11-12T12:01:06.679000000Z",
            "active_until": null,
            "created_by_actor": {
              "type": "workspace-member",
              "id": "bbe415be-7a1d-45c7-9a8b-2af7b3cc962a"
            },
            "referenced_actor_type": "workspace-member",
            "referenced_actor_id": "bbe415be-7a1d-45c7-9a8b-2af7b3cc962a",
            "attribute_type": "actor-reference"
          }
        ],
        "deal_name": [],
        "company": []
      }
    },
    {
      "id": {
        "workspace_id": "515117c4-5fd1-4bfd-bc63-58f639d3f357",
        "list_id": "030f5287-761d-42ef-9feb-7d2e9a1ba52b",
        "entry_id": "4e6f67a9-1102-4faa-ae46-f094c97cee28"
      },
      "parent_record_id": "bc745293-4c1d-4e68-ad7a-e030c16658db",
      "parent_object": "companies",
      "created_at": "2024-11-12T12:01:09.686000000Z",
      "entry_values": {
        "stage": [
          {
            "active_from": "2024-11-12T12:01:09.686000000Z",
            "active_until": null,
            "created_by_actor": {
              "type": "workspace-member",
              "id": "bbe415be-7a1d-45c7-9a8b-2af7b3cc962a"
            },
            "status": {
              "id": {
                "workspace_id": "515117c4-5fd1-4bfd-bc63-58f639d3f357",
                "object_id": "030f5287-761d-42ef-9feb-7d2e9a1ba52b",
                "attribute_id": "1a04f7e7-9392-40cb-9071-b1024f2eec73",
                "status_id": "10e0b809-893f-438a-a6a4-d69153c38ddc"
              },
              "title": "Prospecting",
              "is_archived": false,
              "target_time_in_status": null,
              "celebration_enabled": false
            },
            "attribute_type": "status"
          }
        ],
        "entry_id": [
          {
            "active_from": "2024-11-12T12:01:09.686000000Z",
            "active_until": null,
            "created_by_actor": {
              "type": "workspace-member",
              "id": "bbe415be-7a1d-45c7-9a8b-2af7b3cc962a"
            },
            "value": "4e6f67a9-1102-4faa-ae46-f094c97cee28",
            "attribute_type": "text"
          }
        ],
        "main_point_of_contact": [],
        "owner": [
          {
            "active_from": "2024-11-12T12:01:09.686000000Z",
            "active_until": null,
            "created_by_actor": {
              "type": "workspace-member",
              "id": "bbe415be-7a1d-45c7-9a8b-2af7b3cc962a"
            },
            "referenced_actor_type": "workspace-member",
            "referenced_actor_id": "bbe415be-7a1d-45c7-9a8b-2af7b3cc962a",
            "attribute_type": "actor-reference"
          }
        ],
        "priority": [],
        "estimated_contract_value": [],
        "projected_close_date": [
          {
            "active_from": "2024-11-12T12:01:09.686000000Z",
            "active_until": null,
            "created_by_actor": {
              "type": "workspace-member",
              "id": "bbe415be-7a1d-45c7-9a8b-2af7b3cc962a"
            },
            "value": "2024-11-26",
            "attribute_type": "date"
          }
        ],
        "close_confidence": [],
        "close_lost_reason": [],
        "notes": [],
        "created_at": [
          {
            "active_from": "2024-11-12T12:01:09.686000000Z",
            "active_until": null,
            "created_by_actor": {
              "type": "workspace-member",
              "id": "bbe415be-7a1d-45c7-9a8b-2af7b3cc962a"
            },
            "value": "2024-11-12T12:01:09.739000000Z",
            "attribute_type": "timestamp"
          }
        ],
        "created_by": [
          {
            "active_from": "2024-11-12T12:01:09.686000000Z",
            "active_until": null,
            "created_by_actor": {
              "type": "workspace-member",
              "id": "bbe415be-7a1d-45c7-9a8b-2af7b3cc962a"
            },
            "referenced_actor_type": "workspace-member",
            "referenced_actor_id": "bbe415be-7a1d-45c7-9a8b-2af7b3cc962a",
            "attribute_type": "actor-reference"
          }
        ],
        "deal_name": [],
        "company": []
      }
    },
    {
      "id": {
        "workspace_id": "515117c4-5fd1-4bfd-bc63-58f639d3f357",
        "list_id": "030f5287-761d-42ef-9feb-7d2e9a1ba52b",
        "entry_id": "4f8cd556-8cb8-4ef2-8702-e715bd409324"
      },
      "parent_record_id": "570e34ed-5ea4-4791-810e-4042aa9c5b93",
      "parent_object": "companies",
      "created_at": "2024-11-12T12:01:07.196000000Z",
      "entry_values": {
        "stage": [
          {
            "active_from": "2024-11-12T12:01:07.196000000Z",
            "active_until": null,
            "created_by_actor": {
              "type": "workspace-member",
              "id": "bbe415be-7a1d-45c7-9a8b-2af7b3cc962a"
            },
            "status": {
              "id": {
                "workspace_id": "515117c4-5fd1-4bfd-bc63-58f639d3f357",
                "object_id": "030f5287-761d-42ef-9feb-7d2e9a1ba52b",
                "attribute_id": "1a04f7e7-9392-40cb-9071-b1024f2eec73",
                "status_id": "10e0b809-893f-438a-a6a4-d69153c38ddc"
              },
              "title": "Prospecting",
              "is_archived": false,
              "target_time_in_status": null,
              "celebration_enabled": false
            },
            "attribute_type": "status"
          }
        ],
        "entry_id": [
          {
            "active_from": "2024-11-12T12:01:07.196000000Z",
            "active_until": null,
            "created_by_actor": {
              "type": "workspace-member",
              "id": "bbe415be-7a1d-45c7-9a8b-2af7b3cc962a"
            },
            "value": "4f8cd556-8cb8-4ef2-8702-e715bd409324",
            "attribute_type": "text"
          }
        ],
        "main_point_of_contact": [],
        "owner": [
          {
            "active_from": "2024-11-12T12:01:07.196000000Z",
            "active_until": null,
            "created_by_actor": {
              "type": "workspace-member",
              "id": "bbe415be-7a1d-45c7-9a8b-2af7b3cc962a"
            },
            "referenced_actor_type": "workspace-member",
            "referenced_actor_id": "bbe415be-7a1d-45c7-9a8b-2af7b3cc962a",
            "attribute_type": "actor-reference"
          }
        ],
        "priority": [],
        "estimated_contract_value": [],
        "projected_close_date": [
          {
            "active_from": "2024-11-12T12:01:07.196000000Z",
            "active_until": null,
            "created_by_actor": {
              "type": "workspace-member",
              "id": "bbe415be-7a1d-45c7-9a8b-2af7b3cc962a"
            },
            "value": "2024-11-26",
            "attribute_type": "date"
          }
        ],
        "close_confidence": [],
        "close_lost_reason": [],
        "notes": [],
        "created_at": [
          {
            "active_from": "2024-11-12T12:01:07.196000000Z",
            "active_until": null,
            "created_by_actor": {
              "type": "workspace-member",
              "id": "bbe415be-7a1d-45c7-9a8b-2af7b3cc962a"
            },
            "value": "2024-11-12T12:01:07.233000000Z",
            "attribute_type": "timestamp"
          }
        ],
        "created_by": [
          {
            "active_from": "2024-11-12T12:01:07.196000000Z",
            "active_until": null,
            "created_by_actor": {
              "type": "workspace-member",
              "id": "bbe415be-7a1d-45c7-9a8b-2af7b3cc962a"
            },
            "referenced_actor_type": "workspace-member",
            "referenced_actor_id": "bbe415be-7a1d-45c7-9a8b-2af7b3cc962a",
            "attribute_type": "actor-reference"
          }
        ],
        "deal_name": [],
        "company": []
      }
    },
    {
      "id": {
        "workspace_id": "515117c4-5fd1-4bfd-bc63-58f639d3f357",
        "list_id": "030f5287-761d-42ef-9feb-7d2e9a1ba52b",
        "entry_id": "50e433d0-c3f9-483e-9311-7d41e2591377"
      },
      "parent_record_id": "c7c19ef0-6496-476d-970b-304b8ec9f5ba",
      "parent_object": "companies",
      "created_at": "2024-11-12T12:01:09.891000000Z",
      "entry_values": {
        "stage": [
          {
            "active_from": "2024-11-12T12:01:09.891000000Z",
            "active_until": null,
            "created_by_actor": {
              "type": "workspace-member",
              "id": "bbe415be-7a1d-45c7-9a8b-2af7b3cc962a"
            },
            "status": {
              "id": {
                "workspace_id": "515117c4-5fd1-4bfd-bc63-58f639d3f357",
                "object_id": "030f5287-761d-42ef-9feb-7d2e9a1ba52b",
                "attribute_id": "1a04f7e7-9392-40cb-9071-b1024f2eec73",
                "status_id": "10e0b809-893f-438a-a6a4-d69153c38ddc"
              },
              "title": "Prospecting",
              "is_archived": false,
              "target_time_in_status": null,
              "celebration_enabled": false
            },
            "attribute_type": "status"
          }
        ],
        "entry_id": [
          {
            "active_from": "2024-11-12T12:01:09.891000000Z",
            "active_until": null,
            "created_by_actor": {
              "type": "workspace-member",
              "id": "bbe415be-7a1d-45c7-9a8b-2af7b3cc962a"
            },
            "value": "50e433d0-c3f9-483e-9311-7d41e2591377",
            "attribute_type": "text"
          }
        ],
        "main_point_of_contact": [],
        "owner": [
          {
            "active_from": "2024-11-12T12:01:09.891000000Z",
            "active_until": null,
            "created_by_actor": {
              "type": "workspace-member",
              "id": "bbe415be-7a1d-45c7-9a8b-2af7b3cc962a"
            },
            "referenced_actor_type": "workspace-member",
            "referenced_actor_id": "bbe415be-7a1d-45c7-9a8b-2af7b3cc962a",
            "attribute_type": "actor-reference"
          }
        ],
        "priority": [],
        "estimated_contract_value": [],
        "projected_close_date": [
          {
            "active_from": "2024-11-12T12:01:09.891000000Z",
            "active_until": null,
            "created_by_actor": {
              "type": "workspace-member",
              "id": "bbe415be-7a1d-45c7-9a8b-2af7b3cc962a"
            },
            "value": "2024-11-26",
            "attribute_type": "date"
          }
        ],
        "close_confidence": [],
        "close_lost_reason": [],
        "notes": [],
        "created_at": [
          {
            "active_from": "2024-11-12T12:01:09.891000000Z",
            "active_until": null,
            "created_by_actor": {
              "type": "workspace-member",
              "id": "bbe415be-7a1d-45c7-9a8b-2af7b3cc962a"
            },
            "value": "2024-11-12T12:01:09.924000000Z",
            "attribute_type": "timestamp"
          }
        ],
        "created_by": [
          {
            "active_from": "2024-11-12T12:01:09.891000000Z",
            "active_until": null,
            "created_by_actor": {
              "type": "workspace-member",
              "id": "bbe415be-7a1d-45c7-9a8b-2af7b3cc962a"
            },
            "referenced_actor_type": "workspace-member",
            "referenced_actor_id": "bbe415be-7a1d-45c7-9a8b-2af7b3cc962a",
            "attribute_type": "actor-reference"
          }
        ],
        "deal_name": [],
        "company": []
      }
    },
    {
      "id": {
        "workspace_id": "515117c4-5fd1-4bfd-bc63-58f639d3f357",
        "list_id": "030f5287-761d-42ef-9feb-7d2e9a1ba52b",
        "entry_id": "512c47b2-ad65-4b15-869f-8a2ec74c810d"
      },
      "parent_record_id": "9a490a10-9c0b-4c62-9437-9ff1efd532fe",
      "parent_object": "companies",
      "created_at": "2024-11-12T12:01:08.985000000Z",
      "entry_values": {
        "stage": [
          {
            "active_from": "2024-11-12T12:01:08.985000000Z",
            "active_until": null,
            "created_by_actor": {
              "type": "workspace-member",
              "id": "bbe415be-7a1d-45c7-9a8b-2af7b3cc962a"
            },
            "status": {
              "id": {
                "workspace_id": "515117c4-5fd1-4bfd-bc63-58f639d3f357",
                "object_id": "030f5287-761d-42ef-9feb-7d2e9a1ba52b",
                "attribute_id": "1a04f7e7-9392-40cb-9071-b1024f2eec73",
                "status_id": "10e0b809-893f-438a-a6a4-d69153c38ddc"
              },
              "title": "Prospecting",
              "is_archived": false,
              "target_time_in_status": null,
              "celebration_enabled": false
            },
            "attribute_type": "status"
          }
        ],
        "entry_id": [
          {
            "active_from": "2024-11-12T12:01:08.985000000Z",
            "active_until": null,
            "created_by_actor": {
              "type": "workspace-member",
              "id": "bbe415be-7a1d-45c7-9a8b-2af7b3cc962a"
            },
            "value": "512c47b2-ad65-4b15-869f-8a2ec74c810d",
            "attribute_type": "text"
          }
        ],
        "main_point_of_contact": [],
        "owner": [
          {
            "active_from": "2024-11-12T12:01:08.985000000Z",
            "active_until": null,
            "created_by_actor": {
              "type": "workspace-member",
              "id": "bbe415be-7a1d-45c7-9a8b-2af7b3cc962a"
            },
            "referenced_actor_type": "workspace-member",
            "referenced_actor_id": "bbe415be-7a1d-45c7-9a8b-2af7b3cc962a",
            "attribute_type": "actor-reference"
          }
        ],
        "priority": [],
        "estimated_contract_value": [],
        "projected_close_date": [
          {
            "active_from": "2024-11-12T12:01:08.985000000Z",
            "active_until": null,
            "created_by_actor": {
              "type": "workspace-member",
              "id": "bbe415be-7a1d-45c7-9a8b-2af7b3cc962a"
            },
            "value": "2024-11-26",
            "attribute_type": "date"
          }
        ],
        "close_confidence": [],
        "close_lost_reason": [],
        "notes": [],
        "created_at": [
          {
            "active_from": "2024-11-12T12:01:08.985000000Z",
            "active_until": null,
            "created_by_actor": {
              "type": "workspace-member",
              "id": "bbe415be-7a1d-45c7-9a8b-2af7b3cc962a"
            },
            "value": "2024-11-12T12:01:09.029000000Z",
            "attribute_type": "timestamp"
          }
        ],
        "created_by": [
          {
            "active_from": "2024-11-12T12:01:08.985000000Z",
            "active_until": null,
            "created_by_actor": {
              "type": "workspace-member",
              "id": "bbe415be-7a1d-45c7-9a8b-2af7b3cc962a"
            },
            "referenced_actor_type": "workspace-member",
            "referenced_actor_id": "bbe415be-7a1d-45c7-9a8b-2af7b3cc962a",
            "attribute_type": "actor-reference"
          }
        ],
        "deal_name": [],
        "company": []
      }
    },
    {
      "id": {
        "workspace_id": "515117c4-5fd1-4bfd-bc63-58f639d3f357",
        "list_id": "030f5287-761d-42ef-9feb-7d2e9a1ba52b",
        "entry_id": "56f7a86b-e538-4f48-a181-c33cc56a1b58"
      },
      "parent_record_id": "8c524b10-0af6-4c8e-8c6f-894bc9da9c9b",
      "parent_object": "companies",
      "created_at": "2024-11-07T13:34:29.893000000Z",
      "entry_values": {
        "stage": [
          {
            "active_from": "2024-11-07T13:34:29.893000000Z",
            "active_until": null,
            "created_by_actor": {
              "type": "workspace-member",
              "id": "bbe415be-7a1d-45c7-9a8b-2af7b3cc962a"
            },
            "status": {
              "id": {
                "workspace_id": "515117c4-5fd1-4bfd-bc63-58f639d3f357",
                "object_id": "030f5287-761d-42ef-9feb-7d2e9a1ba52b",
                "attribute_id": "1a04f7e7-9392-40cb-9071-b1024f2eec73",
                "status_id": "10e0b809-893f-438a-a6a4-d69153c38ddc"
              },
              "title": "Prospecting",
              "is_archived": false,
              "target_time_in_status": null,
              "celebration_enabled": false
            },
            "attribute_type": "status"
          }
        ],
        "entry_id": [
          {
            "active_from": "2024-11-07T13:34:29.893000000Z",
            "active_until": null,
            "created_by_actor": {
              "type": "workspace-member",
              "id": "bbe415be-7a1d-45c7-9a8b-2af7b3cc962a"
            },
            "value": "56f7a86b-e538-4f48-a181-c33cc56a1b58",
            "attribute_type": "text"
          }
        ],
        "main_point_of_contact": [
          {
            "active_from": "2024-11-07T13:34:29.893000000Z",
            "active_until": null,
            "created_by_actor": {
              "type": "workspace-member",
              "id": "bbe415be-7a1d-45c7-9a8b-2af7b3cc962a"
            },
            "target_object": "people",
            "target_record_id": "967b153c-e714-4156-ba8b-df4843dba9ca",
            "attribute_type": "record-reference"
          }
        ],
        "owner": [
          {
            "active_from": "2024-11-07T13:34:29.893000000Z",
            "active_until": null,
            "created_by_actor": {
              "type": "workspace-member",
              "id": "bbe415be-7a1d-45c7-9a8b-2af7b3cc962a"
            },
            "referenced_actor_type": "workspace-member",
            "referenced_actor_id": "bbe415be-7a1d-45c7-9a8b-2af7b3cc962a",
            "attribute_type": "actor-reference"
          }
        ],
        "priority": [
          {
            "active_from": "2024-11-07T13:34:29.893000000Z",
            "active_until": null,
            "created_by_actor": {
              "type": "workspace-member",
              "id": "bbe415be-7a1d-45c7-9a8b-2af7b3cc962a"
            },
            "option": {
              "id": {
                "workspace_id": "515117c4-5fd1-4bfd-bc63-58f639d3f357",
                "object_id": "030f5287-761d-42ef-9feb-7d2e9a1ba52b",
                "attribute_id": "01a83343-3e0a-453a-bfb8-23bafa76a59b",
                "option_id": "bb178c28-767e-4e99-bd52-f9c8ef28f5a8"
              },
              "title": "Medium",
              "is_archived": false
            },
            "attribute_type": "select"
          }
        ],
        "estimated_contract_value": [
          {
            "active_from": "2024-11-07T13:34:29.893000000Z",
            "active_until": null,
            "created_by_actor": {
              "type": "workspace-member",
              "id": "bbe415be-7a1d-45c7-9a8b-2af7b3cc962a"
            },
            "currency_code": "USD",
            "currency_value": 100012,
            "attribute_type": "currency"
          }
        ],
        "projected_close_date": [
          {
            "active_from": "2024-11-07T13:34:29.893000000Z",
            "active_until": null,
            "created_by_actor": {
              "type": "workspace-member",
              "id": "bbe415be-7a1d-45c7-9a8b-2af7b3cc962a"
            },
            "value": "2024-11-21",
            "attribute_type": "date"
          }
        ],
        "close_confidence": [
          {
            "active_from": "2024-11-07T13:34:29.893000000Z",
            "active_until": null,
            "created_by_actor": {
              "type": "workspace-member",
              "id": "bbe415be-7a1d-45c7-9a8b-2af7b3cc962a"
            },
            "value": 2,
            "attribute_type": "rating"
          }
        ],
        "close_lost_reason": [],
        "notes": [],
        "created_at": [
          {
            "active_from": "2024-11-07T13:34:29.893000000Z",
            "active_until": null,
            "created_by_actor": {
              "type": "workspace-member",
              "id": "bbe415be-7a1d-45c7-9a8b-2af7b3cc962a"
            },
            "value": "2024-11-07T13:34:05.430000000Z",
            "attribute_type": "timestamp"
          }
        ],
        "created_by": [
          {
            "active_from": "2024-11-07T13:34:29.893000000Z",
            "active_until": null,
            "created_by_actor": {
              "type": "workspace-member",
              "id": "bbe415be-7a1d-45c7-9a8b-2af7b3cc962a"
            },
            "referenced_actor_type": "workspace-member",
            "referenced_actor_id": "bbe415be-7a1d-45c7-9a8b-2af7b3cc962a",
            "attribute_type": "actor-reference"
          }
        ],
        "deal_name": [
          {
            "active_from": "2024-11-08T11:03:29.406000000Z",
            "active_until": null,
            "created_by_actor": {
              "type": "workspace-member",
              "id": "bbe415be-7a1d-45c7-9a8b-2af7b3cc962a"
            },
            "value": "Concrete - newbiz",
            "attribute_type": "text"
          }
        ],
        "company": []
      }
    },
    {
      "id": {
        "workspace_id": "515117c4-5fd1-4bfd-bc63-58f639d3f357",
        "list_id": "030f5287-761d-42ef-9feb-7d2e9a1ba52b",
        "entry_id": "58970421-9cef-4095-bffe-19c3a877434a"
      },
      "parent_record_id": "e971480d-847d-433e-9897-3ef858827898",
      "parent_object": "companies",
      "created_at": "2024-11-12T12:01:10.730000000Z",
      "entry_values": {
        "stage": [
          {
            "active_from": "2024-11-12T12:01:10.730000000Z",
            "active_until": null,
            "created_by_actor": {
              "type": "workspace-member",
              "id": "bbe415be-7a1d-45c7-9a8b-2af7b3cc962a"
            },
            "status": {
              "id": {
                "workspace_id": "515117c4-5fd1-4bfd-bc63-58f639d3f357",
                "object_id": "030f5287-761d-42ef-9feb-7d2e9a1ba52b",
                "attribute_id": "1a04f7e7-9392-40cb-9071-b1024f2eec73",
                "status_id": "10e0b809-893f-438a-a6a4-d69153c38ddc"
              },
              "title": "Prospecting",
              "is_archived": false,
              "target_time_in_status": null,
              "celebration_enabled": false
            },
            "attribute_type": "status"
          }
        ],
        "entry_id": [
          {
            "active_from": "2024-11-12T12:01:10.730000000Z",
            "active_until": null,
            "created_by_actor": {
              "type": "workspace-member",
              "id": "bbe415be-7a1d-45c7-9a8b-2af7b3cc962a"
            },
            "value": "58970421-9cef-4095-bffe-19c3a877434a",
            "attribute_type": "text"
          }
        ],
        "main_point_of_contact": [],
        "owner": [
          {
            "active_from": "2024-11-12T12:01:10.730000000Z",
            "active_until": null,
            "created_by_actor": {
              "type": "workspace-member",
              "id": "bbe415be-7a1d-45c7-9a8b-2af7b3cc962a"
            },
            "referenced_actor_type": "workspace-member",
            "referenced_actor_id": "bbe415be-7a1d-45c7-9a8b-2af7b3cc962a",
            "attribute_type": "actor-reference"
          }
        ],
        "priority": [],
        "estimated_contract_value": [],
        "projected_close_date": [
          {
            "active_from": "2024-11-12T12:01:10.730000000Z",
            "active_until": null,
            "created_by_actor": {
              "type": "workspace-member",
              "id": "bbe415be-7a1d-45c7-9a8b-2af7b3cc962a"
            },
            "value": "2024-11-26",
            "attribute_type": "date"
          }
        ],
        "close_confidence": [],
        "close_lost_reason": [],
        "notes": [],
        "created_at": [
          {
            "active_from": "2024-11-12T12:01:10.730000000Z",
            "active_until": null,
            "created_by_actor": {
              "type": "workspace-member",
              "id": "bbe415be-7a1d-45c7-9a8b-2af7b3cc962a"
            },
            "value": "2024-11-12T12:01:10.766000000Z",
            "attribute_type": "timestamp"
          }
        ],
        "created_by": [
          {
            "active_from": "2024-11-12T12:01:10.730000000Z",
            "active_until": null,
            "created_by_actor": {
              "type": "workspace-member",
              "id": "bbe415be-7a1d-45c7-9a8b-2af7b3cc962a"
            },
            "referenced_actor_type": "workspace-member",
            "referenced_actor_id": "bbe415be-7a1d-45c7-9a8b-2af7b3cc962a",
            "attribute_type": "actor-reference"
          }
        ],
        "deal_name": [],
        "company": []
      }
    },
    {
      "id": {
        "workspace_id": "515117c4-5fd1-4bfd-bc63-58f639d3f357",
        "list_id": "030f5287-761d-42ef-9feb-7d2e9a1ba52b",
        "entry_id": "652686bc-1115-4a7a-92de-7507bd8de904"
      },
      "parent_record_id": "d5eb490b-b88d-49af-90f3-ecc69bcd32d9",
      "parent_object": "companies",
      "created_at": "2024-11-12T12:01:10.392000000Z",
      "entry_values": {
        "stage": [
          {
            "active_from": "2024-11-12T12:01:10.392000000Z",
            "active_until": null,
            "created_by_actor": {
              "type": "workspace-member",
              "id": "bbe415be-7a1d-45c7-9a8b-2af7b3cc962a"
            },
            "status": {
              "id": {
                "workspace_id": "515117c4-5fd1-4bfd-bc63-58f639d3f357",
                "object_id": "030f5287-761d-42ef-9feb-7d2e9a1ba52b",
                "attribute_id": "1a04f7e7-9392-40cb-9071-b1024f2eec73",
                "status_id": "10e0b809-893f-438a-a6a4-d69153c38ddc"
              },
              "title": "Prospecting",
              "is_archived": false,
              "target_time_in_status": null,
              "celebration_enabled": false
            },
            "attribute_type": "status"
          }
        ],
        "entry_id": [
          {
            "active_from": "2024-11-12T12:01:10.392000000Z",
            "active_until": null,
            "created_by_actor": {
              "type": "workspace-member",
              "id": "bbe415be-7a1d-45c7-9a8b-2af7b3cc962a"
            },
            "value": "652686bc-1115-4a7a-92de-7507bd8de904",
            "attribute_type": "text"
          }
        ],
        "main_point_of_contact": [],
        "owner": [
          {
            "active_from": "2024-11-12T12:01:10.392000000Z",
            "active_until": null,
            "created_by_actor": {
              "type": "workspace-member",
              "id": "bbe415be-7a1d-45c7-9a8b-2af7b3cc962a"
            },
            "referenced_actor_type": "workspace-member",
            "referenced_actor_id": "bbe415be-7a1d-45c7-9a8b-2af7b3cc962a",
            "attribute_type": "actor-reference"
          }
        ],
        "priority": [],
        "estimated_contract_value": [],
        "projected_close_date": [
          {
            "active_from": "2024-11-12T12:01:10.392000000Z",
            "active_until": null,
            "created_by_actor": {
              "type": "workspace-member",
              "id": "bbe415be-7a1d-45c7-9a8b-2af7b3cc962a"
            },
            "value": "2024-11-26",
            "attribute_type": "date"
          }
        ],
        "close_confidence": [],
        "close_lost_reason": [],
        "notes": [],
        "created_at": [
          {
            "active_from": "2024-11-12T12:01:10.392000000Z",
            "active_until": null,
            "created_by_actor": {
              "type": "workspace-member",
              "id": "bbe415be-7a1d-45c7-9a8b-2af7b3cc962a"
            },
            "value": "2024-11-12T12:01:10.444000000Z",
            "attribute_type": "timestamp"
          }
        ],
        "created_by": [
          {
            "active_from": "2024-11-12T12:01:10.392000000Z",
            "active_until": null,
            "created_by_actor": {
              "type": "workspace-member",
              "id": "bbe415be-7a1d-45c7-9a8b-2af7b3cc962a"
            },
            "referenced_actor_type": "workspace-member",
            "referenced_actor_id": "bbe415be-7a1d-45c7-9a8b-2af7b3cc962a",
            "attribute_type": "actor-reference"
          }
        ],
        "deal_name": [],
        "company": []
      }
    },
    {
      "id": {
        "workspace_id": "515117c4-5fd1-4bfd-bc63-58f639d3f357",
        "list_id": "030f5287-761d-42ef-9feb-7d2e9a1ba52b",
        "entry_id": "66397a66-8769-457f-8cbc-b44da76edd72"
      },
      "parent_record_id": "66378f76-6345-4778-8457-6767701e2131",
      "parent_object": "companies",
      "created_at": "2024-11-12T12:01:07.864000000Z",
      "entry_values": {
        "stage": [
          {
            "active_from": "2024-11-12T12:01:07.864000000Z",
            "active_until": null,
            "created_by_actor": {
              "type": "workspace-member",
              "id": "bbe415be-7a1d-45c7-9a8b-2af7b3cc962a"
            },
            "status": {
              "id": {
                "workspace_id": "515117c4-5fd1-4bfd-bc63-58f639d3f357",
                "object_id": "030f5287-761d-42ef-9feb-7d2e9a1ba52b",
                "attribute_id": "1a04f7e7-9392-40cb-9071-b1024f2eec73",
                "status_id": "10e0b809-893f-438a-a6a4-d69153c38ddc"
              },
              "title": "Prospecting",
              "is_archived": false,
              "target_time_in_status": null,
              "celebration_enabled": false
            },
            "attribute_type": "status"
          }
        ],
        "entry_id": [
          {
            "active_from": "2024-11-12T12:01:07.864000000Z",
            "active_until": null,
            "created_by_actor": {
              "type": "workspace-member",
              "id": "bbe415be-7a1d-45c7-9a8b-2af7b3cc962a"
            },
            "value": "66397a66-8769-457f-8cbc-b44da76edd72",
            "attribute_type": "text"
          }
        ],
        "main_point_of_contact": [],
        "owner": [
          {
            "active_from": "2024-11-12T12:01:07.864000000Z",
            "active_until": null,
            "created_by_actor": {
              "type": "workspace-member",
              "id": "bbe415be-7a1d-45c7-9a8b-2af7b3cc962a"
            },
            "referenced_actor_type": "workspace-member",
            "referenced_actor_id": "bbe415be-7a1d-45c7-9a8b-2af7b3cc962a",
            "attribute_type": "actor-reference"
          }
        ],
        "priority": [],
        "estimated_contract_value": [],
        "projected_close_date": [
          {
            "active_from": "2024-11-12T12:01:07.864000000Z",
            "active_until": null,
            "created_by_actor": {
              "type": "workspace-member",
              "id": "bbe415be-7a1d-45c7-9a8b-2af7b3cc962a"
            },
            "value": "2024-11-26",
            "attribute_type": "date"
          }
        ],
        "close_confidence": [],
        "close_lost_reason": [],
        "notes": [],
        "created_at": [
          {
            "active_from": "2024-11-12T12:01:07.864000000Z",
            "active_until": null,
            "created_by_actor": {
              "type": "workspace-member",
              "id": "bbe415be-7a1d-45c7-9a8b-2af7b3cc962a"
            },
            "value": "2024-11-12T12:01:07.984000000Z",
            "attribute_type": "timestamp"
          }
        ],
        "created_by": [
          {
            "active_from": "2024-11-12T12:01:07.864000000Z",
            "active_until": null,
            "created_by_actor": {
              "type": "workspace-member",
              "id": "bbe415be-7a1d-45c7-9a8b-2af7b3cc962a"
            },
            "referenced_actor_type": "workspace-member",
            "referenced_actor_id": "bbe415be-7a1d-45c7-9a8b-2af7b3cc962a",
            "attribute_type": "actor-reference"
          }
        ],
        "deal_name": [],
        "company": []
      }
    },
    {
      "id": {
        "workspace_id": "515117c4-5fd1-4bfd-bc63-58f639d3f357",
        "list_id": "030f5287-761d-42ef-9feb-7d2e9a1ba52b",
        "entry_id": "67484c92-241a-42ff-be4a-3ffbc813c31c"
      },
      "parent_record_id": "cf36bf07-4b7e-476d-8bd4-54276e850e71",
      "parent_object": "companies",
      "created_at": "2024-11-12T12:01:10.234000000Z",
      "entry_values": {
        "stage": [
          {
            "active_from": "2024-11-12T12:01:10.234000000Z",
            "active_until": null,
            "created_by_actor": {
              "type": "workspace-member",
              "id": "bbe415be-7a1d-45c7-9a8b-2af7b3cc962a"
            },
            "status": {
              "id": {
                "workspace_id": "515117c4-5fd1-4bfd-bc63-58f639d3f357",
                "object_id": "030f5287-761d-42ef-9feb-7d2e9a1ba52b",
                "attribute_id": "1a04f7e7-9392-40cb-9071-b1024f2eec73",
                "status_id": "10e0b809-893f-438a-a6a4-d69153c38ddc"
              },
              "title": "Prospecting",
              "is_archived": false,
              "target_time_in_status": null,
              "celebration_enabled": false
            },
            "attribute_type": "status"
          }
        ],
        "entry_id": [
          {
            "active_from": "2024-11-12T12:01:10.234000000Z",
            "active_until": null,
            "created_by_actor": {
              "type": "workspace-member",
              "id": "bbe415be-7a1d-45c7-9a8b-2af7b3cc962a"
            },
            "value": "67484c92-241a-42ff-be4a-3ffbc813c31c",
            "attribute_type": "text"
          }
        ],
        "main_point_of_contact": [],
        "owner": [
          {
            "active_from": "2024-11-12T12:01:10.234000000Z",
            "active_until": null,
            "created_by_actor": {
              "type": "workspace-member",
              "id": "bbe415be-7a1d-45c7-9a8b-2af7b3cc962a"
            },
            "referenced_actor_type": "workspace-member",
            "referenced_actor_id": "bbe415be-7a1d-45c7-9a8b-2af7b3cc962a",
            "attribute_type": "actor-reference"
          }
        ],
        "priority": [],
        "estimated_contract_value": [],
        "projected_close_date": [
          {
            "active_from": "2024-11-12T12:01:10.234000000Z",
            "active_until": null,
            "created_by_actor": {
              "type": "workspace-member",
              "id": "bbe415be-7a1d-45c7-9a8b-2af7b3cc962a"
            },
            "value": "2024-11-26",
            "attribute_type": "date"
          }
        ],
        "close_confidence": [],
        "close_lost_reason": [],
        "notes": [],
        "created_at": [
          {
            "active_from": "2024-11-12T12:01:10.234000000Z",
            "active_until": null,
            "created_by_actor": {
              "type": "workspace-member",
              "id": "bbe415be-7a1d-45c7-9a8b-2af7b3cc962a"
            },
            "value": "2024-11-12T12:01:10.267000000Z",
            "attribute_type": "timestamp"
          }
        ],
        "created_by": [
          {
            "active_from": "2024-11-12T12:01:10.234000000Z",
            "active_until": null,
            "created_by_actor": {
              "type": "workspace-member",
              "id": "bbe415be-7a1d-45c7-9a8b-2af7b3cc962a"
            },
            "referenced_actor_type": "workspace-member",
            "referenced_actor_id": "bbe415be-7a1d-45c7-9a8b-2af7b3cc962a",
            "attribute_type": "actor-reference"
          }
        ],
        "deal_name": [],
        "company": []
      }
    },
    {
      "id": {
        "workspace_id": "515117c4-5fd1-4bfd-bc63-58f639d3f357",
        "list_id": "030f5287-761d-42ef-9feb-7d2e9a1ba52b",
        "entry_id": "6ae76b3c-cc85-43bc-9443-ec25eac02192"
      },
      "parent_record_id": "90f824e1-f254-4933-933b-ac01e59096c6",
      "parent_object": "companies",
      "created_at": "2024-11-12T12:01:08.496000000Z",
      "entry_values": {
        "stage": [
          {
            "active_from": "2024-11-12T12:01:08.496000000Z",
            "active_until": null,
            "created_by_actor": {
              "type": "workspace-member",
              "id": "bbe415be-7a1d-45c7-9a8b-2af7b3cc962a"
            },
            "status": {
              "id": {
                "workspace_id": "515117c4-5fd1-4bfd-bc63-58f639d3f357",
                "object_id": "030f5287-761d-42ef-9feb-7d2e9a1ba52b",
                "attribute_id": "1a04f7e7-9392-40cb-9071-b1024f2eec73",
                "status_id": "10e0b809-893f-438a-a6a4-d69153c38ddc"
              },
              "title": "Prospecting",
              "is_archived": false,
              "target_time_in_status": null,
              "celebration_enabled": false
            },
            "attribute_type": "status"
          }
        ],
        "entry_id": [
          {
            "active_from": "2024-11-12T12:01:08.496000000Z",
            "active_until": null,
            "created_by_actor": {
              "type": "workspace-member",
              "id": "bbe415be-7a1d-45c7-9a8b-2af7b3cc962a"
            },
            "value": "6ae76b3c-cc85-43bc-9443-ec25eac02192",
            "attribute_type": "text"
          }
        ],
        "main_point_of_contact": [],
        "owner": [
          {
            "active_from": "2024-11-12T12:01:08.496000000Z",
            "active_until": null,
            "created_by_actor": {
              "type": "workspace-member",
              "id": "bbe415be-7a1d-45c7-9a8b-2af7b3cc962a"
            },
            "referenced_actor_type": "workspace-member",
            "referenced_actor_id": "bbe415be-7a1d-45c7-9a8b-2af7b3cc962a",
            "attribute_type": "actor-reference"
          }
        ],
        "priority": [],
        "estimated_contract_value": [],
        "projected_close_date": [
          {
            "active_from": "2024-11-12T12:01:08.496000000Z",
            "active_until": null,
            "created_by_actor": {
              "type": "workspace-member",
              "id": "bbe415be-7a1d-45c7-9a8b-2af7b3cc962a"
            },
            "value": "2024-11-26",
            "attribute_type": "date"
          }
        ],
        "close_confidence": [],
        "close_lost_reason": [],
        "notes": [],
        "created_at": [
          {
            "active_from": "2024-11-12T12:01:08.496000000Z",
            "active_until": null,
            "created_by_actor": {
              "type": "workspace-member",
              "id": "bbe415be-7a1d-45c7-9a8b-2af7b3cc962a"
            },
            "value": "2024-11-12T12:01:08.524000000Z",
            "attribute_type": "timestamp"
          }
        ],
        "created_by": [
          {
            "active_from": "2024-11-12T12:01:08.496000000Z",
            "active_until": null,
            "created_by_actor": {
              "type": "workspace-member",
              "id": "bbe415be-7a1d-45c7-9a8b-2af7b3cc962a"
            },
            "referenced_actor_type": "workspace-member",
            "referenced_actor_id": "bbe415be-7a1d-45c7-9a8b-2af7b3cc962a",
            "attribute_type": "actor-reference"
          }
        ],
        "deal_name": [],
        "company": []
      }
    },
    {
      "id": {
        "workspace_id": "515117c4-5fd1-4bfd-bc63-58f639d3f357",
        "list_id": "030f5287-761d-42ef-9feb-7d2e9a1ba52b",
        "entry_id": "6d9a9e0c-6844-432e-a17a-dd048e3c64c8"
      },
      "parent_record_id": "fc653808-d43f-465b-8365-785a020bf39d",
      "parent_object": "companies",
      "created_at": "2024-11-12T12:01:10.888000000Z",
      "entry_values": {
        "stage": [
          {
            "active_from": "2024-11-12T12:01:10.888000000Z",
            "active_until": null,
            "created_by_actor": {
              "type": "workspace-member",
              "id": "bbe415be-7a1d-45c7-9a8b-2af7b3cc962a"
            },
            "status": {
              "id": {
                "workspace_id": "515117c4-5fd1-4bfd-bc63-58f639d3f357",
                "object_id": "030f5287-761d-42ef-9feb-7d2e9a1ba52b",
                "attribute_id": "1a04f7e7-9392-40cb-9071-b1024f2eec73",
                "status_id": "10e0b809-893f-438a-a6a4-d69153c38ddc"
              },
              "title": "Prospecting",
              "is_archived": false,
              "target_time_in_status": null,
              "celebration_enabled": false
            },
            "attribute_type": "status"
          }
        ],
        "entry_id": [
          {
            "active_from": "2024-11-12T12:01:10.888000000Z",
            "active_until": null,
            "created_by_actor": {
              "type": "workspace-member",
              "id": "bbe415be-7a1d-45c7-9a8b-2af7b3cc962a"
            },
            "value": "6d9a9e0c-6844-432e-a17a-dd048e3c64c8",
            "attribute_type": "text"
          }
        ],
        "main_point_of_contact": [],
        "owner": [
          {
            "active_from": "2024-11-12T12:01:10.888000000Z",
            "active_until": null,
            "created_by_actor": {
              "type": "workspace-member",
              "id": "bbe415be-7a1d-45c7-9a8b-2af7b3cc962a"
            },
            "referenced_actor_type": "workspace-member",
            "referenced_actor_id": "bbe415be-7a1d-45c7-9a8b-2af7b3cc962a",
            "attribute_type": "actor-reference"
          }
        ],
        "priority": [],
        "estimated_contract_value": [],
        "projected_close_date": [
          {
            "active_from": "2024-11-12T12:01:10.888000000Z",
            "active_until": null,
            "created_by_actor": {
              "type": "workspace-member",
              "id": "bbe415be-7a1d-45c7-9a8b-2af7b3cc962a"
            },
            "value": "2024-11-26",
            "attribute_type": "date"
          }
        ],
        "close_confidence": [],
        "close_lost_reason": [],
        "notes": [],
        "created_at": [
          {
            "active_from": "2024-11-12T12:01:10.888000000Z",
            "active_until": null,
            "created_by_actor": {
              "type": "workspace-member",
              "id": "bbe415be-7a1d-45c7-9a8b-2af7b3cc962a"
            },
            "value": "2024-11-12T12:01:10.919000000Z",
            "attribute_type": "timestamp"
          }
        ],
        "created_by": [
          {
            "active_from": "2024-11-12T12:01:10.888000000Z",
            "active_until": null,
            "created_by_actor": {
              "type": "workspace-member",
              "id": "bbe415be-7a1d-45c7-9a8b-2af7b3cc962a"
            },
            "referenced_actor_type": "workspace-member",
            "referenced_actor_id": "bbe415be-7a1d-45c7-9a8b-2af7b3cc962a",
            "attribute_type": "actor-reference"
          }
        ],
        "deal_name": [],
        "company": []
      }
    },
    {
      "id": {
        "workspace_id": "515117c4-5fd1-4bfd-bc63-58f639d3f357",
        "list_id": "030f5287-761d-42ef-9feb-7d2e9a1ba52b",
        "entry_id": "6f1f8ab9-63fb-40c0-878c-06339573252b"
      },
      "parent_record_id": "aa121fb7-d0d5-4675-a6bf-06937c10679e",
      "parent_object": "companies",
      "created_at": "2024-11-12T12:01:09.035000000Z",
      "entry_values": {
        "stage": [
          {
            "active_from": "2024-11-12T12:01:09.035000000Z",
            "active_until": null,
            "created_by_actor": {
              "type": "workspace-member",
              "id": "bbe415be-7a1d-45c7-9a8b-2af7b3cc962a"
            },
            "status": {
              "id": {
                "workspace_id": "515117c4-5fd1-4bfd-bc63-58f639d3f357",
                "object_id": "030f5287-761d-42ef-9feb-7d2e9a1ba52b",
                "attribute_id": "1a04f7e7-9392-40cb-9071-b1024f2eec73",
                "status_id": "10e0b809-893f-438a-a6a4-d69153c38ddc"
              },
              "title": "Prospecting",
              "is_archived": false,
              "target_time_in_status": null,
              "celebration_enabled": false
            },
            "attribute_type": "status"
          }
        ],
        "entry_id": [
          {
            "active_from": "2024-11-12T12:01:09.035000000Z",
            "active_until": null,
            "created_by_actor": {
              "type": "workspace-member",
              "id": "bbe415be-7a1d-45c7-9a8b-2af7b3cc962a"
            },
            "value": "6f1f8ab9-63fb-40c0-878c-06339573252b",
            "attribute_type": "text"
          }
        ],
        "main_point_of_contact": [],
        "owner": [
          {
            "active_from": "2024-11-12T12:01:09.035000000Z",
            "active_until": null,
            "created_by_actor": {
              "type": "workspace-member",
              "id": "bbe415be-7a1d-45c7-9a8b-2af7b3cc962a"
            },
            "referenced_actor_type": "workspace-member",
            "referenced_actor_id": "bbe415be-7a1d-45c7-9a8b-2af7b3cc962a",
            "attribute_type": "actor-reference"
          }
        ],
        "priority": [],
        "estimated_contract_value": [],
        "projected_close_date": [
          {
            "active_from": "2024-11-12T12:01:09.035000000Z",
            "active_until": null,
            "created_by_actor": {
              "type": "workspace-member",
              "id": "bbe415be-7a1d-45c7-9a8b-2af7b3cc962a"
            },
            "value": "2024-11-26",
            "attribute_type": "date"
          }
        ],
        "close_confidence": [],
        "close_lost_reason": [],
        "notes": [],
        "created_at": [
          {
            "active_from": "2024-11-12T12:01:09.035000000Z",
            "active_until": null,
            "created_by_actor": {
              "type": "workspace-member",
              "id": "bbe415be-7a1d-45c7-9a8b-2af7b3cc962a"
            },
            "value": "2024-11-12T12:01:09.064000000Z",
            "attribute_type": "timestamp"
          }
        ],
        "created_by": [
          {
            "active_from": "2024-11-12T12:01:09.035000000Z",
            "active_until": null,
            "created_by_actor": {
              "type": "workspace-member",
              "id": "bbe415be-7a1d-45c7-9a8b-2af7b3cc962a"
            },
            "referenced_actor_type": "workspace-member",
            "referenced_actor_id": "bbe415be-7a1d-45c7-9a8b-2af7b3cc962a",
            "attribute_type": "actor-reference"
          }
        ],
        "deal_name": [],
        "company": []
      }
    },
    {
      "id": {
        "workspace_id": "515117c4-5fd1-4bfd-bc63-58f639d3f357",
        "list_id": "030f5287-761d-42ef-9feb-7d2e9a1ba52b",
        "entry_id": "771fd82b-8b60-4735-adb3-9fca861e6c72"
      },
      "parent_record_id": "32b2889f-668c-4f53-96b4-4a753eae5a03",
      "parent_object": "companies",
      "created_at": "2024-11-12T12:01:06.575000000Z",
      "entry_values": {
        "stage": [
          {
            "active_from": "2024-11-12T12:01:06.575000000Z",
            "active_until": null,
            "created_by_actor": {
              "type": "workspace-member",
              "id": "bbe415be-7a1d-45c7-9a8b-2af7b3cc962a"
            },
            "status": {
              "id": {
                "workspace_id": "515117c4-5fd1-4bfd-bc63-58f639d3f357",
                "object_id": "030f5287-761d-42ef-9feb-7d2e9a1ba52b",
                "attribute_id": "1a04f7e7-9392-40cb-9071-b1024f2eec73",
                "status_id": "10e0b809-893f-438a-a6a4-d69153c38ddc"
              },
              "title": "Prospecting",
              "is_archived": false,
              "target_time_in_status": null,
              "celebration_enabled": false
            },
            "attribute_type": "status"
          }
        ],
        "entry_id": [
          {
            "active_from": "2024-11-12T12:01:06.575000000Z",
            "active_until": null,
            "created_by_actor": {
              "type": "workspace-member",
              "id": "bbe415be-7a1d-45c7-9a8b-2af7b3cc962a"
            },
            "value": "771fd82b-8b60-4735-adb3-9fca861e6c72",
            "attribute_type": "text"
          }
        ],
        "main_point_of_contact": [],
        "owner": [
          {
            "active_from": "2024-11-12T12:01:06.575000000Z",
            "active_until": null,
            "created_by_actor": {
              "type": "workspace-member",
              "id": "bbe415be-7a1d-45c7-9a8b-2af7b3cc962a"
            },
            "referenced_actor_type": "workspace-member",
            "referenced_actor_id": "bbe415be-7a1d-45c7-9a8b-2af7b3cc962a",
            "attribute_type": "actor-reference"
          }
        ],
        "priority": [],
        "estimated_contract_value": [],
        "projected_close_date": [
          {
            "active_from": "2024-11-12T12:01:06.575000000Z",
            "active_until": null,
            "created_by_actor": {
              "type": "workspace-member",
              "id": "bbe415be-7a1d-45c7-9a8b-2af7b3cc962a"
            },
            "value": "2024-11-26",
            "attribute_type": "date"
          }
        ],
        "close_confidence": [],
        "close_lost_reason": [],
        "notes": [],
        "created_at": [
          {
            "active_from": "2024-11-12T12:01:06.575000000Z",
            "active_until": null,
            "created_by_actor": {
              "type": "workspace-member",
              "id": "bbe415be-7a1d-45c7-9a8b-2af7b3cc962a"
            },
            "value": "2024-11-12T12:01:06.616000000Z",
            "attribute_type": "timestamp"
          }
        ],
        "created_by": [
          {
            "active_from": "2024-11-12T12:01:06.575000000Z",
            "active_until": null,
            "created_by_actor": {
              "type": "workspace-member",
              "id": "bbe415be-7a1d-45c7-9a8b-2af7b3cc962a"
            },
            "referenced_actor_type": "workspace-member",
            "referenced_actor_id": "bbe415be-7a1d-45c7-9a8b-2af7b3cc962a",
            "attribute_type": "actor-reference"
          }
        ],
        "deal_name": [],
        "company": []
      }
    },
    {
      "id": {
        "workspace_id": "515117c4-5fd1-4bfd-bc63-58f639d3f357",
        "list_id": "030f5287-761d-42ef-9feb-7d2e9a1ba52b",
        "entry_id": "77d97973-ac09-42cc-af63-83faca52f748"
      },
      "parent_record_id": "bd48cb8f-8f2f-4b8d-b217-ef3310f570e4",
      "parent_object": "companies",
      "created_at": "2024-11-12T12:01:09.729000000Z",
      "entry_values": {
        "stage": [
          {
            "active_from": "2024-11-12T12:01:09.729000000Z",
            "active_until": null,
            "created_by_actor": {
              "type": "workspace-member",
              "id": "bbe415be-7a1d-45c7-9a8b-2af7b3cc962a"
            },
            "status": {
              "id": {
                "workspace_id": "515117c4-5fd1-4bfd-bc63-58f639d3f357",
                "object_id": "030f5287-761d-42ef-9feb-7d2e9a1ba52b",
                "attribute_id": "1a04f7e7-9392-40cb-9071-b1024f2eec73",
                "status_id": "10e0b809-893f-438a-a6a4-d69153c38ddc"
              },
              "title": "Prospecting",
              "is_archived": false,
              "target_time_in_status": null,
              "celebration_enabled": false
            },
            "attribute_type": "status"
          }
        ],
        "entry_id": [
          {
            "active_from": "2024-11-12T12:01:09.729000000Z",
            "active_until": null,
            "created_by_actor": {
              "type": "workspace-member",
              "id": "bbe415be-7a1d-45c7-9a8b-2af7b3cc962a"
            },
            "value": "77d97973-ac09-42cc-af63-83faca52f748",
            "attribute_type": "text"
          }
        ],
        "main_point_of_contact": [],
        "owner": [
          {
            "active_from": "2024-11-12T12:01:09.729000000Z",
            "active_until": null,
            "created_by_actor": {
              "type": "workspace-member",
              "id": "bbe415be-7a1d-45c7-9a8b-2af7b3cc962a"
            },
            "referenced_actor_type": "workspace-member",
            "referenced_actor_id": "bbe415be-7a1d-45c7-9a8b-2af7b3cc962a",
            "attribute_type": "actor-reference"
          }
        ],
        "priority": [],
        "estimated_contract_value": [],
        "projected_close_date": [
          {
            "active_from": "2024-11-12T12:01:09.729000000Z",
            "active_until": null,
            "created_by_actor": {
              "type": "workspace-member",
              "id": "bbe415be-7a1d-45c7-9a8b-2af7b3cc962a"
            },
            "value": "2024-11-26",
            "attribute_type": "date"
          }
        ],
        "close_confidence": [],
        "close_lost_reason": [],
        "notes": [],
        "created_at": [
          {
            "active_from": "2024-11-12T12:01:09.729000000Z",
            "active_until": null,
            "created_by_actor": {
              "type": "workspace-member",
              "id": "bbe415be-7a1d-45c7-9a8b-2af7b3cc962a"
            },
            "value": "2024-11-12T12:01:09.778000000Z",
            "attribute_type": "timestamp"
          }
        ],
        "created_by": [
          {
            "active_from": "2024-11-12T12:01:09.729000000Z",
            "active_until": null,
            "created_by_actor": {
              "type": "workspace-member",
              "id": "bbe415be-7a1d-45c7-9a8b-2af7b3cc962a"
            },
            "referenced_actor_type": "workspace-member",
            "referenced_actor_id": "bbe415be-7a1d-45c7-9a8b-2af7b3cc962a",
            "attribute_type": "actor-reference"
          }
        ],
        "deal_name": [],
        "company": []
      }
    },
    {
      "id": {
        "workspace_id": "515117c4-5fd1-4bfd-bc63-58f639d3f357",
        "list_id": "030f5287-761d-42ef-9feb-7d2e9a1ba52b",
        "entry_id": "814752b5-2bf2-4152-a6d6-ed5cf90f9d08"
      },
      "parent_record_id": "350fa7dd-1c39-493e-9dda-c010f7d0d089",
      "parent_object": "companies",
      "created_at": "2024-11-12T12:01:06.587000000Z",
      "entry_values": {
        "stage": [
          {
            "active_from": "2024-11-12T12:01:06.587000000Z",
            "active_until": null,
            "created_by_actor": {
              "type": "workspace-member",
              "id": "bbe415be-7a1d-45c7-9a8b-2af7b3cc962a"
            },
            "status": {
              "id": {
                "workspace_id": "515117c4-5fd1-4bfd-bc63-58f639d3f357",
                "object_id": "030f5287-761d-42ef-9feb-7d2e9a1ba52b",
                "attribute_id": "1a04f7e7-9392-40cb-9071-b1024f2eec73",
                "status_id": "10e0b809-893f-438a-a6a4-d69153c38ddc"
              },
              "title": "Prospecting",
              "is_archived": false,
              "target_time_in_status": null,
              "celebration_enabled": false
            },
            "attribute_type": "status"
          }
        ],
        "entry_id": [
          {
            "active_from": "2024-11-12T12:01:06.587000000Z",
            "active_until": null,
            "created_by_actor": {
              "type": "workspace-member",
              "id": "bbe415be-7a1d-45c7-9a8b-2af7b3cc962a"
            },
            "value": "814752b5-2bf2-4152-a6d6-ed5cf90f9d08",
            "attribute_type": "text"
          }
        ],
        "main_point_of_contact": [],
        "owner": [
          {
            "active_from": "2024-11-12T12:01:06.587000000Z",
            "active_until": null,
            "created_by_actor": {
              "type": "workspace-member",
              "id": "bbe415be-7a1d-45c7-9a8b-2af7b3cc962a"
            },
            "referenced_actor_type": "workspace-member",
            "referenced_actor_id": "bbe415be-7a1d-45c7-9a8b-2af7b3cc962a",
            "attribute_type": "actor-reference"
          }
        ],
        "priority": [],
        "estimated_contract_value": [],
        "projected_close_date": [
          {
            "active_from": "2024-11-12T12:01:06.587000000Z",
            "active_until": null,
            "created_by_actor": {
              "type": "workspace-member",
              "id": "bbe415be-7a1d-45c7-9a8b-2af7b3cc962a"
            },
            "value": "2024-11-26",
            "attribute_type": "date"
          }
        ],
        "close_confidence": [],
        "close_lost_reason": [],
        "notes": [],
        "created_at": [
          {
            "active_from": "2024-11-12T12:01:06.587000000Z",
            "active_until": null,
            "created_by_actor": {
              "type": "workspace-member",
              "id": "bbe415be-7a1d-45c7-9a8b-2af7b3cc962a"
            },
            "value": "2024-11-12T12:01:06.618000000Z",
            "attribute_type": "timestamp"
          }
        ],
        "created_by": [
          {
            "active_from": "2024-11-12T12:01:06.587000000Z",
            "active_until": null,
            "created_by_actor": {
              "type": "workspace-member",
              "id": "bbe415be-7a1d-45c7-9a8b-2af7b3cc962a"
            },
            "referenced_actor_type": "workspace-member",
            "referenced_actor_id": "bbe415be-7a1d-45c7-9a8b-2af7b3cc962a",
            "attribute_type": "actor-reference"
          }
        ],
        "deal_name": [],
        "company": []
      }
    },
    {
      "id": {
        "workspace_id": "515117c4-5fd1-4bfd-bc63-58f639d3f357",
        "list_id": "030f5287-761d-42ef-9feb-7d2e9a1ba52b",
        "entry_id": "86133d0d-5ab3-4cb3-84cb-30af08387ffb"
      },
      "parent_record_id": "58fd504d-4334-457a-b1b9-d797a0a2411d",
      "parent_object": "companies",
      "created_at": "2024-11-12T12:01:07.380000000Z",
      "entry_values": {
        "stage": [
          {
            "active_from": "2024-11-12T12:01:07.380000000Z",
            "active_until": null,
            "created_by_actor": {
              "type": "workspace-member",
              "id": "bbe415be-7a1d-45c7-9a8b-2af7b3cc962a"
            },
            "status": {
              "id": {
                "workspace_id": "515117c4-5fd1-4bfd-bc63-58f639d3f357",
                "object_id": "030f5287-761d-42ef-9feb-7d2e9a1ba52b",
                "attribute_id": "1a04f7e7-9392-40cb-9071-b1024f2eec73",
                "status_id": "10e0b809-893f-438a-a6a4-d69153c38ddc"
              },
              "title": "Prospecting",
              "is_archived": false,
              "target_time_in_status": null,
              "celebration_enabled": false
            },
            "attribute_type": "status"
          }
        ],
        "entry_id": [
          {
            "active_from": "2024-11-12T12:01:07.380000000Z",
            "active_until": null,
            "created_by_actor": {
              "type": "workspace-member",
              "id": "bbe415be-7a1d-45c7-9a8b-2af7b3cc962a"
            },
            "value": "86133d0d-5ab3-4cb3-84cb-30af08387ffb",
            "attribute_type": "text"
          }
        ],
        "main_point_of_contact": [],
        "owner": [
          {
            "active_from": "2024-11-12T12:01:07.380000000Z",
            "active_until": null,
            "created_by_actor": {
              "type": "workspace-member",
              "id": "bbe415be-7a1d-45c7-9a8b-2af7b3cc962a"
            },
            "referenced_actor_type": "workspace-member",
            "referenced_actor_id": "bbe415be-7a1d-45c7-9a8b-2af7b3cc962a",
            "attribute_type": "actor-reference"
          }
        ],
        "priority": [],
        "estimated_contract_value": [],
        "projected_close_date": [
          {
            "active_from": "2024-11-12T12:01:07.380000000Z",
            "active_until": null,
            "created_by_actor": {
              "type": "workspace-member",
              "id": "bbe415be-7a1d-45c7-9a8b-2af7b3cc962a"
            },
            "value": "2024-11-26",
            "attribute_type": "date"
          }
        ],
        "close_confidence": [],
        "close_lost_reason": [],
        "notes": [],
        "created_at": [
          {
            "active_from": "2024-11-12T12:01:07.380000000Z",
            "active_until": null,
            "created_by_actor": {
              "type": "workspace-member",
              "id": "bbe415be-7a1d-45c7-9a8b-2af7b3cc962a"
            },
            "value": "2024-11-12T12:01:07.448000000Z",
            "attribute_type": "timestamp"
          }
        ],
        "created_by": [
          {
            "active_from": "2024-11-12T12:01:07.380000000Z",
            "active_until": null,
            "created_by_actor": {
              "type": "workspace-member",
              "id": "bbe415be-7a1d-45c7-9a8b-2af7b3cc962a"
            },
            "referenced_actor_type": "workspace-member",
            "referenced_actor_id": "bbe415be-7a1d-45c7-9a8b-2af7b3cc962a",
            "attribute_type": "actor-reference"
          }
        ],
        "deal_name": [],
        "company": []
      }
    },
    {
      "id": {
        "workspace_id": "515117c4-5fd1-4bfd-bc63-58f639d3f357",
        "list_id": "030f5287-761d-42ef-9feb-7d2e9a1ba52b",
        "entry_id": "877c4b41-1d94-42a5-9100-ecc2ca91018e"
      },
      "parent_record_id": "16504cd8-6e0c-4091-9385-98dabfe378d8",
      "parent_object": "companies",
      "created_at": "2024-11-12T12:01:06.022000000Z",
      "entry_values": {
        "stage": [
          {
            "active_from": "2024-11-12T12:01:06.022000000Z",
            "active_until": null,
            "created_by_actor": {
              "type": "workspace-member",
              "id": "bbe415be-7a1d-45c7-9a8b-2af7b3cc962a"
            },
            "status": {
              "id": {
                "workspace_id": "515117c4-5fd1-4bfd-bc63-58f639d3f357",
                "object_id": "030f5287-761d-42ef-9feb-7d2e9a1ba52b",
                "attribute_id": "1a04f7e7-9392-40cb-9071-b1024f2eec73",
                "status_id": "10e0b809-893f-438a-a6a4-d69153c38ddc"
              },
              "title": "Prospecting",
              "is_archived": false,
              "target_time_in_status": null,
              "celebration_enabled": false
            },
            "attribute_type": "status"
          }
        ],
        "entry_id": [
          {
            "active_from": "2024-11-12T12:01:06.022000000Z",
            "active_until": null,
            "created_by_actor": {
              "type": "workspace-member",
              "id": "bbe415be-7a1d-45c7-9a8b-2af7b3cc962a"
            },
            "value": "877c4b41-1d94-42a5-9100-ecc2ca91018e",
            "attribute_type": "text"
          }
        ],
        "main_point_of_contact": [],
        "owner": [
          {
            "active_from": "2024-11-12T12:01:06.022000000Z",
            "active_until": null,
            "created_by_actor": {
              "type": "workspace-member",
              "id": "bbe415be-7a1d-45c7-9a8b-2af7b3cc962a"
            },
            "referenced_actor_type": "workspace-member",
            "referenced_actor_id": "bbe415be-7a1d-45c7-9a8b-2af7b3cc962a",
            "attribute_type": "actor-reference"
          }
        ],
        "priority": [],
        "estimated_contract_value": [],
        "projected_close_date": [
          {
            "active_from": "2024-11-12T12:01:06.022000000Z",
            "active_until": null,
            "created_by_actor": {
              "type": "workspace-member",
              "id": "bbe415be-7a1d-45c7-9a8b-2af7b3cc962a"
            },
            "value": "2024-11-26",
            "attribute_type": "date"
          }
        ],
        "close_confidence": [],
        "close_lost_reason": [],
        "notes": [],
        "created_at": [
          {
            "active_from": "2024-11-12T12:01:06.022000000Z",
            "active_until": null,
            "created_by_actor": {
              "type": "workspace-member",
              "id": "bbe415be-7a1d-45c7-9a8b-2af7b3cc962a"
            },
            "value": "2024-11-12T12:01:06.053000000Z",
            "attribute_type": "timestamp"
          }
        ],
        "created_by": [
          {
            "active_from": "2024-11-12T12:01:06.022000000Z",
            "active_until": null,
            "created_by_actor": {
              "type": "workspace-member",
              "id": "bbe415be-7a1d-45c7-9a8b-2af7b3cc962a"
            },
            "referenced_actor_type": "workspace-member",
            "referenced_actor_id": "bbe415be-7a1d-45c7-9a8b-2af7b3cc962a",
            "attribute_type": "actor-reference"
          }
        ],
        "deal_name": [],
        "company": []
      }
    },
    {
      "id": {
        "workspace_id": "515117c4-5fd1-4bfd-bc63-58f639d3f357",
        "list_id": "030f5287-761d-42ef-9feb-7d2e9a1ba52b",
        "entry_id": "8ca0f53f-74ec-4479-bc88-5aec8ff30ee0"
      },
      "parent_record_id": "f77d15ad-7506-4ef5-b109-36450462b084",
      "parent_object": "companies",
      "created_at": "2024-11-12T12:01:10.671000000Z",
      "entry_values": {
        "stage": [
          {
            "active_from": "2024-11-12T12:01:10.671000000Z",
            "active_until": null,
            "created_by_actor": {
              "type": "workspace-member",
              "id": "bbe415be-7a1d-45c7-9a8b-2af7b3cc962a"
            },
            "status": {
              "id": {
                "workspace_id": "515117c4-5fd1-4bfd-bc63-58f639d3f357",
                "object_id": "030f5287-761d-42ef-9feb-7d2e9a1ba52b",
                "attribute_id": "1a04f7e7-9392-40cb-9071-b1024f2eec73",
                "status_id": "10e0b809-893f-438a-a6a4-d69153c38ddc"
              },
              "title": "Prospecting",
              "is_archived": false,
              "target_time_in_status": null,
              "celebration_enabled": false
            },
            "attribute_type": "status"
          }
        ],
        "entry_id": [
          {
            "active_from": "2024-11-12T12:01:10.671000000Z",
            "active_until": null,
            "created_by_actor": {
              "type": "workspace-member",
              "id": "bbe415be-7a1d-45c7-9a8b-2af7b3cc962a"
            },
            "value": "8ca0f53f-74ec-4479-bc88-5aec8ff30ee0",
            "attribute_type": "text"
          }
        ],
        "main_point_of_contact": [],
        "owner": [
          {
            "active_from": "2024-11-12T12:01:10.671000000Z",
            "active_until": null,
            "created_by_actor": {
              "type": "workspace-member",
              "id": "bbe415be-7a1d-45c7-9a8b-2af7b3cc962a"
            },
            "referenced_actor_type": "workspace-member",
            "referenced_actor_id": "bbe415be-7a1d-45c7-9a8b-2af7b3cc962a",
            "attribute_type": "actor-reference"
          }
        ],
        "priority": [],
        "estimated_contract_value": [],
        "projected_close_date": [
          {
            "active_from": "2024-11-12T12:01:10.671000000Z",
            "active_until": null,
            "created_by_actor": {
              "type": "workspace-member",
              "id": "bbe415be-7a1d-45c7-9a8b-2af7b3cc962a"
            },
            "value": "2024-11-26",
            "attribute_type": "date"
          }
        ],
        "close_confidence": [],
        "close_lost_reason": [],
        "notes": [],
        "created_at": [
          {
            "active_from": "2024-11-12T12:01:10.671000000Z",
            "active_until": null,
            "created_by_actor": {
              "type": "workspace-member",
              "id": "bbe415be-7a1d-45c7-9a8b-2af7b3cc962a"
            },
            "value": "2024-11-12T12:01:10.715000000Z",
            "attribute_type": "timestamp"
          }
        ],
        "created_by": [
          {
            "active_from": "2024-11-12T12:01:10.671000000Z",
            "active_until": null,
            "created_by_actor": {
              "type": "workspace-member",
              "id": "bbe415be-7a1d-45c7-9a8b-2af7b3cc962a"
            },
            "referenced_actor_type": "workspace-member",
            "referenced_actor_id": "bbe415be-7a1d-45c7-9a8b-2af7b3cc962a",
            "attribute_type": "actor-reference"
          }
        ],
        "deal_name": [],
        "company": []
      }
    },
    {
      "id": {
        "workspace_id": "515117c4-5fd1-4bfd-bc63-58f639d3f357",
        "list_id": "030f5287-761d-42ef-9feb-7d2e9a1ba52b",
        "entry_id": "9034340a-7c2a-4e74-8dc5-0a99497b57e6"
      },
      "parent_record_id": "cd6c4f2e-5f5f-471f-86df-8380ae5cd1ec",
      "parent_object": "companies",
      "created_at": "2024-11-12T12:01:09.978000000Z",
      "entry_values": {
        "stage": [
          {
            "active_from": "2024-11-12T12:01:09.978000000Z",
            "active_until": null,
            "created_by_actor": {
              "type": "workspace-member",
              "id": "bbe415be-7a1d-45c7-9a8b-2af7b3cc962a"
            },
            "status": {
              "id": {
                "workspace_id": "515117c4-5fd1-4bfd-bc63-58f639d3f357",
                "object_id": "030f5287-761d-42ef-9feb-7d2e9a1ba52b",
                "attribute_id": "1a04f7e7-9392-40cb-9071-b1024f2eec73",
                "status_id": "10e0b809-893f-438a-a6a4-d69153c38ddc"
              },
              "title": "Prospecting",
              "is_archived": false,
              "target_time_in_status": null,
              "celebration_enabled": false
            },
            "attribute_type": "status"
          }
        ],
        "entry_id": [
          {
            "active_from": "2024-11-12T12:01:09.978000000Z",
            "active_until": null,
            "created_by_actor": {
              "type": "workspace-member",
              "id": "bbe415be-7a1d-45c7-9a8b-2af7b3cc962a"
            },
            "value": "9034340a-7c2a-4e74-8dc5-0a99497b57e6",
            "attribute_type": "text"
          }
        ],
        "main_point_of_contact": [],
        "owner": [
          {
            "active_from": "2024-11-12T12:01:09.978000000Z",
            "active_until": null,
            "created_by_actor": {
              "type": "workspace-member",
              "id": "bbe415be-7a1d-45c7-9a8b-2af7b3cc962a"
            },
            "referenced_actor_type": "workspace-member",
            "referenced_actor_id": "bbe415be-7a1d-45c7-9a8b-2af7b3cc962a",
            "attribute_type": "actor-reference"
          }
        ],
        "priority": [],
        "estimated_contract_value": [],
        "projected_close_date": [
          {
            "active_from": "2024-11-12T12:01:09.978000000Z",
            "active_until": null,
            "created_by_actor": {
              "type": "workspace-member",
              "id": "bbe415be-7a1d-45c7-9a8b-2af7b3cc962a"
            },
            "value": "2024-11-26",
            "attribute_type": "date"
          }
        ],
        "close_confidence": [],
        "close_lost_reason": [],
        "notes": [],
        "created_at": [
          {
            "active_from": "2024-11-12T12:01:09.978000000Z",
            "active_until": null,
            "created_by_actor": {
              "type": "workspace-member",
              "id": "bbe415be-7a1d-45c7-9a8b-2af7b3cc962a"
            },
            "value": "2024-11-12T12:01:10.014000000Z",
            "attribute_type": "timestamp"
          }
        ],
        "created_by": [
          {
            "active_from": "2024-11-12T12:01:09.978000000Z",
            "active_until": null,
            "created_by_actor": {
              "type": "workspace-member",
              "id": "bbe415be-7a1d-45c7-9a8b-2af7b3cc962a"
            },
            "referenced_actor_type": "workspace-member",
            "referenced_actor_id": "bbe415be-7a1d-45c7-9a8b-2af7b3cc962a",
            "attribute_type": "actor-reference"
          }
        ],
        "deal_name": [],
        "company": []
      }
    },
    {
      "id": {
        "workspace_id": "515117c4-5fd1-4bfd-bc63-58f639d3f357",
        "list_id": "030f5287-761d-42ef-9feb-7d2e9a1ba52b",
        "entry_id": "9487bd35-ec5d-42f9-ac47-f4120201574f"
      },
      "parent_record_id": "96036ed8-65fd-415f-8829-fd01812ce489",
      "parent_object": "companies",
      "created_at": "2024-11-12T12:01:08.591000000Z",
      "entry_values": {
        "stage": [
          {
            "active_from": "2024-11-12T12:01:08.591000000Z",
            "active_until": null,
            "created_by_actor": {
              "type": "workspace-member",
              "id": "bbe415be-7a1d-45c7-9a8b-2af7b3cc962a"
            },
            "status": {
              "id": {
                "workspace_id": "515117c4-5fd1-4bfd-bc63-58f639d3f357",
                "object_id": "030f5287-761d-42ef-9feb-7d2e9a1ba52b",
                "attribute_id": "1a04f7e7-9392-40cb-9071-b1024f2eec73",
                "status_id": "10e0b809-893f-438a-a6a4-d69153c38ddc"
              },
              "title": "Prospecting",
              "is_archived": false,
              "target_time_in_status": null,
              "celebration_enabled": false
            },
            "attribute_type": "status"
          }
        ],
        "entry_id": [
          {
            "active_from": "2024-11-12T12:01:08.591000000Z",
            "active_until": null,
            "created_by_actor": {
              "type": "workspace-member",
              "id": "bbe415be-7a1d-45c7-9a8b-2af7b3cc962a"
            },
            "value": "9487bd35-ec5d-42f9-ac47-f4120201574f",
            "attribute_type": "text"
          }
        ],
        "main_point_of_contact": [],
        "owner": [
          {
            "active_from": "2024-11-12T12:01:08.591000000Z",
            "active_until": null,
            "created_by_actor": {
              "type": "workspace-member",
              "id": "bbe415be-7a1d-45c7-9a8b-2af7b3cc962a"
            },
            "referenced_actor_type": "workspace-member",
            "referenced_actor_id": "bbe415be-7a1d-45c7-9a8b-2af7b3cc962a",
            "attribute_type": "actor-reference"
          }
        ],
        "priority": [],
        "estimated_contract_value": [],
        "projected_close_date": [
          {
            "active_from": "2024-11-12T12:01:08.591000000Z",
            "active_until": null,
            "created_by_actor": {
              "type": "workspace-member",
              "id": "bbe415be-7a1d-45c7-9a8b-2af7b3cc962a"
            },
            "value": "2024-11-26",
            "attribute_type": "date"
          }
        ],
        "close_confidence": [],
        "close_lost_reason": [],
        "notes": [],
        "created_at": [
          {
            "active_from": "2024-11-12T12:01:08.591000000Z",
            "active_until": null,
            "created_by_actor": {
              "type": "workspace-member",
              "id": "bbe415be-7a1d-45c7-9a8b-2af7b3cc962a"
            },
            "value": "2024-11-12T12:01:08.624000000Z",
            "attribute_type": "timestamp"
          }
        ],
        "created_by": [
          {
            "active_from": "2024-11-12T12:01:08.591000000Z",
            "active_until": null,
            "created_by_actor": {
              "type": "workspace-member",
              "id": "bbe415be-7a1d-45c7-9a8b-2af7b3cc962a"
            },
            "referenced_actor_type": "workspace-member",
            "referenced_actor_id": "bbe415be-7a1d-45c7-9a8b-2af7b3cc962a",
            "attribute_type": "actor-reference"
          }
        ],
        "deal_name": [],
        "company": []
      }
    },
    {
      "id": {
        "workspace_id": "515117c4-5fd1-4bfd-bc63-58f639d3f357",
        "list_id": "030f5287-761d-42ef-9feb-7d2e9a1ba52b",
        "entry_id": "9548dd25-b292-4273-8154-e1c3f91256ef"
      },
      "parent_record_id": "8dca2a1f-0d32-4e8d-a303-0bbc5bffa2df",
      "parent_object": "companies",
      "created_at": "2024-11-12T12:01:08.352000000Z",
      "entry_values": {
        "stage": [
          {
            "active_from": "2024-11-12T12:01:08.352000000Z",
            "active_until": null,
            "created_by_actor": {
              "type": "workspace-member",
              "id": "bbe415be-7a1d-45c7-9a8b-2af7b3cc962a"
            },
            "status": {
              "id": {
                "workspace_id": "515117c4-5fd1-4bfd-bc63-58f639d3f357",
                "object_id": "030f5287-761d-42ef-9feb-7d2e9a1ba52b",
                "attribute_id": "1a04f7e7-9392-40cb-9071-b1024f2eec73",
                "status_id": "10e0b809-893f-438a-a6a4-d69153c38ddc"
              },
              "title": "Prospecting",
              "is_archived": false,
              "target_time_in_status": null,
              "celebration_enabled": false
            },
            "attribute_type": "status"
          }
        ],
        "entry_id": [
          {
            "active_from": "2024-11-12T12:01:08.352000000Z",
            "active_until": null,
            "created_by_actor": {
              "type": "workspace-member",
              "id": "bbe415be-7a1d-45c7-9a8b-2af7b3cc962a"
            },
            "value": "9548dd25-b292-4273-8154-e1c3f91256ef",
            "attribute_type": "text"
          }
        ],
        "main_point_of_contact": [],
        "owner": [
          {
            "active_from": "2024-11-12T12:01:08.352000000Z",
            "active_until": null,
            "created_by_actor": {
              "type": "workspace-member",
              "id": "bbe415be-7a1d-45c7-9a8b-2af7b3cc962a"
            },
            "referenced_actor_type": "workspace-member",
            "referenced_actor_id": "bbe415be-7a1d-45c7-9a8b-2af7b3cc962a",
            "attribute_type": "actor-reference"
          }
        ],
        "priority": [],
        "estimated_contract_value": [],
        "projected_close_date": [
          {
            "active_from": "2024-11-12T12:01:08.352000000Z",
            "active_until": null,
            "created_by_actor": {
              "type": "workspace-member",
              "id": "bbe415be-7a1d-45c7-9a8b-2af7b3cc962a"
            },
            "value": "2024-11-26",
            "attribute_type": "date"
          }
        ],
        "close_confidence": [],
        "close_lost_reason": [],
        "notes": [],
        "created_at": [
          {
            "active_from": "2024-11-12T12:01:08.352000000Z",
            "active_until": null,
            "created_by_actor": {
              "type": "workspace-member",
              "id": "bbe415be-7a1d-45c7-9a8b-2af7b3cc962a"
            },
            "value": "2024-11-12T12:01:08.388000000Z",
            "attribute_type": "timestamp"
          }
        ],
        "created_by": [
          {
            "active_from": "2024-11-12T12:01:08.352000000Z",
            "active_until": null,
            "created_by_actor": {
              "type": "workspace-member",
              "id": "bbe415be-7a1d-45c7-9a8b-2af7b3cc962a"
            },
            "referenced_actor_type": "workspace-member",
            "referenced_actor_id": "bbe415be-7a1d-45c7-9a8b-2af7b3cc962a",
            "attribute_type": "actor-reference"
          }
        ],
        "deal_name": [],
        "company": []
      }
    },
    {
      "id": {
        "workspace_id": "515117c4-5fd1-4bfd-bc63-58f639d3f357",
        "list_id": "030f5287-761d-42ef-9feb-7d2e9a1ba52b",
        "entry_id": "9890e067-4324-4ef1-9eae-6a02c4d40e0c"
      },
      "parent_record_id": "8eba8b59-f0c3-40be-974f-42eeefc199a1",
      "parent_object": "companies",
      "created_at": "2024-11-12T12:01:08.361000000Z",
      "entry_values": {
        "stage": [
          {
            "active_from": "2024-11-12T12:01:08.361000000Z",
            "active_until": null,
            "created_by_actor": {
              "type": "workspace-member",
              "id": "bbe415be-7a1d-45c7-9a8b-2af7b3cc962a"
            },
            "status": {
              "id": {
                "workspace_id": "515117c4-5fd1-4bfd-bc63-58f639d3f357",
                "object_id": "030f5287-761d-42ef-9feb-7d2e9a1ba52b",
                "attribute_id": "1a04f7e7-9392-40cb-9071-b1024f2eec73",
                "status_id": "10e0b809-893f-438a-a6a4-d69153c38ddc"
              },
              "title": "Prospecting",
              "is_archived": false,
              "target_time_in_status": null,
              "celebration_enabled": false
            },
            "attribute_type": "status"
          }
        ],
        "entry_id": [
          {
            "active_from": "2024-11-12T12:01:08.361000000Z",
            "active_until": null,
            "created_by_actor": {
              "type": "workspace-member",
              "id": "bbe415be-7a1d-45c7-9a8b-2af7b3cc962a"
            },
            "value": "9890e067-4324-4ef1-9eae-6a02c4d40e0c",
            "attribute_type": "text"
          }
        ],
        "main_point_of_contact": [],
        "owner": [
          {
            "active_from": "2024-11-12T12:01:08.361000000Z",
            "active_until": null,
            "created_by_actor": {
              "type": "workspace-member",
              "id": "bbe415be-7a1d-45c7-9a8b-2af7b3cc962a"
            },
            "referenced_actor_type": "workspace-member",
            "referenced_actor_id": "bbe415be-7a1d-45c7-9a8b-2af7b3cc962a",
            "attribute_type": "actor-reference"
          }
        ],
        "priority": [],
        "estimated_contract_value": [],
        "projected_close_date": [
          {
            "active_from": "2024-11-12T12:01:08.361000000Z",
            "active_until": null,
            "created_by_actor": {
              "type": "workspace-member",
              "id": "bbe415be-7a1d-45c7-9a8b-2af7b3cc962a"
            },
            "value": "2024-11-26",
            "attribute_type": "date"
          }
        ],
        "close_confidence": [],
        "close_lost_reason": [],
        "notes": [],
        "created_at": [
          {
            "active_from": "2024-11-12T12:01:08.361000000Z",
            "active_until": null,
            "created_by_actor": {
              "type": "workspace-member",
              "id": "bbe415be-7a1d-45c7-9a8b-2af7b3cc962a"
            },
            "value": "2024-11-12T12:01:08.389000000Z",
            "attribute_type": "timestamp"
          }
        ],
        "created_by": [
          {
            "active_from": "2024-11-12T12:01:08.361000000Z",
            "active_until": null,
            "created_by_actor": {
              "type": "workspace-member",
              "id": "bbe415be-7a1d-45c7-9a8b-2af7b3cc962a"
            },
            "referenced_actor_type": "workspace-member",
            "referenced_actor_id": "bbe415be-7a1d-45c7-9a8b-2af7b3cc962a",
            "attribute_type": "actor-reference"
          }
        ],
        "deal_name": [],
        "company": []
      }
    },
    {
      "id": {
        "workspace_id": "515117c4-5fd1-4bfd-bc63-58f639d3f357",
        "list_id": "030f5287-761d-42ef-9feb-7d2e9a1ba52b",
        "entry_id": "9abb5505-8a4a-4734-9d11-aeca477d2ee2"
      },
      "parent_record_id": "437df222-c97e-4300-8a5a-d10831895ae2",
      "parent_object": "companies",
      "created_at": "2024-11-12T12:01:06.777000000Z",
      "entry_values": {
        "stage": [
          {
            "active_from": "2024-11-12T12:01:06.777000000Z",
            "active_until": null,
            "created_by_actor": {
              "type": "workspace-member",
              "id": "bbe415be-7a1d-45c7-9a8b-2af7b3cc962a"
            },
            "status": {
              "id": {
                "workspace_id": "515117c4-5fd1-4bfd-bc63-58f639d3f357",
                "object_id": "030f5287-761d-42ef-9feb-7d2e9a1ba52b",
                "attribute_id": "1a04f7e7-9392-40cb-9071-b1024f2eec73",
                "status_id": "10e0b809-893f-438a-a6a4-d69153c38ddc"
              },
              "title": "Prospecting",
              "is_archived": false,
              "target_time_in_status": null,
              "celebration_enabled": false
            },
            "attribute_type": "status"
          }
        ],
        "entry_id": [
          {
            "active_from": "2024-11-12T12:01:06.777000000Z",
            "active_until": null,
            "created_by_actor": {
              "type": "workspace-member",
              "id": "bbe415be-7a1d-45c7-9a8b-2af7b3cc962a"
            },
            "value": "9abb5505-8a4a-4734-9d11-aeca477d2ee2",
            "attribute_type": "text"
          }
        ],
        "main_point_of_contact": [],
        "owner": [
          {
            "active_from": "2024-11-12T12:01:06.777000000Z",
            "active_until": null,
            "created_by_actor": {
              "type": "workspace-member",
              "id": "bbe415be-7a1d-45c7-9a8b-2af7b3cc962a"
            },
            "referenced_actor_type": "workspace-member",
            "referenced_actor_id": "bbe415be-7a1d-45c7-9a8b-2af7b3cc962a",
            "attribute_type": "actor-reference"
          }
        ],
        "priority": [],
        "estimated_contract_value": [],
        "projected_close_date": [
          {
            "active_from": "2024-11-12T12:01:06.777000000Z",
            "active_until": null,
            "created_by_actor": {
              "type": "workspace-member",
              "id": "bbe415be-7a1d-45c7-9a8b-2af7b3cc962a"
            },
            "value": "2024-11-26",
            "attribute_type": "date"
          }
        ],
        "close_confidence": [],
        "close_lost_reason": [],
        "notes": [],
        "created_at": [
          {
            "active_from": "2024-11-12T12:01:06.777000000Z",
            "active_until": null,
            "created_by_actor": {
              "type": "workspace-member",
              "id": "bbe415be-7a1d-45c7-9a8b-2af7b3cc962a"
            },
            "value": "2024-11-12T12:01:06.811000000Z",
            "attribute_type": "timestamp"
          }
        ],
        "created_by": [
          {
            "active_from": "2024-11-12T12:01:06.777000000Z",
            "active_until": null,
            "created_by_actor": {
              "type": "workspace-member",
              "id": "bbe415be-7a1d-45c7-9a8b-2af7b3cc962a"
            },
            "referenced_actor_type": "workspace-member",
            "referenced_actor_id": "bbe415be-7a1d-45c7-9a8b-2af7b3cc962a",
            "attribute_type": "actor-reference"
          }
        ],
        "deal_name": [],
        "company": []
      }
    },
    {
      "id": {
        "workspace_id": "515117c4-5fd1-4bfd-bc63-58f639d3f357",
        "list_id": "030f5287-761d-42ef-9feb-7d2e9a1ba52b",
        "entry_id": "9c4bc583-2bfb-4de3-922c-ea2f78d2ca9d"
      },
      "parent_record_id": "b279a5d8-b9e1-430c-b966-1c2824ac6afc",
      "parent_object": "companies",
      "created_at": "2024-11-12T12:01:09.581000000Z",
      "entry_values": {
        "stage": [
          {
            "active_from": "2024-11-12T12:01:09.581000000Z",
            "active_until": null,
            "created_by_actor": {
              "type": "workspace-member",
              "id": "bbe415be-7a1d-45c7-9a8b-2af7b3cc962a"
            },
            "status": {
              "id": {
                "workspace_id": "515117c4-5fd1-4bfd-bc63-58f639d3f357",
                "object_id": "030f5287-761d-42ef-9feb-7d2e9a1ba52b",
                "attribute_id": "1a04f7e7-9392-40cb-9071-b1024f2eec73",
                "status_id": "10e0b809-893f-438a-a6a4-d69153c38ddc"
              },
              "title": "Prospecting",
              "is_archived": false,
              "target_time_in_status": null,
              "celebration_enabled": false
            },
            "attribute_type": "status"
          }
        ],
        "entry_id": [
          {
            "active_from": "2024-11-12T12:01:09.581000000Z",
            "active_until": null,
            "created_by_actor": {
              "type": "workspace-member",
              "id": "bbe415be-7a1d-45c7-9a8b-2af7b3cc962a"
            },
            "value": "9c4bc583-2bfb-4de3-922c-ea2f78d2ca9d",
            "attribute_type": "text"
          }
        ],
        "main_point_of_contact": [],
        "owner": [
          {
            "active_from": "2024-11-12T12:01:09.581000000Z",
            "active_until": null,
            "created_by_actor": {
              "type": "workspace-member",
              "id": "bbe415be-7a1d-45c7-9a8b-2af7b3cc962a"
            },
            "referenced_actor_type": "workspace-member",
            "referenced_actor_id": "bbe415be-7a1d-45c7-9a8b-2af7b3cc962a",
            "attribute_type": "actor-reference"
          }
        ],
        "priority": [],
        "estimated_contract_value": [],
        "projected_close_date": [
          {
            "active_from": "2024-11-12T12:01:09.581000000Z",
            "active_until": null,
            "created_by_actor": {
              "type": "workspace-member",
              "id": "bbe415be-7a1d-45c7-9a8b-2af7b3cc962a"
            },
            "value": "2024-11-26",
            "attribute_type": "date"
          }
        ],
        "close_confidence": [],
        "close_lost_reason": [],
        "notes": [],
        "created_at": [
          {
            "active_from": "2024-11-12T12:01:09.581000000Z",
            "active_until": null,
            "created_by_actor": {
              "type": "workspace-member",
              "id": "bbe415be-7a1d-45c7-9a8b-2af7b3cc962a"
            },
            "value": "2024-11-12T12:01:09.605000000Z",
            "attribute_type": "timestamp"
          }
        ],
        "created_by": [
          {
            "active_from": "2024-11-12T12:01:09.581000000Z",
            "active_until": null,
            "created_by_actor": {
              "type": "workspace-member",
              "id": "bbe415be-7a1d-45c7-9a8b-2af7b3cc962a"
            },
            "referenced_actor_type": "workspace-member",
            "referenced_actor_id": "bbe415be-7a1d-45c7-9a8b-2af7b3cc962a",
            "attribute_type": "actor-reference"
          }
        ],
        "deal_name": [],
        "company": []
      }
    },
    {
      "id": {
        "workspace_id": "515117c4-5fd1-4bfd-bc63-58f639d3f357",
        "list_id": "030f5287-761d-42ef-9feb-7d2e9a1ba52b",
        "entry_id": "9e1eeb52-8292-4b6e-bf8c-f83e1cc8116a"
      },
      "parent_record_id": "2702673d-0656-4cce-aceb-df1ca54f2fa3",
      "parent_object": "companies",
      "created_at": "2024-11-12T12:01:06.046000000Z",
      "entry_values": {
        "stage": [
          {
            "active_from": "2024-11-12T12:01:06.046000000Z",
            "active_until": null,
            "created_by_actor": {
              "type": "workspace-member",
              "id": "bbe415be-7a1d-45c7-9a8b-2af7b3cc962a"
            },
            "status": {
              "id": {
                "workspace_id": "515117c4-5fd1-4bfd-bc63-58f639d3f357",
                "object_id": "030f5287-761d-42ef-9feb-7d2e9a1ba52b",
                "attribute_id": "1a04f7e7-9392-40cb-9071-b1024f2eec73",
                "status_id": "10e0b809-893f-438a-a6a4-d69153c38ddc"
              },
              "title": "Prospecting",
              "is_archived": false,
              "target_time_in_status": null,
              "celebration_enabled": false
            },
            "attribute_type": "status"
          }
        ],
        "entry_id": [
          {
            "active_from": "2024-11-12T12:01:06.046000000Z",
            "active_until": null,
            "created_by_actor": {
              "type": "workspace-member",
              "id": "bbe415be-7a1d-45c7-9a8b-2af7b3cc962a"
            },
            "value": "9e1eeb52-8292-4b6e-bf8c-f83e1cc8116a",
            "attribute_type": "text"
          }
        ],
        "main_point_of_contact": [],
        "owner": [
          {
            "active_from": "2024-11-12T12:01:06.046000000Z",
            "active_until": null,
            "created_by_actor": {
              "type": "workspace-member",
              "id": "bbe415be-7a1d-45c7-9a8b-2af7b3cc962a"
            },
            "referenced_actor_type": "workspace-member",
            "referenced_actor_id": "bbe415be-7a1d-45c7-9a8b-2af7b3cc962a",
            "attribute_type": "actor-reference"
          }
        ],
        "priority": [],
        "estimated_contract_value": [],
        "projected_close_date": [
          {
            "active_from": "2024-11-12T12:01:06.046000000Z",
            "active_until": null,
            "created_by_actor": {
              "type": "workspace-member",
              "id": "bbe415be-7a1d-45c7-9a8b-2af7b3cc962a"
            },
            "value": "2024-11-26",
            "attribute_type": "date"
          }
        ],
        "close_confidence": [],
        "close_lost_reason": [],
        "notes": [],
        "created_at": [
          {
            "active_from": "2024-11-12T12:01:06.046000000Z",
            "active_until": null,
            "created_by_actor": {
              "type": "workspace-member",
              "id": "bbe415be-7a1d-45c7-9a8b-2af7b3cc962a"
            },
            "value": "2024-11-12T12:01:06.078000000Z",
            "attribute_type": "timestamp"
          }
        ],
        "created_by": [
          {
            "active_from": "2024-11-12T12:01:06.046000000Z",
            "active_until": null,
            "created_by_actor": {
              "type": "workspace-member",
              "id": "bbe415be-7a1d-45c7-9a8b-2af7b3cc962a"
            },
            "referenced_actor_type": "workspace-member",
            "referenced_actor_id": "bbe415be-7a1d-45c7-9a8b-2af7b3cc962a",
            "attribute_type": "actor-reference"
          }
        ],
        "deal_name": [],
        "company": []
      }
    },
    {
      "id": {
        "workspace_id": "515117c4-5fd1-4bfd-bc63-58f639d3f357",
        "list_id": "030f5287-761d-42ef-9feb-7d2e9a1ba52b",
        "entry_id": "a063b5d3-6a29-416b-9002-a309df7daabc"
      },
      "parent_record_id": "5e0de09f-bfc8-41e0-b6f0-6ae7a92d650f",
      "parent_object": "companies",
      "created_at": "2024-11-12T12:01:07.625000000Z",
      "entry_values": {
        "stage": [
          {
            "active_from": "2024-11-12T12:01:07.625000000Z",
            "active_until": null,
            "created_by_actor": {
              "type": "workspace-member",
              "id": "bbe415be-7a1d-45c7-9a8b-2af7b3cc962a"
            },
            "status": {
              "id": {
                "workspace_id": "515117c4-5fd1-4bfd-bc63-58f639d3f357",
                "object_id": "030f5287-761d-42ef-9feb-7d2e9a1ba52b",
                "attribute_id": "1a04f7e7-9392-40cb-9071-b1024f2eec73",
                "status_id": "10e0b809-893f-438a-a6a4-d69153c38ddc"
              },
              "title": "Prospecting",
              "is_archived": false,
              "target_time_in_status": null,
              "celebration_enabled": false
            },
            "attribute_type": "status"
          }
        ],
        "entry_id": [
          {
            "active_from": "2024-11-12T12:01:07.625000000Z",
            "active_until": null,
            "created_by_actor": {
              "type": "workspace-member",
              "id": "bbe415be-7a1d-45c7-9a8b-2af7b3cc962a"
            },
            "value": "a063b5d3-6a29-416b-9002-a309df7daabc",
            "attribute_type": "text"
          }
        ],
        "main_point_of_contact": [],
        "owner": [
          {
            "active_from": "2024-11-12T12:01:07.625000000Z",
            "active_until": null,
            "created_by_actor": {
              "type": "workspace-member",
              "id": "bbe415be-7a1d-45c7-9a8b-2af7b3cc962a"
            },
            "referenced_actor_type": "workspace-member",
            "referenced_actor_id": "bbe415be-7a1d-45c7-9a8b-2af7b3cc962a",
            "attribute_type": "actor-reference"
          }
        ],
        "priority": [],
        "estimated_contract_value": [],
        "projected_close_date": [
          {
            "active_from": "2024-11-12T12:01:07.625000000Z",
            "active_until": null,
            "created_by_actor": {
              "type": "workspace-member",
              "id": "bbe415be-7a1d-45c7-9a8b-2af7b3cc962a"
            },
            "value": "2024-11-26",
            "attribute_type": "date"
          }
        ],
        "close_confidence": [],
        "close_lost_reason": [],
        "notes": [],
        "created_at": [
          {
            "active_from": "2024-11-12T12:01:07.625000000Z",
            "active_until": null,
            "created_by_actor": {
              "type": "workspace-member",
              "id": "bbe415be-7a1d-45c7-9a8b-2af7b3cc962a"
            },
            "value": "2024-11-12T12:01:07.657000000Z",
            "attribute_type": "timestamp"
          }
        ],
        "created_by": [
          {
            "active_from": "2024-11-12T12:01:07.625000000Z",
            "active_until": null,
            "created_by_actor": {
              "type": "workspace-member",
              "id": "bbe415be-7a1d-45c7-9a8b-2af7b3cc962a"
            },
            "referenced_actor_type": "workspace-member",
            "referenced_actor_id": "bbe415be-7a1d-45c7-9a8b-2af7b3cc962a",
            "attribute_type": "actor-reference"
          }
        ],
        "deal_name": [],
        "company": []
      }
    },
    {
      "id": {
        "workspace_id": "515117c4-5fd1-4bfd-bc63-58f639d3f357",
        "list_id": "030f5287-761d-42ef-9feb-7d2e9a1ba52b",
        "entry_id": "a1243871-4aa1-4a4b-aaf2-76b2d9975a2e"
      },
      "parent_record_id": "c2b121a7-69d8-4907-bf21-ea708cc5471c",
      "parent_object": "companies",
      "created_at": "2024-11-12T12:01:09.879000000Z",
      "entry_values": {
        "stage": [
          {
            "active_from": "2024-11-12T12:01:09.879000000Z",
            "active_until": null,
            "created_by_actor": {
              "type": "workspace-member",
              "id": "bbe415be-7a1d-45c7-9a8b-2af7b3cc962a"
            },
            "status": {
              "id": {
                "workspace_id": "515117c4-5fd1-4bfd-bc63-58f639d3f357",
                "object_id": "030f5287-761d-42ef-9feb-7d2e9a1ba52b",
                "attribute_id": "1a04f7e7-9392-40cb-9071-b1024f2eec73",
                "status_id": "10e0b809-893f-438a-a6a4-d69153c38ddc"
              },
              "title": "Prospecting",
              "is_archived": false,
              "target_time_in_status": null,
              "celebration_enabled": false
            },
            "attribute_type": "status"
          }
        ],
        "entry_id": [
          {
            "active_from": "2024-11-12T12:01:09.879000000Z",
            "active_until": null,
            "created_by_actor": {
              "type": "workspace-member",
              "id": "bbe415be-7a1d-45c7-9a8b-2af7b3cc962a"
            },
            "value": "a1243871-4aa1-4a4b-aaf2-76b2d9975a2e",
            "attribute_type": "text"
          }
        ],
        "main_point_of_contact": [],
        "owner": [
          {
            "active_from": "2024-11-12T12:01:09.879000000Z",
            "active_until": null,
            "created_by_actor": {
              "type": "workspace-member",
              "id": "bbe415be-7a1d-45c7-9a8b-2af7b3cc962a"
            },
            "referenced_actor_type": "workspace-member",
            "referenced_actor_id": "bbe415be-7a1d-45c7-9a8b-2af7b3cc962a",
            "attribute_type": "actor-reference"
          }
        ],
        "priority": [],
        "estimated_contract_value": [],
        "projected_close_date": [
          {
            "active_from": "2024-11-12T12:01:09.879000000Z",
            "active_until": null,
            "created_by_actor": {
              "type": "workspace-member",
              "id": "bbe415be-7a1d-45c7-9a8b-2af7b3cc962a"
            },
            "value": "2024-11-26",
            "attribute_type": "date"
          }
        ],
        "close_confidence": [],
        "close_lost_reason": [],
        "notes": [],
        "created_at": [
          {
            "active_from": "2024-11-12T12:01:09.879000000Z",
            "active_until": null,
            "created_by_actor": {
              "type": "workspace-member",
              "id": "bbe415be-7a1d-45c7-9a8b-2af7b3cc962a"
            },
            "value": "2024-11-12T12:01:09.926000000Z",
            "attribute_type": "timestamp"
          }
        ],
        "created_by": [
          {
            "active_from": "2024-11-12T12:01:09.879000000Z",
            "active_until": null,
            "created_by_actor": {
              "type": "workspace-member",
              "id": "bbe415be-7a1d-45c7-9a8b-2af7b3cc962a"
            },
            "referenced_actor_type": "workspace-member",
            "referenced_actor_id": "bbe415be-7a1d-45c7-9a8b-2af7b3cc962a",
            "attribute_type": "actor-reference"
          }
        ],
        "deal_name": [],
        "company": []
      }
    },
    {
      "id": {
        "workspace_id": "515117c4-5fd1-4bfd-bc63-58f639d3f357",
        "list_id": "030f5287-761d-42ef-9feb-7d2e9a1ba52b",
        "entry_id": "a2989e32-c029-44f3-9f8d-9a3a1f0d4ece"
      },
      "parent_record_id": "afdca9fb-5c64-4f8d-8b6f-38e93a9ad798",
      "parent_object": "companies",
      "created_at": "2024-11-12T12:01:09.308000000Z",
      "entry_values": {
        "stage": [
          {
            "active_from": "2024-11-12T12:01:09.308000000Z",
            "active_until": null,
            "created_by_actor": {
              "type": "workspace-member",
              "id": "bbe415be-7a1d-45c7-9a8b-2af7b3cc962a"
            },
            "status": {
              "id": {
                "workspace_id": "515117c4-5fd1-4bfd-bc63-58f639d3f357",
                "object_id": "030f5287-761d-42ef-9feb-7d2e9a1ba52b",
                "attribute_id": "1a04f7e7-9392-40cb-9071-b1024f2eec73",
                "status_id": "10e0b809-893f-438a-a6a4-d69153c38ddc"
              },
              "title": "Prospecting",
              "is_archived": false,
              "target_time_in_status": null,
              "celebration_enabled": false
            },
            "attribute_type": "status"
          }
        ],
        "entry_id": [
          {
            "active_from": "2024-11-12T12:01:09.308000000Z",
            "active_until": null,
            "created_by_actor": {
              "type": "workspace-member",
              "id": "bbe415be-7a1d-45c7-9a8b-2af7b3cc962a"
            },
            "value": "a2989e32-c029-44f3-9f8d-9a3a1f0d4ece",
            "attribute_type": "text"
          }
        ],
        "main_point_of_contact": [],
        "owner": [
          {
            "active_from": "2024-11-12T12:01:09.308000000Z",
            "active_until": null,
            "created_by_actor": {
              "type": "workspace-member",
              "id": "bbe415be-7a1d-45c7-9a8b-2af7b3cc962a"
            },
            "referenced_actor_type": "workspace-member",
            "referenced_actor_id": "bbe415be-7a1d-45c7-9a8b-2af7b3cc962a",
            "attribute_type": "actor-reference"
          }
        ],
        "priority": [],
        "estimated_contract_value": [],
        "projected_close_date": [
          {
            "active_from": "2024-11-12T12:01:09.308000000Z",
            "active_until": null,
            "created_by_actor": {
              "type": "workspace-member",
              "id": "bbe415be-7a1d-45c7-9a8b-2af7b3cc962a"
            },
            "value": "2024-11-26",
            "attribute_type": "date"
          }
        ],
        "close_confidence": [],
        "close_lost_reason": [],
        "notes": [],
        "created_at": [
          {
            "active_from": "2024-11-12T12:01:09.308000000Z",
            "active_until": null,
            "created_by_actor": {
              "type": "workspace-member",
              "id": "bbe415be-7a1d-45c7-9a8b-2af7b3cc962a"
            },
            "value": "2024-11-12T12:01:09.338000000Z",
            "attribute_type": "timestamp"
          }
        ],
        "created_by": [
          {
            "active_from": "2024-11-12T12:01:09.308000000Z",
            "active_until": null,
            "created_by_actor": {
              "type": "workspace-member",
              "id": "bbe415be-7a1d-45c7-9a8b-2af7b3cc962a"
            },
            "referenced_actor_type": "workspace-member",
            "referenced_actor_id": "bbe415be-7a1d-45c7-9a8b-2af7b3cc962a",
            "attribute_type": "actor-reference"
          }
        ],
        "deal_name": [],
        "company": []
      }
    },
    {
      "id": {
        "workspace_id": "515117c4-5fd1-4bfd-bc63-58f639d3f357",
        "list_id": "030f5287-761d-42ef-9feb-7d2e9a1ba52b",
        "entry_id": "aa2764ad-72a8-45a9-98d5-6459d1d36631"
      },
      "parent_record_id": "367b9f29-a7b0-4d94-9eb5-5bc9303811b6",
      "parent_object": "companies",
      "created_at": "2024-11-12T12:01:06.663000000Z",
      "entry_values": {
        "stage": [
          {
            "active_from": "2024-11-12T12:01:06.663000000Z",
            "active_until": null,
            "created_by_actor": {
              "type": "workspace-member",
              "id": "bbe415be-7a1d-45c7-9a8b-2af7b3cc962a"
            },
            "status": {
              "id": {
                "workspace_id": "515117c4-5fd1-4bfd-bc63-58f639d3f357",
                "object_id": "030f5287-761d-42ef-9feb-7d2e9a1ba52b",
                "attribute_id": "1a04f7e7-9392-40cb-9071-b1024f2eec73",
                "status_id": "10e0b809-893f-438a-a6a4-d69153c38ddc"
              },
              "title": "Prospecting",
              "is_archived": false,
              "target_time_in_status": null,
              "celebration_enabled": false
            },
            "attribute_type": "status"
          }
        ],
        "entry_id": [
          {
            "active_from": "2024-11-12T12:01:06.663000000Z",
            "active_until": null,
            "created_by_actor": {
              "type": "workspace-member",
              "id": "bbe415be-7a1d-45c7-9a8b-2af7b3cc962a"
            },
            "value": "aa2764ad-72a8-45a9-98d5-6459d1d36631",
            "attribute_type": "text"
          }
        ],
        "main_point_of_contact": [],
        "owner": [
          {
            "active_from": "2024-11-12T12:01:06.663000000Z",
            "active_until": null,
            "created_by_actor": {
              "type": "workspace-member",
              "id": "bbe415be-7a1d-45c7-9a8b-2af7b3cc962a"
            },
            "referenced_actor_type": "workspace-member",
            "referenced_actor_id": "bbe415be-7a1d-45c7-9a8b-2af7b3cc962a",
            "attribute_type": "actor-reference"
          }
        ],
        "priority": [],
        "estimated_contract_value": [],
        "projected_close_date": [
          {
            "active_from": "2024-11-12T12:01:06.663000000Z",
            "active_until": null,
            "created_by_actor": {
              "type": "workspace-member",
              "id": "bbe415be-7a1d-45c7-9a8b-2af7b3cc962a"
            },
            "value": "2024-11-26",
            "attribute_type": "date"
          }
        ],
        "close_confidence": [],
        "close_lost_reason": [],
        "notes": [],
        "created_at": [
          {
            "active_from": "2024-11-12T12:01:06.663000000Z",
            "active_until": null,
            "created_by_actor": {
              "type": "workspace-member",
              "id": "bbe415be-7a1d-45c7-9a8b-2af7b3cc962a"
            },
            "value": "2024-11-12T12:01:06.697000000Z",
            "attribute_type": "timestamp"
          }
        ],
        "created_by": [
          {
            "active_from": "2024-11-12T12:01:06.663000000Z",
            "active_until": null,
            "created_by_actor": {
              "type": "workspace-member",
              "id": "bbe415be-7a1d-45c7-9a8b-2af7b3cc962a"
            },
            "referenced_actor_type": "workspace-member",
            "referenced_actor_id": "bbe415be-7a1d-45c7-9a8b-2af7b3cc962a",
            "attribute_type": "actor-reference"
          }
        ],
        "deal_name": [],
        "company": []
      }
    },
    {
      "id": {
        "workspace_id": "515117c4-5fd1-4bfd-bc63-58f639d3f357",
        "list_id": "030f5287-761d-42ef-9feb-7d2e9a1ba52b",
        "entry_id": "aca81893-947e-4365-b2a1-e93f319a9063"
      },
      "parent_record_id": "1fff5ade-d81f-40f4-b342-bdd2d2ccf778",
      "parent_object": "companies",
      "created_at": "2024-11-12T12:01:06.042000000Z",
      "entry_values": {
        "stage": [
          {
            "active_from": "2024-11-12T12:01:06.042000000Z",
            "active_until": null,
            "created_by_actor": {
              "type": "workspace-member",
              "id": "bbe415be-7a1d-45c7-9a8b-2af7b3cc962a"
            },
            "status": {
              "id": {
                "workspace_id": "515117c4-5fd1-4bfd-bc63-58f639d3f357",
                "object_id": "030f5287-761d-42ef-9feb-7d2e9a1ba52b",
                "attribute_id": "1a04f7e7-9392-40cb-9071-b1024f2eec73",
                "status_id": "10e0b809-893f-438a-a6a4-d69153c38ddc"
              },
              "title": "Prospecting",
              "is_archived": false,
              "target_time_in_status": null,
              "celebration_enabled": false
            },
            "attribute_type": "status"
          }
        ],
        "entry_id": [
          {
            "active_from": "2024-11-12T12:01:06.042000000Z",
            "active_until": null,
            "created_by_actor": {
              "type": "workspace-member",
              "id": "bbe415be-7a1d-45c7-9a8b-2af7b3cc962a"
            },
            "value": "aca81893-947e-4365-b2a1-e93f319a9063",
            "attribute_type": "text"
          }
        ],
        "main_point_of_contact": [],
        "owner": [
          {
            "active_from": "2024-11-12T12:01:06.042000000Z",
            "active_until": null,
            "created_by_actor": {
              "type": "workspace-member",
              "id": "bbe415be-7a1d-45c7-9a8b-2af7b3cc962a"
            },
            "referenced_actor_type": "workspace-member",
            "referenced_actor_id": "bbe415be-7a1d-45c7-9a8b-2af7b3cc962a",
            "attribute_type": "actor-reference"
          }
        ],
        "priority": [],
        "estimated_contract_value": [],
        "projected_close_date": [
          {
            "active_from": "2024-11-12T12:01:06.042000000Z",
            "active_until": null,
            "created_by_actor": {
              "type": "workspace-member",
              "id": "bbe415be-7a1d-45c7-9a8b-2af7b3cc962a"
            },
            "value": "2024-11-26",
            "attribute_type": "date"
          }
        ],
        "close_confidence": [],
        "close_lost_reason": [],
        "notes": [],
        "created_at": [
          {
            "active_from": "2024-11-12T12:01:06.042000000Z",
            "active_until": null,
            "created_by_actor": {
              "type": "workspace-member",
              "id": "bbe415be-7a1d-45c7-9a8b-2af7b3cc962a"
            },
            "value": "2024-11-12T12:01:06.069000000Z",
            "attribute_type": "timestamp"
          }
        ],
        "created_by": [
          {
            "active_from": "2024-11-12T12:01:06.042000000Z",
            "active_until": null,
            "created_by_actor": {
              "type": "workspace-member",
              "id": "bbe415be-7a1d-45c7-9a8b-2af7b3cc962a"
            },
            "referenced_actor_type": "workspace-member",
            "referenced_actor_id": "bbe415be-7a1d-45c7-9a8b-2af7b3cc962a",
            "attribute_type": "actor-reference"
          }
        ],
        "deal_name": [],
        "company": []
      }
    },
    {
      "id": {
        "workspace_id": "515117c4-5fd1-4bfd-bc63-58f639d3f357",
        "list_id": "030f5287-761d-42ef-9feb-7d2e9a1ba52b",
        "entry_id": "b0bfc991-5983-42bc-9e70-43f9134b188b"
      },
      "parent_record_id": "8e4fea40-30f3-455e-a883-971cb43a192e",
      "parent_object": "companies",
      "created_at": "2024-11-12T12:01:08.354000000Z",
      "entry_values": {
        "stage": [
          {
            "active_from": "2024-11-12T12:01:08.354000000Z",
            "active_until": null,
            "created_by_actor": {
              "type": "workspace-member",
              "id": "bbe415be-7a1d-45c7-9a8b-2af7b3cc962a"
            },
            "status": {
              "id": {
                "workspace_id": "515117c4-5fd1-4bfd-bc63-58f639d3f357",
                "object_id": "030f5287-761d-42ef-9feb-7d2e9a1ba52b",
                "attribute_id": "1a04f7e7-9392-40cb-9071-b1024f2eec73",
                "status_id": "10e0b809-893f-438a-a6a4-d69153c38ddc"
              },
              "title": "Prospecting",
              "is_archived": false,
              "target_time_in_status": null,
              "celebration_enabled": false
            },
            "attribute_type": "status"
          }
        ],
        "entry_id": [
          {
            "active_from": "2024-11-12T12:01:08.354000000Z",
            "active_until": null,
            "created_by_actor": {
              "type": "workspace-member",
              "id": "bbe415be-7a1d-45c7-9a8b-2af7b3cc962a"
            },
            "value": "b0bfc991-5983-42bc-9e70-43f9134b188b",
            "attribute_type": "text"
          }
        ],
        "main_point_of_contact": [],
        "owner": [
          {
            "active_from": "2024-11-12T12:01:08.354000000Z",
            "active_until": null,
            "created_by_actor": {
              "type": "workspace-member",
              "id": "bbe415be-7a1d-45c7-9a8b-2af7b3cc962a"
            },
            "referenced_actor_type": "workspace-member",
            "referenced_actor_id": "bbe415be-7a1d-45c7-9a8b-2af7b3cc962a",
            "attribute_type": "actor-reference"
          }
        ],
        "priority": [],
        "estimated_contract_value": [],
        "projected_close_date": [
          {
            "active_from": "2024-11-12T12:01:08.354000000Z",
            "active_until": null,
            "created_by_actor": {
              "type": "workspace-member",
              "id": "bbe415be-7a1d-45c7-9a8b-2af7b3cc962a"
            },
            "value": "2024-11-26",
            "attribute_type": "date"
          }
        ],
        "close_confidence": [],
        "close_lost_reason": [],
        "notes": [],
        "created_at": [
          {
            "active_from": "2024-11-12T12:01:08.354000000Z",
            "active_until": null,
            "created_by_actor": {
              "type": "workspace-member",
              "id": "bbe415be-7a1d-45c7-9a8b-2af7b3cc962a"
            },
            "value": "2024-11-12T12:01:08.381000000Z",
            "attribute_type": "timestamp"
          }
        ],
        "created_by": [
          {
            "active_from": "2024-11-12T12:01:08.354000000Z",
            "active_until": null,
            "created_by_actor": {
              "type": "workspace-member",
              "id": "bbe415be-7a1d-45c7-9a8b-2af7b3cc962a"
            },
            "referenced_actor_type": "workspace-member",
            "referenced_actor_id": "bbe415be-7a1d-45c7-9a8b-2af7b3cc962a",
            "attribute_type": "actor-reference"
          }
        ],
        "deal_name": [],
        "company": []
      }
    },
    {
      "id": {
        "workspace_id": "515117c4-5fd1-4bfd-bc63-58f639d3f357",
        "list_id": "030f5287-761d-42ef-9feb-7d2e9a1ba52b",
        "entry_id": "b0e10036-051b-47b1-a960-8d8e617ace3e"
      },
      "parent_record_id": "347f936a-9643-4907-bb3b-f746ca4c4c38",
      "parent_object": "companies",
      "created_at": "2024-11-12T12:01:06.568000000Z",
      "entry_values": {
        "stage": [
          {
            "active_from": "2024-11-12T12:01:06.568000000Z",
            "active_until": null,
            "created_by_actor": {
              "type": "workspace-member",
              "id": "bbe415be-7a1d-45c7-9a8b-2af7b3cc962a"
            },
            "status": {
              "id": {
                "workspace_id": "515117c4-5fd1-4bfd-bc63-58f639d3f357",
                "object_id": "030f5287-761d-42ef-9feb-7d2e9a1ba52b",
                "attribute_id": "1a04f7e7-9392-40cb-9071-b1024f2eec73",
                "status_id": "10e0b809-893f-438a-a6a4-d69153c38ddc"
              },
              "title": "Prospecting",
              "is_archived": false,
              "target_time_in_status": null,
              "celebration_enabled": false
            },
            "attribute_type": "status"
          }
        ],
        "entry_id": [
          {
            "active_from": "2024-11-12T12:01:06.568000000Z",
            "active_until": null,
            "created_by_actor": {
              "type": "workspace-member",
              "id": "bbe415be-7a1d-45c7-9a8b-2af7b3cc962a"
            },
            "value": "b0e10036-051b-47b1-a960-8d8e617ace3e",
            "attribute_type": "text"
          }
        ],
        "main_point_of_contact": [],
        "owner": [
          {
            "active_from": "2024-11-12T12:01:06.568000000Z",
            "active_until": null,
            "created_by_actor": {
              "type": "workspace-member",
              "id": "bbe415be-7a1d-45c7-9a8b-2af7b3cc962a"
            },
            "referenced_actor_type": "workspace-member",
            "referenced_actor_id": "bbe415be-7a1d-45c7-9a8b-2af7b3cc962a",
            "attribute_type": "actor-reference"
          }
        ],
        "priority": [],
        "estimated_contract_value": [],
        "projected_close_date": [
          {
            "active_from": "2024-11-12T12:01:06.568000000Z",
            "active_until": null,
            "created_by_actor": {
              "type": "workspace-member",
              "id": "bbe415be-7a1d-45c7-9a8b-2af7b3cc962a"
            },
            "value": "2024-11-26",
            "attribute_type": "date"
          }
        ],
        "close_confidence": [],
        "close_lost_reason": [],
        "notes": [],
        "created_at": [
          {
            "active_from": "2024-11-12T12:01:06.568000000Z",
            "active_until": null,
            "created_by_actor": {
              "type": "workspace-member",
              "id": "bbe415be-7a1d-45c7-9a8b-2af7b3cc962a"
            },
            "value": "2024-11-12T12:01:06.600000000Z",
            "attribute_type": "timestamp"
          }
        ],
        "created_by": [
          {
            "active_from": "2024-11-12T12:01:06.568000000Z",
            "active_until": null,
            "created_by_actor": {
              "type": "workspace-member",
              "id": "bbe415be-7a1d-45c7-9a8b-2af7b3cc962a"
            },
            "referenced_actor_type": "workspace-member",
            "referenced_actor_id": "bbe415be-7a1d-45c7-9a8b-2af7b3cc962a",
            "attribute_type": "actor-reference"
          }
        ],
        "deal_name": [],
        "company": []
      }
    },
    {
      "id": {
        "workspace_id": "515117c4-5fd1-4bfd-bc63-58f639d3f357",
        "list_id": "030f5287-761d-42ef-9feb-7d2e9a1ba52b",
        "entry_id": "b14a691f-809c-4f54-aa3d-b266013ae2bd"
      },
      "parent_record_id": "4b9a408f-0eea-4bfd-a5e3-bda5387f6459",
      "parent_object": "companies",
      "created_at": "2024-11-12T12:01:07.198000000Z",
      "entry_values": {
        "stage": [
          {
            "active_from": "2024-11-12T12:01:07.198000000Z",
            "active_until": null,
            "created_by_actor": {
              "type": "workspace-member",
              "id": "bbe415be-7a1d-45c7-9a8b-2af7b3cc962a"
            },
            "status": {
              "id": {
                "workspace_id": "515117c4-5fd1-4bfd-bc63-58f639d3f357",
                "object_id": "030f5287-761d-42ef-9feb-7d2e9a1ba52b",
                "attribute_id": "1a04f7e7-9392-40cb-9071-b1024f2eec73",
                "status_id": "10e0b809-893f-438a-a6a4-d69153c38ddc"
              },
              "title": "Prospecting",
              "is_archived": false,
              "target_time_in_status": null,
              "celebration_enabled": false
            },
            "attribute_type": "status"
          }
        ],
        "entry_id": [
          {
            "active_from": "2024-11-12T12:01:07.198000000Z",
            "active_until": null,
            "created_by_actor": {
              "type": "workspace-member",
              "id": "bbe415be-7a1d-45c7-9a8b-2af7b3cc962a"
            },
            "value": "b14a691f-809c-4f54-aa3d-b266013ae2bd",
            "attribute_type": "text"
          }
        ],
        "main_point_of_contact": [],
        "owner": [
          {
            "active_from": "2024-11-12T12:01:07.198000000Z",
            "active_until": null,
            "created_by_actor": {
              "type": "workspace-member",
              "id": "bbe415be-7a1d-45c7-9a8b-2af7b3cc962a"
            },
            "referenced_actor_type": "workspace-member",
            "referenced_actor_id": "bbe415be-7a1d-45c7-9a8b-2af7b3cc962a",
            "attribute_type": "actor-reference"
          }
        ],
        "priority": [],
        "estimated_contract_value": [],
        "projected_close_date": [
          {
            "active_from": "2024-11-12T12:01:07.198000000Z",
            "active_until": null,
            "created_by_actor": {
              "type": "workspace-member",
              "id": "bbe415be-7a1d-45c7-9a8b-2af7b3cc962a"
            },
            "value": "2024-11-26",
            "attribute_type": "date"
          }
        ],
        "close_confidence": [],
        "close_lost_reason": [],
        "notes": [],
        "created_at": [
          {
            "active_from": "2024-11-12T12:01:07.198000000Z",
            "active_until": null,
            "created_by_actor": {
              "type": "workspace-member",
              "id": "bbe415be-7a1d-45c7-9a8b-2af7b3cc962a"
            },
            "value": "2024-11-12T12:01:07.231000000Z",
            "attribute_type": "timestamp"
          }
        ],
        "created_by": [
          {
            "active_from": "2024-11-12T12:01:07.198000000Z",
            "active_until": null,
            "created_by_actor": {
              "type": "workspace-member",
              "id": "bbe415be-7a1d-45c7-9a8b-2af7b3cc962a"
            },
            "referenced_actor_type": "workspace-member",
            "referenced_actor_id": "bbe415be-7a1d-45c7-9a8b-2af7b3cc962a",
            "attribute_type": "actor-reference"
          }
        ],
        "deal_name": [],
        "company": []
      }
    },
    {
      "id": {
        "workspace_id": "515117c4-5fd1-4bfd-bc63-58f639d3f357",
        "list_id": "030f5287-761d-42ef-9feb-7d2e9a1ba52b",
        "entry_id": "bd0ad301-d9bf-4214-b429-480cf17bc0d1"
      },
      "parent_record_id": "88debc82-5a92-4731-ba22-0ff9d6cf7e77",
      "parent_object": "companies",
      "created_at": "2024-11-12T12:01:07.837000000Z",
      "entry_values": {
        "stage": [
          {
            "active_from": "2024-11-12T12:01:07.837000000Z",
            "active_until": null,
            "created_by_actor": {
              "type": "workspace-member",
              "id": "bbe415be-7a1d-45c7-9a8b-2af7b3cc962a"
            },
            "status": {
              "id": {
                "workspace_id": "515117c4-5fd1-4bfd-bc63-58f639d3f357",
                "object_id": "030f5287-761d-42ef-9feb-7d2e9a1ba52b",
                "attribute_id": "1a04f7e7-9392-40cb-9071-b1024f2eec73",
                "status_id": "10e0b809-893f-438a-a6a4-d69153c38ddc"
              },
              "title": "Prospecting",
              "is_archived": false,
              "target_time_in_status": null,
              "celebration_enabled": false
            },
            "attribute_type": "status"
          }
        ],
        "entry_id": [
          {
            "active_from": "2024-11-12T12:01:07.837000000Z",
            "active_until": null,
            "created_by_actor": {
              "type": "workspace-member",
              "id": "bbe415be-7a1d-45c7-9a8b-2af7b3cc962a"
            },
            "value": "bd0ad301-d9bf-4214-b429-480cf17bc0d1",
            "attribute_type": "text"
          }
        ],
        "main_point_of_contact": [],
        "owner": [
          {
            "active_from": "2024-11-12T12:01:07.837000000Z",
            "active_until": null,
            "created_by_actor": {
              "type": "workspace-member",
              "id": "bbe415be-7a1d-45c7-9a8b-2af7b3cc962a"
            },
            "referenced_actor_type": "workspace-member",
            "referenced_actor_id": "bbe415be-7a1d-45c7-9a8b-2af7b3cc962a",
            "attribute_type": "actor-reference"
          }
        ],
        "priority": [],
        "estimated_contract_value": [],
        "projected_close_date": [
          {
            "active_from": "2024-11-12T12:01:07.837000000Z",
            "active_until": null,
            "created_by_actor": {
              "type": "workspace-member",
              "id": "bbe415be-7a1d-45c7-9a8b-2af7b3cc962a"
            },
            "value": "2024-11-26",
            "attribute_type": "date"
          }
        ],
        "close_confidence": [],
        "close_lost_reason": [],
        "notes": [],
        "created_at": [
          {
            "active_from": "2024-11-12T12:01:07.837000000Z",
            "active_until": null,
            "created_by_actor": {
              "type": "workspace-member",
              "id": "bbe415be-7a1d-45c7-9a8b-2af7b3cc962a"
            },
            "value": "2024-11-12T12:01:07.874000000Z",
            "attribute_type": "timestamp"
          }
        ],
        "created_by": [
          {
            "active_from": "2024-11-12T12:01:07.837000000Z",
            "active_until": null,
            "created_by_actor": {
              "type": "workspace-member",
              "id": "bbe415be-7a1d-45c7-9a8b-2af7b3cc962a"
            },
            "referenced_actor_type": "workspace-member",
            "referenced_actor_id": "bbe415be-7a1d-45c7-9a8b-2af7b3cc962a",
            "attribute_type": "actor-reference"
          }
        ],
        "deal_name": [],
        "company": []
      }
    },
    {
      "id": {
        "workspace_id": "515117c4-5fd1-4bfd-bc63-58f639d3f357",
        "list_id": "030f5287-761d-42ef-9feb-7d2e9a1ba52b",
        "entry_id": "bf3f4974-2197-49c8-8c94-a519bf41aaf6"
      },
      "parent_record_id": "43310639-9828-460b-951d-c89fb7479fe0",
      "parent_object": "companies",
      "created_at": "2024-11-12T12:01:06.785000000Z",
      "entry_values": {
        "stage": [
          {
            "active_from": "2024-11-12T12:01:06.785000000Z",
            "active_until": null,
            "created_by_actor": {
              "type": "workspace-member",
              "id": "bbe415be-7a1d-45c7-9a8b-2af7b3cc962a"
            },
            "status": {
              "id": {
                "workspace_id": "515117c4-5fd1-4bfd-bc63-58f639d3f357",
                "object_id": "030f5287-761d-42ef-9feb-7d2e9a1ba52b",
                "attribute_id": "1a04f7e7-9392-40cb-9071-b1024f2eec73",
                "status_id": "10e0b809-893f-438a-a6a4-d69153c38ddc"
              },
              "title": "Prospecting",
              "is_archived": false,
              "target_time_in_status": null,
              "celebration_enabled": false
            },
            "attribute_type": "status"
          }
        ],
        "entry_id": [
          {
            "active_from": "2024-11-12T12:01:06.785000000Z",
            "active_until": null,
            "created_by_actor": {
              "type": "workspace-member",
              "id": "bbe415be-7a1d-45c7-9a8b-2af7b3cc962a"
            },
            "value": "bf3f4974-2197-49c8-8c94-a519bf41aaf6",
            "attribute_type": "text"
          }
        ],
        "main_point_of_contact": [],
        "owner": [
          {
            "active_from": "2024-11-12T12:01:06.785000000Z",
            "active_until": null,
            "created_by_actor": {
              "type": "workspace-member",
              "id": "bbe415be-7a1d-45c7-9a8b-2af7b3cc962a"
            },
            "referenced_actor_type": "workspace-member",
            "referenced_actor_id": "bbe415be-7a1d-45c7-9a8b-2af7b3cc962a",
            "attribute_type": "actor-reference"
          }
        ],
        "priority": [],
        "estimated_contract_value": [],
        "projected_close_date": [
          {
            "active_from": "2024-11-12T12:01:06.785000000Z",
            "active_until": null,
            "created_by_actor": {
              "type": "workspace-member",
              "id": "bbe415be-7a1d-45c7-9a8b-2af7b3cc962a"
            },
            "value": "2024-11-26",
            "attribute_type": "date"
          }
        ],
        "close_confidence": [],
        "close_lost_reason": [],
        "notes": [],
        "created_at": [
          {
            "active_from": "2024-11-12T12:01:06.785000000Z",
            "active_until": null,
            "created_by_actor": {
              "type": "workspace-member",
              "id": "bbe415be-7a1d-45c7-9a8b-2af7b3cc962a"
            },
            "value": "2024-11-12T12:01:06.810000000Z",
            "attribute_type": "timestamp"
          }
        ],
        "created_by": [
          {
            "active_from": "2024-11-12T12:01:06.785000000Z",
            "active_until": null,
            "created_by_actor": {
              "type": "workspace-member",
              "id": "bbe415be-7a1d-45c7-9a8b-2af7b3cc962a"
            },
            "referenced_actor_type": "workspace-member",
            "referenced_actor_id": "bbe415be-7a1d-45c7-9a8b-2af7b3cc962a",
            "attribute_type": "actor-reference"
          }
        ],
        "deal_name": [],
        "company": []
      }
    },
    {
      "id": {
        "workspace_id": "515117c4-5fd1-4bfd-bc63-58f639d3f357",
        "list_id": "030f5287-761d-42ef-9feb-7d2e9a1ba52b",
        "entry_id": "c2b89f15-8249-47bc-97cc-54cb9eb004af"
      },
      "parent_record_id": "d44690d9-b5f5-4abc-8bde-e979b71c88d6",
      "parent_object": "companies",
      "created_at": "2024-11-12T12:01:10.268000000Z",
      "entry_values": {
        "stage": [
          {
            "active_from": "2024-11-12T12:01:10.268000000Z",
            "active_until": null,
            "created_by_actor": {
              "type": "workspace-member",
              "id": "bbe415be-7a1d-45c7-9a8b-2af7b3cc962a"
            },
            "status": {
              "id": {
                "workspace_id": "515117c4-5fd1-4bfd-bc63-58f639d3f357",
                "object_id": "030f5287-761d-42ef-9feb-7d2e9a1ba52b",
                "attribute_id": "1a04f7e7-9392-40cb-9071-b1024f2eec73",
                "status_id": "10e0b809-893f-438a-a6a4-d69153c38ddc"
              },
              "title": "Prospecting",
              "is_archived": false,
              "target_time_in_status": null,
              "celebration_enabled": false
            },
            "attribute_type": "status"
          }
        ],
        "entry_id": [
          {
            "active_from": "2024-11-12T12:01:10.268000000Z",
            "active_until": null,
            "created_by_actor": {
              "type": "workspace-member",
              "id": "bbe415be-7a1d-45c7-9a8b-2af7b3cc962a"
            },
            "value": "c2b89f15-8249-47bc-97cc-54cb9eb004af",
            "attribute_type": "text"
          }
        ],
        "main_point_of_contact": [],
        "owner": [
          {
            "active_from": "2024-11-12T12:01:10.268000000Z",
            "active_until": null,
            "created_by_actor": {
              "type": "workspace-member",
              "id": "bbe415be-7a1d-45c7-9a8b-2af7b3cc962a"
            },
            "referenced_actor_type": "workspace-member",
            "referenced_actor_id": "bbe415be-7a1d-45c7-9a8b-2af7b3cc962a",
            "attribute_type": "actor-reference"
          }
        ],
        "priority": [],
        "estimated_contract_value": [],
        "projected_close_date": [
          {
            "active_from": "2024-11-12T12:01:10.268000000Z",
            "active_until": null,
            "created_by_actor": {
              "type": "workspace-member",
              "id": "bbe415be-7a1d-45c7-9a8b-2af7b3cc962a"
            },
            "value": "2024-11-26",
            "attribute_type": "date"
          }
        ],
        "close_confidence": [],
        "close_lost_reason": [],
        "notes": [],
        "created_at": [
          {
            "active_from": "2024-11-12T12:01:10.268000000Z",
            "active_until": null,
            "created_by_actor": {
              "type": "workspace-member",
              "id": "bbe415be-7a1d-45c7-9a8b-2af7b3cc962a"
            },
            "value": "2024-11-12T12:01:10.298000000Z",
            "attribute_type": "timestamp"
          }
        ],
        "created_by": [
          {
            "active_from": "2024-11-12T12:01:10.268000000Z",
            "active_until": null,
            "created_by_actor": {
              "type": "workspace-member",
              "id": "bbe415be-7a1d-45c7-9a8b-2af7b3cc962a"
            },
            "referenced_actor_type": "workspace-member",
            "referenced_actor_id": "bbe415be-7a1d-45c7-9a8b-2af7b3cc962a",
            "attribute_type": "actor-reference"
          }
        ],
        "deal_name": [],
        "company": []
      }
    },
    {
      "id": {
        "workspace_id": "515117c4-5fd1-4bfd-bc63-58f639d3f357",
        "list_id": "030f5287-761d-42ef-9feb-7d2e9a1ba52b",
        "entry_id": "c4e5e169-4416-4219-9f84-9e57ea25f9e0"
      },
      "parent_record_id": "308f80c8-59b2-46b0-9ea1-962543737b29",
      "parent_object": "companies",
      "created_at": "2024-11-12T12:01:06.043000000Z",
      "entry_values": {
        "stage": [
          {
            "active_from": "2024-11-12T12:01:06.043000000Z",
            "active_until": null,
            "created_by_actor": {
              "type": "workspace-member",
              "id": "bbe415be-7a1d-45c7-9a8b-2af7b3cc962a"
            },
            "status": {
              "id": {
                "workspace_id": "515117c4-5fd1-4bfd-bc63-58f639d3f357",
                "object_id": "030f5287-761d-42ef-9feb-7d2e9a1ba52b",
                "attribute_id": "1a04f7e7-9392-40cb-9071-b1024f2eec73",
                "status_id": "10e0b809-893f-438a-a6a4-d69153c38ddc"
              },
              "title": "Prospecting",
              "is_archived": false,
              "target_time_in_status": null,
              "celebration_enabled": false
            },
            "attribute_type": "status"
          }
        ],
        "entry_id": [
          {
            "active_from": "2024-11-12T12:01:06.043000000Z",
            "active_until": null,
            "created_by_actor": {
              "type": "workspace-member",
              "id": "bbe415be-7a1d-45c7-9a8b-2af7b3cc962a"
            },
            "value": "c4e5e169-4416-4219-9f84-9e57ea25f9e0",
            "attribute_type": "text"
          }
        ],
        "main_point_of_contact": [],
        "owner": [
          {
            "active_from": "2024-11-12T12:01:06.043000000Z",
            "active_until": null,
            "created_by_actor": {
              "type": "workspace-member",
              "id": "bbe415be-7a1d-45c7-9a8b-2af7b3cc962a"
            },
            "referenced_actor_type": "workspace-member",
            "referenced_actor_id": "bbe415be-7a1d-45c7-9a8b-2af7b3cc962a",
            "attribute_type": "actor-reference"
          }
        ],
        "priority": [],
        "estimated_contract_value": [],
        "projected_close_date": [
          {
            "active_from": "2024-11-12T12:01:06.043000000Z",
            "active_until": null,
            "created_by_actor": {
              "type": "workspace-member",
              "id": "bbe415be-7a1d-45c7-9a8b-2af7b3cc962a"
            },
            "value": "2024-11-26",
            "attribute_type": "date"
          }
        ],
        "close_confidence": [],
        "close_lost_reason": [],
        "notes": [],
        "created_at": [
          {
            "active_from": "2024-11-12T12:01:06.043000000Z",
            "active_until": null,
            "created_by_actor": {
              "type": "workspace-member",
              "id": "bbe415be-7a1d-45c7-9a8b-2af7b3cc962a"
            },
            "value": "2024-11-12T12:01:06.091000000Z",
            "attribute_type": "timestamp"
          }
        ],
        "created_by": [
          {
            "active_from": "2024-11-12T12:01:06.043000000Z",
            "active_until": null,
            "created_by_actor": {
              "type": "workspace-member",
              "id": "bbe415be-7a1d-45c7-9a8b-2af7b3cc962a"
            },
            "referenced_actor_type": "workspace-member",
            "referenced_actor_id": "bbe415be-7a1d-45c7-9a8b-2af7b3cc962a",
            "attribute_type": "actor-reference"
          }
        ],
        "deal_name": [],
        "company": []
      }
    },
    {
      "id": {
        "workspace_id": "515117c4-5fd1-4bfd-bc63-58f639d3f357",
        "list_id": "030f5287-761d-42ef-9feb-7d2e9a1ba52b",
        "entry_id": "ca2c62d1-cb36-4308-a545-0cd138dcb49d"
      },
      "parent_record_id": "04e26eb1-3c8b-4ca8-a54f-f2dd4c3e6b2d",
      "parent_object": "companies",
      "created_at": "2024-11-12T12:01:06.020000000Z",
      "entry_values": {
        "stage": [
          {
            "active_from": "2024-11-12T12:01:06.020000000Z",
            "active_until": null,
            "created_by_actor": {
              "type": "workspace-member",
              "id": "bbe415be-7a1d-45c7-9a8b-2af7b3cc962a"
            },
            "status": {
              "id": {
                "workspace_id": "515117c4-5fd1-4bfd-bc63-58f639d3f357",
                "object_id": "030f5287-761d-42ef-9feb-7d2e9a1ba52b",
                "attribute_id": "1a04f7e7-9392-40cb-9071-b1024f2eec73",
                "status_id": "10e0b809-893f-438a-a6a4-d69153c38ddc"
              },
              "title": "Prospecting",
              "is_archived": false,
              "target_time_in_status": null,
              "celebration_enabled": false
            },
            "attribute_type": "status"
          }
        ],
        "entry_id": [
          {
            "active_from": "2024-11-12T12:01:06.020000000Z",
            "active_until": null,
            "created_by_actor": {
              "type": "workspace-member",
              "id": "bbe415be-7a1d-45c7-9a8b-2af7b3cc962a"
            },
            "value": "ca2c62d1-cb36-4308-a545-0cd138dcb49d",
            "attribute_type": "text"
          }
        ],
        "main_point_of_contact": [],
        "owner": [
          {
            "active_from": "2024-11-12T12:01:06.020000000Z",
            "active_until": null,
            "created_by_actor": {
              "type": "workspace-member",
              "id": "bbe415be-7a1d-45c7-9a8b-2af7b3cc962a"
            },
            "referenced_actor_type": "workspace-member",
            "referenced_actor_id": "bbe415be-7a1d-45c7-9a8b-2af7b3cc962a",
            "attribute_type": "actor-reference"
          }
        ],
        "priority": [],
        "estimated_contract_value": [],
        "projected_close_date": [
          {
            "active_from": "2024-11-12T12:01:06.020000000Z",
            "active_until": null,
            "created_by_actor": {
              "type": "workspace-member",
              "id": "bbe415be-7a1d-45c7-9a8b-2af7b3cc962a"
            },
            "value": "2024-11-26",
            "attribute_type": "date"
          }
        ],
        "close_confidence": [],
        "close_lost_reason": [],
        "notes": [],
        "created_at": [
          {
            "active_from": "2024-11-12T12:01:06.020000000Z",
            "active_until": null,
            "created_by_actor": {
              "type": "workspace-member",
              "id": "bbe415be-7a1d-45c7-9a8b-2af7b3cc962a"
            },
            "value": "2024-11-12T12:01:06.049000000Z",
            "attribute_type": "timestamp"
          }
        ],
        "created_by": [
          {
            "active_from": "2024-11-12T12:01:06.020000000Z",
            "active_until": null,
            "created_by_actor": {
              "type": "workspace-member",
              "id": "bbe415be-7a1d-45c7-9a8b-2af7b3cc962a"
            },
            "referenced_actor_type": "workspace-member",
            "referenced_actor_id": "bbe415be-7a1d-45c7-9a8b-2af7b3cc962a",
            "attribute_type": "actor-reference"
          }
        ],
        "deal_name": [],
        "company": []
      }
    },
    {
      "id": {
        "workspace_id": "515117c4-5fd1-4bfd-bc63-58f639d3f357",
        "list_id": "030f5287-761d-42ef-9feb-7d2e9a1ba52b",
        "entry_id": "d23819b6-51c8-42df-a54e-da643bdc0275"
      },
      "parent_record_id": "47e839a3-03cb-4753-895a-2c5e4b7dfa87",
      "parent_object": "companies",
      "created_at": "2024-11-12T12:01:06.830000000Z",
      "entry_values": {
        "stage": [
          {
            "active_from": "2024-11-12T12:01:06.830000000Z",
            "active_until": null,
            "created_by_actor": {
              "type": "workspace-member",
              "id": "bbe415be-7a1d-45c7-9a8b-2af7b3cc962a"
            },
            "status": {
              "id": {
                "workspace_id": "515117c4-5fd1-4bfd-bc63-58f639d3f357",
                "object_id": "030f5287-761d-42ef-9feb-7d2e9a1ba52b",
                "attribute_id": "1a04f7e7-9392-40cb-9071-b1024f2eec73",
                "status_id": "10e0b809-893f-438a-a6a4-d69153c38ddc"
              },
              "title": "Prospecting",
              "is_archived": false,
              "target_time_in_status": null,
              "celebration_enabled": false
            },
            "attribute_type": "status"
          }
        ],
        "entry_id": [
          {
            "active_from": "2024-11-12T12:01:06.830000000Z",
            "active_until": null,
            "created_by_actor": {
              "type": "workspace-member",
              "id": "bbe415be-7a1d-45c7-9a8b-2af7b3cc962a"
            },
            "value": "d23819b6-51c8-42df-a54e-da643bdc0275",
            "attribute_type": "text"
          }
        ],
        "main_point_of_contact": [],
        "owner": [
          {
            "active_from": "2024-11-12T12:01:06.830000000Z",
            "active_until": null,
            "created_by_actor": {
              "type": "workspace-member",
              "id": "bbe415be-7a1d-45c7-9a8b-2af7b3cc962a"
            },
            "referenced_actor_type": "workspace-member",
            "referenced_actor_id": "bbe415be-7a1d-45c7-9a8b-2af7b3cc962a",
            "attribute_type": "actor-reference"
          }
        ],
        "priority": [],
        "estimated_contract_value": [],
        "projected_close_date": [
          {
            "active_from": "2024-11-12T12:01:06.830000000Z",
            "active_until": null,
            "created_by_actor": {
              "type": "workspace-member",
              "id": "bbe415be-7a1d-45c7-9a8b-2af7b3cc962a"
            },
            "value": "2024-11-26",
            "attribute_type": "date"
          }
        ],
        "close_confidence": [],
        "close_lost_reason": [],
        "notes": [],
        "created_at": [
          {
            "active_from": "2024-11-12T12:01:06.830000000Z",
            "active_until": null,
            "created_by_actor": {
              "type": "workspace-member",
              "id": "bbe415be-7a1d-45c7-9a8b-2af7b3cc962a"
            },
            "value": "2024-11-12T12:01:06.866000000Z",
            "attribute_type": "timestamp"
          }
        ],
        "created_by": [
          {
            "active_from": "2024-11-12T12:01:06.830000000Z",
            "active_until": null,
            "created_by_actor": {
              "type": "workspace-member",
              "id": "bbe415be-7a1d-45c7-9a8b-2af7b3cc962a"
            },
            "referenced_actor_type": "workspace-member",
            "referenced_actor_id": "bbe415be-7a1d-45c7-9a8b-2af7b3cc962a",
            "attribute_type": "actor-reference"
          }
        ],
        "deal_name": [],
        "company": []
      }
    },
    {
      "id": {
        "workspace_id": "515117c4-5fd1-4bfd-bc63-58f639d3f357",
        "list_id": "030f5287-761d-42ef-9feb-7d2e9a1ba52b",
        "entry_id": "d36aa78b-a0d6-4f76-8970-a02275859b9f"
      },
      "parent_record_id": "2803f63c-7f01-49d0-908c-6dff41fdf23a",
      "parent_object": "companies",
      "created_at": "2024-11-12T12:01:06.044000000Z",
      "entry_values": {
        "stage": [
          {
            "active_from": "2024-11-12T12:01:06.044000000Z",
            "active_until": null,
            "created_by_actor": {
              "type": "workspace-member",
              "id": "bbe415be-7a1d-45c7-9a8b-2af7b3cc962a"
            },
            "status": {
              "id": {
                "workspace_id": "515117c4-5fd1-4bfd-bc63-58f639d3f357",
                "object_id": "030f5287-761d-42ef-9feb-7d2e9a1ba52b",
                "attribute_id": "1a04f7e7-9392-40cb-9071-b1024f2eec73",
                "status_id": "10e0b809-893f-438a-a6a4-d69153c38ddc"
              },
              "title": "Prospecting",
              "is_archived": false,
              "target_time_in_status": null,
              "celebration_enabled": false
            },
            "attribute_type": "status"
          }
        ],
        "entry_id": [
          {
            "active_from": "2024-11-12T12:01:06.044000000Z",
            "active_until": null,
            "created_by_actor": {
              "type": "workspace-member",
              "id": "bbe415be-7a1d-45c7-9a8b-2af7b3cc962a"
            },
            "value": "d36aa78b-a0d6-4f76-8970-a02275859b9f",
            "attribute_type": "text"
          }
        ],
        "main_point_of_contact": [],
        "owner": [
          {
            "active_from": "2024-11-12T12:01:06.044000000Z",
            "active_until": null,
            "created_by_actor": {
              "type": "workspace-member",
              "id": "bbe415be-7a1d-45c7-9a8b-2af7b3cc962a"
            },
            "referenced_actor_type": "workspace-member",
            "referenced_actor_id": "bbe415be-7a1d-45c7-9a8b-2af7b3cc962a",
            "attribute_type": "actor-reference"
          }
        ],
        "priority": [],
        "estimated_contract_value": [],
        "projected_close_date": [
          {
            "active_from": "2024-11-12T12:01:06.044000000Z",
            "active_until": null,
            "created_by_actor": {
              "type": "workspace-member",
              "id": "bbe415be-7a1d-45c7-9a8b-2af7b3cc962a"
            },
            "value": "2024-11-26",
            "attribute_type": "date"
          }
        ],
        "close_confidence": [],
        "close_lost_reason": [],
        "notes": [],
        "created_at": [
          {
            "active_from": "2024-11-12T12:01:06.044000000Z",
            "active_until": null,
            "created_by_actor": {
              "type": "workspace-member",
              "id": "bbe415be-7a1d-45c7-9a8b-2af7b3cc962a"
            },
            "value": "2024-11-12T12:01:06.084000000Z",
            "attribute_type": "timestamp"
          }
        ],
        "created_by": [
          {
            "active_from": "2024-11-12T12:01:06.044000000Z",
            "active_until": null,
            "created_by_actor": {
              "type": "workspace-member",
              "id": "bbe415be-7a1d-45c7-9a8b-2af7b3cc962a"
            },
            "referenced_actor_type": "workspace-member",
            "referenced_actor_id": "bbe415be-7a1d-45c7-9a8b-2af7b3cc962a",
            "attribute_type": "actor-reference"
          }
        ],
        "deal_name": [],
        "company": []
      }
    },
    {
      "id": {
        "workspace_id": "515117c4-5fd1-4bfd-bc63-58f639d3f357",
        "list_id": "030f5287-761d-42ef-9feb-7d2e9a1ba52b",
        "entry_id": "d715607e-1794-403e-811b-f602ead3aed7"
      },
      "parent_record_id": "d2ecb6da-8088-46e3-b46c-dead3c4eff46",
      "parent_object": "companies",
      "created_at": "2024-11-12T12:01:10.283000000Z",
      "entry_values": {
        "stage": [
          {
            "active_from": "2024-11-12T12:01:10.283000000Z",
            "active_until": null,
            "created_by_actor": {
              "type": "workspace-member",
              "id": "bbe415be-7a1d-45c7-9a8b-2af7b3cc962a"
            },
            "status": {
              "id": {
                "workspace_id": "515117c4-5fd1-4bfd-bc63-58f639d3f357",
                "object_id": "030f5287-761d-42ef-9feb-7d2e9a1ba52b",
                "attribute_id": "1a04f7e7-9392-40cb-9071-b1024f2eec73",
                "status_id": "10e0b809-893f-438a-a6a4-d69153c38ddc"
              },
              "title": "Prospecting",
              "is_archived": false,
              "target_time_in_status": null,
              "celebration_enabled": false
            },
            "attribute_type": "status"
          }
        ],
        "entry_id": [
          {
            "active_from": "2024-11-12T12:01:10.283000000Z",
            "active_until": null,
            "created_by_actor": {
              "type": "workspace-member",
              "id": "bbe415be-7a1d-45c7-9a8b-2af7b3cc962a"
            },
            "value": "d715607e-1794-403e-811b-f602ead3aed7",
            "attribute_type": "text"
          }
        ],
        "main_point_of_contact": [],
        "owner": [
          {
            "active_from": "2024-11-12T12:01:10.283000000Z",
            "active_until": null,
            "created_by_actor": {
              "type": "workspace-member",
              "id": "bbe415be-7a1d-45c7-9a8b-2af7b3cc962a"
            },
            "referenced_actor_type": "workspace-member",
            "referenced_actor_id": "bbe415be-7a1d-45c7-9a8b-2af7b3cc962a",
            "attribute_type": "actor-reference"
          }
        ],
        "priority": [],
        "estimated_contract_value": [],
        "projected_close_date": [
          {
            "active_from": "2024-11-12T12:01:10.283000000Z",
            "active_until": null,
            "created_by_actor": {
              "type": "workspace-member",
              "id": "bbe415be-7a1d-45c7-9a8b-2af7b3cc962a"
            },
            "value": "2024-11-26",
            "attribute_type": "date"
          }
        ],
        "close_confidence": [],
        "close_lost_reason": [],
        "notes": [],
        "created_at": [
          {
            "active_from": "2024-11-12T12:01:10.283000000Z",
            "active_until": null,
            "created_by_actor": {
              "type": "workspace-member",
              "id": "bbe415be-7a1d-45c7-9a8b-2af7b3cc962a"
            },
            "value": "2024-11-12T12:01:10.314000000Z",
            "attribute_type": "timestamp"
          }
        ],
        "created_by": [
          {
            "active_from": "2024-11-12T12:01:10.283000000Z",
            "active_until": null,
            "created_by_actor": {
              "type": "workspace-member",
              "id": "bbe415be-7a1d-45c7-9a8b-2af7b3cc962a"
            },
            "referenced_actor_type": "workspace-member",
            "referenced_actor_id": "bbe415be-7a1d-45c7-9a8b-2af7b3cc962a",
            "attribute_type": "actor-reference"
          }
        ],
        "deal_name": [],
        "company": []
      }
    },
    {
      "id": {
        "workspace_id": "515117c4-5fd1-4bfd-bc63-58f639d3f357",
        "list_id": "030f5287-761d-42ef-9feb-7d2e9a1ba52b",
        "entry_id": "dede67f7-e8fe-4779-873e-09b5e570f045"
      },
      "parent_record_id": "5c64b116-eeee-4be0-8e34-3054b9ed48d7",
      "parent_object": "companies",
      "created_at": "2024-11-12T12:01:07.399000000Z",
      "entry_values": {
        "stage": [
          {
            "active_from": "2024-11-12T12:01:07.399000000Z",
            "active_until": null,
            "created_by_actor": {
              "type": "workspace-member",
              "id": "bbe415be-7a1d-45c7-9a8b-2af7b3cc962a"
            },
            "status": {
              "id": {
                "workspace_id": "515117c4-5fd1-4bfd-bc63-58f639d3f357",
                "object_id": "030f5287-761d-42ef-9feb-7d2e9a1ba52b",
                "attribute_id": "1a04f7e7-9392-40cb-9071-b1024f2eec73",
                "status_id": "10e0b809-893f-438a-a6a4-d69153c38ddc"
              },
              "title": "Prospecting",
              "is_archived": false,
              "target_time_in_status": null,
              "celebration_enabled": false
            },
            "attribute_type": "status"
          }
        ],
        "entry_id": [
          {
            "active_from": "2024-11-12T12:01:07.399000000Z",
            "active_until": null,
            "created_by_actor": {
              "type": "workspace-member",
              "id": "bbe415be-7a1d-45c7-9a8b-2af7b3cc962a"
            },
            "value": "dede67f7-e8fe-4779-873e-09b5e570f045",
            "attribute_type": "text"
          }
        ],
        "main_point_of_contact": [],
        "owner": [
          {
            "active_from": "2024-11-12T12:01:07.399000000Z",
            "active_until": null,
            "created_by_actor": {
              "type": "workspace-member",
              "id": "bbe415be-7a1d-45c7-9a8b-2af7b3cc962a"
            },
            "referenced_actor_type": "workspace-member",
            "referenced_actor_id": "bbe415be-7a1d-45c7-9a8b-2af7b3cc962a",
            "attribute_type": "actor-reference"
          }
        ],
        "priority": [],
        "estimated_contract_value": [],
        "projected_close_date": [
          {
            "active_from": "2024-11-12T12:01:07.399000000Z",
            "active_until": null,
            "created_by_actor": {
              "type": "workspace-member",
              "id": "bbe415be-7a1d-45c7-9a8b-2af7b3cc962a"
            },
            "value": "2024-11-26",
            "attribute_type": "date"
          }
        ],
        "close_confidence": [],
        "close_lost_reason": [],
        "notes": [],
        "created_at": [
          {
            "active_from": "2024-11-12T12:01:07.399000000Z",
            "active_until": null,
            "created_by_actor": {
              "type": "workspace-member",
              "id": "bbe415be-7a1d-45c7-9a8b-2af7b3cc962a"
            },
            "value": "2024-11-12T12:01:07.431000000Z",
            "attribute_type": "timestamp"
          }
        ],
        "created_by": [
          {
            "active_from": "2024-11-12T12:01:07.399000000Z",
            "active_until": null,
            "created_by_actor": {
              "type": "workspace-member",
              "id": "bbe415be-7a1d-45c7-9a8b-2af7b3cc962a"
            },
            "referenced_actor_type": "workspace-member",
            "referenced_actor_id": "bbe415be-7a1d-45c7-9a8b-2af7b3cc962a",
            "attribute_type": "actor-reference"
          }
        ],
        "deal_name": [],
        "company": []
      }
    },
    {
      "id": {
        "workspace_id": "515117c4-5fd1-4bfd-bc63-58f639d3f357",
        "list_id": "030f5287-761d-42ef-9feb-7d2e9a1ba52b",
        "entry_id": "e0eda398-03db-4730-a9ae-60e23339459c"
      },
      "parent_record_id": "65f045f1-f81b-483f-8f08-f19919bc496d",
      "parent_object": "companies",
      "created_at": "2024-11-12T12:01:07.672000000Z",
      "entry_values": {
        "stage": [
          {
            "active_from": "2024-11-12T12:01:07.672000000Z",
            "active_until": null,
            "created_by_actor": {
              "type": "workspace-member",
              "id": "bbe415be-7a1d-45c7-9a8b-2af7b3cc962a"
            },
            "status": {
              "id": {
                "workspace_id": "515117c4-5fd1-4bfd-bc63-58f639d3f357",
                "object_id": "030f5287-761d-42ef-9feb-7d2e9a1ba52b",
                "attribute_id": "1a04f7e7-9392-40cb-9071-b1024f2eec73",
                "status_id": "10e0b809-893f-438a-a6a4-d69153c38ddc"
              },
              "title": "Prospecting",
              "is_archived": false,
              "target_time_in_status": null,
              "celebration_enabled": false
            },
            "attribute_type": "status"
          }
        ],
        "entry_id": [
          {
            "active_from": "2024-11-12T12:01:07.672000000Z",
            "active_until": null,
            "created_by_actor": {
              "type": "workspace-member",
              "id": "bbe415be-7a1d-45c7-9a8b-2af7b3cc962a"
            },
            "value": "e0eda398-03db-4730-a9ae-60e23339459c",
            "attribute_type": "text"
          }
        ],
        "main_point_of_contact": [],
        "owner": [
          {
            "active_from": "2024-11-12T12:01:07.672000000Z",
            "active_until": null,
            "created_by_actor": {
              "type": "workspace-member",
              "id": "bbe415be-7a1d-45c7-9a8b-2af7b3cc962a"
            },
            "referenced_actor_type": "workspace-member",
            "referenced_actor_id": "bbe415be-7a1d-45c7-9a8b-2af7b3cc962a",
            "attribute_type": "actor-reference"
          }
        ],
        "priority": [],
        "estimated_contract_value": [],
        "projected_close_date": [
          {
            "active_from": "2024-11-12T12:01:07.672000000Z",
            "active_until": null,
            "created_by_actor": {
              "type": "workspace-member",
              "id": "bbe415be-7a1d-45c7-9a8b-2af7b3cc962a"
            },
            "value": "2024-11-26",
            "attribute_type": "date"
          }
        ],
        "close_confidence": [],
        "close_lost_reason": [],
        "notes": [],
        "created_at": [
          {
            "active_from": "2024-11-12T12:01:07.672000000Z",
            "active_until": null,
            "created_by_actor": {
              "type": "workspace-member",
              "id": "bbe415be-7a1d-45c7-9a8b-2af7b3cc962a"
            },
            "value": "2024-11-12T12:01:07.721000000Z",
            "attribute_type": "timestamp"
          }
        ],
        "created_by": [
          {
            "active_from": "2024-11-12T12:01:07.672000000Z",
            "active_until": null,
            "created_by_actor": {
              "type": "workspace-member",
              "id": "bbe415be-7a1d-45c7-9a8b-2af7b3cc962a"
            },
            "referenced_actor_type": "workspace-member",
            "referenced_actor_id": "bbe415be-7a1d-45c7-9a8b-2af7b3cc962a",
            "attribute_type": "actor-reference"
          }
        ],
        "deal_name": [],
        "company": []
      }
    },
    {
      "id": {
        "workspace_id": "515117c4-5fd1-4bfd-bc63-58f639d3f357",
        "list_id": "030f5287-761d-42ef-9feb-7d2e9a1ba52b",
        "entry_id": "e96294f6-647b-4157-86f7-67196703d49b"
      },
      "parent_record_id": "40cbc27c-69c0-4b8b-ba1d-11aa12c316e6",
      "parent_object": "companies",
      "created_at": "2024-11-12T12:01:06.654000000Z",
      "entry_values": {
        "stage": [
          {
            "active_from": "2024-11-12T12:01:06.654000000Z",
            "active_until": null,
            "created_by_actor": {
              "type": "workspace-member",
              "id": "bbe415be-7a1d-45c7-9a8b-2af7b3cc962a"
            },
            "status": {
              "id": {
                "workspace_id": "515117c4-5fd1-4bfd-bc63-58f639d3f357",
                "object_id": "030f5287-761d-42ef-9feb-7d2e9a1ba52b",
                "attribute_id": "1a04f7e7-9392-40cb-9071-b1024f2eec73",
                "status_id": "10e0b809-893f-438a-a6a4-d69153c38ddc"
              },
              "title": "Prospecting",
              "is_archived": false,
              "target_time_in_status": null,
              "celebration_enabled": false
            },
            "attribute_type": "status"
          }
        ],
        "entry_id": [
          {
            "active_from": "2024-11-12T12:01:06.654000000Z",
            "active_until": null,
            "created_by_actor": {
              "type": "workspace-member",
              "id": "bbe415be-7a1d-45c7-9a8b-2af7b3cc962a"
            },
            "value": "e96294f6-647b-4157-86f7-67196703d49b",
            "attribute_type": "text"
          }
        ],
        "main_point_of_contact": [],
        "owner": [
          {
            "active_from": "2024-11-12T12:01:06.654000000Z",
            "active_until": null,
            "created_by_actor": {
              "type": "workspace-member",
              "id": "bbe415be-7a1d-45c7-9a8b-2af7b3cc962a"
            },
            "referenced_actor_type": "workspace-member",
            "referenced_actor_id": "bbe415be-7a1d-45c7-9a8b-2af7b3cc962a",
            "attribute_type": "actor-reference"
          }
        ],
        "priority": [],
        "estimated_contract_value": [],
        "projected_close_date": [
          {
            "active_from": "2024-11-12T12:01:06.654000000Z",
            "active_until": null,
            "created_by_actor": {
              "type": "workspace-member",
              "id": "bbe415be-7a1d-45c7-9a8b-2af7b3cc962a"
            },
            "value": "2024-11-26",
            "attribute_type": "date"
          }
        ],
        "close_confidence": [],
        "close_lost_reason": [],
        "notes": [],
        "created_at": [
          {
            "active_from": "2024-11-12T12:01:06.654000000Z",
            "active_until": null,
            "created_by_actor": {
              "type": "workspace-member",
              "id": "bbe415be-7a1d-45c7-9a8b-2af7b3cc962a"
            },
            "value": "2024-11-12T12:01:06.683000000Z",
            "attribute_type": "timestamp"
          }
        ],
        "created_by": [
          {
            "active_from": "2024-11-12T12:01:06.654000000Z",
            "active_until": null,
            "created_by_actor": {
              "type": "workspace-member",
              "id": "bbe415be-7a1d-45c7-9a8b-2af7b3cc962a"
            },
            "referenced_actor_type": "workspace-member",
            "referenced_actor_id": "bbe415be-7a1d-45c7-9a8b-2af7b3cc962a",
            "attribute_type": "actor-reference"
          }
        ],
        "deal_name": [],
        "company": []
      }
    },
    {
      "id": {
        "workspace_id": "515117c4-5fd1-4bfd-bc63-58f639d3f357",
        "list_id": "030f5287-761d-42ef-9feb-7d2e9a1ba52b",
        "entry_id": "eba9baf8-fb6c-4f70-a606-010b5f4ed71f"
      },
      "parent_record_id": "1a3286cc-af9e-4d2a-9b0c-fd0449bb9e40",
      "parent_object": "companies",
      "created_at": "2024-11-12T12:01:06.066000000Z",
      "entry_values": {
        "stage": [
          {
            "active_from": "2024-11-12T12:01:06.066000000Z",
            "active_until": null,
            "created_by_actor": {
              "type": "workspace-member",
              "id": "bbe415be-7a1d-45c7-9a8b-2af7b3cc962a"
            },
            "status": {
              "id": {
                "workspace_id": "515117c4-5fd1-4bfd-bc63-58f639d3f357",
                "object_id": "030f5287-761d-42ef-9feb-7d2e9a1ba52b",
                "attribute_id": "1a04f7e7-9392-40cb-9071-b1024f2eec73",
                "status_id": "10e0b809-893f-438a-a6a4-d69153c38ddc"
              },
              "title": "Prospecting",
              "is_archived": false,
              "target_time_in_status": null,
              "celebration_enabled": false
            },
            "attribute_type": "status"
          }
        ],
        "entry_id": [
          {
            "active_from": "2024-11-12T12:01:06.066000000Z",
            "active_until": null,
            "created_by_actor": {
              "type": "workspace-member",
              "id": "bbe415be-7a1d-45c7-9a8b-2af7b3cc962a"
            },
            "value": "eba9baf8-fb6c-4f70-a606-010b5f4ed71f",
            "attribute_type": "text"
          }
        ],
        "main_point_of_contact": [],
        "owner": [
          {
            "active_from": "2024-11-12T12:01:06.066000000Z",
            "active_until": null,
            "created_by_actor": {
              "type": "workspace-member",
              "id": "bbe415be-7a1d-45c7-9a8b-2af7b3cc962a"
            },
            "referenced_actor_type": "workspace-member",
            "referenced_actor_id": "bbe415be-7a1d-45c7-9a8b-2af7b3cc962a",
            "attribute_type": "actor-reference"
          }
        ],
        "priority": [],
        "estimated_contract_value": [],
        "projected_close_date": [
          {
            "active_from": "2024-11-12T12:01:06.066000000Z",
            "active_until": null,
            "created_by_actor": {
              "type": "workspace-member",
              "id": "bbe415be-7a1d-45c7-9a8b-2af7b3cc962a"
            },
            "value": "2024-11-26",
            "attribute_type": "date"
          }
        ],
        "close_confidence": [],
        "close_lost_reason": [],
        "notes": [],
        "created_at": [
          {
            "active_from": "2024-11-12T12:01:06.066000000Z",
            "active_until": null,
            "created_by_actor": {
              "type": "workspace-member",
              "id": "bbe415be-7a1d-45c7-9a8b-2af7b3cc962a"
            },
            "value": "2024-11-12T12:01:06.101000000Z",
            "attribute_type": "timestamp"
          }
        ],
        "created_by": [
          {
            "active_from": "2024-11-12T12:01:06.066000000Z",
            "active_until": null,
            "created_by_actor": {
              "type": "workspace-member",
              "id": "bbe415be-7a1d-45c7-9a8b-2af7b3cc962a"
            },
            "referenced_actor_type": "workspace-member",
            "referenced_actor_id": "bbe415be-7a1d-45c7-9a8b-2af7b3cc962a",
            "attribute_type": "actor-reference"
          }
        ],
        "deal_name": [],
        "company": []
      }
    },
    {
      "id": {
        "workspace_id": "515117c4-5fd1-4bfd-bc63-58f639d3f357",
        "list_id": "030f5287-761d-42ef-9feb-7d2e9a1ba52b",
        "entry_id": "f0e1a0c8-de2a-4527-a0cc-1db27819bbdb"
      },
      "parent_record_id": "5b251d67-a5ee-4a5d-a723-4faab41a09e2",
      "parent_object": "companies",
      "created_at": "2024-11-12T12:01:07.403000000Z",
      "entry_values": {
        "stage": [
          {
            "active_from": "2024-11-12T12:01:07.403000000Z",
            "active_until": null,
            "created_by_actor": {
              "type": "workspace-member",
              "id": "bbe415be-7a1d-45c7-9a8b-2af7b3cc962a"
            },
            "status": {
              "id": {
                "workspace_id": "515117c4-5fd1-4bfd-bc63-58f639d3f357",
                "object_id": "030f5287-761d-42ef-9feb-7d2e9a1ba52b",
                "attribute_id": "1a04f7e7-9392-40cb-9071-b1024f2eec73",
                "status_id": "10e0b809-893f-438a-a6a4-d69153c38ddc"
              },
              "title": "Prospecting",
              "is_archived": false,
              "target_time_in_status": null,
              "celebration_enabled": false
            },
            "attribute_type": "status"
          }
        ],
        "entry_id": [
          {
            "active_from": "2024-11-12T12:01:07.403000000Z",
            "active_until": null,
            "created_by_actor": {
              "type": "workspace-member",
              "id": "bbe415be-7a1d-45c7-9a8b-2af7b3cc962a"
            },
            "value": "f0e1a0c8-de2a-4527-a0cc-1db27819bbdb",
            "attribute_type": "text"
          }
        ],
        "main_point_of_contact": [],
        "owner": [
          {
            "active_from": "2024-11-12T12:01:07.403000000Z",
            "active_until": null,
            "created_by_actor": {
              "type": "workspace-member",
              "id": "bbe415be-7a1d-45c7-9a8b-2af7b3cc962a"
            },
            "referenced_actor_type": "workspace-member",
            "referenced_actor_id": "bbe415be-7a1d-45c7-9a8b-2af7b3cc962a",
            "attribute_type": "actor-reference"
          }
        ],
        "priority": [],
        "estimated_contract_value": [],
        "projected_close_date": [
          {
            "active_from": "2024-11-12T12:01:07.403000000Z",
            "active_until": null,
            "created_by_actor": {
              "type": "workspace-member",
              "id": "bbe415be-7a1d-45c7-9a8b-2af7b3cc962a"
            },
            "value": "2024-11-26",
            "attribute_type": "date"
          }
        ],
        "close_confidence": [],
        "close_lost_reason": [],
        "notes": [],
        "created_at": [
          {
            "active_from": "2024-11-12T12:01:07.403000000Z",
            "active_until": null,
            "created_by_actor": {
              "type": "workspace-member",
              "id": "bbe415be-7a1d-45c7-9a8b-2af7b3cc962a"
            },
            "value": "2024-11-12T12:01:07.434000000Z",
            "attribute_type": "timestamp"
          }
        ],
        "created_by": [
          {
            "active_from": "2024-11-12T12:01:07.403000000Z",
            "active_until": null,
            "created_by_actor": {
              "type": "workspace-member",
              "id": "bbe415be-7a1d-45c7-9a8b-2af7b3cc962a"
            },
            "referenced_actor_type": "workspace-member",
            "referenced_actor_id": "bbe415be-7a1d-45c7-9a8b-2af7b3cc962a",
            "attribute_type": "actor-reference"
          }
        ],
        "deal_name": [],
        "company": []
      }
    },
    {
      "id": {
        "workspace_id": "515117c4-5fd1-4bfd-bc63-58f639d3f357",
        "list_id": "030f5287-761d-42ef-9feb-7d2e9a1ba52b",
        "entry_id": "f5cdff5b-65b5-4467-a14b-03723809f64c"
      },
      "parent_record_id": "89b316c1-9253-436e-9387-6c35fbbbf1a6",
      "parent_object": "companies",
      "created_at": "2024-11-12T12:01:08.265000000Z",
      "entry_values": {
        "stage": [
          {
            "active_from": "2024-11-12T12:01:08.265000000Z",
            "active_until": null,
            "created_by_actor": {
              "type": "workspace-member",
              "id": "bbe415be-7a1d-45c7-9a8b-2af7b3cc962a"
            },
            "status": {
              "id": {
                "workspace_id": "515117c4-5fd1-4bfd-bc63-58f639d3f357",
                "object_id": "030f5287-761d-42ef-9feb-7d2e9a1ba52b",
                "attribute_id": "1a04f7e7-9392-40cb-9071-b1024f2eec73",
                "status_id": "10e0b809-893f-438a-a6a4-d69153c38ddc"
              },
              "title": "Prospecting",
              "is_archived": false,
              "target_time_in_status": null,
              "celebration_enabled": false
            },
            "attribute_type": "status"
          }
        ],
        "entry_id": [
          {
            "active_from": "2024-11-12T12:01:08.265000000Z",
            "active_until": null,
            "created_by_actor": {
              "type": "workspace-member",
              "id": "bbe415be-7a1d-45c7-9a8b-2af7b3cc962a"
            },
            "value": "f5cdff5b-65b5-4467-a14b-03723809f64c",
            "attribute_type": "text"
          }
        ],
        "main_point_of_contact": [],
        "owner": [
          {
            "active_from": "2024-11-12T12:01:08.265000000Z",
            "active_until": null,
            "created_by_actor": {
              "type": "workspace-member",
              "id": "bbe415be-7a1d-45c7-9a8b-2af7b3cc962a"
            },
            "referenced_actor_type": "workspace-member",
            "referenced_actor_id": "bbe415be-7a1d-45c7-9a8b-2af7b3cc962a",
            "attribute_type": "actor-reference"
          }
        ],
        "priority": [],
        "estimated_contract_value": [],
        "projected_close_date": [
          {
            "active_from": "2024-11-12T12:01:08.265000000Z",
            "active_until": null,
            "created_by_actor": {
              "type": "workspace-member",
              "id": "bbe415be-7a1d-45c7-9a8b-2af7b3cc962a"
            },
            "value": "2024-11-26",
            "attribute_type": "date"
          }
        ],
        "close_confidence": [],
        "close_lost_reason": [],
        "notes": [],
        "created_at": [
          {
            "active_from": "2024-11-12T12:01:08.265000000Z",
            "active_until": null,
            "created_by_actor": {
              "type": "workspace-member",
              "id": "bbe415be-7a1d-45c7-9a8b-2af7b3cc962a"
            },
            "value": "2024-11-12T12:01:08.292000000Z",
            "attribute_type": "timestamp"
          }
        ],
        "created_by": [
          {
            "active_from": "2024-11-12T12:01:08.265000000Z",
            "active_until": null,
            "created_by_actor": {
              "type": "workspace-member",
              "id": "bbe415be-7a1d-45c7-9a8b-2af7b3cc962a"
            },
            "referenced_actor_type": "workspace-member",
            "referenced_actor_id": "bbe415be-7a1d-45c7-9a8b-2af7b3cc962a",
            "attribute_type": "actor-reference"
          }
        ],
        "deal_name": [],
        "company": []
      }
    },
    {
      "id": {
        "workspace_id": "515117c4-5fd1-4bfd-bc63-58f639d3f357",
        "list_id": "030f5287-761d-42ef-9feb-7d2e9a1ba52b",
        "entry_id": "fad3e020-4523-478c-b2df-a8da394c382e"
      },
      "parent_record_id": "a510e2c8-06cf-47a4-8ed5-d6d900d6a325",
      "parent_object": "companies",
      "created_at": "2024-11-12T12:01:09.044000000Z",
      "entry_values": {
        "stage": [
          {
            "active_from": "2024-11-12T12:01:09.044000000Z",
            "active_until": null,
            "created_by_actor": {
              "type": "workspace-member",
              "id": "bbe415be-7a1d-45c7-9a8b-2af7b3cc962a"
            },
            "status": {
              "id": {
                "workspace_id": "515117c4-5fd1-4bfd-bc63-58f639d3f357",
                "object_id": "030f5287-761d-42ef-9feb-7d2e9a1ba52b",
                "attribute_id": "1a04f7e7-9392-40cb-9071-b1024f2eec73",
                "status_id": "10e0b809-893f-438a-a6a4-d69153c38ddc"
              },
              "title": "Prospecting",
              "is_archived": false,
              "target_time_in_status": null,
              "celebration_enabled": false
            },
            "attribute_type": "status"
          }
        ],
        "entry_id": [
          {
            "active_from": "2024-11-12T12:01:09.044000000Z",
            "active_until": null,
            "created_by_actor": {
              "type": "workspace-member",
              "id": "bbe415be-7a1d-45c7-9a8b-2af7b3cc962a"
            },
            "value": "fad3e020-4523-478c-b2df-a8da394c382e",
            "attribute_type": "text"
          }
        ],
        "main_point_of_contact": [],
        "owner": [
          {
            "active_from": "2024-11-12T12:01:09.044000000Z",
            "active_until": null,
            "created_by_actor": {
              "type": "workspace-member",
              "id": "bbe415be-7a1d-45c7-9a8b-2af7b3cc962a"
            },
            "referenced_actor_type": "workspace-member",
            "referenced_actor_id": "bbe415be-7a1d-45c7-9a8b-2af7b3cc962a",
            "attribute_type": "actor-reference"
          }
        ],
        "priority": [],
        "estimated_contract_value": [],
        "projected_close_date": [
          {
            "active_from": "2024-11-12T12:01:09.044000000Z",
            "active_until": null,
            "created_by_actor": {
              "type": "workspace-member",
              "id": "bbe415be-7a1d-45c7-9a8b-2af7b3cc962a"
            },
            "value": "2024-11-26",
            "attribute_type": "date"
          }
        ],
        "close_confidence": [],
        "close_lost_reason": [],
        "notes": [],
        "created_at": [
          {
            "active_from": "2024-11-12T12:01:09.044000000Z",
            "active_until": null,
            "created_by_actor": {
              "type": "workspace-member",
              "id": "bbe415be-7a1d-45c7-9a8b-2af7b3cc962a"
            },
            "value": "2024-11-12T12:01:09.089000000Z",
            "attribute_type": "timestamp"
          }
        ],
        "created_by": [
          {
            "active_from": "2024-11-12T12:01:09.044000000Z",
            "active_until": null,
            "created_by_actor": {
              "type": "workspace-member",
              "id": "bbe415be-7a1d-45c7-9a8b-2af7b3cc962a"
            },
            "referenced_actor_type": "workspace-member",
            "referenced_actor_id": "bbe415be-7a1d-45c7-9a8b-2af7b3cc962a",
            "attribute_type": "actor-reference"
          }
        ],
        "deal_name": [],
        "company": []
      }
    }
  ]
}

## Company records API response, truncated

{
  "data": [
    {
      "id": {
        "workspace_id": "515117c4-5fd1-4bfd-bc63-58f639d3f357",
        "object_id": "e5bc4394-99f9-454a-8fc5-1b82628d019a",
        "record_id": "04e26eb1-3c8b-4ca8-a54f-f2dd4c3e6b2d"
      },
      "created_at": "2024-10-02T09:33:50.339000000Z",
      "values": {
        "record_id": [
          {
            "active_from": "2024-10-02T09:33:50.339000000Z",
            "active_until": null,
            "created_by_actor": {
              "type": "system",
              "id": null
            },
            "value": "04e26eb1-3c8b-4ca8-a54f-f2dd4c3e6b2d",
            "attribute_type": "text"
          }
        ],
        "domains": [
          {
            "active_from": "2024-10-02T09:33:50.339000000Z",
            "active_until": null,
            "created_by_actor": {
              "type": "system",
              "id": null
            },
            "domain": "actioncoach.com",
            "root_domain": "actioncoach.com",
            "attribute_type": "domain"
          }
        ],
        "name": [
          {
            "active_from": "2024-10-02T09:33:50.339000000Z",
            "active_until": null,
            "created_by_actor": {
              "type": "system",
              "id": null
            },
            "value": "ActionCOACH",
            "attribute_type": "text"
          }
        ],
        "description": [
          {
            "active_from": "2024-10-02T09:33:50.599000000Z",
            "active_until": null,
            "created_by_actor": {
              "type": "system",
              "id": null
            },
            "value": "ActionCOACH specializes in providing business coaching, consulting, mentoring, and education services to help business owners enhance their operational efficiency, build effective teams, and increase profitability.",
            "attribute_type": "text"
          }
        ],
        "team": [
          {
            "active_from": "2024-10-02T09:34:32.631000000Z",
            "active_until": null,
            "created_by_actor": {
              "type": "system",
              "id": null
            },
            "target_object": "people",
            "target_record_id": "e0d7713b-7c2d-485d-83bd-31ce687111d4",
            "attribute_type": "record-reference"
          },
          {
            "active_from": "2024-10-02T09:34:37.098000000Z",
            "active_until": null,
            "created_by_actor": {
              "type": "system",
              "id": null
            },
            "target_object": "people",
            "target_record_id": "da93f157-8250-46be-a7b5-a651ca279531",
            "attribute_type": "record-reference"
          },
          {
            "active_from": "2024-10-02T09:34:44.776000000Z",
            "active_until": null,
            "created_by_actor": {
              "type": "system",
              "id": null
            },
            "target_object": "people",
            "target_record_id": "56bc970d-11fb-479e-830b-8d922fa75690",
            "attribute_type": "record-reference"
          },
          {
            "active_from": "2024-10-02T09:34:40.444000000Z",
            "active_until": null,
            "created_by_actor": {
              "type": "system",
              "id": null
            },
            "target_object": "people",
            "target_record_id": "9e873f1e-4753-4437-8bd4-c8a622745928",
            "attribute_type": "record-reference"
          },
          {
            "active_from": "2024-10-02T09:34:49.619000000Z",
            "active_until": null,
            "created_by_actor": {
              "type": "system",
              "id": null
            },
            "target_object": "people",
            "target_record_id": "d2c0de10-a6dd-495a-b4f6-df5b99360e60",
            "attribute_type": "record-reference"
          },
          {
            "active_from": "2024-10-02T09:34:33.891000000Z",
            "active_until": null,
            "created_by_actor": {
              "type": "system",
              "id": null
            },
            "target_object": "people",
            "target_record_id": "4d4e00e3-2faa-404f-bb85-aa59206cc608",
            "attribute_type": "record-reference"
          }
        ],
        "categories": [
          {
            "active_from": "2024-10-02T09:33:50.603000000Z",
            "active_until": null,
            "created_by_actor": {
              "type": "system",
              "id": null
            },
            "option": {
              "id": {
                "workspace_id": "515117c4-5fd1-4bfd-bc63-58f639d3f357",
                "object_id": "e5bc4394-99f9-454a-8fc5-1b82628d019a",
                "attribute_id": "b5340e0e-9918-434f-9a23-594389c86884",
                "option_id": "f8c721c3-5c57-4482-9d7f-6b6017fbc54d"
              },
              "title": "B2B",
              "is_archived": false
            },
            "attribute_type": "select"
          },
          {
            "active_from": "2024-10-02T09:33:50.603000000Z",
            "active_until": null,
            "created_by_actor": {
              "type": "system",
              "id": null
            },
            "option": {
              "id": {
                "workspace_id": "515117c4-5fd1-4bfd-bc63-58f639d3f357",
                "object_id": "e5bc4394-99f9-454a-8fc5-1b82628d019a",
                "attribute_id": "b5340e0e-9918-434f-9a23-594389c86884",
                "option_id": "54a85c21-39a4-4f9a-b5ff-6799dffadfb6"
              },
              "title": "Consulting & Professional Services",
              "is_archived": false
            },
            "attribute_type": "select"
          },
          {
            "active_from": "2024-10-02T09:33:50.603000000Z",
            "active_until": null,
            "created_by_actor": {
              "type": "system",
              "id": null
            },
            "option": {
              "id": {
                "workspace_id": "515117c4-5fd1-4bfd-bc63-58f639d3f357",
                "object_id": "e5bc4394-99f9-454a-8fc5-1b82628d019a",
                "attribute_id": "b5340e0e-9918-434f-9a23-594389c86884",
                "option_id": "619954d8-4c1a-47c5-92fa-8c676063a0d1"
              },
              "title": "Education",
              "is_archived": false
            },
            "attribute_type": "select"
          },
          {
            "active_from": "2024-10-02T09:33:50.603000000Z",
            "active_until": null,
            "created_by_actor": {
              "type": "system",
              "id": null
            },
            "option": {
              "id": {
                "workspace_id": "515117c4-5fd1-4bfd-bc63-58f639d3f357",
                "object_id": "e5bc4394-99f9-454a-8fc5-1b82628d019a",
                "attribute_id": "b5340e0e-9918-434f-9a23-594389c86884",
                "option_id": "b0c2b520-ecd1-41e3-810c-a2ed25f256a2"
              },
              "title": "Telecommunications",
              "is_archived": false
            },
            "attribute_type": "select"
          }
        ],
        "primary_location": [
          {
            "active_from": "2024-10-02T09:33:50.599000000Z",
            "active_until": null,
            "created_by_actor": {
              "type": "system",
              "id": null
            },
            "line_1": "5781 South Fort Apache Road",
            "line_2": null,
            "line_3": null,
            "line_4": null,
            "locality": "Las Vegas",
            "region": "Nevada",
            "postcode": "89148",
            "country_code": "US",
            "latitude": "36.0835906",
            "longitude": "-115.2983435",
            "attribute_type": "location"
          }
        ],
        "logo_url": [
          {
            "active_from": "2024-10-02T09:33:50.599000000Z",
            "active_until": null,
            "created_by_actor": {
              "type": "system",
              "id": null
            },
            "value": "https://logo.clearbit.com/actioncoach.com",
            "attribute_type": "text"
          }
        ],
        "angellist": [],
        "facebook": [
          {
            "active_from": "2024-10-02T09:33:50.600000000Z",
            "active_until": null,
            "created_by_actor": {
              "type": "system",
              "id": null
            },
            "value": "https://facebook.com/actioncoachbusinesscoaching",
            "attribute_type": "text"
          }
        ],
        "instagram": [],
        "linkedin": [
          {
            "active_from": "2024-10-02T09:33:50.600000000Z",
            "active_until": null,
            "created_by_actor": {
              "type": "system",
              "id": null
            },
            "value": "https://linkedin.com/company/actioncoach",
            "attribute_type": "text"
          }
        ],
        "twitter": [
          {
            "active_from": "2024-10-02T09:33:50.600000000Z",
            "active_until": null,
            "created_by_actor": {
              "type": "system",
              "id": null
            },
            "value": "https://x.com/ActionCOACH",
            "attribute_type": "text"
          }
        ],
        "twitter_follower_count": [
          {
            "active_from": "2024-10-02T09:33:50.601000000Z",
            "active_until": null,
            "created_by_actor": {
              "type": "system",
              "id": null
            },
            "value": 7067,
            "attribute_type": "number"
          }
        ],
        "estimated_arr_usd": [
          {
            "active_from": "2024-10-02T09:33:50.602000000Z",
            "active_until": null,
            "created_by_actor": {
              "type": "system",
              "id": null
            },
            "option": {
              "id": {
                "workspace_id": "515117c4-5fd1-4bfd-bc63-58f639d3f357",
                "object_id": "e5bc4394-99f9-454a-8fc5-1b82628d019a",
                "attribute_id": "c0476cf1-e2d2-4ae1-b11a-5024e0fe4881",
                "option_id": "c025529c-9dd3-4b8a-988e-3821ecd57459"
              },
              "title": "$250M-$500M",
              "is_archived": false
            },
            "attribute_type": "select"
          }
        ],
        "funding_raised_usd": [],
        "foundation_date": [
          {
            "active_from": "2024-10-02T09:33:50.601000000Z",
            "active_until": null,
            "created_by_actor": {
              "type": "system",
              "id": null
            },
            "value": "1993-01-01",
            "attribute_type": "date"
          }
        ],
        "employee_range": [
          {
            "active_from": "2024-10-02T09:33:50.603000000Z",
            "active_until": null,
            "created_by_actor": {
              "type": "system",
              "id": null
            },
            "option": {
              "id": {
                "workspace_id": "515117c4-5fd1-4bfd-bc63-58f639d3f357",
                "object_id": "e5bc4394-99f9-454a-8fc5-1b82628d019a",
                "attribute_id": "942e20af-a793-48bd-b0ff-b628b19e5579",
                "option_id": "6806fbf0-f7dc-4fc8-8e40-13d60c202e35"
              },
              "title": "1K-5K",
              "is_archived": false
            },
            "attribute_type": "select"
          }
        ],
        "first_calendar_interaction": [
          {
            "active_from": "2024-10-02T09:41:13.357000000Z",
            "active_until": null,
            "created_by_actor": {
              "type": "system",
              "id": null
            },
            "interaction_type": "calendar-event",
            "interacted_at": "2022-11-25T13:00:00.697000000Z",
            "owner_actor": {
              "type": "workspace-member",
              "id": "a493e9ae-e850-42b3-ad44-c7513f21ec79"
            },
            "attribute_type": "interaction"
          }
        ],
        "last_calendar_interaction": [
          {
            "active_from": "2024-10-02T09:41:13.357000000Z",
            "active_until": null,
            "created_by_actor": {
              "type": "system",
              "id": null
            },
            "interaction_type": "calendar-event",
            "interacted_at": "2024-08-06T17:00:00.135000000Z",
            "owner_actor": {
              "type": "workspace-member",
              "id": "a493e9ae-e850-42b3-ad44-c7513f21ec79"
            },
            "attribute_type": "interaction"
          }
        ],
        "next_calendar_interaction": [],
        "first_email_interaction": [
          {
            "active_from": "2024-10-02T09:41:13.357000000Z",
            "active_until": null,
            "created_by_actor": {
              "type": "system",
              "id": null
            },
            "interaction_type": "email",
            "interacted_at": "2022-11-06T23:07:37.211000000Z",
            "owner_actor": {
              "type": "workspace-member",
              "id": "bbe415be-7a1d-45c7-9a8b-2af7b3cc962a"
            },
            "attribute_type": "interaction"
          }
        ],
        "last_email_interaction": [
          {
            "active_from": "2024-10-02T09:35:14.956000000Z",
            "active_until": null,
            "created_by_actor": {
              "type": "system",
              "id": null
            },
            "interaction_type": "email",
            "interacted_at": "2024-09-10T11:37:20.215000000Z",
            "owner_actor": {
              "type": "workspace-member",
              "id": "a493e9ae-e850-42b3-ad44-c7513f21ec79"
            },
            "attribute_type": "interaction"
          }
        ],
        "first_call_interaction": [],
        "last_call_interaction": [],
        "next_call_interaction": [],
        "first_in_person_meeting_interaction": [],
        "last_in_person_meeting_interaction": [],
        "next_in_person_meeting_interaction": [],
        "first_interaction": [
          {
            "active_from": "2024-10-02T09:41:13.357000000Z",
            "active_until": null,
            "created_by_actor": {
              "type": "system",
              "id": null
            },
            "interaction_type": "email",
            "interacted_at": "2022-11-06T23:07:37.211000000Z",
            "owner_actor": {
              "type": "workspace-member",
              "id": "bbe415be-7a1d-45c7-9a8b-2af7b3cc962a"
            },
            "attribute_type": "interaction"
          }
        ],
        "last_interaction": [
          {
            "active_from": "2024-10-02T09:35:14.956000000Z",
            "active_until": null,
            "created_by_actor": {
              "type": "system",
              "id": null
            },
            "interaction_type": "email",
            "interacted_at": "2024-09-10T11:37:20.215000000Z",
            "owner_actor": {
              "type": "workspace-member",
              "id": "a493e9ae-e850-42b3-ad44-c7513f21ec79"
            },
            "attribute_type": "interaction"
          }
        ],
        "next_interaction": [],
        "strongest_connection_strength_legacy": [
          {
            "active_from": "2024-11-09T15:41:47.224000000Z",
            "active_until": null,
            "created_by_actor": {
              "type": "system",
              "id": null
            },
            "value": 3.7742425596369813,
            "attribute_type": "number"
          }
        ],
        "strongest_connection_strength": [
          {
            "active_from": "2024-10-02T09:35:14.956000000Z",
            "active_until": null,
            "created_by_actor": {
              "type": "system",
              "id": null
            },
            "option": {
              "id": {
                "workspace_id": "515117c4-5fd1-4bfd-bc63-58f639d3f357",
                "object_id": "e5bc4394-99f9-454a-8fc5-1b82628d019a",
                "attribute_id": "6a4ad0e2-d57c-4efc-b2c6-6398ed2e3684",
                "option_id": "f81b4fbc-f832-469a-9110-de41c6ff3248"
              },
              "title": "Very weak",
              "is_archived": false
            },
            "attribute_type": "select"
          }
        ],
        "strongest_connection_user": [
          {
            "active_from": "2024-10-02T09:35:14.956000000Z",
            "active_until": null,
            "created_by_actor": {
              "type": "system",
              "id": null
            },
            "referenced_actor_type": "workspace-member",
            "referenced_actor_id": "a493e9ae-e850-42b3-ad44-c7513f21ec79",
            "attribute_type": "actor-reference"
          }
        ],
        "associated_deals": [
          {
            "active_from": "2024-11-12T15:49:36.649000000Z",
            "active_until": null,
            "created_by_actor": {
              "type": "workspace-member",
              "id": "bbe415be-7a1d-45c7-9a8b-2af7b3cc962a"
            },
            "target_object": "deals",
            "target_record_id": "fe3646cb-bdc1-4053-b9aa-bec3d49e751b",
            "attribute_type": "record-reference"
          }
        ],
        "associated_workspaces": [],
        "created_at": [
          {
            "active_from": "2024-10-02T09:33:50.339000000Z",
            "active_until": null,
            "created_by_actor": {
              "type": "system",
              "id": null
            },
            "value": "2024-10-02T09:33:50.354000000Z",
            "attribute_type": "timestamp"
          }
        ],
        "created_by": [
          {
            "active_from": "2024-10-02T09:33:50.339000000Z",
            "active_until": null,
            "created_by_actor": {
              "type": "system",
              "id": null
            },
            "referenced_actor_type": "system",
            "referenced_actor_id": null,
            "attribute_type": "actor-reference"
          }
        ],
        "number_of_users": [],
        "subscriptions": [],
        "ltv": [],
        "yelp_address": [
          {
            "active_from": "2024-11-11T17:58:08.810000000Z",
            "active_until": null,
            "created_by_actor": {
              "type": "workspace-member",
              "id": "bbe415be-7a1d-45c7-9a8b-2af7b3cc962a"
            },
            "value": "test123",
            "attribute_type": "text"
          }
        ]
      }
    },
    {
      "id": {
        "workspace_id": "515117c4-5fd1-4bfd-bc63-58f639d3f357",
        "object_id": "e5bc4394-99f9-454a-8fc5-1b82628d019a",
        "record_id": "16504cd8-6e0c-4091-9385-98dabfe378d8"
      },
      "created_at": "2024-10-02T09:33:49.529000000Z",
      "values": {
        "record_id": [
          {
            "active_from": "2024-10-02T09:33:49.529000000Z",
            "active_until": null,
            "created_by_actor": {
              "type": "system",
              "id": null
            },
            "value": "16504cd8-6e0c-4091-9385-98dabfe378d8",
            "attribute_type": "text"
          }
        ],
        "domains": [
          {
            "active_from": "2024-10-02T09:33:49.529000000Z",
            "active_until": null,
            "created_by_actor": {
              "type": "system",
              "id": null
            },
            "domain": "anvilcp.com",
            "root_domain": "anvilcp.com",
            "attribute_type": "domain"
          }
        ],


---

OK, the lists API isn't actually any simpler. It just returns the list attributes
on a record. And then it links to the parent record. So any time that I'm using the
list entry API I will need to query the records API anyway. The benefit of lists
is that it forces the user to define a filtered subset of records up front which 
I can then fetch all of – provided it's not insanely large.

There is definitely no way I can sync all of an object. Deals is maybe an exception
but otherwise you just can't grab all that data up front, even if you're only selecting for a few attributes. And for a spreadsheet you don't ever only care
about a few attributes.

Either way, it is possible to make the record fetches more manageable by specifying
which data we want back. I'm only going to show certain attributes, so I don't need
the whole record. Sure, but I don't know ahead of time what they are. I think the
list tradeoff currently is a pretty good one.

The main thing to think about is handling views.

Option 1:

Require user to create a list, then load that list and all its relations and have
the user manually construct filters out of them. This is possible and not terrible
to do with Sheets' UI for hiding columns or constructing views. Problem is that
using lists could get annoying if you're actually working with objects. Imagine
you're looking to analyze Deals on an ongoing basis, you'd need to create a new list each time based on your view in addition to refreshing the data so that you
capture new records that are in the view. In other words, the view is the actual
source of truth.

In general when Zev talks about objects being a priority he is really talking about
views. If you are talking about records of a given attribute, filtered by certain
attributes, with certain attributes displayed, that is just a view. 

Info from Zev:

"Sounds good. I know for certain that Roberto would use this a ton with just a full dump of all workspace data. Drew too"

^ all workspaces in total is 50k records

something I wanted to try was using a chrome extension to capture view data but..
this isnt really optimal at all, its very hacky. you would need to read DOM elements and parse them into an LLM to retrieve attribute settings, then read the
network traffic and first read the request for listing filters and then each of 
the individual requests by id to retrieve the filter data. Yeah that's completely 
insane. It's a nice idea but you'd need the information to be in the DOM.

So in that case, you need to find a way to make this work that is simple and effective. I don't think I can figure that out until I have at least some feedback
from people that are gonna use this. I frankly have no idea what they're using it
for.

Alright, after a quick look in Intercom I have one example to go off: 

- Hi, we want to have tabular reports on deals that are summed by attributes we have. For example, a table that shows revenue by division, by year, and % of goal.




---

# Actions

- Speak to Roberto and get his feedback on what he needs this to do from a finance POV
- Get Zev setup with initial alpha version (script install) so that he can give
  feedback
- Create Notion documentation on how to use with FAQ etc