# Manage dictionaries with the Automation API

## Overview

Dictionaries provide key-value data stores that can be referenced in API policies and configurations. Gravitee supports two dictionary types: MANUAL dictionaries for static data updated by administrators, and DYNAMIC dictionaries that automatically refresh from external HTTP sources on a scheduled interval. Dictionaries are scoped to an environment and can be deployed to the gateway for runtime use.

## Key concepts

### Dictionary types

Gravitee supports two dictionary types that determine how data is populated and updated:

| Type | Data Source | Update Method | Use Case |
|------|-------------|---------------|----------|
| MANUAL | Administrator-defined properties | Manual updates via API or UI | Static configuration data, feature flags, environment-specific constants |
| DYNAMIC | External HTTP provider | Automatic polling at configured intervals | Real-time data from external systems, frequently changing reference data |

### MANUAL dictionaries

MANUAL dictionaries store static key-value pairs defined by administrators. Each dictionary contains a `properties` map where keys and values are both strings. When deployed, the dictionary data becomes available to policies running on the gateway. Administrators update MANUAL dictionary data through the Management API or Console, and changes take effect after redeployment.

### DYNAMIC dictionaries

DYNAMIC dictionaries fetch data from an external HTTP endpoint at regular intervals. Each DYNAMIC dictionary requires a `provider` configuration (HTTP endpoint details) and a `trigger` configuration (polling schedule). The provider's `specification` field contains a JOLT transformation that converts the HTTP response into Gravitee key-value properties. When started, the dictionary polls the endpoint according to the trigger schedule and automatically updates gateway data.

### Dictionary deployment states

| Type | Deployed: true | Deployed: false |
|------|----------------|-----------------|
| MANUAL | Dictionary is deployed to gateway; data is available to policies | Dictionary is undeployed from gateway; data is unavailable |
| DYNAMIC | Dictionary is started; polling begins and data refreshes automatically | Dictionary is stopped; polling ends and data becomes stale |

### HTTP provider configuration

DYNAMIC dictionaries use HTTP providers to fetch external data. Each provider specifies:

* **URL**: The endpoint to call
* **Method**: HTTP method (GET, POST, PUT, PATCH, DELETE, HEAD, OPTIONS, TRACE, CONNECT)
* **Specification**: JOLT transformation to convert response into properties
* **Headers**: Optional HTTP headers (array of name-value pairs)
* **Body**: Optional request payload
* **Use System Proxy**: Toggle to route requests through system proxy

The JOLT specification transforms the HTTP response into a flat key-value structure. For example, a specification can extract response headers and convert them into dictionary properties.

### Dictionary identifiers

Each dictionary has two identifiers:

* **HRID** (Human-Readable ID): A unique identifier within the environment, following the pattern `^[a-zA-Z0-9][a-zA-Z0-9_-]+[a-zA-Z0-9]$` (max 256 characters). Used for lookups and references.
* **ID**: A system-generated UUID used internally. For dictionaries created before multi-tenant support, the ID may match the HRID for backward compatibility.

## Prerequisites

Before managing dictionaries through the Automation API, make sure these requirements are met:

* Organization and environment IDs for the target APIM instance
* `ENVIRONMENT_DICTIONARY` permission with the `CREATE`, `UPDATE`, `DELETE`, and `READ` actions
* For DYNAMIC dictionaries:
  * A reachable HTTP endpoint accessible from the gateway
  * A valid JOLT transformation specification
  * Polling interval configured (rate and time unit)
* For MANUAL dictionaries:
  * At least one property (key-value pair) defined

{% hint style="info" %}
Users without `CREATE`, `UPDATE`, or `DELETE` permissions on `ENVIRONMENT_DICTIONARY` can view MANUAL dictionary properties but cannot view DYNAMIC dictionary provider and trigger configurations.
{% endhint %}

## Create a dictionary

To create a dictionary, send a `PUT` request to `/organizations/{orgId}/environments/{envId}/dictionaries` with a JSON body containing the dictionary specification.

The request body includes these required fields:

* `hrid`: Human-readable ID matching the pattern `^[a-zA-Z0-9][a-zA-Z0-9_-]+[a-zA-Z0-9]$` with a maximum length of 256 characters. The HRID is used as the dictionary key.
* `name`: Display name of the dictionary
* `type`: `MANUAL` or `DYNAMIC`
* `deployed`: Boolean flag that controls the deployment state

The `description` field is optional.

All dictionaries are created with an initial state of STOPPED. Setting `deployed` to `true` during creation will deploy (MANUAL) or start (DYNAMIC) the dictionary after creation.

### Dictionary configuration reference

