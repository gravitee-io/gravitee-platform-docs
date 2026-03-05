# AM 4.11

## Highlights

## Breaking Changes

## New Features


<!-- PIPELINE:AM-6321 -->
#### **Protected Resource Management and Token Exchange**

* Manage OAuth 2.0 resource servers independently from client applications, with support for secret rotation, certificate-based authentication, and resource identifier configuration.
* Enable token exchange flows for MCP (Model Context Protocol) Servers, allowing secure token delegation while preserving claims and enforcing expiration constraints.
* Configure authentication methods including client secrets with automatic expiration notifications or JWT signature verification using uploaded certificates.
* Restrict MCP Server resources to `client_credentials` and token exchange grant types, with exchanged tokens limited to the subject token's remaining lifetime.
<!-- /PIPELINE:AM-6321 -->

## Improvements

## Bug Fixes
