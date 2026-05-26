# Managing Dictionaries via Automation API

## Prerequisites

Before managing dictionaries via the Automation API, ensure the following requirements are met:

* Organization and environment IDs for the target APIM instance
* `ENVIRONMENT_DICTIONARY` permissions with `CREATE`, `UPDATE`, `DELETE`, and `READ` actions
* For dynamic dictionaries: a reachable HTTP endpoint and valid JOLT transformation specification
* For Kubernetes CRD: GKO operator installed and `ManagementContext` resource configured
* For Kubernetes templating: Secrets or ConfigMaps must exist before dictionary creation

## Creating a Dictionary

To create a dictionary via the Automation API, send a PUT request to `/organizations/{orgId}/environments/{envId}/dictionaries` with a JSON body containing the dictionary specification.

The request body must include:

* `hrid`: Human-readable ID matching the pattern `^[a-zA-Z0-9][a-zA-Z0-9_-]+[a-zA-Z0-9]$` with a maximum length of 256 characters
* `name`: Dictionary name (minimum 3 characters)
* `type`: `MANUAL` or `DYNAMIC`
* `deployed`: Boolean flag indicating deployment state

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

For dynamic dictionaries, define a `dynamic.provider` object with the HTTP endpoint URL, method, JOLT specification, optional headers, and a `dynamic.trigger` object specifying the polling rate and unit:

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

Use the `dryRun=true` query parameter to validate the specification without persisting it:

```
PUT /organizations/{orgId}/environments/{envId}/dictionaries?dryRun=true
```

## Managing Dictionaries

### Retrieving a Dictionary

Retrieve a dictionary by sending a GET request to `/organizations/{orgId}/environments/{envId}/dictionaries/{hrid}`. The response includes the dictionary state with all configuration fields.

Users without `CREATE`, `UPDATE`, or `DELETE` permissions on `ENVIRONMENT_DICTIONARY` will receive a response with the `dynamic` field stripped.

### Updating a Dictionary

Update a dictionary by sending a PUT request to `/organizations/{orgId}/environments/{envId}/dictionaries` with the modified specification. The system validates type consistency and deploys or undeploys the dictionary based on the `deployed` flag.

The dictionary type cannot be changed after creation. Attempting to change `type` from `MANUAL` to `DYNAMIC` or vice versa will result in a validation error.

### Deleting a Dictionary

Delete a dictionary by sending a DELETE request to `/organizations/{orgId}/environments/{envId}/dictionaries/{hrid}`. The API returns `204 No Content` on success.
