# OAuth 2.0 Token Exchange - Administrator Guide

## Overview

OAuth 2.0 Token Exchange (RFC 8693) enables clients to exchange one security token for another, supporting both impersonation (acting as the subject) and delegation (acting on behalf of the subject). This feature allows cross-domain token exchange with trusted external issuers, scope mapping, and user binding to domain identities.

## Key Concepts

### Impersonation vs. Delegation

**Impersonation** allows a client to exchange a subject token for a new token representing the same subject, without preserving the original actor's identity. The client acts as the subject user. No `actor_token` is provided in the request.

**Delegation** allows a client to exchange a subject token while preserving the actor's identity in the resulting token. The issued token includes an `act` claim containing the actor's identity and any prior delegation chain. Requires both `subject_token` and `actor_token` in the request.

| Mode | `actor_token` Required | `act` Claim in Result | Use Case |
|:-----|:----------------------|:---------------------|:---------|
| Impersonation | No | No | Client assumes subject identity |
| Delegation | Yes | Yes | Client acts on behalf of subject, preserving actor identity |

### Token Types

Token exchange supports multiple token types as input and output. Each type is identified by a URN.

| Type | URN | Allowed As |
|:-----|:----|:-----------|
| Access Token | `urn:ietf:params:oauth:token-type:access_token` | Subject, Actor, Requested |
| Refresh Token | `urn:ietf:params:oauth:token-type:refresh_token` | Subject, Actor |
| ID Token | `urn:ietf:params:oauth:token-type:id_token` | Subject, Actor, Requested |
| JWT | `urn:ietf:params:oauth:token-type:jwt` | Subject, Actor |

When `requested_token_type` is `urn:ietf:params:oauth:token-type:id_token`, the ID token is returned in the `access_token` field with `token_type` set to `"N_A"`. No `scope` or `refresh_token` is included.

### Scope Handling Modes

Scope handling determines how scopes are granted during token exchange.

**DOWNSCOPING**: Granted scopes are the intersection of subject token scopes (and actor token scopes if delegation) with the union of client scopes and resource scopes. Subject and actor tokens act as upper bounds.

```
allowedScopes = subjectScopes ∩ (clientScopes ∪ resourceScopes)
// For delegation:
allowedScopes = subjectScopes ∩ actorScopes ∩ (clientScopes ∪ resourceScopes)
```

**PERMISSIVE**: Granted scopes are the union of client scopes and resource scopes. Subject and actor token scopes impose no restriction.

```
allowedScopes = clientScopes ∪ resourceScopes
```

### Trusted Issuers

Trusted issuers are external JWT issuers whose tokens are accepted for token exchange. Each trusted issuer configuration includes:

* **Issuer URL**: Must match the `iss` claim in the JWT
* **Key Resolution Method**: `JWKS_URL` (fetch public keys from JWKS endpoint) or `PEM` (use provided PEM-encoded certificate)
* **Scope Mappings**: Map external scopes to domain scopes (e.g., `external:read` → `domain:read`)
* **User Binding**: Optionally resolve external subject to a domain user via EL expressions

### Delegation Depth

Delegation depth tracks the number of nested `act` claims in a token. Each delegation adds one level. The `maxDelegationDepth` setting (1-100, default 25) prevents unbounded delegation chains.

```
resultingDepth = 1 + max(subjectTokenDepth, actorTokenDepth)
```

If the resulting depth exceeds `maxDelegationDepth`, the request is rejected with `Delegation depth exceeds maximum allowed depth of <maxDelegationDepth>`.

### User Binding

User binding resolves an external token's subject to a domain user. Each binding criterion specifies:

* **Attribute**: User attribute to match (e.g., `email`, `username`)
* **Expression**: EL expression evaluated against token claims (e.g., `{#token['email']}`)

The system evaluates all criteria and matches users. If zero users match, the error is `No user found matching binding criteria`. If multiple users match, the error is `Multiple users found matching binding criteria`. If user binding is disabled or no criteria are configured, a virtual user is created from token claims.

## Prerequisites

* OAuth 2.0 client configured with `urn:ietf:params:oauth:grant-type:token-exchange` grant type
* Token exchange enabled at domain level
* For external tokens: trusted issuer configured with valid key material (JWKS URL or PEM certificate)
* For user binding: domain users with attributes matching binding criteria
* For delegation: `allowDelegation` enabled at domain level

## Gateway Configuration

### Domain-Level Token Exchange Settings

Configure token exchange behavior at the domain level.

| Property | Type | Default | Description |
|:---------|:-----|:--------|:------------|
| `enabled` | boolean | `false` | Enable RFC 8693 OAuth 2.0 Token Exchange |
| `allowedSubjectTokenTypes` | Set<String> | `[ACCESS_TOKEN, REFRESH_TOKEN, ID_TOKEN]` | Token types accepted as `subject_token` |
| `allowedRequestedTokenTypes` | Set<String> | `[ACCESS_TOKEN]` | Token types that can be requested via `requested_token_type` |
| `allowImpersonation` | boolean | `true` | Allow token exchange without `actor_token` (impersonation) |
| `allowDelegation` | boolean | `false` | Allow token exchange with `actor_token` (delegation) |
| `allowedActorTokenTypes` | Set<String> | `[ACCESS_TOKEN, REFRESH_TOKEN, ID_TOKEN]` | Token types accepted as `actor_token` when delegation enabled |
| `maxDelegationDepth` | int | `25` | Maximum depth of nested "act" claims (1-100) |

