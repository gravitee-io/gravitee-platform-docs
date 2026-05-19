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

* Enables OAuth clients to use a URL as their `client_id` and present configuration dynamically via a metadata document hosted at that URL, eliminating the need for pre-registration.
* CIMD clients inherit settings from a designated template application and are authenticated on-demand by fetching and validating their metadata document.
* Includes built-in SSRF protection that blocks requests to private IP addresses and enforces HTTPS by default, with configurable domain restrictions using wildcard patterns.
* Supports optional metadata caching with automatic token and consent revocation when client metadata changes are detected.
* Requires at least one application marked as a template and gateway configuration via `oidc.cimdSettings.enabled` and `oidc.cimdSettings.templateId` properties.
<!-- /PIPELINE:AM-6906 -->

## Improvements

## Bug Fixes
