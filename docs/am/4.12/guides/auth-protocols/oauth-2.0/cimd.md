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

## Creating a CIMD-Enabled Domain

1. Navigate to **Settings → OAuth 2.0 → CIMD** in the domain console.

    <figure><img src="../../../.gitbook/assets/am-cimd-settings-overview.png" alt="CIMD settings page showing Enable CIMD toggle and Template Application selector"><figcaption></figcaption></figure>

2. Toggle **Enable CIMD** to enable Client ID Metadata Document support.
3. Select a **Template Application** from the autocomplete dropdown.
4. Add domains to the **Allowed Domains** chip list to restrict metadata fetching to specific domains (supports `*.example.com` wildcard for first-level subdomains; empty list allows all domains).

    <figure><img src="../../../.gitbook/assets/am-cimd-allowed-domains.png" alt="CIMD allowed domains chip list for domain restriction"><figcaption></figcaption></figure>

5. Click **SAVE**.

### CIMD Settings Reference

| Field | Description | Default |
|:------|:------------|:--------|
| **Enable CIMD** | Enable/disable Client ID Metadata Document support | Disabled |
| **Template Application** | Template application for CIMD clients | None (required) |
| **Allow Private/Loopback IP Addresses** | SSRF protection: allow metadata requests to private IPs | Disabled |
| **Allow Unsecured HTTP URIs** | SSRF protection: allow metadata requests to HTTP URIs | Disabled |
| **Fetch Timeout (ms)** | Timeout for metadata fetch | 5000 |
| **Max Response Size (KB)** | Maximum metadata response size | 10 |
| **Allowed Domains** | Restrict metadata to these domains (supports `*.example.com`) | Empty (allow all) |
| **Cache TTL (seconds)** | Metadata cache time-to-live | 86400 |
| **Cache Max Entries** | Maximum cache entries | 1000 |
| **Revoke Tokens and Consents When Client Metadata Changes** | Revoke tokens when metadata hash changes | Disabled |

## CIMD API Reference

### Validate CIMD URL

**POST** `/organizations/{organizationId}/environments/{environmentId}/domains/{domain}/cimd/validate`

Validates a CIMD URL and returns a preview of the parsed metadata.

**Request Body:**

```json
{
  "url": "https://agents.example.com/metadata/hotel-agent"
}
```

**Response:**

```json
{
  "url": "https://agents.example.com/metadata/hotel-agent",
  "hasInlineJwks": true,
  "missing": {
    "clientId": false,
    "clientName": false
  },
  "metadata": {
    "client_id": "https://agents.example.com/metadata/hotel-agent",
    "client_name": "Hotel Agent",
    "redirect_uris": ["https://app.example.com/callback"],
    "grant_types": ["authorization_code"],
    "token_endpoint_auth_method": "private_key_jwt",
    "jwks": { "keys": [...] }
  }
}
```

**Response Fields:**

| Field | Description |
|:------|:------------|
| `url` | The validated CIMD URL |
| `hasInlineJwks` | Whether the metadata contains an inline JWKS |
| `missing.clientId` | Whether `client_id` is missing from the metadata |
| `missing.clientName` | Whether `client_name` is missing from the metadata |
| `metadata` | The parsed CIMD metadata document |

### Create Application from CIMD

**POST** `/organizations/{organizationId}/environments/{environmentId}/domains/{domain}/cimd/applications`

Creates an application from a CIMD URL.

**Request Body:**

```json
{
  "cimdUrl": "https://agents.example.com/metadata/hotel-agent",
  "name": "Hotel Agent",
  "clientName": "Hotel Agent",
  "description": "AI agent for hotel bookings",
  "type": "WEB"
}
```

**Request Fields:**

| Field | Description | Required |
|:------|:------------|:---------|
| `cimdUrl` | CIMD URL to fetch metadata from | Yes |
| `name` | Application name | Yes if `client_name` missing in metadata |
| `clientName` | OAuth client name | No |
| `description` | Application description | No |
| `type` | Application type (WEB, NATIVE, BROWSER, SERVICE, RESOURCE_SERVER) | Yes |


<figure><img src="../../../.gitbook/assets/am-cimd-ssrf-protection.png" alt="CIMD SSRF protection settings"><figcaption></figcaption></figure>

<figure><img src="../../../.gitbook/assets/am-cimd-cache-settings.png" alt="CIMD cache configuration"><figcaption></figcaption></figure>
