# AM 4.11

## Highlights

## Breaking Changes

## New Features


<!-- PIPELINE:AM-6321 -->
#### **Protected Resource Secret Management and Certificate Authentication**

* Protected Resources now support client secret management with expiration tracking and zero-downtime rotation, enabling them to participate in token introspection and OAuth 2.0 token exchange flows as confidential clients.
* Certificate-based authentication allows Protected Resources to use X.509 certificates for mutual TLS authentication during token introspection workflows.
* Role-based membership controls grant users and service accounts specific permissions (LIST, CREATE, UPDATE, DELETE) for managing Protected Resource secrets, settings, and membership.
* Token introspection resolves audiences against both Applications and Protected Resources, following RFC 8707 resource identifier rules for multiple audiences.
* Requires Access Management 4.11.0 or later with OAuth 2.0 enabled at the domain level.
<!-- /PIPELINE:AM-6321 -->

## Improvements

## Bug Fixes
