# SPIFFE Workload Identity and CIMD Management API Reference

## Management API

Trust domains are managed via REST endpoints under the domain resource path:

```http
GET    /organizations/{organizationId}/environments/{environmentId}/domains/{domain}/trust-domains
POST   /organizations/{organizationId}/environments/{environmentId}/domains/{domain}/trust-domains
GET    /organizations/{organizationId}/environments/{environmentId}/domains/{domain}/trust-domains/{trustDomainId}
PUT    /organizations/{organizationId}/environments/{environmentId}/domains/{domain}/trust-domains/{trustDomainId}
DELETE /organizations/{organizationId}/environments/{environmentId}/domains/{domain}/trust-domains/{trustDomainId}
```

## Application Listing API

The application listing endpoint supports multi-value `type` filtering:

```http
GET /organizations/{organizationId}/environments/{environmentId}/domains/{domain}/applications?type=WEB&type=AGENT
```

**Query Parameters:**

| Parameter | Description | Example |
|:----------|:------------|:--------|
| `type` | Filter by one or more application types | `?type=WEB&type=AGENT` |
| `status` | Filter by enabled/disabled status | `?status=enabled` |
| `page` | Page number (zero-indexed) | `?page=0` |
| `size` | Page size | `?size=50` |

### CIMD API

CIMD validation and application creation are exposed via REST endpoints.

#### Validate CIMD document

Use the following endpoint to validate a CIMD document:

```http
POST /organizations/{organizationId}/environments/{environmentId}/domains/{domain}/cimd/validate
Content-Type: application/json

{
  "url": "https://example.com/.well-known/client-metadata"
}
```

**Response (200):**

```json
{
  "url": "https://example.com/.well-known/client-metadata",
  "hasInlineJwks": true,
  "missing": {
    "clientId": false,
    "clientName": false
  },
  "metadata": {
    "client_id": "...",
    "client_name": "...",
    "redirect_uris": ["..."],
    "grant_types": ["..."],
    "token_endpoint_auth_method": "...",
    "jwks_uri": "...",
    "scope": "openid profile"
  }
}
```

#### Create application from CIMD

Use the following endpoint to create an application from a CIMD document:

```http
POST /organizations/{organizationId}/environments/{environmentId}/domains/{domain}/cimd/applications
Content-Type: application/json

{
  "cimdUrl": "https://example.com/.well-known/client-metadata",
  "name": "My Application",
  "type": "WEB"
}
```


**Response (201):**

Returns the full application object with a `Location` header.
