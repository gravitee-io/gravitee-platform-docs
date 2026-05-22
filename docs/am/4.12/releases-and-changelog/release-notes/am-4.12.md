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

* Enables OAuth clients to use HTTPS URLs as their `client_id` and provide configuration dynamically via a hosted metadata document, eliminating pre-registration requirements.
* Designed for AI agents and Model Context Protocol (MCP) clients, allowing agent-driven workflows without manual application setup in the Management Console.
* CIMD clients inherit default settings from a designated template application, with metadata values overriding template configuration where specified.
* Includes built-in SSRF protection (HTTPS-only by default, private IP blocking) and configurable metadata caching with optional automatic token revocation when remote metadata changes.
* Template applications must be created in **Domain Settings → Client Registration → Templates** before enabling CIMD for a domain.
<!-- /PIPELINE:AM-6906 -->

## Improvements

## Bug Fixes
