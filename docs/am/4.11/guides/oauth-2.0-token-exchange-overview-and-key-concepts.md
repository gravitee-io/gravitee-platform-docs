# OAuth 2.0 Token Exchange: Overview and Key Concepts

## Overview

OAuth 2.0 Token Exchange (RFC 8693) enables clients to exchange one security token for another. This feature supports both impersonation (acting as the subject) and delegation (acting on behalf of the subject). Token exchange allows API administrators to configure trusted external JWT issuers, control scope resolution behavior, and enforce delegation depth limits. It is designed for scenarios requiring cross-domain token translation, privilege escalation control, and audit-compliant delegation chains.

## Key Concepts

### Impersonation vs Delegation

Impersonation occurs when a client exchanges a subject token without providing an actor token, effectively assuming the subject's identity. Delegation occurs when both subject and actor tokens are provided, creating a chain where the actor performs actions on behalf of the subject.

The resulting access token includes an `act` claim that preserves the full delegation chain for audit purposes. Domain administrators control which mode is permitted via `allowImpersonation` and `allowDelegation` settings.

### Token Types

Token exchange accepts and issues tokens identified by RFC 8693 URNs. Subject tokens can be access tokens, refresh tokens, or ID tokens depending on domain configuration. Requested token types are limited to access tokens and ID tokens.

When requesting an ID token, the response returns it in the `access_token` field with `token_type` set to `N_A` per RFC 8693. No refresh tokens are issued during token exchange.

| Token Type URI | Description |
|:---------------|:------------|
| `urn:ietf:params:oauth:token-type:access_token` | OAuth 2.0 access token |
| `urn:ietf:params:oauth:token-type:refresh_token` | OAuth 2.0 refresh token |
| `urn:ietf:params:oauth:token-type:id_token` | OpenID Connect ID token |
| `urn:ietf:params:oauth:token-type:jwt` | Generic JWT |

### Scope Handling Modes

Scope resolution behavior is controlled by the `scopeHandling` setting. In `DOWNSCOPING` mode (default), granted scopes are capped by the intersection of subject and actor token scopes, preventing privilege escalation. In `PERMISSIVE` mode, subject and actor token scopes impose no restriction, allowing clients to request any scope configured on the client or associated with target resources.

The final granted scopes are computed as the intersection of requested scopes and allowed scopes based on the selected mode.

| Mode | Allowed Scopes Formula | Use Case |
|:-----|:----------------------|:---------|
| `DOWNSCOPING` | `subjectScopes ∩ (clientScopes ∪ resourceScopes)` | Prevent privilege escalation |
| `PERMISSIVE` | `clientScopes ∪ resourceScopes` | Trust subject/actor tokens implicitly |

### Trusted Issuers

Trusted issuers enable token exchange with external JWTs issued outside the domain. Each trusted issuer configuration specifies the issuer URL (matching the JWT `iss` claim), key resolution method (JWKS URL or PEM certificate), and optional scope mappings to translate external scopes to domain scopes. User binding criteria allow external subjects to be resolved to domain users via EL expressions evaluated against token claims.

### Delegation Depth

Delegation depth tracks the number of nested `act` claims in a delegation chain. Each token exchange increments the depth by one, with the resulting depth calculated as `1 + max(subjectTokenDepth, actorTokenDepth)`. The `maxDelegationDepth` setting (1-100, default 25) prevents unbounded delegation chains. Requests exceeding this limit are rejected with an error.

### User Binding

When user binding is enabled on a trusted issuer, the gateway evaluates EL expressions against token claims to resolve the external subject to a domain user. Each binding criterion specifies a user attribute (e.g., `email`, `username`) and an EL expression (e.g., `{#token['email']}`). The gateway queries users matching all criteria and rejects the request if zero or multiple users are found. When user binding is disabled, a virtual user is created from token claims.

## Prerequisites

Before using token exchange, ensure the following:

* Domain must have token exchange enabled (`TokenExchangeSettings.enabled = true`)
* OAuth 2.0 client must include `urn:ietf:params:oauth:grant-type:token-exchange` in authorized grant types
* Subject token must be a valid JWT issued by the domain or a configured trusted issuer
* Actor token (if provided) must be a valid JWT issued by the domain or a configured trusted issuer
* Client must have scopes configured or target resources must have associated scopes
* For external JWTs: trusted issuer must be configured with valid JWKS URL or PEM certificate
