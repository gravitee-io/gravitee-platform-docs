# AM 4.11

## Highlights

## Breaking Changes

## New Features


<!-- PIPELINE:AM-6321 -->
#### **Protected Resource Secret Management**

* Protected Resources now support OAuth2-compliant credential rotation with multiple active secrets per resource
* Administrators can create, renew, and delete client secrets through REST endpoints while the system automatically applies OAuth2 defaults (`client_credentials` grant type, `client_secret_basic` authentication)
* Certificate-based authentication is supported via an optional `certificate` field that references domain certificates for token signature verification
* Secret deletion automatically cleans up orphaned secret settings entries to maintain data integrity
<!-- /PIPELINE:AM-6321 -->

## Improvements

## Bug Fixes
