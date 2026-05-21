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

* Enables dynamic client configuration by allowing OAuth clients to use an HTTPS URL as their `client_id`, with the Authorization Server retrieving metadata from that URL instead of requiring pre-registration.
* Supports the Model Context Protocol (MCP) authentication specification for AI agents and MCP clients, making AM compatible with emerging AI-driven integration patterns.
* Requires a template application to define baseline configuration and security policies; CIMD metadata fields (grant types, response types, scopes) are intersected with template settings to enforce domain-level restrictions.
* Includes built-in SSRF protection (private IP blocking, domain allowlisting) and optional token revocation when remote metadata changes are detected.
* Configured at the domain level via `oidc.cimdSettings.enabled` and `oidc.cimdSettings.templateId`; metadata is cached in-memory with configurable TTL and size limits.
<!-- /PIPELINE:AM-6906 -->

## Improvements

## Bug Fixes