### Trusted Issuer Configuration

Configure external JWT issuers trusted for token exchange.

| Property | Type | Description |
|:---------|:-----|:------------|
| `issuer` | String | Issuer URL (must match JWT `iss` claim) |
| `keyResolutionMethod` | Enum | `JWKS_URL` or `PEM` |
| `jwksUri` | String | JWKS endpoint URL (required when method is `JWKS_URL`) |
| `certificate` | String | PEM-encoded certificate (required when method is `PEM`) |
| `scopeMappings` | Map<String, String> | External scope → domain scope mappings |
| `userBindingEnabled` | boolean | Enable user binding via EL expressions |
| `userBindingCriteria` | List<UserBindingCriterion> | EL expressions to resolve external subject to domain user |

**User Binding Criterion:**

| Property | Type | Description |
|:---------|:-----|:------------|
| `attribute` | String | User attribute to match (e.g., `email`, `username`) |
| `expression` | String | EL expression evaluated against token claims (e.g., `{#token['email']}`) |

### Client-Level Scope Handling

Override scope handling mode at the client level.

| Property | Type | Default | Description |
|:---------|:-----|:--------|:------------|
| `inherited` | boolean | `true` | Inherit scope handling from domain settings |
| `scopeHandling` | Enum | `DOWNSCOPING` | `DOWNSCOPING` or `PERMISSIVE` |

## Creating a Token Exchange Request

To exchange a token, send a POST request to the token endpoint with `grant_type` set to `urn:ietf:params:oauth:grant-type:token-exchange`.

1. Include the `subject_token` and `subject_token_type` parameters to specify the token being exchanged.
2. Optionally include `requested_token_type` to specify the desired output token type (defaults to access token if allowed).
3. For delegation, include `actor_token` and `actor_token_type` to preserve the actor's identity in the resulting token.
4. Optionally include `scope` to request a subset of allowed scopes, or omit to receive all allowed scopes.
5. The response includes the issued token in the `access_token` field, with `issued_token_type` indicating the actual token type returned.

**Example Impersonation Request:**

```http
POST /oauth/token HTTP/1.1
Content-Type: application/x-www-form-urlencoded

grant_type=urn:ietf:params:oauth:grant-type:token-exchange
&subject_token=eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9...
&subject_token_type=urn:ietf:params:oauth:token-type:access_token
&requested_token_type=urn:ietf:params:oauth:token-type:access_token
&scope=openid profile
&client_id=my-client
&client_secret=my-secret
```

**Example Delegation Request:**

```http
POST /oauth/token HTTP/1.1
Content-Type: application/x-www-form-urlencoded

grant_type=urn:ietf:params:oauth:grant-type:token-exchange
&subject_token=eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9...
&subject_token_type=urn:ietf:params:oauth:token-type:access_token
&actor_token=eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9...
&actor_token_type=urn:ietf:params:oauth:token-type:access_token
&requested_token_type=urn:ietf:params:oauth:token-type:access_token
&client_id=my-client
&client_secret=my-secret
```

## Managing Trusted Issuers

Configure trusted issuers via the domain settings UI.

1. Navigate to the Token Exchange settings page and enable token exchange.
2. Add a trusted issuer by specifying the issuer URL, which must match the `iss` claim in incoming JWTs.
3. Select the key resolution method: use `JWKS_URL` to fetch public keys from a JWKS endpoint, or `PEM` to provide a PEM-encoded certificate directly.
4. Optionally configure scope mappings to translate external scopes to domain scopes (the UI provides autocomplete for domain scopes).
5. Enable user binding and define binding criteria to resolve external subjects to domain users via EL expressions evaluated against token claims.

## End-user Configuration

### Token Exchange Request Parameters

| Parameter | Type | Required | Description |
|:----------|:-----|:---------|:------------|
| `grant_type` | String | Yes | Must be `urn:ietf:params:oauth:grant-type:token-exchange` |
| `subject_token` | String | Yes | Security token representing the subject |
| `subject_token_type` | String | Yes | Type URI of subject token (e.g., `urn:ietf:params:oauth:token-type:access_token`) |
| `requested_token_type` | String | No | Type URI of requested token (defaults to `access_token` if allowed) |
| `actor_token` | String | No | Security token representing the actor (delegation only) |
| `actor_token_type` | String | Conditional | Type URI of actor token (required when `actor_token` provided) |
| `scope` | String | No | Space-delimited scopes (subset of allowed scopes) |
| `resource` | String | No | Target resource URIs |

### Token Exchange Response

**Access Token Response:**

```json
{
  "access_token": "eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "Bearer",
  "expires_in": 3600,
  "issued_token_type": "urn:ietf:params:oauth:token-type:access_token",
  "scope": "openid profile"
}
```

**ID Token Response:**

```json
{
  "access_token": "eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "N_A",
  "expires_in": 3600,
  "issued_token_type": "urn:ietf:params:oauth:token-type:id_token"
}
```

### Delegation Claims

When delegation is enabled and `actor_token` is provided, the issued token includes an `act` claim identifying the actor:

* `sub` - The actor's subject identifier
* `gis` - The actor's internal subject identifier (source and user ID)
