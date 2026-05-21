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

* Enables OAuth clients to authenticate using a URL as their `client_id`, with configuration retrieved dynamically from a metadata document hosted at that URL.
* Designed for AI agents and Model Context Protocol (MCP) clients, allowing agent-driven workflows to authenticate without pre-registration in Access Management.
* Clients inherit settings from a designated template application, with metadata values overriding template defaults for OAuth-specific configurations (grant types, response types, scopes).
* Includes SSRF protection that blocks requests to private IP ranges, loopback addresses, and link-local networks unless explicitly allowed via domain allowlist.
* Supports optional token revocation on metadata change: when enabled, all tokens and approvals are revoked if the remote metadata document is modified.
<!-- /PIPELINE:AM-6906 -->

## Improvements

## Bug Fixes
