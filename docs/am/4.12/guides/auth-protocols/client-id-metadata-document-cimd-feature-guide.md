# Client ID Metadata Document (CIMD) Feature Guide

## Overview

Client ID Metadata Document (CIMD) is an OAuth extension that allows clients to present a URL as their `client_id`. The Authorization Server retrieves a metadata document from that URL and derives the client's configuration dynamically, eliminating the need for pre-registration. CIMD is the preferred client authentication mechanism for AI agents and MCP clients as defined by the Model Context Protocol (MCP) Authentication Specification (November 2025).

## Key Concepts

### CIMD Client Identity

A `client_id` matching the pattern `^https?://` is treated as a CIMD client. The URL serves as both the stable identity anchor and the source of truth for configuration. The `client_id` is normalized to canonical form: scheme and host are lowercased, default ports are removed, and empty paths are preserved. Pre-registered clients take precedence over CIMD clients — if an application is created in Access Management with a `client_id` that matches a remote CIMD resource URL, the pre-registered application's configuration applies.

### Template Application

CIMD requires a template application that defines baseline configuration and restrictions. Valid OAuth settings present in the CIMD metadata are applied to the synthesized client; when omitted, values from the template are used. The template application defines all non-OAuth/OIDC settings (identity provider, metadata, token validity, certificates, MFA) that cannot be specified in CIMD metadata. The template application cannot be deleted or un-templated while CIMD is enabled.

### Metadata Resolution and Caching

When a CIMD client initiates authorization, the gateway checks an in-memory cache for the `client_id`. On cache miss, the gateway fetches the metadata document from the `client_id` URL with configurable timeout and size limits. The metadata is validated for required fields (`client_id`, `redirect_uris`, `token_endpoint_auth_method`) and SSRF protection rules (private IP, HTTP scheme, domain allowlist). The synthesized client is stored in cache with TTL from the `Cache-Control` header or the configured default. JWKS public keys from CIMD metadata are stored in the same in-memory cache as keys for pre-registered clients.

### Configuration Intersection

| Field | Behavior |
|:------|:---------|
| `token_endpoint_auth_method` | Defaults to `none` when omitted in metadata, overriding template value |
| `grant_types` | Defaults to `["authorization_code"]` if absent; intersected with template's authorized grant types |
| `response_types` | Defaults to `["code"]` if absent; intersected with template's response types |
| `scope` | If present, intersected with template's scope settings; if absent, inherits all template scopes |

Values not present in the template are silently dropped.

### Token Revocation on Metadata Change

When enabled, the gateway stores a SHA-256 hash of each CIMD metadata document per domain. On subsequent metadata fetches, if the hash changes, all access tokens, refresh tokens, and scope approvals for the client are revoked. This policy detects changes in remote CIMD metadata only; changes to template application settings do not trigger revocation. The stored hash data persists indefinitely while the policy is enabled and is deleted when disabled.

## Prerequisites

- At least one application must be configured as a template (`template=true`)
- CIMD must be enabled at the domain level (`oidc.cimdSettings.enabled=true`)
- A template application must be selected (`oidc.cimdSettings.templateId`)
- SSRF protection settings must be configured based on security requirements

## Gateway Configuration

### CIMD Settings

| Property | Description | Example |
|:---------|:------------|:--------|
| `oidc.cimdSettings.enabled` | Enable Client ID Metadata Document support | `false` |
| `oidc.cimdSettings.templateId` | Application ID of the template used for CIMD clients (required when enabled) | `app-123` |
| `oidc.cimdSettings.allowPrivateIpAddress` | Allow metadata document requests to private IP addresses | `false` |
| `oidc.cimdSettings.allowUnsecuredHttpUri` | Allow metadata document requests to plain HTTP URIs | `false` |
| `oidc.cimdSettings.fetchTimeoutMs` | Timeout in milliseconds for fetching client metadata documents | `3000` |
| `oidc.cimdSettings.maxResponseSizeKb` | Maximum allowed size of a metadata response in kilobytes | `20` |
| `oidc.cimdSettings.allowedDomains` | Restrict metadata document to these domains (supports wildcard for first-level subdomain); empty list allows all | `["*.example.com", "trusted.org"]` |
| `oidc.cimdSettings.cacheTtlSeconds` | Time-to-live for cached metadata responses in seconds | `3600` |
| `oidc.cimdSettings.cacheMaxEntries` | Maximum number of entries to store in the metadata cache | `500` |
| `oidc.cimdSettings.revokeOnDocumentChange` | Revoke all tokens and consents when metadata document changes | `false` |

### SSRF Protection

Metadata and logo URIs resolving to private, loopback, link-local, or any-local addresses are rejected unless `allowPrivateIpAddress=true`. Plain HTTP URIs are rejected unless `allowUnsecuredHttpUri=true`. If `allowedDomains` is non-empty, only URIs matching the list (with wildcard support for first-level subdomain) are allowed. The `jwks_uri` field in metadata is validated using the same trust rules as `client_id`.

## Authorizing a CIMD Client

A client initiates OAuth authorization with a URL-shaped `client_id` (e.g., `https://example.com/metadata`). The gateway detects the URL pattern and checks if CIMD is enabled. On cache miss, the gateway fetches the metadata document from the `client_id` URL, validates SSRF rules, and parses the JSON. The gateway loads the template application by `templateId`, merges metadata with the template (intersecting `grant_types`, `response_types`, and `scope`), and stores the synthesized client in cache. The gateway validates the `redirect_uri` using exact matching (no prefix matching) and proceeds with the standard OAuth authorization flow. Tokens are issued with the `aud` claim set to the URL-shaped `client_id`.

## End-User Configuration

CIMD clients are configured by publishing a metadata document at the URL specified in the `client_id`. The metadata document must be a JSON object containing at minimum `client_id`, `redirect_uris`, and `token_endpoint_auth_method`. The `client_id` in the metadata must match the requested `client_id`. The `token_endpoint_auth_method` must be `none`, `private_key_jwt`, or `self_signed_tls_client_auth` — secret-based methods are not allowed. If `private_key_jwt` is specified, the metadata must include `jwks` or `jwks_uri`. The `redirect_uris` field must be an array of valid redirect URIs. The gateway validates the `redirect_uri` in authorization requests using exact matching against this list.

## Restrictions

- CIMD clients cannot use secret-based authentication methods (`client_secret_basic`, `client_secret_post`, `client_secret_jwt`)
- CIMD clients always require exact `redirect_uri` matching, even when the domain allows non-strict matching
- Logos are fetched by the gateway and never served directly from remote `logo_uri` values
- Metadata documents larger than `maxResponseSizeKb` are rejected
- Metadata fetch timeout is not configurable per-client
- The template application cannot be deleted or un-templated while CIMD is enabled
- `grant_types`, `response_types`, and `scope` in metadata are intersected with template values; values not in the template are silently dropped
- Revoke-on-change logic requires `revokeOnDocumentChange=true` and only triggers when the metadata document hash changes (not on cache expiry)
- Changes to template application settings do not trigger token revocation
- Pre-registered clients take precedence over CIMD clients when `client_id` values match
- Breaking change: `oidc.cimdSettings.softwareId` has been renamed to `templateId`
