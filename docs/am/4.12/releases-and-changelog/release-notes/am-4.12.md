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

* Enables OAuth 2.0 clients to use a URL as their `client_id` and retrieve configuration dynamically from that URL, eliminating the need for pre-registration.
* The Authorization Server fetches a metadata document from the URL and synthesizes client configuration on-demand using a designated template application as the baseline.
* Designed for AI agents and Model Context Protocol (MCP) clients, allowing agent-driven workflows to authenticate without manual registration.
* Requires a template application to be configured in domain OIDC settings and supports optional token revocation when remote metadata changes are detected.
* Metadata documents are cached in-memory with configurable TTL, and SSRF protection rules are enforced during metadata fetching.
<!-- /PIPELINE:AM-6906 -->

## Improvements

## Bug Fixes
