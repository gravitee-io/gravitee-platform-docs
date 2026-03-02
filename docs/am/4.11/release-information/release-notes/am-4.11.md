# AM 4.11

## Highlights

## Breaking Changes

## New Features


<!-- PIPELINE:AM-6321 -->
#### **Protected Resource Management with Token Exchange**

* Protected resources enable OAuth2 resource servers to authenticate with the authorization server for token introspection and server-to-server communication patterns, including Model Context Protocol (MCP) server integration.
* Supports multiple concurrent client secrets with independent expiration tracking, certificate-based authentication (TLS client auth), and automatic secret rotation workflows.
* Implements RFC 8707 token exchange, allowing MCP servers to exchange existing tokens (access, refresh, ID, or JWT) for new access tokens while preserving the subject's identity.
* Token exchange must be explicitly enabled at the domain level with allowed subject token types configured before protected resources can participate in exchange flows.
* Protected resources default to `client_credentials` grant type and `client_secret_basic` authentication method, with support for certificate-based authentication as an alternative.
<!-- /PIPELINE:AM-6321 -->

## Improvements

## Bug Fixes
