# AM 4.12

## Highlights

## Breaking Changes

## New Features


<!-- PIPELINE:AM-6833 -->
#### **SAML Assertion Attribute Mapping**

* Customize NameID and assertion attributes in SAML responses using Expression Language (EL) expressions for flexible service provider integration.
* Configure custom NameID mapping to override the default internal user ID, with automatic fallback to email address when the service provider requests EMAIL format.
* Define custom assertion attributes as name-value pairs to replace the default attribute set (sub, preferred_username, email, given_name, family_name, name).
* Omit custom attribute mappings to maintain backward compatibility with the standard attribute set from previous versions.
<!-- /PIPELINE:AM-6833 -->


<!-- PIPELINE:AM-6906 -->
#### **Client ID Metadata Document (CIMD) Support**

* Enables OAuth clients to use a URL as their `client_id` and retrieve configuration dynamically from that URL, eliminating the need for pre-registration.
* The gateway fetches a JSON metadata document from the client_id URL, validates it against SSRF protection rules, and synthesizes client configuration by merging it with a designated template application.
* Supports automatic token revocation when remote metadata changes are detected, with configurable in-memory caching.
* Requires a template application configured in the domain and CIMD enabled in domain OIDC settings with SSRF protection configured (private IP blocking, HTTPS enforcement, domain allowlists).
* Designed for AI agents and Model Context Protocol (MCP) clients requiring agent-driven authentication workflows without manual registration.
<!-- /PIPELINE:AM-6906 -->


<!-- PIPELINE:AM-6980 -->
#### **Application Filtering, Cursor Pagination, and Expand Parameters**

* Filter applications by status (`enabled`/`disabled`) and owner email address using query parameters on the application list API.
* Expand API responses to include OAuth client IDs with the `expand=clientId` parameter, reducing the need for follow-up API calls.
* Use cursor-based pagination (`/applications/search/_cursor`) for efficient traversal of large application datasets with opaque Base64-encoded tokens.
* Combine filters with AND logic (status and owner) and OR logic (application types) to enable granular application discovery workflows.
* Requires `DOMAIN_APPLICATION[LIST]` permission for the target domain and `ORGANIZATION_USER[READ]` permission to filter by owner email.
<!-- /PIPELINE:AM-6980 -->

## Improvements

## Bug Fixes
