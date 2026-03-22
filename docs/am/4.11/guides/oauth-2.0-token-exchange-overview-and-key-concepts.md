# OAuth 2.0 Token Exchange Overview and Key Concepts

## Overview

OAuth 2.0 Token Exchange (RFC 8693) enables clients to exchange one security token for another, supporting both impersonation (acting as another user) and delegation (acting on behalf of another user) scenarios. This feature allows applications to obtain tokens with different scopes, audiences, or token types while maintaining a secure chain of trust. It is designed for API administrators and developers building multi-tier service architectures or integrating with external identity providers.

## Key Concepts

### Impersonation vs. Delegation

**Impersonation** allows a client to exchange a subject token for a new token representing the same user, potentially with reduced scopes or a different token type. The client acts as the subject user without preserving the original caller's identity. No `actor_token` is provided in the request.

**Delegation** allows a client to exchange a subject token while providing an `actor_token`, creating a new token that includes an `act` claim documenting the delegation chain. The issued token represents the subject user but includes metadata about the actor performing the exchange. Delegation depth is capped by the `maxDelegationDepth` setting (default: 25, range: 1-100).

### Token Types

The feature supports three token types as defined by RFC 8693:

| Token Type | URN | Usage |
|:-----------|:----|:------|
| Access Token | `urn:ietf:params:oauth:token-type:access_token` | Standard OAuth 2.0 access token |
| Refresh Token | `urn:ietf:params:oauth:token-type:refresh_token` | Long-lived token for obtaining new access tokens |
| ID Token | `urn:ietf:params:oauth:token-type:id_token` | OpenID Connect identity token |

When `requested_token_type` is `id_token`, the ID token is returned in the `access_token` response field with `token_type` set to `"N_A"`. No `scope` or `refresh_token` is included in the response.

### Scope Handling Modes

Two modes control how scopes are resolved during token exchange:

| Mode | Behavior | Formula |
|:-----|:---------|:--------|
| **DOWNSCOPING** | Subject/actor token scopes cap what can be granted | `allowed = base ∩ (client ∪ resource)` |
| **PERMISSIVE** | Subject/actor token scopes impose no restriction | `allowed = client ∪ resource` |

For impersonation, `base = subject token scopes`. For delegation, `base = subject token scopes ∩ actor token scopes`. If the `scope` parameter is omitted, all allowed scopes are granted. If provided, the requested scopes must be a subset of allowed scopes or the request fails with `invalid_scope`.

### Trusted Issuers

Trusted issuers enable token exchange with external JWT tokens not issued by the domain. Each trusted issuer configuration includes:

- **Issuer URL**: Must match the JWT `iss` claim
- **Key Resolution Method**: `JWKS_URL` (fetch public keys from a JWKS endpoint) or `PEM` (use a PEM-encoded certificate)
- **Scope Mappings**: Map external scopes to domain scopes (e.g., `read:data` → `data.read`)
- **User Binding**: Optionally resolve the external subject to a domain user using SpEL expressions evaluated against token claims

### Delegation Chain (`act` Claim)

When delegation is enabled, the issued token includes an `act` claim documenting the actor and any prior delegation chain:

```json
{
  "sub": "subject-user-id",
  "act": {
    "sub": "actor-user-id",
    "gis": "actor-internal-id",
    "act": { "sub": "prior-actor-id" },
    "actor_act": { "sub": "actor-token-actor-id" }
  }
}
```

- `sub`: Subject of the actor
- `gis`: Gravitee Internal Subject (for V2 domains)
- `act`: Nested `act` claim from the subject token (delegation chain)
- `actor_act`: Actor token's own `act` claim (for audit traceability)

## Prerequisites

- OAuth 2.0 client configured in the domain
- Token exchange enabled in domain OAuth settings (`enabled: true`)
- For delegation: `allowDelegation` set to `true`
- For impersonation: `allowImpersonation` set to `true`
- For external tokens: Trusted issuer configured with valid JWKS URL or PEM certificate
- For user binding: User binding criteria defined with valid SpEL expressions

## Gateway Configuration

### Domain-Level Token Exchange Settings

Configure token exchange at the domain level under OAuth settings:

| Property | Description | Example |
|:---------|:------------|:--------|
| `enabled` | Enable RFC 8693 OAuth 2.0 Token Exchange | `true` |
| `allowedSubjectTokenTypes` | Token types accepted as `subject_token` | `[ACCESS_TOKEN, REFRESH_TOKEN, ID_TOKEN]` |
| `allowedRequestedTokenTypes` | Token types that can be requested via `requested_token_type` | `[ACCESS_TOKEN, ID_TOKEN]` |
| `allowImpersonation` | Allow token exchange without `actor_token` | `true` |
| `allowDelegation` | Allow token exchange with `actor_token` | `false` |
| `allowedActorTokenTypes` | Token types accepted as `actor_token` for delegation | `[ACCESS_TOKEN, REFRESH_TOKEN, ID_TOKEN]` |
| `maxDelegationDepth` | Maximum depth of nested `act` claims (1-100) | `25` |
