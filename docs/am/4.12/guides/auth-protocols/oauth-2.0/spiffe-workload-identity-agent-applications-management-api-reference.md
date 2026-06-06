# SPIFFE Workload Identity & Agent Applications: Management API Reference

## Management API

Trust domain CRUD operations are available via the Management API:

```http
GET    /organizations/{organizationId}/environments/{environmentId}/domains/{domain}/trust-domains
POST   /organizations/{organizationId}/environments/{environmentId}/domains/{domain}/trust-domains
GET    /organizations/{organizationId}/environments/{environmentId}/domains/{domain}/trust-domains/{trustDomainId}
PUT    /organizations/{organizationId}/environments/{environmentId}/domains/{domain}/trust-domains/{trustDomainId}
DELETE /organizations/{organizationId}/environments/{environmentId}/domains/{domain}/trust-domains/{trustDomainId}
```

## CIMD Validation API

Validate a CIMD document before creating an application. Requires `APPLICATION[CREATE]` permission and a CIMD-enabled domain.

**Endpoint:**

```
POST /organizations/{organizationId}/environments/{environmentId}/domains/{domain}/cimd/validate
```

**Request body:**

```json
{
  "url": "https://cimd.acme.com/agent-billing"
}
```

**Response (`CimdValidationResponse`):**

```json
{
  "url": "string",
  "hasInlineJwks": "boolean",
  "missing": {
    "clientId": "boolean",
    "clientName": "boolean"
  },
  "metadata": {
    "client_id": "string",
    "client_name": "string",
    "redirect_uris": ["string"],
    "grant_types": ["string"],
    "token_endpoint_auth_method": "string",
    "jwks_uri": "string",
    "application_type": "string",
    "subject_type": "string",
    "id_token_signed_response_alg": "string",
    "request_object_signing_alg": "string",
    "backchannel_token_delivery_mode": "string",
    "backchannel_client_notification_endpoint": "string",
    "backchannel_authentication_request_signing_alg": "string",
    "backchannel_user_code_parameter": "boolean",
    "tls_client_certificate_bound_access_tokens": "boolean",
    "tls_client_auth_subject_dn": "string",
    "tls_client_auth_san_dns": "string",
    "tls_client_auth_san_uri": "string",
    "tls_client_auth_san_ip": "string",
    "tls_client_auth_san_email": "string",
    "software_id": "string",
    "software_version": "string",
    "software_statement": "string",
    "scope": "string",
    "contacts": ["string"],
    "logo_uri": "string",
    "client_uri": "string",
    "policy_uri": "string",
    "tos_uri": "string",
    "post_logout_redirect_uris": ["string"],
    "request_uris": ["string"],
    "response_types": ["string"],
    "sector_identifier_uri": "string"
  }
}
```

The response includes parsed metadata and validation warnings (e.g., missing `client_id`, missing `client_name`, inline JWKS not supported).

**Create an application from a validated CIMD document.** Requires `APPLICATION[CREATE]` permission and a CIMD-enabled domain.

**Endpoint:**

```
POST /organizations/{organizationId}/environments/{environmentId}/domains/{domain}/cimd/applications
```

**Request body (`NewCimdApplication`):**

```json
{
  "cimdUrl": "https://cimd.acme.com/agent-billing",
  "name": "Billing Agent",
  "clientName": "billing-agent",
  "description": "Autonomous billing agent",
  "type": "SERVICE"
}
```

**Response:** `201 Created` with `Application` entity.
