# AM 4.11

## Highlights

## Breaking Changes

## New Features


<!-- PIPELINE:AM-6339 -->
#### **Certificate Fallback for Domains**

* Domains can now specify a backup certificate that is used automatically when the primary client certificate fails to load or is unavailable, preventing service disruption during certificate rotation.
* The system follows a three-tier fallback hierarchy: primary client certificate → domain fallback certificate → default HMAC certificate (if enabled).
* Configure the fallback certificate using the domain certificate settings endpoint (`PUT /organizations/{organizationId}/environments/{environmentId}/domains/{domain}/certificate-settings`).
* Fallback certificates must belong to the same domain, except for master domains which can access certificates from any domain for cross-domain introspection scenarios.
<!-- /PIPELINE:AM-6339 -->

## Improvements

## Bug Fixes
