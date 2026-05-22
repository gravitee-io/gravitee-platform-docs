# Client ID Metadata Document (CIMD) Overview

## Overview

Client ID Metadata Document (CIMD) is an OAuth 2.0 extension that allows clients to present a URL as their `client_id` and retrieve configuration dynamically from that URL, eliminating the need for pre-registration. The Authorization Server fetches a metadata document from the client ID URL and derives the client's configuration on-demand. CIMD is the preferred authentication mechanism for AI agents and Model Context Protocol (MCP) clients, enabling agent-driven workflows at scale.

## Key Concepts

### URL-Based Client Identity

A `client_id` matching the pattern `^https?://` is treated as a CIMD client. The URL serves as both the stable identity anchor and the source of truth for configuration. The `client_id` is normalized to canonical form: scheme and host are lowercased, and default ports (80 for HTTP, 443 for HTTPS) are removed. When a CIMD client authenticates, the Authorization Server fetches the metadata document from the canonical URL, validates it, and synthesizes an ephemeral client object.

### Template Application

CIMD clients inherit configuration from a designated template application. The template defines baseline settings such as identity providers, multi-factor authentication, token validity, and certificates. OAuth settings present in the CIMD metadata document override template values, except for `grant_types`, `response_types`, and `scope`, which are intersected with the template's allowed values. If the metadata omits a setting, the template value applies. The `token_endpoint_auth_method` defaults to `none` when omitted in metadata, regardless of the template value.

### Metadata Caching and Revocation

Metadata documents are cached in-memory for a configurable time-to-live (default 3600 seconds). When the **Revoke Tokens and Consents When Client Metadata Changes** policy is enabled, the Authorization Server computes a SHA-256 hash of each metadata document and stores it in the `cimd_client_state` table. On subsequent fetches, if the hash differs, all access tokens, refresh tokens, and scope approvals for the client are revoked. This policy detects changes in remote CIMD metadata only; changes to the template application do not trigger revocation.

| Component | Description |
|:----------|:------------|
| **Metadata Cache** | In-memory cache storing fetched metadata documents, keyed by canonical `client_id`. Not shared across gateway instances. |
| **Logo Cache** | Separate in-memory cache storing logos fetched from `logo_uri` in metadata. Shares the same TTL as metadata cache. |
| **Client State Table** | Database table (`cimd_client_state`) storing metadata document hashes for revoke-on-change tracking. Persists indefinitely while the policy is enabled. |

### SSRF Protection

CIMD metadata and logo fetching apply Server-Side Request Forgery (SSRF) protection. By default, requests to private IP addresses (RFC 1918), loopback addresses (127.0.0.0/8, ::1), link-local addresses (169.254.0.0/16, fe80::/10), and any-local addresses (0.0.0.0, ::) are rejected. Plain HTTP URIs are rejected unless explicitly allowed. Administrators can restrict metadata fetching to specific domains using a wildcard-enabled allowlist (e.g., `*.example.com` for first-level subdomains). DNS resolution is validated to ensure the host does not resolve to a private IP unless overridden.

## Prerequisites

- Access Management 4.6 or later
- A template application configured with baseline OAuth settings (grant types, response types, scopes, identity providers, MFA policies)
- Domain-level permission `domain_openid_read` to configure CIMD settings
- HTTPS-accessible metadata document endpoint for each CIMD client (or HTTP if `allowUnsecuredHttpUri` is enabled)
