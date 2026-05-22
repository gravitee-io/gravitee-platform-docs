# Client ID Metadata Document (CIMD) Overview

## Overview

Client ID Metadata Document (CIMD) is an OAuth extension that allows clients to present a URL as their `client_id`. Instead of pre-registering, the Authorization Server retrieves a metadata document from that URL and derives the client's configuration dynamically. CIMD is the preferred authentication mechanism for AI agents and Model Context Protocol (MCP) clients, enabling agent-driven workflows without pre-registration.

Ensure the domain has [`domain_openid_read` and `domain_openid_update` permissions](../../guides/administration.md) for CIMD settings management.

## Key Concepts

### CIMD Client Identity

A client is identified as a CIMD client when its `client_id` matches the pattern `^https?://`. The URL serves as both the stable identity anchor and the source of truth for configuration. The `client_id` is normalized to canonical form: scheme and host are lowercased, and default ports are removed. Pre-registered clients take precedence over CIMD clients — if an application is created in Access Management with a `client_id` that is also a remote CIMD resource URL, the pre-registered application's configuration applies.

### Template Application

CIMD clients inherit configuration from a designated template application. The template defines identity providers, MFA settings, token validity, certificates, and other application-level settings that cannot be specified in the metadata document. Valid OAuth settings present in the metadata document are applied to the synthesized client; when omitted, values from the template are used. Template applications are marked with a "CIMD Template" badge and cannot be deleted or un-templated while referenced as the CIMD template.

### Metadata Document Validation

The metadata document is fetched from the `client_id` URL and validated against OAuth client registration rules. The document must include `client_id` (matching the request URL exactly), `redirect_uris` (non-empty array), and cannot contain `client_secret` or `client_secret_expires_at`. The `token_endpoint_auth_method` defaults to `none` when omitted and overrides the template value; secret-based methods (`client_secret_basic`, `client_secret_post`, `client_secret_jwt`) are forbidden. Grant types default to `["authorization_code"]` and are intersected with the template's allowed grant types. Response types default to `["code"]` and are intersected with the template's allowed response types. Scopes are intersected with the template's scope settings when present in metadata; otherwise, template scopes are used verbatim. When `token_endpoint_auth_method` is `private_key_jwt`, the document must include `jwks` or `jwks_uri`.

### SSRF Protection

Metadata document requests are protected against Server-Side Request Forgery (SSRF) attacks. Private, loopback, link-local, and any-local IP addresses are rejected unless **Allow Private/Loopback IP Addresses** is enabled. HTTP (non-HTTPS) URIs are rejected unless **Allow Unsecured HTTP URIs** is enabled. If **Allowed Domains** is configured, the host must match one of the specified domains (supports `*.example.com` for first-level subdomain wildcards). DNS resolution is validated to ensure the host does not resolve to a private IP unless explicitly allowed. The same protection applies to `jwks_uri` and `logo_uri` fetches.

### Metadata Caching

Fetched metadata documents are cached in memory with a configurable time-to-live (default 3600 seconds) and maximum entry count (default 500). Cache eviction is LRU-based. JWKS public keys presented in CIMD metadata are stored in the same in-memory cache as keys for pre-registered clients, using the gateway's standard JWKS cache settings. Metadata fetch retries up to 3 times with 100ms delay between attempts.

### Token Revocation on Metadata Change

When **Revoke Tokens and Consents When Client Metadata Changes** is enabled, the gateway computes a SHA-256 hash of each metadata document and stores it in the `cimd_client_state` table. On subsequent fetches, if the hash differs, all access tokens, refresh tokens, and scope approvals for the client are revoked, and the new hash is stored. This policy detects changes in remote CIMD metadata only; changes to template application settings do not trigger revocation. The stored hash data persists indefinitely while the policy is enabled and is deleted when the policy is disabled. Storage impact may be relevant for environments managing a large volume of CIMD clients.
