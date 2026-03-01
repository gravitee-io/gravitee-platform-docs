# AM 4.11

## Highlights

## Breaking Changes

## New Features


<!-- PIPELINE:AM-6339 -->
#### **Certificate Fallback for JWT Signing**

* Domains can now configure a fallback certificate that automatically activates when a client's primary certificate fails or is unavailable during JWT signing operations.
* Fallback certificates are configured via the domain certificate settings API endpoint (`PUT /organizations/{organizationId}/environments/{environmentId}/domains/{domain}/certificate-settings`) and apply immediately without requiring a domain restart.
* The fallback certificate must belong to the same domain unless the domain is a master domain, which can access certificates from any domain in the organization.
* All fallback attempts are logged at WARN level with certificate IDs for operational visibility and troubleshooting.
* Requires `DOMAIN_SETTINGS[UPDATE]` permission to configure fallback settings.
<!-- /PIPELINE:AM-6339 -->

## Improvements

## Bug Fixes
