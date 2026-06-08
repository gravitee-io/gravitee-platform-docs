# Client ID Metadata Document (CIMD)

## Overview

Client ID Metadata Document (CIMD) is an OAuth 2.0 extension that allows clients to present a URL as their `client_id` and retrieve configuration dynamically from that URL, eliminating the need for pre-registration. The Authorization Server fetches a metadata document from the client_id URL and synthesizes the client's configuration by merging it with a designated template application. CIMD is the preferred authentication mechanism for AI agents and Model Context Protocol (MCP) clients, enabling agent-driven workflows to authenticate without manual registration.

When CIMD is enabled, the OIDC discovery document (`/.well-known/openid-configuration`) advertises `client_id_metadata_document_supported: true`.

## Key Concepts

### CIMD Client Identification

A client is treated as a CIMD client when its `client_id` matches the pattern `^https?://` (a URL). During OAuth authentication, the gateway fetches a JSON metadata document from the client_id URL, validates it against SSRF protection rules, and synthesizes a client configuration by merging the metadata with a template application.

Pre-registered applications take precedence: if an application exists in Access Management with a client_id that is also a valid CIMD URL, the pre-registered configuration applies instead of the remote metadata.

### Template Application

The template application defines default settings and restrictions for all CIMD clients in a domain. Valid OAuth settings present in CIMD metadata override template values, with the following exceptions:

- `token_endpoint_auth_method`: Defaults to `"none"` when omitted in metadata
- `grant_types`: Intersected with template values (metadata defaults to `["authorization_code"]`)
- `response_types`: Intersected with template values (metadata defaults to `["code"]`)
- `scope`: Intersected with template scopes when present in metadata; otherwise uses template scopes verbatim

{% hint style="info" %}
Applications are individually elected to be templates in their **Settings** > **General tab**.
{% endhint %}

Non-OAuth application configurations (identity providers, metadata, token validity, certificates, MFA) can only be defined in the [template application](../../applications/). The template application cannot be deleted or un-templated while CIMD is enabled.

### Metadata Caching and Change Detection

CIMD metadata documents are cached in-memory with a configurable TTL (default 24 hours) and maximum entry count (default 1000). When automatic token revocation is enabled, the gateway stores a SHA-256 hash of each metadata document and compares it on subsequent fetches. If the hash changes, all tokens and scope approvals for that client are revoked. This policy detects changes in remote CIMD metadata only; changes to the template application do not trigger revocation.

Stored hashes persist indefinitely while the policy is enabled and are deleted when it is disabled.

{% hint style="info" %}
When clients declare a `jwks_uri`, public keys are resolved using the [JWKS resolver and cache](../../../getting-started/configuration/configure-am-gateway/#jwks-resolver-and-cache), separate from the CIMD cache.
{% endhint %}

### SSRF Protection

All metadata and logo fetches are subject to Server-Side Request Forgery (SSRF) protection. The gateway validates that URLs do not resolve to private, loopback, link-local, or any-local IP addresses (unless explicitly allowed), enforces HTTPS (unless HTTP is explicitly allowed), restricts requests to allowed domains (when configured), and enforces fetch timeout and maximum response size limits. JWKS URIs declared in metadata are validated with the same SSRF rules.

## Creating Agent Applications

For agent application creation, see [Agent Applications](../../applications/application-types.md#agent-applications).

## Domain-Level CIMD Settings

Configure CIMD metadata fetching behavior at the domain level via **Settings → OAuth 2.0 → CIMD**.

<figure><img src="../../../.gitbook/assets/am-cimd-ssrf-protection.png" alt="CIMD SSRF protection settings showing private IP and unsecured HTTP URI toggles"><figcaption></figcaption></figure>

<figure><img src="../../../.gitbook/assets/am-cimd-fetch-settings.png" alt="CIMD fetch timeout and max response size configuration"><figcaption></figcaption></figure>

| Setting | Description | Default |
|:--------|:------------|:--------|
| **Allow Private IP Address** | Allow CIMD URLs resolving to private IP addresses | Disabled |
| **Allow Unsecured HTTP URI** | Allow unsecured HTTP URIs for CIMD URLs (development only) | Disabled |
| **Fetch Timeout (ms)** | Fetch timeout for CIMD URLs in milliseconds | 5000 |
| **Max Response Size (KB)** | Maximum CIMD response size in kilobytes | 512 |


<figure><img src="../../../.gitbook/assets/am-cimd-ssrf-protection.png" alt="CIMD SSRF protection settings showing private IP and unsecured HTTP URI toggles"><figcaption></figcaption></figure>

<figure><img src="../../../.gitbook/assets/am-cimd-settings-overview.png" alt="CIMD domain settings overview showing enabled state and basic configuration"><figcaption></figcaption></figure>

<figure><img src="../../../.gitbook/assets/am-cimd-fetch-settings.png" alt="CIMD fetch timeout and max response size configuration"><figcaption></figcaption></figure>

## Management API Endpoints

### CIMD Validation

**POST** `/organizations/{organizationId}/environments/{environmentId}/domains/{domain}/cimd/validate`

Validate a CIMD URL and preview metadata. Requires `APPLICATION[CREATE]` permission and a CIMD-enabled domain.

Request body:

```json
{
  "url": "https://agents.example.com/.well-known/client-metadata"
}
```

Response:

```json
{
  "url": "https://agents.example.com/.well-known/client-metadata",
  "hasInlineJwks": true,
  "missing": {
    "clientId": false,
    "clientName": false
  },
  "metadata": {
    "client_id": "spiffe://prod.example/hotel-agent",
    "client_name": "Hotel Agent",
    "redirect_uris": ["https://app.example.com/callback"],
    "grant_types": ["authorization_code"],
    "token_endpoint_auth_method": "spiffe_jwt",
    "jwks": { "keys": [...] }
  }
}
```

### CIMD Application Creation

**POST** `/organizations/{organizationId}/environments/{environmentId}/domains/{domain}/cimd/applications`

Create an application from a CIMD URL. Requires `APPLICATION[CREATE]` permission and a CIMD-enabled domain.

Request body:

```json
{
  "cimdUrl": "https://agents.example.com/.well-known/client-metadata",
  "name": "Hotel Agent",
  "clientName": "Hotel Agent",
  "description": "AI agent for hotel bookings",
  "type": "AGENT"
}
```

### Application Filtering

**GET** `/organizations/{organizationId}/environments/{environmentId}/domains/{domain}/applications`

List applications with optional type filtering. The endpoint accepts a multi-valued `type` filter parameter.

Query parameters:

- `type`: Array of application types (e.g., `type=AGENT`, `type=WEB&type=SERVICE`)
- `page`: Page number (default 0)
- `size`: Page size (default 50)
- `q`: Search query
- `expand`: Array of fields to expand
- `status`: `enabled` or `disabled`
- `owner.email`: Filter by owner email

Example: `GET /applications?type=AGENT` returns only agent applications. `GET /applications?type=WEB&type=SERVICE` returns applications where `type IN (WEB, SERVICE)`.
