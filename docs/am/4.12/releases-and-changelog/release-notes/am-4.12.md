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

* Enables OAuth clients to use a URL as their `client_id`, allowing the Authorization Server to dynamically retrieve client configuration from a metadata document hosted at that URL.
* Designed for AI agents and Model Context Protocol (MCP) clients that require authentication without pre-registration.
* CIMD clients inherit configuration from a designated template application, with OAuth-specific settings (grant types, response types, scopes) intersected between the template and metadata document.
* Supports automatic token revocation when metadata changes are detected, with configurable caching and SSRF protection for metadata document retrieval.
* Requires domain-level configuration in `gravitee.yml` or via the Management API, including a template application ID and optional security controls for private IPs and HTTP URIs.
<!-- /PIPELINE:AM-6906 -->

## Improvements

## Bug Fixes
