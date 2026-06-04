# Remote URL Import: Concepts and Security

## Overview

API Import from Remote URL enables administrators to create or update v4 APIs by fetching Gravitee API definitions or OpenAPI specifications from remote HTTP(S) endpoints. The Management API server retrieves the definition file server-side. This feature streamlines API lifecycle management when definitions are hosted in version control systems, CDNs, or internal repositories.

## Key Concepts

### Remote Gravitee Definition Import

Gravitee API definitions exported in JSON format can be imported from a remote URL. The Management API fetches the definition file, validates its structure, and creates or updates the API. If an import whitelist is configured, the URL must match it; if no whitelist is set (the default), any HTTP(S) URL is allowed. When private-address blocking is enabled, the URL must not resolve to private, link-local, or loopback addresses (e.g., `http://169.254.169.254/`). The API ID in the path parameter takes precedence over any `api.id` field in the fetched definition body during updates.

### Remote OpenAPI/Swagger Import

OpenAPI and Swagger specifications can be imported from remote URLs by placing the URL in the `payload` field of the `ImportSwaggerDescriptor`. The backend detects a remote import by inspecting the `payload`: when it is a valid HTTP(S) URL, the specification is fetched server-side; otherwise the `payload` is treated as inline specification content. The Console sets the descriptor's `type` field to `URL` for remote imports, but the field is advisory — the `payload` content determines the behavior. Remote fetches apply the same whitelist and SSRF protection rules as Gravitee definition imports.

### SSRF Protection

All remote URL imports enforce Server-Side Request Forgery (SSRF) protection. Before fetching, the backend validates each URL: if an import whitelist is configured, the URL must match an allowed entry. When private-address blocking is enabled, URLs resolving to private, link-local, or loopback addresses are rejected with a `400 Bad Request` error. This prevents attackers from using the import feature to probe internal network resources.

## Prerequisites

Before importing APIs from remote URLs, ensure the following requirements are met:

* **v4 API support**: Remote URL import is available only for v4 APIs. v2 APIs are not supported.
* **Import restrictions (optional)**: By default, no import whitelist is configured and private-address blocking is disabled (`imports.allow-from-private` defaults to `true`), so any reachable HTTP(S) URL can be imported. To restrict this, configure an import whitelist (remote URLs must then match at least one whitelist entry) and/or enable private-address blocking.
* **Network reachability**: The Management API server must be able to reach the remote URL over HTTP(S). CORS restrictions do not apply because the fetch occurs server-side.
* **Permissions**: Users must hold `ENVIRONMENT_API[CREATE]` permission to create APIs from remote URLs, or `API_DEFINITION[UPDATE]` permission to update existing APIs.
