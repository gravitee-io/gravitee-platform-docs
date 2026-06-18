# Manage dictionaries with the Automation API

## Prerequisites

Before managing dictionaries through the Automation API, make sure these requirements are met:

* Organization and environment IDs for the target APIM instance
* `ENVIRONMENT_DICTIONARY` permission with the `CREATE`, `UPDATE`, `DELETE`, and `READ` actions
* For dynamic dictionaries: a reachable HTTP endpoint and a valid JOLT transformation specification

## Create a dictionary

To create a dictionary, send a `PUT` request to `/organizations/{orgId}/environments/{envId}/dictionaries` with a JSON body containing the dictionary specification.

The request body includes these required fields:

* `hrid`: Human-readable ID matching the pattern `^[a-zA-Z0-9][a-zA-Z0-9_-]+[a-zA-Z0-9]$` with a maximum length of 256 characters. The HRID is used as the dictionary key.
* `name`: Display name of the dictionary
* `type`: `MANUAL` or `DYNAMIC`
* `deployed`: Boolean flag that controls the deployment state

The `description` field is optional.

For manual dictionaries, provide a `manual.properties` object with at least one key-value pair:

```json
{
  "hrid": "my-dict",
  "name": "My Dictionary",
  "type": "MANUAL",
  "deployed": true,
  "manual": {
    "properties": {
      "key1": "value1"
    }
  }
}
```

For dynamic dictionaries, define a `dynamic.provider` object with the HTTP endpoint URL, method, JOLT specification, and optional headers, plus a `dynamic.trigger` object that sets the polling rate and unit:

```json
{
  "hrid": "my-dynamic-dict",
  "name": "My Dynamic Dictionary",
  "type": "DYNAMIC",
  "deployed": true,
  "dynamic": {
    "provider": {
      "type": "HTTP",
      "url": "https://example.com/data",
      "method": "GET",
      "specification": "[{\"operation\":\"shift\",\"spec\":{\"*\":\"\"}}]",
      "headers": [
        {
          "name": "Authorization",
          "value": "Bearer token"
        }
      ]
    },
    "trigger": {
      "rate": 60,
      "unit": "SECONDS"
    }
  }
}
```

The API returns a `DictionaryState` object with the assigned UUID, environment ID, and organization ID:

```json
{
  "id": "dict-uuid",
  "environmentId": "env-id",
  "organizationId": "org-id",
  "hrid": "my-dict",
  "name": "My Dictionary",
  "deployed": true,
  "type": "MANUAL",
  "manual": {
    "properties": {
      "key1": "value1"
    }
  }
}
```

To validate the specification without persisting it, add the `dryRun=true` query parameter:

```
PUT /organizations/{orgId}/environments/{envId}/dictionaries?dryRun=true
```

## Manage dictionaries

After a dictionary exists, you can retrieve, update, or delete it through the Automation API.

### Retrieve a dictionary

Retrieve a dictionary by sending a `GET` request to `/organizations/{orgId}/environments/{envId}/dictionaries/{hrid}`. The response is the `DictionaryState` for that dictionary.

A caller that doesn't hold the `CREATE`, `UPDATE`, or `DELETE` action on `ENVIRONMENT_DICTIONARY` receives a response with the `dynamic` field removed.

### Update a dictionary

Update a dictionary by sending a `PUT` request to `/organizations/{orgId}/environments/{envId}/dictionaries` with the modified specification. The request is validated for type consistency: a `MANUAL` dictionary can't carry `dynamic` configuration, and a `DYNAMIC` dictionary can't carry `manual` properties. The dictionary is then deployed or undeployed based on the `deployed` flag.

### Delete a dictionary

Delete a dictionary by sending a `DELETE` request to `/organizations/{orgId}/environments/{envId}/dictionaries/{hrid}`. The API returns `204 No Content` on success.

## Verification

To verify a dictionary was created, send a `GET` request to `/organizations/{orgId}/environments/{envId}/dictionaries/{hrid}`. A `200` response with the dictionary's `id`, `name`, `type`, and `deployed` fields confirms the dictionary exists in the target environment.
