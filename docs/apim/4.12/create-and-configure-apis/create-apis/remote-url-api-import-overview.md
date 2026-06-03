# Remote URL API Import Overview

## Overview

API Import from Remote URL enables platform administrators to create and update v4 APIs by fetching Gravitee API definitions or OpenAPI specifications from remote HTTP(S) endpoints. The gateway fetches definitions server-side, eliminating browser CORS restrictions and enforcing URL whitelist and SSRF protection policies. This feature streamlines API lifecycle management when definitions are hosted in version control systems, artifact repositories, or internal catalogs.

## Key Concepts

### Remote Source Import

The gateway fetches API definitions directly from user-provided URLs. Administrators submit a URL to the Management API; the backend validates the URL against the configured import whitelist, retrieves the definition, and creates or updates the API. This server-side fetch removes the need for browser-accessible endpoints and applies centralized security controls.

### Import Format Types

The platform distinguishes between inline and URL payloads for OpenAPI/Swagger imports. When the import descriptor's `type` field is set to `INLINE`, the payload contains the raw OpenAPI content. When set to `URL`, the payload is a remote endpoint address, and the backend fetches the specification before processing. Gravitee definition imports always treat the payload as a URL when using the `_import/definition-url` endpoints.

<figure><img src="../../.gitbook/assets/apim-api-import-from-remote-url-step-01.png" alt="API format selection showing Gravitee definition and OpenAPI specification options"><figcaption></figcaption></figure>

### SSRF Protection

All remote URL imports are validated by the gateway's URL sanitizer before fetch. Private and link-local addresses (e.g., `http://169.254.169.254/`) are rejected unless the `allowImportFromPrivate` configuration flag is enabled. URLs must also match at least one pattern in the configured import whitelist. This prevents attackers from using the import feature to probe internal network resources.
