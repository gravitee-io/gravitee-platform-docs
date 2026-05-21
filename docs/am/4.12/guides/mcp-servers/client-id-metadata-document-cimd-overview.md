# Client ID Metadata Document (CIMD) Overview

## Overview

Client ID Metadata Document (CIMD) is an OAuth extension that allows clients to present a URL as their `client_id`. Instead of pre-registering, the Authorization Server retrieves a metadata document from that URL and derives the client's configuration dynamically. CIMD is the preferred authentication mechanism for AI agents and Model Context Protocol (MCP) clients, enabling agent-driven workflows to authenticate without pre-registration.

## Key Concepts

### CIMD Client Identification

A `client_id` is treated as a CIMD client when it matches the pattern `^https?://` (case-insensitive) and the domain's CIMD support is enabled. The URL serves as both the stable identity anchor and the source of truth for configuration. Pre-registered applications take precedence: if an application exists in Access Management with a `client_id` matching a CIMD URL, the pre-registered configuration applies instead of the remote metadata.

### Template Application

CIMD clients inherit settings from a designated template application. The template defines identity providers, token validity, certificates, MFA policies, and other application-level configurations that can't be specified in CIMD metadata. Valid OAuth settings present in the metadata are applied to the synthesized client; when omitted, values from the template are used. The template application can't be deleted or have its template flag removed while referenced by CIMD settings.

### Metadata Synthesis

When a CIMD client authenticates, the gateway fetches its metadata document and synthesizes an ephemeral client configuration. **Token Endpoint Auth Method** defaults to `none` when omitted in metadata, overriding the template value. **Grant Types** become the intersection of metadata (default `authorization_code`) and the template's authorized grant types. **Response Types** become the intersection of metadata (default `code`) and the template's response types. **Scope** becomes the intersection of metadata and template scopes when present in metadata; otherwise uses template scopes verbatim. Metadata is cached for the configured TTL; clients aren't persisted in the applications table.

### SSRF Protection

Metadata and logo fetches enforce Server-Side Request Forgery (SSRF) protection. The gateway resolves hostnames to IP addresses and rejects requests to private, loopback, link-local, or any-local ranges (including AWS IMDS `169.254.169.254`) unless explicitly allowed. Plain HTTP URIs are rejected unless unsecured HTTP is enabled. An optional domain allowlist restricts metadata sources to specific domains (supports first-level subdomain wildcards like `*.example.com`). Fetch timeout and maximum response size limits apply to all requests.

| Protected Range | Description |
|:----------------|:------------|
| `10.0.0.0/8`, `172.16.0.0/12`, `192.168.0.0/16` | Private IPv4 |
| `169.254.0.0/16` | Link-local (includes AWS IMDS) |
| `127.0.0.0/8` | Loopback IPv4 |
| `::1` | Loopback IPv6 |
| `fe80::/10` | Link-local IPv6 |
| `fc00::/7` | Unique-local IPv6 |

### Token Revocation on Metadata Change

When enabled, the gateway computes a SHA-256 hash of each fetched metadata document and stores it in the `cimd_client_state` table. On subsequent fetches, if the hash differs, all access tokens, refresh tokens, and scope approvals for that `client_id` are revoked. This policy detects changes in remote CIMD metadata only; changes to template application settings don't trigger revocation. The stored hash is a lightweight thumbprint that persists indefinitely while the policy is enabled and is deleted when disabled.

## Prerequisites

- Access Management domain with OIDC provider enabled
- At least one application configured as a template (template flag enabled)
- Network access to CIMD metadata URLs (subject to SSRF protection rules)
- For [`private_key_jwt` authentication](#supported-authentication-methods): CIMD metadata must include `jwks` or `jwks_uri`

## Gateway Configuration

| Property | Description | Example |
|:---------|:------------|:--------|
| `oidc.cimdSettings.enabled` | Enable Client ID Metadata Document support | `false` |
| `oidc.cimdSettings.templateId` | Application ID of the template used for CIMD clients (required when enabled) | `a1b2c3d4-...` |
| `oidc.cimdSettings.allowPrivateIpAddress` | Allow metadata requests to private IP addresses | `false` |
| `oidc.cimdSettings.allowUnsecuredHttpUri` | Allow metadata requests to plain HTTP URIs | `false` |
| `oidc.cimdSettings.fetchTimeoutMs` | Timeout in milliseconds for fetching metadata documents (must be > 0) | `3000` |
| `oidc.cimdSettings.maxResponseSizeKb` | Maximum allowed size of metadata response in kilobytes (must be > 0) | `20` |
| `oidc.cimdSettings.allowedDomains` | Restrict metadata sources to these domains (supports `*.example.com`). Empty list allows all domains | `["*.example.com", "trusted.org"]` |
| `oidc.cimdSettings.cacheTtlSeconds` | Time-to-live for cached metadata responses in seconds (must be > 0) | `3600` |
| `oidc.cimdSettings.cacheMaxEntries` | Maximum number of entries in the metadata cache (must be > 0) | `500` |
| `oidc.cimdSettings.revokeOnDocumentChange` | Revoke all tokens when CIMD metadata document changes | `false` |
