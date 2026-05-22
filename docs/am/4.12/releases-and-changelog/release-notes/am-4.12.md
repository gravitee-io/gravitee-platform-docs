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

* Enables OAuth clients to use HTTPS URLs as `client_id` values, with configuration retrieved dynamically from a metadata document hosted at that URL.
* Eliminates pre-registration requirements for AI agents and Model Context Protocol (MCP) clients, allowing agent-driven workflows to authenticate without manual setup.
* CIMD clients inherit settings from a designated template application, which defines identity providers, MFA, token validity, and other application-level configurations.
* Includes SSRF protection with configurable allowlists for domains and IP address ranges, plus metadata caching with configurable TTL (default 3600 seconds).
* Supports automatic token revocation when client metadata changes, ensuring security policies remain synchronized with remote configuration updates.
<!-- /PIPELINE:AM-6906 -->

## Improvements

## Bug Fixes
