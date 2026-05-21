# CIMD Feature Overview and Key Concepts

## Overview

Client ID Metadata Document (CIMD) is an OAuth extension that allows clients to use a URL as their `client_id` and present their configuration dynamically via a metadata document hosted at that URL, eliminating the need for pre-registration. Adopted by the Model Context Protocol (MCP) Authentication Specification in November 2025, CIMD is the preferred authentication mechanism for AI agents and MCP clients. This feature enables API platform administrators to support agent-driven workflows at scale without manual client onboarding.

## Key Concepts

### CIMD Client

A CIMD client is identified by a `client_id` that matches the pattern `^https?://`. When such a client authenticates, the Authorization Server fetches a metadata document from the `client_id` URL and synthesizes an ephemeral client configuration. Pre-registered applications take precedence: if an application exists in Access Management with a `client_id` matching a CIMD URL, the pre-registered configuration applies instead of the remote metadata.

### Template Application

A template application defines the baseline configuration for all CIMD clients in a domain. Valid OAuth settings from the CIMD metadata document are applied to the synthesized client; when omitted, values from the template application are used. The template application cannot be deleted or un-templated while it is the active CIMD template. Template-only settings (identity providers, MFA, token validity, certificates) apply to all CIMD clients and cannot be overridden by metadata.

| Setting | Metadata Behavior | Template Fallback |
|:--------|:------------------|:------------------|
| `token_endpoint_auth_method` | Defaults to `none` when omitted; overrides template | Template value ignored |
| `grant_types` | Intersected with template's allowed grant types | Template grant types if metadata omits field |
| `response_types` | Intersected with template's allowed response types | Template response types if metadata omits field |
| `scope` | Intersected with template scopes when present | Template scopes used verbatim if metadata omits field |
| Identity providers, MFA, certificates | Not configurable via metadata | Template values always apply |

### Metadata Document Cache

Metadata documents and JWKS public keys are cached in-memory to reduce latency and external requests. Cache entries expire after the configured TTL. Logo URIs referenced in metadata are fetched on-demand and cached separately. The cache does not persist across gateway restarts.

### Token Revocation on Metadata Change

When enabled, Access Management tracks a SHA-256 hash of each CIMD client's metadata document. If the hash changes (indicating updated configuration), all access tokens, refresh tokens, and scope approvals for that client are revoked. This policy detects changes in remote CIMD metadata only; changes to the template application do not trigger revocation. Hash data persists indefinitely while the policy is enabled and is deleted when disabled.

## Prerequisites

- A domain with OAuth 2.0 enabled
- At least one application configured as a template (`template = true`)
- `domain_openid_read` permission to view CIMD settings
- `domain_openid_update` permission to modify CIMD settings
