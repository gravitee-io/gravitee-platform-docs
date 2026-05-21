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

* Enables OAuth 2.0 clients to use HTTPS URLs as `client_id` values and retrieve configuration dynamically from hosted metadata documents, eliminating pre-registration requirements.
* Supports AI agents and Model Context Protocol (MCP) clients by allowing agent-driven workflows to authenticate at scale without manual application setup.
* Requires a template application to define baseline configuration and constraints; metadata parameters (grant types, response types, scopes) are intersected with template values.
* Enforces SSRF protection by blocking private/loopback IPs and requiring HTTPS for metadata and logo URIs; administrators can configure allowed domains and fetch limits.
* Optionally revokes all tokens and approvals when remote metadata changes are detected via SHA-256 hash comparison.
<!-- /PIPELINE:AM-6906 -->

## Improvements

## Bug Fixes
