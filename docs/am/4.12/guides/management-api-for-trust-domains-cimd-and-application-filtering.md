# Management API for Trust Domains, CIMD, and Application Filtering

## CIMD API

The CIMD API provides endpoints for validating Client Identity Metadata Documents and creating applications from CIMD URLs. Both endpoints require `APPLICATION[CREATE]` permission and a CIMD-enabled domain.

### POST `/organizations/{organizationId}/environments/{environmentId}/domains/{domain}/cimd/validate`

Validates a CIMD URL and returns parsed metadata preview.

**Request Body:**

```json
{
  "url": "string"
}
```

**Response (200):**

```json
{
  "url": "string",
  "hasInlineJwks": true,
  "missing": {
    "clientId": false,
    "clientName": false
  },
  "metadata": {
    "client_id": "string",
    "client_name": "string",
    "redirect_uris": ["string"],
    "grant_types": ["string"],
    "response_types": ["string"],
    "token_endpoint_auth_method": "string",
    "jwks_uri": "string",
    "application_type": "string",
    "subject_type": "string",
    "id_token_signed_response_alg": "string",
    "scope": "string",
    "contacts": ["string"],
    "logo_uri": "string",
    "client_uri": "string",
    "policy_uri": "string",
    "tos_uri": "string",
    "software_id": "string",
    "software_version": "string",
    "software_statement": "string",
    "tls_client_auth_subject_dn": "string",
    "tls_client_auth_san_dns": "string",
    "tls_client_auth_san_uri": "string",
    "tls_client_auth_san_ip": "string",
    "tls_client_auth_san_email": "string",
    "tls_client_certificate_bound_access_tokens": true,
    "backchannel_token_delivery_mode": "string",
    "backchannel_client_notification_endpoint": "string",
    "backchannel_authentication_request_signing_alg": "string",
    "backchannel_user_code_parameter": true,
    "post_logout_redirect_uris": ["string"],
    "request_uris": ["string"],
    "sector_identifier_uri": "string"
  }
}
```

### POST `/organizations/{organizationId}/environments/{environmentId}/domains/{domain}/cimd/applications`

Creates an application from a CIMD document URL. The CIMD URL becomes the application's `client_id`. All parsed metadata is persisted, and the document is upserted to pre-warm the gateway cache.

**Request Body:**

```json
{
  "cimdUrl": "string",
  "name": "string",
  "clientName": "string",
  "description": "string",
  "type": "WEB | NATIVE | BROWSER | SERVICE | RESOURCE_SERVER"
}
```

## Application Filtering API

The Application Filtering API supports multi-valued type filtering for application listings.

### GET `/organizations/{organizationId}/environments/{environmentId}/domains/{domain}/applications?type=AGENT&type=SERVICE`

The `type` query parameter accepts multiple values (array). Each value must be one of:

- `WEB`
- `NATIVE`
- `BROWSER`
- `SERVICE`
- `RESOURCE_SERVER`
- `AGENT`

The Applications list in the management console excludes agents. The Agents list filters to `type=AGENT` only.

### Management API

The following Management API endpoints manage SPIFFE trust domain registrations:

#### Create a trust domain

**POST** `/organizations/{organizationId}/environments/{environmentId}/domains/{domain}/trust-domains`

Creates a SPIFFE trust domain registration.

#### List trust domains

**GET** `/organizations/{organizationId}/environments/{environmentId}/domains/{domain}/trust-domains`

Lists all trust domains for a security domain.

#### Retrieve a trust domain

**GET** `/organizations/{organizationId}/environments/{environmentId}/domains/{domain}/trust-domains/{trustDomainId}`

Retrieves a single trust domain.

#### Update a trust domain

**PUT** `/organizations/{organizationId}/environments/{environmentId}/domains/{domain}/trust-domains/{trustDomainId}`

Updates a trust domain.

#### Delete a trust domain

**DELETE** `/organizations/{organizationId}/environments/{environmentId}/domains/{domain}/trust-domains/{trustDomainId}`

Deletes a trust domain.
