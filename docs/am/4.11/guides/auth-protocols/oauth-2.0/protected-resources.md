### Overview

Protected Resources in support secret management, certificate-based JWT verification, and membership controls. These enhancements enable secure token introspection workflows for MCP Servers and other OAuth 2.0 clients. Protected Resources can act as audience targets in token exchange flows and introspection requests, with configurable authentication methods and grant type restrictions.

### Key Concepts

#### Protected Resource Secrets

Protected Resources manage multiple client secrets with independent lifecycle controls. Each secret includes a name, expiration date, and algorithm configuration. Secrets are created, renewed, and deleted via REST API. List operations return masked secret values. Secret lifecycle events trigger notifications when expiration approaches.

#### Token Introspection with Protected Resources

When a caller introspects a JWT access token, the system validates the token's `aud` (audience) claim against both Applications and Protected Resources. For single-audience tokens, the system first checks Applications, then Protected Resources, then falls back to RFC 8707 resource identifier validation. Multi-audience tokens always use RFC 8707 validation. The matched entity's certificate is used to verify the JWT signature.

#### MCP Server Grant Type Restrictions

Protected Resources of type MCP Server are restricted to `client_credentials` and `urn:ietf:params:oauth:grant-type:token-exchange` grant types. Token endpoint authentication methods are limited to `client_secret_basic`, `client_secret_post`, and `client_secret_jwt`.
