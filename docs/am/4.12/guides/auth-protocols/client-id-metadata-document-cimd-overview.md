# Client ID Metadata Document (CIMD) Overview

## Overview

Client ID Metadata Document (CIMD) is an OAuth extension that allows clients to use a URL as their `client_id` and present their configuration dynamically via a metadata document hosted at that URL. Instead of pre-registering with the authorization server, CIMD clients are authenticated and configured on-demand by fetching and validating their metadata. This feature is essential for modern agentic architectures, including AI agents and Model Context Protocol (MCP) clients, where pre-registration is impractical at scale.

## Key Concepts

### CIMD Client Identity

A CIMD client is identified by a URL-shaped `client_id` (matching `^https?://`). The URL serves as both the stable identity anchor and the source of the client's OAuth configuration. When a CIMD client initiates an OAuth flow, Gravitee Access Management fetches the metadata document from the `client_id` URL, validates it, and synthesizes an ephemeral client configuration. The `client_id` is normalized to canonical form: scheme and host are lowercased, and default ports are removed.

### Template Application

CIMD clients inherit configuration from a designated template application. The template defines allowed grant types, response types, scopes, identity providers, token validity, certificates, and MFA settings. CIMD metadata can only specify OAuth/OIDC client-registration fields; all other application settings (identity provider, metadata, token validity, certificates, MFA) are inherited from the template. Valid OAuth settings in the metadata override template defaults, except for:

* `token_endpoint_auth_method`: Defaults to `none` when omitted in metadata
* `grant_types`: Intersected with template's allowed grant types (metadata defaults to `["authorization_code"]`)
* `response_types`: Intersected with template's allowed response types (metadata defaults to `["code"]`)
* `scope`: Intersected with template's scopes when present in metadata; otherwise uses template scopes verbatim

### Metadata Caching and Revocation

Metadata documents are cached in-memory with a configurable TTL. When the **Revoke Tokens And Consents When Client Metadata Changes** setting is enabled, Gravitee stores a SHA-256 hash of each CIMD client's metadata document. If the hash changes on a subsequent fetch, all access tokens, refresh tokens, and scope approvals for that client are revoked. This policy detects changes in remote CIMD metadata only; changes to the template application do not trigger revocation. The stored hash data persists per domain and data plane while the policy is enabled and is deleted when disabled.

### SSRF Protection

CIMD metadata fetching includes Server-Side Request Forgery (SSRF) protection. By default, requests to private, loopback, link-local, and any-local IP addresses are rejected. HTTP (non-HTTPS) URIs are also rejected unless explicitly allowed. Administrators can restrict metadata fetching to specific domains using wildcard patterns (e.g., `*.example.com` matches first-level subdomains only). DNS resolution is validated to ensure the host does not resolve to a private IP unless private addresses are explicitly allowed.

## Prerequisites

Before enabling CIMD, complete the following steps:

* Mark at least one application as a template (`template=true`)
* Define allowed grant types, response types, and scopes in the template application
* Ensure CIMD clients host a valid metadata document at the `client_id` URL
* Ensure metadata documents are accessible via HTTPS (or HTTP if `allowUnsecuredHttpUri` is enabled)

## Gateway Configuration

Configure CIMD settings in `gravitee.yml`:

| Property | Description | Default |
|:---------|:------------|:--------|
| `oidc.cimdSettings.enabled` | Enable Client ID Metadata Document support | `false` |
| `oidc.cimdSettings.templateId` | Application ID of the template used for CIMD clients (required when enabled) | — |
| `oidc.cimdSettings.allowPrivateIpAddress` | Allow metadata document requests to private, loopback, and link-local IP addresses | `false` |
| `oidc.cimdSettings.allowUnsecuredHttpUri` | Allow metadata document requests to plain HTTP (non-HTTPS) URIs | `false` |
| `oidc.cimdSettings.fetchTimeoutMs` | Timeout in milliseconds for fetching client metadata documents | `3000` |
| `oidc.cimdSettings.maxResponseSizeKb` | Maximum allowed size of a metadata response in kilobytes | `20` |
| `oidc.cimdSettings.allowedDomains` | Restrict metadata document to these domains (supports wildcard for first-level subdomain). Empty list allows all domains | `[]` |
| `oidc.cimdSettings.cacheTtlSeconds` | Time-to-live for cached metadata responses in seconds | `3600` |
| `oidc.cimdSettings.cacheMaxEntries` | Maximum number of entries to store in the metadata cache | `500` |
| `oidc.cimdSettings.revokeOnDocumentChange` | Revoke all tokens and consents when CIMD metadata document changes | `false` |
