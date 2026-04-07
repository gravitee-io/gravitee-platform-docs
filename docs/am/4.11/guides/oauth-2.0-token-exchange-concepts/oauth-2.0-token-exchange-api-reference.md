# OAuth 2.0 Token Exchange API

## Token Exchange API

**Endpoint:** `POST /{domainPath}/oauth/token`

The client must authenticate on the token endpoint (e.g., using HTTP Basic authentication with `client_id` and `client_secret`).

### Request Parameters

| Parameter              | Required    | Description                                                                                                                |
| ---------------------- | ----------- | -------------------------------------------------------------------------------------------------------------------------- |
| `grant_type`           | Yes         | Must be `urn:ietf:params:oauth:grant-type:token-exchange`                                                                  |
| `subject_token`        | Yes         | The security token being exchanged                                                                                         |
| `subject_token_type`   | Yes         | URN identifying the type of the subject token                                                                              |
| `actor_token`          | No          | Token representing the acting party (delegation only)                                                                      |
| `actor_token_type`     | Conditional | Required when `actor_token` is present                                                                                     |
| `requested_token_type` | No          | Desired output token type (defaults to Access Token)                                                                       |
| `scope`                | No          | Space-delimited scopes to request (must be subset of allowed scopes)                                                       |
| `resource`             | No          | URI of the target resource server (affects scope resolution per [RFC 8707](https://datatracker.ietf.org/doc/html/rfc8707)) |

### Token Type URNs

| Short Name    | URN                                              |
| ------------- | ------------------------------------------------ |
| Access Token  | `urn:ietf:params:oauth:token-type:access_token`  |
| Refresh Token | `urn:ietf:params:oauth:token-type:refresh_token` |
| ID Token      | `urn:ietf:params:oauth:token-type:id_token`      |
| JWT           | `urn:ietf:params:oauth:token-type:jwt`           |

### Response Fields

| Field               | Description                                                     |
| ------------------- | --------------------------------------------------------------- |
| `access_token`      | The issued security token (also used for ID tokens)             |
| `issued_token_type` | URN of the issued token type                                    |
| `token_type`        | `Bearer` for access tokens, `N_A` for ID tokens                 |
| `expires_in`        | Token lifetime in seconds (bounded by subject token expiration) |
| `scope`             | Granted scopes (present for access tokens only)                 |

{% hint style="warning" %}
Token Exchange never returns a `refresh_token` or a separate `id_token` field. When an ID token is requested, it is returned in the `access_token` field.
{% endhint %}

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

The `token_type` is `"N_A"` and no `scope` is included in the response.

### Access Token JWT Claims (Delegation)

When delegation is used, the issued access token includes an `act` claim identifying the actor. For details on the `act` claim structure, chained delegation, and `actor_act`, see [Delegation](../using-oauth-2.0-token-exchange.md#delegation).

### Error Responses

All errors are returned as HTTP 400 with a JSON body containing `error` and `error_description`.

| Error Code        | Description                                                             |
| ----------------- | ----------------------------------------------------------------------- |
| `invalid_request` | `subject_token_type` is not in the allowed subject token types list     |
| `invalid_request` | `requested_token_type` is not in the allowed requested token types list |
| `invalid_request` | Delegation is not allowed for this domain                               |
| `invalid_request` | `actor_token_type` is required when `actor_token` is present            |
| `invalid_request` | `actor_token_type` is not in the allowed actor token types list         |
| `invalid_request` | `actor_token_type` must not be provided without `actor_token`           |
| `invalid_request` | Maximum delegation depth exceeded                                       |
| `invalid_request` | Actor token must contain a `sub` claim                                  |
| `invalid_request` | Impersonation is not allowed for this domain                            |
| `invalid_scope`   | Requested scope is not a subset of allowed scopes                       |

## Audit Trail

Every token exchange operation is recorded as an audit event, regardless of outcome. The audit entry includes standard token creation details (client, user, grant type) plus Token Exchange-specific parameters:

| Audit Parameter        | Description                                                  |
| ---------------------- | ------------------------------------------------------------ |
| `GRANT_TYPE`           | `urn:ietf:params:oauth:grant-type:token-exchange`            |
| `REQUESTED_TOKEN_TYPE` | The issued token type URN                                    |
| `SUBJECT_TOKEN`        | The `jti` (token ID) of the subject token that was exchanged |
| `SUBJECT_TOKEN_TYPE`   | The URN of the subject token type                            |
| `ACTOR_TOKEN`          | The `jti` of the actor token (delegation only)               |
| `ACTOR_TOKEN_TYPE`     | The URN of the actor token type (delegation only)            |

These parameters allow administrators to trace exactly which tokens were involved in each exchange and whether the exchange was an impersonation or delegation scenario.
