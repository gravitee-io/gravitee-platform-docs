# Client ID Metadata Document (CIMD) Overview

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


Non-OAuth application configurations (identity providers, metadata, token validity, certificates, MFA) can only be defined in the [template application](../applications/).
 The template application cannot be deleted or un-templated while CIMD is enabled.

### Metadata Caching and Change Detection

CIMD metadata documents are cached in-memory with a configurable TTL (default 3600 seconds) and maximum entry count (default 500). When automatic token revocation is enabled, the gateway stores a SHA-256 hash of each metadata document and compares it on subsequent fetches. If the hash changes, all tokens and scope approvals for that client are revoked.

This policy detects changes in remote CIMD metadata only; changes to the template application do not trigger revocation. Stored hashes persist indefinitely while the policy is enabled and are deleted when disabled.

### SSRF Protection

All metadata and logo fetches are subject to Server-Side Request Forgery (SSRF) protection. The gateway validates that URLs do not resolve to private, loopback, link-local, or any-local IP addresses (unless explicitly allowed), enforces HTTPS (unless HTTP is explicitly allowed), restricts requests to allowed domains (when configured), and enforces fetch timeout and maximum response size limits. JWKS URIs declared in metadata are validated with the same SSRF rules.

## Prerequisites

- A template application configured with `template=true` in the domain
- CIMD enabled in domain OIDC settings with a valid `templateId`
- SSRF protection settings configured (`allowPrivateIpAddress`, `allowUnsecuredHttpUri`, `allowedDomains`)
- CIMD clients must host a valid JSON metadata document at their `client_id` URL
