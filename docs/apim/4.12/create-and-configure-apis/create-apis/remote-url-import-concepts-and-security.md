# Remote URL Import: Concepts and Security

## Overview

API Import from Remote URL enables administrators to create or update v4 APIs by fetching Gravitee API definitions or OpenAPI specifications from remote HTTP(S) endpoints. The Management API server retrieves the definition file server-side, enforcing URL whitelist and SSRF protection rules. This feature streamlines API lifecycle management when definitions are hosted in version control systems, CDNs, or internal repositories.

## Key Concepts

### Remote Gravitee Definition Import

Gravitee API definitions exported in JSON format can be imported from a remote URL. The Management API fetches the definition file, validates its structure, and creates or updates the API. The URL must be permitted by the configured import whitelist and, if private-address blocking is enabled, must not resolve to internal or link-local addresses (e.g., `http://169.254.169.254/`). The API ID in the path parameter takes precedence over any `api.id` field in the fetched definition body during updates.

### Remote OpenAPI/Swagger Import

OpenAPI and Swagger specifications can be imported from remote URLs by setting the `type` field to `URL` in the `ImportSwaggerDescriptor` payload. The backend fetches the specification server-side and applies the same whitelist and SSRF protection rules as Gravitee definition imports. When `type` is `INLINE` or omitted, the `payload` field is treated as raw OpenAPI content rather than a URL.

### SSRF Protection

All remote URL imports enforce Server-Side Request Forgery (SSRF) protection. The backend validates each URL against the configured import whitelist before fetching. When private-address blocking is enabled, URLs resolving to private, link-local, or loopback addresses are rejected with a `400 Bad Request` error. This prevents attackers from using the import feature to probe internal network resources.

## Prerequisites

Before importing APIs from remote URLs, ensure the following requirements are met:

* **v4 API support**: Remote URL import is available only for v4 APIs. v2 APIs are not supported.
* **Import whitelist configuration**: The Management API must have an import whitelist configured. Remote URLs must match at least one whitelist pattern.
* **Network reachability**: The Management API server must be able to reach the remote URL over HTTP(S). CORS restrictions do not apply because the fetch occurs server-side.
* **Permissions**: Users must hold `ENVIRONMENT_API[CREATE]` permission to create APIs from remote URLs, or `API_DEFINITION[UPDATE]` permission to update existing APIs.
