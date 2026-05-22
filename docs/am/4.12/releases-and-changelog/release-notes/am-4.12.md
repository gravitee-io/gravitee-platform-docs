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

* Enables OAuth 2.0 clients to use HTTPS URLs as `client_id` values and retrieve configuration dynamically from metadata documents, eliminating the need for pre-registration.
* CIMD clients inherit baseline settings from a designated template application, with OAuth parameters in the metadata document overriding template values (except `grant_types`, `response_types`, and `scope`, which are intersected).
* Metadata documents are cached in-memory with configurable TTL (default 3600 seconds) and support automatic token/consent revocation when metadata changes are detected.
* Includes SSRF protection that blocks requests to private IP ranges, loopback addresses, and plain HTTP URIs by default, with optional domain allowlisting.
* Requires AM 4.6 or later and domain-level permission `domain_openid_read` to configure CIMD settings.
<!-- /PIPELINE:AM-6906 -->

## Improvements

## Bug Fixes
