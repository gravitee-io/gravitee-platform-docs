
# Creating a Token Exchange Request


Clients initiate token exchange by sending a POST request to the `/oauth/token` endpoint with `grant_type=urn:ietf:params:oauth:grant-type:token-exchange`. The request must include the `subject_token` parameter with the JWT to be exchanged and `subject_token_type` with the corresponding token type URI. Optionally specify `requested_token_type` to request an access token or ID token (defaults to access token if allowed). Provide the `scope` parameter to request specific scopes, or omit it to receive all allowed scopes. Include `resource` parameters to target specific resource URIs, which affects the scope pool. For delegation, add `actor_token` and `actor_token_type` parameters. The gateway validates all parameters, resolves the user, computes granted scopes based on the configured scope handling mode, and returns a token response with the issued token, token type, expiration, and granted scopes.

```http
POST /oauth/token
Content-Type: application/x-www-form-urlencoded

grant_type=urn:ietf:params:oauth:grant-type:token-exchange
&subject_token=<JWT>
&subject_token_type=urn:ietf:params:oauth:token-type:access_token
&requested_token_type=urn:ietf:params:oauth:token-type:access_token
&scope=openid profile
&resource=https://api.example.com
&actor_token=<JWT>
&actor_token_type=urn:ietf:params:oauth:token-type:access_token
```

### Token Exchange Request Parameters

| Parameter | Required | Description |
|:----------|:---------|:------------|
| `grant_type` | Yes | Must be `urn:ietf:params:oauth:grant-type:token-exchange` |
| `subject_token` | Yes | The security token representing the subject |
| `subject_token_type` | Yes | Type URI of the subject token |
| `requested_token_type` | No | Defaults to `ACCESS_TOKEN` if allowed; otherwise required |
| `scope` | No | Requested scopes (subject to downscoping or permissive rules) |
| `resource` | No | Target resource URIs (affects scope pool) |
| `actor_token` | No | Token representing the actor (delegation only) |
| `actor_token_type` | No | Type URI of the actor token (required when `actor_token` present) |

### Token Exchange Response (Access Token)

When the gateway issues an access token, the response includes the following fields:

| Field | Description |
|:------|:------------|
| `access_token` | The issued token (JWT) |
| `token_type` | Always `Bearer` for access tokens |
| `expires_in` | Lifetime in seconds (capped by subject token expiration if set) |
| `issued_token_type` | Type URI of the issued token |
| `scope` | Granted scopes (may differ from requested) |

No `refresh_token` is issued during token exchange. Granted scopes may differ from requested scopes based on the scope handling mode. The `expires_in` value is capped by the subject token expiration if set.

### Token Exchange Response (ID Token)

When `requested_token_type=urn:ietf:params:oauth:token-type:id_token`, the gateway returns an ID token in the `access_token` field:

| Field | Description |
|:------|:------------|
| `access_token` | Contains the ID token JWT |
| `token_type` | `N_A` (per RFC 8693 for non-access tokens) |
| `expires_in` | Lifetime in seconds |
| `issued_token_type` | Type URI of the issued token |

The `scope` field is omitted in ID token responses because ID tokens are for identity, not authorization.
