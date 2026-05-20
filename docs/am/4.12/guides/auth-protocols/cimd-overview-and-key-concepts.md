# CIMD Overview and Key Concepts

## Overview

Client ID Metadata Document (CIMD) is an OAuth 2.0 extension that allows clients to present a URL as their `client_id` and retrieve configuration dynamically from that URL, eliminating the need for pre-registration. The Authorization Server fetches a metadata document from the URL and synthesizes the client configuration on-demand, using a template application as the baseline. CIMD is the preferred authentication mechanism for AI agents and Model Context Protocol (MCP) clients, enabling agent-driven workflows to authenticate without manual registration.

## Key Concepts

### CIMD Client Identification

A `client_id` matching the pattern `^https?://` is treated as a CIMD client. The URL serves as both the stable identity anchor and the source of the metadata document. CIMD `client_id` values are normalized to canonical form: scheme and host are lowercased, and default ports (80 for HTTP, 443 for HTTPS) are removed. Pre-registered applications take precedence — if an application exists in Access Management with a `client_id` that is a URL, the pre-registered configuration applies instead of fetching remote metadata.

### Template Application

CIMD clients inherit their baseline configuration from a designated template application. The template defines identity providers, certificates, token validity, MFA settings, and other non-overridable properties. OAuth-specific settings (redirect URIs, authentication methods, grant types, response types, scopes) are overridden or intersected with values from the CIMD metadata document. The template application cannot be deleted or un-templated while referenced as the CIMD template.

### Metadata Document Synthesis

When a CIMD client authenticates, the Authorization Server fetches the metadata document from the `client_id` URL, validates it against SSRF protection rules, and synthesizes a client configuration by cloning the template application and applying metadata overrides. The synthesized client is cached in-memory with a configurable TTL. If the metadata document includes a `logo_uri`, the logo is pre-fetched and cached separately (up to 256 KB). Metadata documents are validated for required fields (`client_id`, `redirect_uris`) and forbidden fields (`client_secret`, `client_secret_expires_at`).

### Token Revocation on Metadata Change

When enabled, the Authorization Server tracks the SHA-256 hash of each CIMD client's metadata document in the `cimd_client_state` database table. On subsequent metadata fetches, if the hash differs, all access tokens, refresh tokens, and scope approvals for that client are revoked. This policy detects changes in remote CIMD metadata only; changes to the template application do not trigger revocation. The stored hash data persists indefinitely while the policy is enabled and is deleted when the policy is disabled.

## Prerequisites

- A template application must be created and marked as a template (`template = true`)
- CIMD must be enabled in domain OIDC settings (`oidc.cimdSettings.enabled = true`)
- The template application ID must be configured as `oidc.cimdSettings.templateId`
- Database support for the `cimd_client_state` table (JDBC) is required if token revocation on metadata change is enabled
