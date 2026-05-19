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

* Enables OAuth clients to use a URL as their `client_id` and provide configuration dynamically via a metadata document hosted at that URL, eliminating the need for pre-registration.
* CIMD clients inherit configuration from a designated template application, with OAuth settings (grant types, response types, scopes) determined by the intersection of metadata values and template settings.
* Metadata documents are cached with configurable TTL (default 3600 seconds), and an optional revocation policy automatically invalidates tokens and consents when remote metadata changes are detected.
* Includes SSRF protection that rejects private/loopback IP addresses and requires HTTPS by default, with administrator-controlled toggles to relax restrictions for development environments.
* Designed for AI agents and Model Context Protocol (MCP) clients requiring agent-driven authentication workflows without manual registration.
<!-- /PIPELINE:AM-6906 -->

## Improvements

## Bug Fixes
