# Client ID Metadata Document (CIMD) Overview

## Overview

Client ID Metadata Document (CIMD) is an OAuth extension that allows clients to present a URL as their `client_id`. Instead of pre-registering, the Authorization Server retrieves a metadata document from that URL and derives the client's configuration dynamically. CIMD is the preferred authentication mechanism for AI agents and Model Context Protocol (MCP) clients, enabling agent-driven workflows without pre-registration.

## Key Concepts

### URL-Shaped Client Identity

A `client_id` matching the pattern `^https?://` is treated as a CIMD client. The URL serves as both the stable identity anchor and the source of truth for configuration. The gateway normalizes the `client_id` to canonical form (scheme and host lowercased, default ports removed) and fetches a JSON metadata document from that URL. Pre-registered clients take precedence: if an application exists in Access Management with a `client_id` that matches a CIMD URL, the pre-registered configuration applies instead of the remote metadata.

### Template Application

CIMD clients inherit configuration from a designated template application. The template defines identity providers, MFA settings, token validity, certificates, and other application-level settings that cannot be specified in the metadata document. OAuth-specific settings (`grant_types`, `response_types`, `scope`) are intersected with the metadata: only values present in both the template and the metadata are applied to the synthesized client.

| Metadata Field | Behavior |
|:---------------|:---------|
| `token_endpoint_auth_method` | Defaults to `none` when omitted; overrides template value |
| `grant_types` | Defaults to `["authorization_code"]` when omitted; intersected with template's authorized grant types |
| `response_types` | Defaults to `["code"]` when omitted; intersected with template's response types |
| `scope` | Intersected with template's scope settings when present; uses template scopes verbatim when omitted |
| Other OAuth settings | Applied from metadata when present; falls back to template when omitted |

### Metadata Caching and Revocation

The gateway caches metadata documents in memory for a configurable TTL (default 3600 seconds). When automatic revocation is enabled, the gateway stores a SHA-256 hash of each metadata document. If the hash changes on a subsequent fetch, all access tokens, refresh tokens, and scope approvals for that client are revoked. This policy detects changes in remote CIMD metadata only; changes to the template application do not trigger revocation. The stored hash data persists indefinitely while the policy is enabled and is deleted when disabled.

## Prerequisites

- A template application configured with `template=true` in Client Registration settings (see [Client Registration settings](../applications/README.md#register-new-client-using-templates))
- CIMD enabled in domain OAuth 2.0 settings with a valid `templateId`
- For `private_key_jwt` authentication: CIMD metadata must include `jwks` or `jwks_uri`
- For `jwks_uri` validation: the URI host must pass SSRF validation (allowed domains, private IP checks)
