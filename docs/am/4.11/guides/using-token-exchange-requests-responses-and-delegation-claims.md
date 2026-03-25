# Using Token Exchange: Requests, Responses, and Delegation Claims

## Creating a Token Exchange Request

To exchange a token, send a POST request to the token endpoint with `grant_type=urn:ietf:params:oauth:grant-type:token-exchange`. Include `subject_token` (the token to exchange) and `subject_token_type` (its type URI). Optionally specify `requested_token_type` (defaults to `ACCESS_TOKEN` if allowed), `scope` (space-delimited scopes), and `resource` (target resource URIs). For delegation, include `actor_token` and `actor_token_type`. Authenticate the client using its configured method (client credentials, JWT bearer, etc.).

The gateway validates the subject token's signature and temporal claims, resolves the user (via trusted issuer binding if applicable), computes allowed scopes based on the configured mode, and issues a new token. The response includes `access_token`, `token_type`, `expires_in`, `issued_token_type`, and `scope` (unless `requested_token_type` is `ID_TOKEN`, in which case `scope` is omitted).

## Managing Trusted Issuers

Administrators configure trusted issuers in the domain settings UI. Navigate to the Token Exchange settings page and add a new trusted issuer. Enter the issuer URL (must match the `iss` claim in external JWTs). Select the key resolution method: choose `JWKS_URL` and provide the JWKS endpoint, or choose `PEM` and paste the PEM-encoded certificate. Optionally configure scope mappings to translate external scopes to domain scopes. Enable user binding and define criteria (attribute + EL expression pairs) to match external token claims to domain users. Save the configuration.

When a token exchange request includes a subject or actor token from this issuer, the gateway verifies the signature using the configured key, applies scope mappings, and resolves the user via binding criteria if enabled.

## End-User Configuration

### Token Exchange Request Parameters

Clients submit token exchange requests with the following parameters:

| Parameter | Required | Description |
|:----------|:---------|:------------|
| `grant_type` | Yes | Must be `urn:ietf:params:oauth:grant-type:token-exchange` |
| `subject_token` | Yes | The token representing the subject |
| `subject_token_type` | Yes | Type URI of `subject_token` (e.g., `urn:ietf:params:oauth:token-type:access_token`) |
| `requested_token_type` | No | Type URI of requested token (defaults to `ACCESS_TOKEN` if allowed) |
| `scope` | No | Space-delimited scopes to request |
| `resource` | No | Target resource URIs (used for scope resolution) |
| `actor_token` | No | Token representing the actor (required for delegation) |
| `actor_token_type` | Conditional | Type URI of `actor_token` (required if `actor_token` is present) |

### Token Exchange Response

**Access Token Response:**

```json
{
  "access_token": "eyJhbGc...",
  "token_type": "Bearer",
  "expires_in": 3600,
  "issued_token_type": "urn:ietf:params:oauth:token-type:access_token",
  "scope": "openid profile"
}
```

**ID Token Response:**

```json
{
  "access_token": "eyJhbGc...",
  "token_type": "N_A",
  "expires_in": 3600,
  "issued_token_type": "urn:ietf:params:oauth:token-type:id_token"
}
```

### Delegation Claims

When delegation is enabled and `actor_token` is provided, the issued access token includes an `act` claim:

```json
{
  "act": {
    "sub": "actor-subject-id",
    "gis": "actor-gis-id",
    "act": { ... }
  },
  "client_id": "requesting-client-id",
  "sub": "subject-id",
  "iss": "https://domain.example.com",
  "aud": ["client-id"],
  "exp": 1234567890,
  "iat": 1234564290,
  "scope": "openid profile"
}
```

The `act` claim contains the actor's `sub` (subject identifier), optional `gis` (Gravitee Internal Subject), and any nested `act` claim from the subject or actor token, preserving the full delegation chain.
