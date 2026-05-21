# Client ID Metadata Document (CIMD) Overview

## Overview

Client ID Metadata Document (CIMD) is an OAuth 2.0 extension that allows clients to present a URL as their `client_id` and retrieve configuration dynamically from that URL, eliminating the need for pre-registration. The Authorization Server fetches a JSON metadata document from the URL and synthesizes an ephemeral client configuration, using the URL as both the stable identity anchor and the source of truth. CIMD is the preferred authentication mechanism for AI agents and Model Context Protocol (MCP) clients, enabling agent-driven workflows to authenticate at scale without manual registration.

## Key Concepts

### CIMD Client Recognition

A client is treated as a CIMD client when its `client_id` is a URL starting with `http://` or `https://` (case-insensitive) and containing `://` after the scheme. The URL is canonicalized by lowercasing the scheme and host, omitting default ports (80 for HTTP, 443 for HTTPS), and preserving the path, query, and fragment as-is. Trailing slashes in the path are significant. Pre-registered applications take precedence: if an application exists in Access Management with a `client_id` matching a CIMD URL, the pre-registered configuration applies instead of the remote metadata.

### Template Application

A template application defines the baseline configuration for all CIMD clients in a domain. It must be an existing application with the "Template" flag enabled. The template specifies allowed grant types, response types, scopes, identity providers, token validity, certificates, and MFA settings. CIMD metadata can override OAuth/OIDC client-registration fields (e.g., `redirect_uris`, `jwks_uri`, `logo_uri`) but inherits all other settings from the template. The template application cannot be deleted or un-templated while referenced as the CIMD template.

### Metadata Synthesis

When a CIMD client authenticates, the Authorization Server fetches the JSON metadata document from the `client_id` URL and synthesizes an ephemeral client configuration. Required fields are `client_id` (must match the request URL) and `redirect_uris` (non-empty array). The `token_endpoint_auth_method` defaults to `none` if absent, overriding the template's value. Grant types and response types are intersected with the template's allowed values; if the intersection is empty, the client cannot use any grant or response type. Scopes are intersected with the template's scopes when present in metadata; otherwise, all template scopes are inherited. Secret-based authentication methods and `client_secret` fields are rejected.

| Metadata Field | Synthesis Rule |
|:---------------|:---------------|
| `client_id` | Must match canonical request URL |
| `redirect_uris` | Required; must be non-empty array |
| `token_endpoint_auth_method` | Defaults to `none`; secret-based methods rejected |
| `grant_types` | Intersection of metadata (default `["authorization_code"]`) and template |
| `response_types` | Intersection of metadata (default `["code"]`) and template |
| `scope` | Intersection with template when present; otherwise inherits template scopes |
| `jwks` / `jwks_uri` | Required for `private_key_jwt`; validated against trust rules |
| `logo_uri` | Fetched on-demand; served from cache |

### Metadata Caching and Revocation

Metadata documents are cached in-memory with a configurable TTL (default 3600 seconds) and maximum entry count (default 500). When **Revoke Tokens and Consents When Client Metadata Changes** is enabled, the Authorization Server computes a SHA-256 hash of each metadata document and stores it in the `cimd_client_state` table. On re-fetch, if the hash differs, all access tokens, refresh tokens, and scope approvals for the client are revoked. This policy detects changes in remote CIMD metadata only; changes to the template application do not trigger revocation. Hash data persists indefinitely while the policy is enabled and is deleted when disabled.

## Prerequisites

- An existing application configured as a template (navigate to Domain Settings → Client Registration → Templates, enable "Template" flag, and configure allowed grant types, response types, and scopes)
- A publicly accessible HTTPS endpoint hosting a JSON metadata document (unless **Allow Unsecured HTTP URIs** is enabled)
- The metadata document must include `client_id` (matching the URL) and `redirect_uris` (non-empty array)
