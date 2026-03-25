# OAuth 2.0 Token Exchange Overview and Concepts

## Overview

OAuth 2.0 Token Exchange (RFC 8693) enables clients to exchange one security token for another, supporting impersonation (acting as another user) and delegation (acting on behalf of another user). This feature allows applications to obtain tokens with different scopes, audiences, or formats while preserving identity context. It is designed for API administrators and developers building multi-tier service architectures or integrating external identity providers.

## Key Concepts

### Impersonation vs Delegation

**Impersonation** allows a client to exchange a subject token for a new token representing the same user, optionally with reduced scopes or different audience. The client acts **as** the subject. No actor token is provided in the request.

**Delegation** allows a client to exchange both a subject token and an actor token, creating a new token that represents the subject but includes an `act` claim identifying the actor. The client acts **on behalf of** the subject. The issued token contains a nested `act` claim structure tracking the delegation chain up to the configured maximum depth (default: 25 levels).

| Mode | Actor Token Required | Use Case |
|:-----|:---------------------|:---------|
| Impersonation | No | Service assumes user identity for downstream calls |
| Delegation | Yes | Service acts on behalf of user while preserving actor identity |

### Token Types

Token exchange supports three token types as input (subject or actor) and two as output (requested):

| Token Type URI | Constant | Allowed As | Allowed As Requested |
|:---------------|:---------|:-----------|:---------------------|
| `urn:ietf:params:oauth:token-type:access_token` | ACCESS_TOKEN | Subject, Actor | Yes (default) |
| `urn:ietf:params:oauth:token-type:refresh_token` | REFRESH_TOKEN | Subject, Actor | No |
| `urn:ietf:params:oauth:token-type:id_token` | ID_TOKEN | Subject, Actor | Yes |

When `requested_token_type` is `ID_TOKEN`, the ID token JWT is returned in the `access_token` response field with `token_type` set to `N_A` per RFC 8693. No `scope` or `refresh_token` is included in the response.

### Scope Handling Modes

Scope resolution behavior is controlled by the `scopeHandling` setting on the client (or inherited from domain defaults):

**DOWNSCOPING (default):** Subject and actor token scopes cap what can be granted. Allowed scopes = `(subject ∩ actor) ∩ (client ∪ resource)`. If no scope is requested, the full allowed set is granted. If requested scopes exceed allowed scopes, the request fails.

**PERMISSIVE:** Subject and actor token scopes are ignored. Allowed scopes = `client ∪ resource`. Granted scopes are determined solely by client configuration and requested resource URIs.

### Trusted Issuers

Trusted issuers enable token exchange with tokens issued by external identity providers. Each trusted issuer configuration specifies:

* **Issuer URL**: Must match the `iss` claim in the external JWT
* **Key resolution method**: `JWKS_URL` (fetch public keys from a JWKS endpoint) or `PEM` (use a static PEM-encoded certificate)
* **Scope mappings**: Map external scopes to domain scopes (e.g., `external:read` → `domain:read`)
* **User binding**: Optionally bind external tokens to domain users via EL expressions matching token claims to user attributes

### User Binding

When user binding is enabled for a trusted issuer, the system evaluates EL expressions against the external token's claims to locate a matching domain user. Each binding criterion specifies a user attribute (e.g., `email`, `username`) and an EL expression (e.g., `{#context.attributes['token']['email']}`). The system queries domain users by the evaluated values and requires exactly one match. If no criteria are configured or binding is disabled, a virtual user is created from the token claims.

## Prerequisites

* Domain must have token exchange enabled (`TokenExchangeSettings.enabled = true`)
* Client application must include `TOKEN_EXCHANGE` in its authorized grant types
* Subject token must be a valid, non-expired JWT issued by the domain or a configured trusted issuer
* If delegation is used, actor token must be a valid, non-expired JWT and `allowDelegation` must be `true`
* Client must have scope settings configured (or resource URIs must resolve to scopes) unless using PERMISSIVE mode with no scope restrictions

## Gateway Configuration

### Domain Token Exchange Settings

Configure token exchange at the domain level via `TokenExchangeSettings`:

| Property | Type | Default | Description |
|:---------|:-----|:--------|:------------|
| `enabled` | boolean | `false` | Enable RFC 8693 OAuth 2.0 Token Exchange |
| `allowedSubjectTokenTypes` | Set\<String> | `[ACCESS_TOKEN, REFRESH_TOKEN, ID_TOKEN]` | Token types accepted as `subject_token` |
| `allowedRequestedTokenTypes` | Set\<String> | `[ACCESS_TOKEN]` | Token types that can be requested via `requested_token_type` |
| `allowImpersonation` | boolean | `true` | Allow token exchange without `actor_token` |
| `allowDelegation` | boolean | `false` | Allow token exchange with `actor_token` |
| `allowedActorTokenTypes` | Set\<String> | `[ACCESS_TOKEN, REFRESH_TOKEN, ID_TOKEN]` | Token types accepted as `actor_token` when delegation enabled |
| `maxDelegationDepth` | int | `25` | Maximum depth of nested `act` claims (range: 1-100) |
| `trustedIssuers` | List\<TrustedIssuer> | `[]` | External issuers whose tokens can be exchanged |

### Trusted Issuer Configuration

Each trusted issuer entry in `trustedIssuers` supports:

| Property | Type | Description |
|:---------|:-----|:------------|
| `issuer` | String | Issuer URL (must match JWT `iss` claim) |
| `keyResolutionMethod` | Enum | `JWKS_URL` or `PEM` |
| `jwksUri` | String | JWKS endpoint URL (when method is JWKS_URL) |
| `certificate` | String | PEM-encoded certificate (when method is PEM) |
| `scopeMappings` | Map\<String, String> | External scope → domain scope mappings |
| `userBindingEnabled` | boolean | Enable user binding via criteria |
| `userBindingCriteria` | List\<UserBindingCriterion> | EL expressions to match external token claims to domain users |

### User Binding Criterion

Each user binding criterion specifies:

| Property | Type | Description |
|:---------|:-----|:------------|
| `attribute` | String | User attribute to match (e.g., `email`, `username`) |
| `expression` | String | EL expression evaluated against token claims (e.g., `{#context.attributes['token']['email']}`) |
