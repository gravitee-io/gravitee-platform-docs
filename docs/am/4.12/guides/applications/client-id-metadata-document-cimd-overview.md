# Client ID Metadata Document (CIMD) Overview

## Overview

Client ID Metadata Document (CIMD) is an OAuth extension that allows clients to use a URL as their `client_id` and provide configuration dynamically via a metadata document hosted at that URL, eliminating the need for pre-registration. Gravitee Access Management retrieves and validates the metadata document on first use, then caches it for subsequent requests. CIMD is the preferred authentication mechanism for AI agents and Model Context Protocol (MCP) clients, enabling agent-driven workflows to authenticate without manual registration.

## Key Concepts

### CIMD Client Identification

A `client_id` is treated as a CIMD client when it matches the pattern `^https?://` (case-insensitive) and CIMD is enabled for the domain. The URL serves as both the stable identity anchor and the source of the client's configuration. Pre-registered applications take precedence: if an application exists in Access Management with a `client_id` matching a CIMD URL, the pre-registered configuration applies instead of the remote metadata.

### Template Application Inheritance

CIMD clients inherit configuration from a designated template application. Valid OAuth settings present in the CIMD metadata are applied to the synthesized client; when omitted, values from the template are used.

- **Grant Types** become the intersection of metadata `grant_types` (default `["authorization_code"]`) and the template's authorized grant types.
- **Response Types** become the intersection of metadata `response_types` (default `["code"]`) and the template's response types.
- **Scopes** become the intersection of metadata `scope` (space-separated) and the template's scope settings when present in metadata; otherwise, template scopes are used verbatim.
- **Token Endpoint Auth Method** defaults to `none` when omitted in metadata, overriding the template value.

Other application settings (identity providers, metadata, token validity, certificates, MFA) are defined exclusively in the template application.

### Metadata Caching and Revocation

The gateway fetches the metadata document from the `client_id` URL on first authorization request and caches it for the configured TTL (default 3600 seconds). Subsequent requests use the cached metadata until expiry.

When **Revoke Tokens and Consents When Client Metadata Changes** is enabled, the gateway stores a SHA-256 hash of each CIMD metadata document and compares it on cache refresh. If the hash changes, all tokens and consents for that client are revoked. This stored hash data persists indefinitely while the policy is enabled and is deleted when disabled. The policy detects changes in remote CIMD metadata only; changes to template application settings do not trigger revocation.

### SSRF Protection

By default, the gateway rejects metadata document URLs that resolve to private, loopback, link-local, or any-local IP addresses. This protection applies to metadata documents, `logo_uri`, and `jwks_uri` fetches. Only HTTPS URLs are allowed unless **Allow Unsecured HTTP URIs** is enabled. Administrators can relax these restrictions via **Allow Private/Loopback IP Addresses** and **Allow Unsecured HTTP URIs** toggles.

### JWKS Key Storage

JWKS public keys presented in CIMD metadata are stored in the in-memory cache alongside keys for pre-registered clients. Cache configuration is managed via `gravitee.yml` settings. Storage impact may be relevant for environments managing a large volume of CIMD clients.

## Prerequisites

- A template application must be created and configured with the `template` flag enabled
- The template application must define the baseline OAuth settings (grant types, response types, scopes) that CIMD clients will inherit
- CIMD must be enabled at the domain level and the template application ID must be specified in **Template Application**
- For production use, CIMD metadata documents, `logo_uri`, and `jwks_uri` should be served over HTTPS
