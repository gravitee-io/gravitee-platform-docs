# Client ID Metadata Document (CIMD) Overview

## Overview

Client ID Metadata Document (CIMD) is an OAuth extension that allows clients to use a URL as their `client_id` and provide configuration dynamically via a metadata document hosted at that URL. Instead of pre-registering with the authorization server, clients present a URL-shaped identifier, and the gateway retrieves and validates their configuration on-demand. CIMD is the preferred authentication mechanism for AI agents and Model Context Protocol (MCP) clients, enabling agent-driven workflows without pre-registration overhead.

## Key Concepts

### URL-Shaped Client Identifiers

CIMD clients use HTTP(S) URLs as their `client_id` (e.g., `https://client.example.com/metadata`). The gateway detects URL-shaped identifiers (matching `^https?://`), normalizes them to canonical form (lowercased scheme and host, default ports removed, fragment stripped), and fetches metadata from the URL. Pre-registered applications take precedence: if an application exists in the Management Console with a `client_id` matching a CIMD URL, the pre-registered configuration applies instead of the remote metadata.

### Template Applications

CIMD clients inherit default settings from a designated template application. The template defines baseline configuration (grant types, response types, scopes, identity providers, MFA settings, token validity, certificates) that applies when metadata omits optional fields. Valid OAuth settings in the metadata override template values, except for:

* `token_endpoint_auth_method`: defaults to `none` when omitted
* `grant_types`: intersected with template
* `response_types`: intersected with template
* `scope`: intersected with template when present; otherwise uses template scopes verbatim

Template applications cannot be deleted or un-templated while referenced in CIMD settings.

### Metadata Caching and Revocation

Metadata documents are cached in-memory (TTL and max entries configurable) and persisted to the database for cross-gateway consistency. The gateway computes a SHA-256 hash of each metadata document and stores it in the `cimd_client_state` table. When "Revoke tokens and consents when client metadata changes" is enabled, the gateway compares hashes on each fetch; if the hash changes, all access tokens, refresh tokens, and scope approvals for that `client_id` are revoked. This policy detects changes in remote CIMD metadata only — changes to template application settings do not trigger revocation. Hash data persists indefinitely while the policy is enabled and is deleted when disabled.

### SSRF Protection

The gateway applies Server-Side Request Forgery (SSRF) protection to all metadata and logo URIs. By default, only HTTPS URIs are allowed, and requests to private IP addresses (RFC 1918, loopback, link-local, any-local) are rejected. Administrators can relax these restrictions via `allowPrivateIpAddress` and `allowUnsecuredHttpUri` settings. The `allowedDomains` list restricts metadata requests to specific domains (supports `*.example.com` for first-level subdomain wildcard). DNS resolution is validated to ensure hosts do not resolve to private addresses unless explicitly allowed.

### Ephemeral Clients

CIMD clients are not persisted in the `applications` table. They exist only in cache and are synthesized on-demand from metadata and template configuration. CIMD clients do not appear in the Management Console's application list and cannot be managed via the Applications UI. Audit logs include a `metadataDocumentHash` attribute for CIMD clients and do not link to application detail pages.

## Prerequisites

* A template application must be created and marked as "Template" in **Domain Settings → Client Registration → Templates**
* The template application must define baseline OAuth settings (grant types, response types, scopes)
* CIMD metadata documents must be hosted at publicly accessible HTTPS URLs (or within `allowedDomains` if configured)
* For `private_key_jwt` authentication, metadata must include `jwks` or `jwks_uri`

## Gateway Configuration

CIMD settings are configured in `gravitee.yml`:

| Property | Description | Example |
|:---------|:------------|:--------|
| `oidc.cimdSettings.enabled` | Enable Client ID Metadata Document support | `false` |
| `oidc.cimdSettings.templateId` | Application ID of the template used for CIMD clients (required when enabled) | `"app-template-001"` |
| `oidc.cimdSettings.allowPrivateIpAddress` | Allow metadata document requests to private IP addresses | `false` |
| `oidc.cimdSettings.allowUnsecuredHttpUri` | Allow metadata document requests to plain HTTP URIs | `false` |
| `oidc.cimdSettings.fetchTimeoutMs` | Timeout in milliseconds for fetching client metadata documents (must be > 0) | `3000` |
| `oidc.cimdSettings.maxResponseSizeKb` | Maximum allowed size of a metadata response in kilobytes (must be > 0) | `20` |
| `oidc.cimdSettings.allowedDomains` | Restrict metadata document to these domains (supports `*.example.com`; empty = allow all) | `["*.example.com", "trusted.org"]` |
| `oidc.cimdSettings.cacheTtlSeconds` | Time-to-live for cached metadata responses in seconds (must be > 0) | `3600` |
| `oidc.cimdSettings.cacheMaxEntries` | Maximum number of entries to store in the metadata cache (must be > 0) | `500` |
| `oidc.cimdSettings.revokeOnDocumentChange` | Revoke all tokens and consents when CIMD metadata document changes | `false` |

JWKS public keys from CIMD metadata are stored in the in-memory cache alongside keys for pre-registered clients. Cache settings are configured in `gravitee.yml`.
