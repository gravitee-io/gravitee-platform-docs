# OAuth 2.0 Token Exchange Concepts

## Overview

OAuth 2.0 Token Exchange (RFC 8693) enables clients to exchange one security token for another, supporting impersonation and delegation scenarios. This feature allows applications to obtain tokens with different scopes, audiences, or subjects by presenting existing valid tokens. It is designed for API administrators and developers building multi-tier architectures, service-to-service authentication, or cross-domain token workflows.

## Key Concepts

### Impersonation vs. Delegation

**Impersonation** occurs when a client exchanges a subject token without providing an actor token. The resulting token represents the original subject with potentially modified scopes or audience. The client acts on behalf of the subject user.

**Delegation** occurs when a client provides both a subject token and an actor token. The resulting token includes an `act` claim that identifies the actor, creating a chain of delegation. This supports scenarios where a service acts on behalf of a user but must preserve the identity of the intermediary actor. Delegation depth is limited by `maxDelegationDepth` (default: 25, range: 1-100).

### Token Types

Token exchange supports three token types as input and output:

| Token Type | URN | Use Case |
|:-----------|:----|:---------|
| Access Token | `urn:ietf:params:oauth:token-type:access_token` | Standard OAuth 2.0 access tokens |
| Refresh Token | `urn:ietf:params:oauth:token-type:refresh_token` | Long-lived tokens (input only) |
| ID Token | `urn:ietf:params:oauth:token-type:id_token` | OpenID Connect identity tokens |

The `subject_token_type` and `actor_token_type` parameters specify the type of input tokens. The `requested_token_type` parameter specifies the desired output token type (defaults to access token if allowed). When requesting an ID token, the token is returned in the `access_token` response field with `token_type` set to `"N_A"` per RFC 8693.

### Scope Handling Modes

Scope handling determines how scopes are granted during token exchange:

| Mode | Behavior |
|:-----|:---------|
| DOWNSCOPING (default) | Granted scopes = subject token scopes ∩ (client scopes ∪ resource scopes). Subject and actor token scopes cap what can be granted. |
| PERMISSIVE | Granted scopes = client scopes ∪ resource scopes. Subject and actor token scopes impose no restriction. |

Clients inherit the domain-level scope handling mode by default but can override it via `TokenExchangeOAuthSettings.scopeHandling`.

### Trusted Issuers

Trusted issuers enable token exchange with tokens issued by external identity providers. Each trusted issuer configuration specifies:

* **Issuer URL**: Must match the JWT `iss` claim
* **Key resolution method**: `JWKS_URL` (fetch keys from JWKS endpoint) or `PEM` (use embedded certificate)
* **Scope mappings**: Map external scopes to domain scopes (e.g., `external:read` → `domain:read`)
* **User binding**: Optionally resolve external subjects to domain users using EL expressions

When user binding is enabled, the system matches external token claims to domain user attributes using configured criteria. If no user is found or binding is disabled, a virtual user is created from token claims.

## Prerequisites

* Domain-level token exchange must be enabled (`TokenExchangeSettings.enabled = true`)
* Client must be authorized to use the `urn:ietf:params:oauth:grant-type:token-exchange` grant type
* Subject token must be valid (not expired, not revoked if domain-issued)
* For delegation scenarios, `allowDelegation` must be enabled
* For impersonation scenarios, `allowImpersonation` must be enabled
* For trusted issuer tokens, a matching trusted issuer configuration must exist with valid key material

## Gateway Configuration

### Domain-Level Token Exchange Settings

Configure token exchange at the domain level using `TokenExchangeSettings`:

| Property | Type | Default | Description |
|:---------|:-----|:--------|:------------|
| `enabled` | boolean | `false` | Enable RFC 8693 Token Exchange for the domain |
| `allowedSubjectTokenTypes` | Set\<String> | `[ACCESS_TOKEN, REFRESH_TOKEN, ID_TOKEN]` | Token types accepted as `subject_token` |
| `allowedRequestedTokenTypes` | Set\<String> | `[ACCESS_TOKEN]` | Token types that can be requested via `requested_token_type` |
| `allowImpersonation` | boolean | `true` | Allow token exchange without `actor_token` |
| `allowDelegation` | boolean | `false` | Allow token exchange with `actor_token` (delegation scenarios) |
| `allowedActorTokenTypes` | Set\<String> | `[ACCESS_TOKEN, REFRESH_TOKEN, ID_TOKEN]` | Token types accepted as `actor_token` when delegation is enabled |
| `maxDelegationDepth` | int | `25` | Maximum depth of nested `act` claims (min: 1, max: 100) |
| `trustedIssuers` | List\<TrustedIssuer> | `[]` | External issuers whose tokens can be exchanged |
