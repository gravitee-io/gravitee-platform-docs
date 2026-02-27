# AM 4.11

## Highlights

## Breaking Changes

## New Features


<!-- PIPELINE:AM-6322 -->
#### **Agent Application Type for Machine-to-Machine Authentication**

* Introduces a security-hardened application profile that enforces strict grant type and response type constraints for M2M scenarios.
* Automatically strips insecure grant types (`implicit`, `password`, `refresh_token`) and response types (`token`, `id_token`, `id_token token`) during Dynamic Client Registration and token issuance.
* Defaults to `authorization_code` grant with `code` response type if no allowed grant types remain after validation.
* Supports agent card metadata exposure through a dedicated proxy endpoint with comprehensive SSRF protection (scheme validation, private IP filtering, 512 KB size limit).
* Enables protected resource management through new member and secret endpoints for granular access control and secure authentication.
<!-- /PIPELINE:AM-6322 -->

## Improvements

## Bug Fixes
