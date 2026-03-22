# OAuth 2.0 Token Exchange Concepts

## Overview

OAuth 2.0 Token Exchange (RFC 8693) enables clients to exchange existing tokens for new tokens with different scopes, audiences, or delegation chains. It supports impersonation (exchanging a subject token without an actor) and delegation (exchanging with an actor token to create a chain of authority). This feature is designed for API administrators configuring multi-tier authorization and developers integrating cross-domain token workflows.

## Key Concepts

### Impersonation

A client exchanges a subject token (access, refresh, or ID token) for a new access token or ID token without introducing an actor. The resulting token represents the original subject user with potentially reduced scopes. The `act` claim is not added to the new token. Impersonation is enabled by default via the `allowImpersonation` domain setting.

### Delegation

A client exchanges a subject token and an actor token to create a new token representing the subject user, with the actor's identity recorded in the `act` claim. The `act` claim nests prior delegation chains from both the subject and actor tokens, creating a verifiable chain of authority. Delegation depth is capped by `maxDelegationDepth` (default 25, range 1-100). Delegation is disabled by default and must be enabled via `allowDelegation`.

### Trusted Issuers

External identity providers can issue subject or actor tokens accepted by the domain. Each trusted issuer is configured with an issuer URL, key resolution method (JWKS endpoint or PEM certificate), optional scope mappings (external scope → domain scope), and optional user binding criteria (EL expressions matching token claims to domain user attributes). Tokens from trusted issuers are validated for signature, temporal claims, and issuer match before use.

### Scope Handling Modes

Two modes control how scopes are granted during token exchange:

| Mode | Behavior |
|:-----|:---------|
| `DOWNSCOPING` | Granted scopes are the intersection of subject/actor token scopes and client/resource scopes. Subject and actor scopes cap the result. Fail-closed: empty client scopes with no resource yields empty granted scopes. |
| `PERMISSIVE` | Granted scopes are drawn only from client and resource scopes. Subject and actor token scopes impose no restriction. Fail-closed: empty client scopes with no resource yields empty granted scopes. |

Scope handling defaults to `DOWNSCOPING` at the domain level and can be overridden per client via `TokenExchangeOAuthSettings.scopeHandling`.

### Token Types

The following token type URNs are supported:

| URN | Label | Use |
|:----|:------|:----|
| `urn:ietf:params:oauth:token-type:access_token` | Access Token | Subject, actor, or requested token |
| `urn:ietf:params:oauth:token-type:refresh_token` | Refresh Token | Subject or actor token only |
| `urn:ietf:params:oauth:token-type:id_token` | ID Token | Subject, actor, or requested token |
| `urn:ietf:params:oauth:token-type:jwt` | JWT | Generic JWT (future use) |

### User Binding

When a trusted issuer has `userBindingEnabled=true`, the domain evaluates `userBindingCriteria` (EL expressions) against the token's claims to match a domain user. Each criterion specifies a user attribute (e.g., `email`, `username`) and an expression (e.g., `{#token['email']}`). The system queries users matching all criteria and returns the single matched user. If zero or multiple users match, the exchange fails. If user binding is disabled or no criteria are configured, a virtual user is created from the token claims.
