# Token Exchange API Reference

## Token Exchange Request Parameters

Clients call the token endpoint with the following parameters:

| Parameter | Required | Description | Example |
|:----------|:---------|:------------|:--------|
| `grant_type` | Yes | Must be `urn:ietf:params:oauth:grant-type:token-exchange` | `urn:ietf:params:oauth:grant-type:token-exchange` |
| `subject_token` | Yes | JWT string to exchange | `eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9...` |
| `subject_token_type` | Yes | URN identifying subject token type | `urn:ietf:params:oauth:token-type:access_token` |
| `requested_token_type` | No | URN identifying desired token type (defaults to access token) | `urn:ietf:params:oauth:token-type:id_token` |
| `scope` | No | Space-separated scopes (defaults to full allowed set) | `openid profile` |
| `resource` | No | Target resource URI(s) | `https://api.example.com` |
| `actor_token` | No | JWT string identifying the actor (delegation only) | `eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9...` |
| `actor_token_type` | No | URN identifying actor token type (required if `actor_token` present) | `urn:ietf:params:oauth:token-type:access_token` |

### Example Request (Impersonation)

```bash
curl -X POST https://am-gateway/{domain}/oauth/token \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "grant_type=urn:ietf:params:oauth:grant-type:token-exchange" \
  -d "client_id=my-client" \
  -d "client_secret=my-secret" \
  -d "subject_token=eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9..." \
  -d "subject_token_type=urn:ietf:params:oauth:token-type:access_token" \
  -d "scope=openid profile"
```

## Token Exchange Response (Access Token)

When `requested_token_type` is omitted or set to `urn:ietf:params:oauth:token-type:access_token`, the response includes:

| Field | Description | Example |
|:------|:------------|:--------|
| `access_token` | JWT access token | `eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9...` |
| `token_type` | Always `Bearer` | `Bearer` |
| `expires_in` | Token lifetime in seconds | `3600` |
| `issued_token_type` | URN confirming token type | `urn:ietf:params:oauth:token-type:access_token` |
| `scope` | Granted scopes (space-separated) | `openid profile` |

### Example Response

```json
{
  "access_token": "eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "Bearer",
  "expires_in": 3600,
  "issued_token_type": "urn:ietf:params:oauth:token-type:access_token",
  "scope": "openid profile"
}
```

## Token Exchange Response (ID Token)

When `requested_token_type` is `urn:ietf:params:oauth:token-type:id_token`, the response includes:

| Field | Description | Example |
|:------|:------------|:--------|
| `access_token` | JWT ID token (per RFC 8693 Section 2.2.1) | `eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9...` |
| `token_type` | Always `N_A` | `N_A` |
| `expires_in` | Token lifetime in seconds | `3600` |
| `issued_token_type` | URN confirming token type | `urn:ietf:params:oauth:token-type:id_token` |

No `scope` or `refresh_token` is included in ID token responses.

## Related Changes

The token exchange feature introduces a new grant type (`urn:ietf:params:oauth:grant-type:token-exchange`) registered in the `CompositeTokenGranter`. The domain settings UI adds a Token Exchange section with controls for enabling the feature, configuring allowed token types, enabling impersonation/delegation, setting delegation depth limits, and managing trusted issuers. The trusted issuer UI includes autocomplete for domain scopes in scope mapping fields and validates issuer URLs, key resolution methods, and user binding criteria. Audit logs capture token exchange parameters (`REQUESTED_TOKEN_TYPE`, `SUBJECT_TOKEN`, `SUBJECT_TOKEN_TYPE`, `ACTOR_TOKEN`, `ACTOR_TOKEN_TYPE`) for compliance tracking. The token service generates exchanged tokens with `client_id` and `act` claims, and the scope computation logic integrates with the existing `ProtectedResourceManager` to resolve resource-based scopes. Error responses use standard OAuth2 error codes (`invalid_grant`, `invalid_scope`, `invalid_request`) with descriptive messages for validation failures.