| Property | Description | Example |
|----------|-------------|---------|
| `hrid` | Human-readable identifier (pattern: `^[a-zA-Z0-9][a-zA-Z0-9_-]+[a-zA-Z0-9]$`, max 256 chars) | `demo_dictionary` |
| `name` | Display name of the dictionary | `Demo Dictionary` |
| `type` | Dictionary type: MANUAL or DYNAMIC | `MANUAL` |
| `deployed` | Deployment status (true = deployed/started, false = undeployed/stopped) | `true` |
| `description` | Detailed description | `Static configuration for demo environment` |
| `manual.properties` | Key-value pairs for MANUAL dictionaries (required for MANUAL, forbidden for DYNAMIC) | `{"key1": "value1", "key2": "value2"}` |
| `dynamic.provider.type` | Provider type (currently only HTTP supported) | `HTTP` |
| `dynamic.provider.url` | HTTP endpoint URL | `https://api.example.com/data` |
| `dynamic.provider.method` | HTTP method | `GET` |
| `dynamic.provider.specification` | JOLT transformation to convert response to properties | `[{"operation": "shift", "spec": {...}}]` |
| `dynamic.provider.headers` | Optional HTTP headers (array of name-value objects) | `[{"name": "Authorization", "value": "Bearer token"}]` |
| `dynamic.provider.body` | Optional request payload | `{"filter": "active"}` |
| `dynamic.provider.useSystemProxy` | Route requests through system proxy | `false` |
| `dynamic.trigger.rate` | Polling interval rate | `5` |
| `dynamic.trigger.unit` | Polling interval time unit | `SECONDS` |

### Create a MANUAL dictionary

For manual dictionaries, provide a `manual.properties` object with at least one key-value pair. Set `type` to `MANUAL` and `deployed` to `true` to deploy the dictionary to the gateway. Do not include `provider` or `trigger` fields.

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

### Create a DYNAMIC dictionary

For dynamic dictionaries, set `type` to `DYNAMIC` and include both `provider` and `trigger` configurations. The provider must specify the HTTP endpoint URL, method, and JOLT specification. The trigger defines the polling interval using `rate` (integer) and `unit` (MICROSECONDS, MILLISECONDS, SECONDS, MINUTES, HOURS, or DAYS). Set `deployed` to `true` to start the dictionary and begin polling. Do not include the `properties` field.

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

### Dictionary type validation

The API enforces mutual exclusion between MANUAL and DYNAMIC fields:

| Dictionary Type | Required Fields | Forbidden Fields | Error Message |
|-----------------|-----------------|------------------|---------------|
| MANUAL | `properties` (non-empty map) | `provider`, `trigger` | "Manual dictionary must not have 'dynamic' properties (provider, trigger). Set type to 'DYNAMIC' or remove them." |
| DYNAMIC | `provider`, `trigger` | `properties` | "Dynamic dictionary must not have 'manual' properties. Set type to 'MANUAL' or remove them." |

### Response

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

### Dry run validation

To validate the specification without persisting it, add the `dryRun=true` query parameter:

```
PUT /organizations/{orgId}/environments/{envId}/dictionaries?dryRun=true
```

## Manage dictionaries

After a dictionary exists, you can retrieve, update, or delete it through the Automation API.

### Automation API reference

**Base path:** `/organizations/{orgId}/environments/{envId}/dictionaries`

| Operation | Method | Path | Description |
|-----------|--------|------|-------------|
| Create or Update | PUT | `/` | Creates a new dictionary or updates an existing one by HRID |
| Get by HRID | GET | `/{hrid}` | Retrieves dictionary configuration and state |
| Delete | DELETE | `/{hrid}` | Removes a dictionary from the environment |

**Query parameters:**
* `dryRun` (boolean, default: false) — Validates configuration without persisting changes

**Response codes:**
* `200` — Success (returns `DictionaryState`)
* `204` — Dictionary successfully deleted
* `400` — Bad Request (validation failure)
* `401` — Unauthenticated
* `403` — Unauthorized (insufficient permissions)
* `404` — Dictionary not found

### Retrieve a dictionary

Retrieve a dictionary by sending a `GET` request to `/{hrid}`. The response is the `DictionaryState` for that dictionary.

A caller that doesn't hold the `CREATE`, `UPDATE`, or `DELETE` action on `ENVIRONMENT_DICTIONARY` receives a response with the `dynamic` field removed.

### Update a dictionary

Update a dictionary by sending a `PUT` request to `/` with the modified specification. The HRID identifies the dictionary to update. The request is validated for type consistency: a `MANUAL` dictionary can't carry `dynamic` configuration, and a `DYNAMIC` dictionary can't carry `manual` properties.

Changes to the `deployed` field control deployment state:

* Setting `deployed` from `false` to `true` deploys a MANUAL dictionary or starts a DYNAMIC dictionary
* Setting `deployed` from `true` to `false` undeploys a MANUAL dictionary or stops a DYNAMIC dictionary

Changing the `type` field requires updating the corresponding type-specific fields (`properties` for MANUAL, `provider` and `trigger` for DYNAMIC). The validation rules enforce mutual exclusion between MANUAL and DYNAMIC fields.

### Delete a dictionary

Delete a dictionary by sending a `DELETE` request to `/{hrid}`. The API returns `204 No Content` on success. Deleting a deployed or started dictionary automatically undeploys or stops it before removal.

### Terraform provider support

The Gravitee Terraform provider supports dictionary management through the `apim_dictionary` resource and data source. Import existing dictionaries using the format:

```json
{
  "environment_id": "a44e0d1b-9fa9-4d64-8b76-3634623a2e27",
  "hrid": "my_demo_api",
  "organization_id": "dedd0e0f-b3e9-4d2f-89cd-b2a9de7cb145"
}
```

## Verification

To verify a dictionary was created, send a `GET` request to `/{hrid}`. A `200` response with the dictionary's `id`, `name`, `type`, and `deployed` fields confirms the dictionary exists in the target environment.
