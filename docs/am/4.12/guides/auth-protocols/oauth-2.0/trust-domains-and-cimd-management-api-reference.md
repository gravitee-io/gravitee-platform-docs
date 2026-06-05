# Trust Domains and CIMD Management API Reference

## Management API

### List Trust Domains

```
GET /organizations/{orgId}/environments/{envId}/domains/{domain}/trust-domains
```

Retrieves all Trust Domains registered for the specified domain.

### Create Trust Domain

```
POST /organizations/{orgId}/environments/{envId}/domains/{domain}/trust-domains
```

Creates a new Trust Domain. The request body must include the Trust Domain name, bundle source type, and allowed signing algorithms.

### Get Trust Domain

```
GET /organizations/{orgId}/environments/{envId}/domains/{domain}/trust-domains/{id}
```

Retrieves a specific Trust Domain by its unique identifier.

### Update Trust Domain

```
PUT /organizations/{orgId}/environments/{envId}/domains/{domain}/trust-domains/{id}
```

Updates an existing Trust Domain. All fields from the original Trust Domain must be included in the request body.

### Delete Trust Domain

```
DELETE /organizations/{orgId}/environments/{envId}/domains/{domain}/trust-domains/{id}
```

Deletes the specified Trust Domain.

### Validate CIMD URL

```
POST /organizations/{orgId}/environments/{envId}/domains/{domain}/cimd/validate
```

Validates a Client ID Metadata Document URL and returns parsed metadata.

**Request body**:

```json
{
  "url": "https://example.com/.well-known/client-metadata"
}
```

**Response**: The response includes parsed metadata, validation status, and any missing required fields.

### Create Application from CIMD

```
POST /organizations/{orgId}/environments/{envId}/domains/{domain}/cimd/applications
```

Creates a new application using metadata from a Client ID Metadata Document URL.

**Request body**:

```json
{
  "cimdUrl": "https://example.com/.well-known/client-metadata",
  "name": "My Application",
  "clientName": "Optional override for client_name",
  "description": "Optional description",
  "type": "WEB"
}
```

| Field | Required | Description |
|:------|:---------|:------------|
| **cimdUrl** | Yes | URL to the Client ID Metadata Document |
| **name** | Yes | Display name for the application |
| **clientName** | No | Override for the `client_name` field from the CIMD document |
| **description** | No | Optional description of the application |
| **type** | Yes | Application type (e.g., `WEB`, `NATIVE`, `BROWSER`, `SERVICE`, `RESOURCE_SERVER`) |

### Filter Applications by Type

```
GET /organizations/{orgId}/environments/{envId}/domains/{domain}/applications?type=AGENT&type=SERVICE
```

Retrieves applications filtered by one or more application types. The `type` query parameter accepts multiple values to filter by application type.

**Example**:

```
GET /applications?type=WEB&type=SERVICE&type=AGENT
```
