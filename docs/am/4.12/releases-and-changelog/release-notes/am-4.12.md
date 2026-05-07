# AM 4.12

## Highlights

## Breaking Changes

## New Features


<!-- PIPELINE:AM-6833 -->
#### **SAML Assertion Attribute Mapping**

* Customize NameID and assertion attributes in SAML responses using Expression Language expressions to map user profile fields, additional information, or computed values to SAML attributes.
* Configure custom NameID mapping to override the default internal user ID, with automatic fallback to email when the service provider requests EMAIL format.
* Define custom assertion attribute mappings that replace the default attribute set (sub, preferred_username, email, given_name, family_name, name), or omit mappings to preserve backward-compatible behavior.
* Expression Language context includes authenticated user object and request attributes, enabling dynamic attribute values based on user data and custom fields.
<!-- /PIPELINE:AM-6833 -->

## Improvements

## Bug Fixes
