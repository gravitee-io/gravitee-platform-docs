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

* Enables OAuth clients to use HTTPS URLs as `client_id` values and present configuration dynamically via hosted metadata documents, eliminating pre-registration requirements.
* Adopted by the Model Context Protocol (MCP) Authentication Specification, CIMD is the preferred authentication mechanism for AI agents and MCP clients.
* Template applications define baseline configuration for all CIMD clients in a domain; valid OAuth settings from metadata documents override template values, while identity providers, MFA, and certificates always inherit from the template.
* Metadata documents and JWKS public keys are cached in-memory with configurable TTL; optional token revocation policy automatically invalidates tokens when remote metadata changes are detected.
* Requires domain-level configuration including template application ID, fetch timeout, and network security policies (private IP and unsecured HTTP restrictions).
<!-- /PIPELINE:AM-6906 -->

## Improvements

## Bug Fixes
