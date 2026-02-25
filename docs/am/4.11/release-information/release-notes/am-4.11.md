# AM 4.11

## Highlights

## Breaking Changes

## New Features


<!-- PIPELINE:AM-6321 -->
#### **Protected Resource Secret Management**

* Protected Resources can now manage client secrets with full lifecycle support, including creation, renewal, deletion, and expiration notifications.
* Protected Resources act as OAuth2 clients during token introspection and authentication flows, using their `clientId` to validate JWT audience claims alongside Applications.
* Certificate-based JWT signature verification is supported by assigning a certificate ID to the Protected Resource.
* Secret expiration policies inherit domain-level settings automatically, and secrets trigger domain events (`CREATE`, `RENEW`, `DELETE`) for notification workflows.
* Default OAuth2 settings are applied automatically when creating Protected Resources without explicit configuration (grant type: `client_credentials`, response type: `code`, auth method: `client_secret_basic`).
<!-- /PIPELINE:AM-6321 -->

## Improvements

## Bug Fixes
