# OAuth 2.0 Token Exchange API Reference

## Token Exchange API

### Request Parameters

| Parameter | Required | Description |
|:----------|:---------|:------------|
| `grant_type` | Yes | Must be `urn:ietf:params:oauth:grant-type:token-exchange` |
| `subject_token` | Yes | JWT string representing the subject |
| `subject_token_type` | Yes | URN identifying subject token type (access, refresh, or ID token) |
| `requested_token_type` | No | URN identifying requested token type (defaults to access token) |
| `scope` | No | Space-separated scopes (defaults to full allowed set) |
| `resource` | No | Target resource URI |
| `actor_token` | No | JWT string representing the actor (required for delegation) |
| `actor_token_type` | No | URN identifying actor token type (required when `actor_token` is present) |

### Response (Access Token)

```json
{
  "access_token": "eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "Bearer",
  "expires_in": 3600,
  "issued_token_type": "urn:ietf:params:oauth:token-type:access_token",
  "scope": "openid profile"
}
```

### Response (ID Token)

```json
{
  "access_token": "eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "N_A",
  "expires_in": 3600,
  "issued_token_type": "urn:ietf:params:oauth:token-type:id_token"
}
```

### Access Token JWT Claims (Delegation)

When delegation is used, the access token includes an `act` claim:

```json
{
  "iss": "https://auth.example.com",
  "sub": "user-123",
  "aud": "client-id",
  "exp": 1735689600,
  "iat": 1735686000,
  "jti": "token-jti",
  "client_id": "client-id",
  "scope": "openid profile",
  "act": {
    "sub": "actor-sub-789",
    "gis": "actor-gis-456",
    "act": { "sub": "prior-actor" }
  }
}
```

The `act` claim contains the actor's `sub` (required), optional `gis` (Gravitee Internal Subject), and nested `act` claims from prior delegation chains.

### Error Responses

| Error Code | Condition |
|:-----------|:----------|
| `invalid_request` | Missing required parameters, unsupported token types, impersonation/delegation not allowed |
| `invalid_grant` | Token expired, not yet valid, revoked, signature verification failed, delegation depth exceeded |
| `invalid_scope` | Requested scopes not allowed |
