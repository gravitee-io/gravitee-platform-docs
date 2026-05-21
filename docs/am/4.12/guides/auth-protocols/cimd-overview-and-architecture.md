# CIMD Overview and Architecture

## Overview

Client ID Metadata Document (CIMD) is an OAuth 2.0 extension that allows clients to present a URL as their `client_id` and retrieve configuration dynamically from a metadata document hosted at that URL, eliminating the need for pre-registration. The Authorization Server fetches the metadata on-demand, validates it against a template application, and synthesizes an ephemeral client configuration. CIMD is the preferred authentication mechanism for AI agents and Model Context Protocol (MCP) clients, enabling agent-driven workflows to authenticate at scale without manual registration.

{% hint style="info" %}
CIMD is an Access Management feature and does not apply to API Management.
{% endhint %}

## Key Concepts

### CIMD Client Identity

A `client_id` is recognized as a CIMD client if it matches the pattern `^https?://`. The URL serves as both the stable identity anchor and the source of the metadata document. CIMD client IDs are canonicalized: scheme and host are lowercased, default ports are removed, and fragments are stripped. Pre-registered applications take precedence — if an application exists in Access Management with a `client_id` matching a CIMD URL, the pre-registered configuration applies instead of the remote metadata.

### Template Application

CIMD requires a template application to define baseline configuration and constraints. The template is a standard application marked as `template = true` and referenced in the domain's CIMD settings. CIMD metadata inherits settings from the template (identity providers, token validity, certificates, MFA) and intersects OAuth-specific parameters (grant types, response types, scopes). A template application in use as the CIMD template cannot be deleted or un-templated.

### Metadata Document

The metadata document is a JSON resource hosted at the `client_id` URL. It must include `client_id` (matching the request URL in canonical form) and `redirect_uris`. Optional fields include `token_endpoint_auth_method` (defaults to `none`), `grant_types` (defaults to `["authorization_code"]`), `response_types` (defaults to `["code"]`), `scope`, `jwks`, `jwks_uri`, `logo_uri`, and standard OAuth client metadata fields. Secret-based authentication methods (`client_secret_basic`, `client_secret_post`, `client_secret_jwt`) are forbidden. The `token_endpoint_auth_method` from metadata overrides the template value; `grant_types`, `response_types`, and `scope` are intersected with the template's allowed values.

### SSRF Protection

CIMD enforces Server-Side Request Forgery (SSRF) protection for metadata and logo URIs. By default, requests to private, loopback, link-local, or any-local IP addresses are blocked, and plain HTTP URIs are rejected (HTTPS required). Administrators can configure allowed domains (supporting wildcard for first-level subdomains, e.g., `*.example.com`), fetch timeout, and maximum response size. JWKS URIs referenced in metadata are subject to the same validation rules.

### Token Revocation on Metadata Change

When enabled, the gateway computes a SHA-256 hash of each CIMD metadata document and stores it in the `cimd_client_state` table. On subsequent fetches, if the hash changes, all access tokens, refresh tokens, and scope approvals for that client are revoked. This policy detects changes in remote metadata only; changes to the template application do not trigger revocation. The stored hash persists indefinitely while the policy is enabled and is deleted when the policy is disabled.

### CIMD Logo Endpoint

The gateway provides a logo endpoint (`GET /{domain}/cimd/logo?clientId={url-encoded-client-id}`) that serves pre-fetched or on-demand fetched logos from the in-memory cache. If the logo is cached, it is returned immediately with `Content-Type` and `Cache-Control` headers. If the logo is not cached but the metadata is valid and includes a `logo_uri`, the gateway fetches the logo synchronously and caches it. If no logo is available, the endpoint returns `404 Not Found`.
