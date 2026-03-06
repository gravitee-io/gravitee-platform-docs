# AM 4.11

## Highlights

## Breaking Changes

## New Features


<!-- PIPELINE:AM-6321 -->
#### **Protected Resource Secret and Certificate Management**

* Protected Resources now support multiple client secrets with individual expiration dates and lifecycle management (create, renew, delete).
* Certificates can be bound to Protected Resources for mTLS authentication scenarios, with validation to prevent deletion of certificates in use.
* Role-based membership control enables granular access management for Protected Resources at the organization, environment, domain, and resource levels.
* At least one secret must exist per Protected Resource at all times; the system prevents deletion of the last remaining secret.
<!-- /PIPELINE:AM-6321 -->

## Improvements

## Bug Fixes
