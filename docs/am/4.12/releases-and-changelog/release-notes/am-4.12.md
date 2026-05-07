# AM 4.12

## Highlights

## Breaking Changes

## New Features


<!-- PIPELINE:AM-6833 -->
#### **SAML 2.0 Assertion Attribute and NameID Mapping**

* Customize SAML response attributes using Expression Language (EL) to map user context data to assertion attributes and NameID elements.
* Define custom NameID values by configuring an EL expression that resolves to any user attribute (e.g., username, employee ID). Falls back to internal user ID if the expression is null or invalid.
* Configure custom assertion attributes to replace the default set (`sub`, `preferred_username`, `email`, `name`, `given_name`, `family_name`). Omitting custom attributes preserves backward-compatible default behavior.
* Supports EMAIL NameID format explicitly; all other formats use the configured mapping or default internal user ID.
<!-- /PIPELINE:AM-6833 -->

## Improvements

## Bug Fixes
