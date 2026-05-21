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
* The Authorization Server fetches a JSON metadata document from the URL and synthesizes an ephemeral client configuration, using the URL as both the stable identity anchor and the source of truth.
* CIMD clients inherit baseline settings from a designated template application, with metadata overriding OAuth/OIDC client-registration fields such as `redirect_uris`, `jwks_uri`, and `logo_uri`.
* Metadata documents are cached in-memory with configurable TTL (default 3600 seconds) and maximum entry count (default 500 entries).
* Optional revocation policy automatically invalidates all tokens and consents when remote metadata changes are detected via SHA-256 hash comparison.
<!-- /PIPELINE:AM-6906 -->

## Improvements

## Bug Fixes
