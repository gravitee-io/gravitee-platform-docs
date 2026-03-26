# Using OAuth 2.0 Token Exchange

## Impersonation

In an impersonation exchange, the client presents a `subject_token` without an `actor_token`. The issued token represents the subject's identity directly — there is no indication that a different party performed the exchange.

### Example Request

```bash
curl -X POST https://auth.example.com/your-domain/oauth/token \
  -u "client_id:client_secret" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "grant_type=urn:ietf:params:oauth:grant-type:token-exchange" \
  -d "subject_token=eyJhbGciOi..." \
  -d "subject_token_type=urn:ietf:params:oauth:token-type:access_token"
```

### Example Response

```json
{
  "access_token": "eyJhbGciOi...",
  "token_type": "Bearer",
  "expires_in": 3600,
  "issued_token_type": "urn:ietf:params:oauth:token-type:access_token",
  "scope": "openid profile"
}
```

### Scope Resolution (Impersonation)

By default, with **Downscoping** Scope Handling, the granted scopes are computed as:

```
allowedScopes = subjectTokenScopes ∩ clientScopes
allowedDefaultScopes = subjectTokenScopes ∩ clientDefaultScopes
grantedScopes = requestedScopes (if subset of allowedScopes) OR allowedDefaultScopes (if no scope requested)
```

If the `scope` parameter is provided, every requested scope must be within the allowed set or the request is rejected with `invalid_scope`.

With **Permissive** Scope Handling, `allowedScopes = clientScopes` and `allowedDefaultScopes = clientDefaultScopes`.

### Requesting an ID Token

To receive an ID token instead of an access token, set `requested_token_type` to the ID token URN:

**Request:**

```bash
curl -X POST https://auth.example.com/your-domain/oauth/token \
  -u "client_id:client_secret" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "grant_type=urn:ietf:params:oauth:grant-type:token-exchange" \
  -d "subject_token=eyJhbGciOi..." \
  -d "subject_token_type=urn:ietf:params:oauth:token-type:access_token" \
  -d "requested_token_type=urn:ietf:params:oauth:token-type:id_token"
```

**Response:**

```json
{
  "access_token": "eyJhbGciOi...",
  "token_type": "N_A",
  "expires_in": 3600,
  "issued_token_type": "urn:ietf:params:oauth:token-type:id_token"
}
```

The `token_type` is `"N_A"` and no `scope` is included in the response.

## Delegation

In a delegation exchange, the client presents both a `subject_token` and an `actor_token`. The issued token includes an `act` claim that records the actor's identity, making it clear that one party is acting on behalf of another.

**Allow Delegation** must be enabled in the domain's Token Exchange settings.

### Example Request

```bash
curl -X POST https://auth.example.com/your-domain/oauth/token \
  -u "client_id:client_secret" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "grant_type=urn:ietf:params:oauth:grant-type:token-exchange" \
  -d "subject_token=eyJhbGciOi..." \
  -d "subject_token_type=urn:ietf:params:oauth:token-type:access_token" \
  -d "actor_token=eyJhbGciOi..." \
  -d "actor_token_type=urn:ietf:params:oauth:token-type:access_token"
```

### Example Response

```json
{
  "access_token": "eyJhbGciOi...",
  "token_type": "Bearer",
  "expires_in": 3600,
  "issued_token_type": "urn:ietf:params:oauth:token-type:access_token",
  "scope": "openid profile"
}
```

### Scope Resolution (Delegation)

For delegation, the actor's scopes also constrain what can be granted.

By default, with **Downscoping** Scope Handling, the granted scopes are computed as:

```
allowedScopes = (subjectTokenScopes ∩ actorTokenScopes) ∩ clientScopes
allowedDefaultScopes = (subjectTokenScopes ∩ actorTokenScopes) ∩ clientDefaultScopes
grantedScopes = requestedScopes (if subset of allowedScopes) OR allowedDefaultScopes (if no scope requested)
```

With **Permissive** Scope Handling, `allowedScopes = clientScopes` and `allowedDefaultScopes = clientDefaultScopes`.

### Chained Delegation

A delegated token can itself be used as a `subject_token` in a subsequent delegation exchange. This creates a chain of `act` claims that records the full delegation history.

**Step 1: First delegation (depth 0 → 1):**

Actor A exchanges User's token:

```json
{
  "sub": "user-123",
  "act": {
    "sub": "actor-A",
    "gis": "source:actor-A"
  }
}
```

**Step 2: Second delegation (depth 1 → 2):**

Actor B exchanges the token from Step 1:

```json
{
  "sub": "user-123",
  "act": {
    "sub": "actor-B",
    "gis": "source:actor-B",
    "act": {
      "sub": "actor-A",
      "gis": "source:actor-A"
    }
  }
}
```

### Actor's Own Delegation Chain (actor\_act)

When the actor token is itself a delegation token (i.e., it already contains an `act` claim), the issued token preserves the actor's delegation chain as `actor_act` inside the top-level `act` claim. This provides complete audit traceability of how the actor obtained its own token.

```json
{
  "sub": "user-123",
  "act": {
    "sub": "service-B",
    "gis": "source:service-B",
    "actor_act": {
      "sub": "service-A",
      "gis": "source:service-A"
    }
  }
}
```

In this example, Service B is acting on behalf of user-123 and Service B's own token was previously obtained via delegation from Service A. The `actor_act` field records that lineage.

{% hint style="info" %}
`actor_act` is distinct from the nested `act` chain. The nested `act` tracks the _subject token's_ prior delegation history, while `actor_act` tracks the _actor token's_ own delegation history.
{% endhint %}

## Example Use Cases

### MCP Server

The [Model Context Protocol (MCP)](https://modelcontextprotocol.io/) defines how AI agents connect to external tools and data sources. MCP servers can use Token Exchange to obtain scoped-down tokens that let them act on behalf of users.

**Setup:**

1. Create an application with the **MCP Server** application type (or a standard Web application).
2. Enable the `urn:ietf:params:oauth:grant-type:token-exchange` grant type on the application.
3. Enable **Allow Delegation** and select **Downscoping** Scope Handling in the domain's Token Exchange settings.

**Flow:**

1. The user authenticates and obtains an access token.
2. The user's client passes the access token to the MCP server.
3. The MCP server exchanges the user's token for a scoped-down delegated token using its own credentials.
4. The MCP server uses the new token to access APIs on behalf of the user.

**Example:**

```bash
curl -X POST https://auth.example.com/your-domain/oauth/token \
  -u "mcp-server-client-id:mcp-server-secret" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "grant_type=urn:ietf:params:oauth:grant-type:token-exchange" \
  -d "subject_token=<user-access-token>" \
  -d "subject_token_type=urn:ietf:params:oauth:token-type:access_token" \
  -d "actor_token=<mcp-server-token>" \
  -d "actor_token_type=urn:ietf:params:oauth:token-type:access_token" \
  -d "scope=openid profile"
```

The response contains a delegated access token with an `act` claim identifying the MCP server as the actor.

### AI Agent Acting on Behalf of a User

An AI agent (e.g., a travel assistant) needs to call third-party APIs, such as a hotel booking service, on behalf of an authenticated user. Token Exchange with delegation lets the agent obtain a scoped-down token that proves the user authorized the action, while the `act` claim identifies the AI agent as the party performing it.

**Flow:**

1. The user authenticates and grants the AI agent permission to manage bookings.
2. The AI agent's backend exchanges the user's access token for a delegated token scoped to the booking API.
3. The booking API receives the token, verifies that the `sub` claim is the user and the `act` claim identifies the AI agent, and processes the reservation.

**Example:**

```bash
curl -X POST https://auth.example.com/your-domain/oauth/token \
  -u "ai-travel-agent-id:ai-travel-agent-secret" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "grant_type=urn:ietf:params:oauth:grant-type:token-exchange" \
  -d "subject_token=<user-access-token>" \
  -d "subject_token_type=urn:ietf:params:oauth:token-type:access_token" \
  -d "actor_token=<ai-agent-token>" \
  -d "actor_token_type=urn:ietf:params:oauth:token-type:access_token" \
  -d "scope=bookings:write"
```

The issued token's `act` claim identifies the AI agent, so the booking API can distinguish the authorizing user (`sub`) from the performing agent (`act`).

### Microservice Delegation Chain

In a microservice architecture, a user request may traverse multiple services. Each service can exchange the incoming token for a new delegated token that adds its own identity to the `act` chain, creating a full trace of every service involved in handling the request.

**Flow:**

1. The user calls the **API Gateway**, which holds the user's access token.
2. The API Gateway exchanges the token with its own actor identity and forwards the delegated token to **Service A**.
3. Service A exchanges the delegated token with its own actor identity and calls **Service B**.
4. Service B receives a token with a nested `act` chain: `Service A → API Gateway`.

**Example — Service A calling Service B:**

```bash
curl -X POST https://auth.example.com/your-domain/oauth/token \
  -u "service-a-id:service-a-secret" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "grant_type=urn:ietf:params:oauth:grant-type:token-exchange" \
  -d "subject_token=<delegated-token-from-gateway>" \
  -d "subject_token_type=urn:ietf:params:oauth:token-type:access_token" \
  -d "actor_token=<service-a-token>" \
  -d "actor_token_type=urn:ietf:params:oauth:token-type:access_token" \
  -d "scope=openid orders:read"
```

The resulting token payload:

```json
{
  "sub": "user-123",
  "scope": "openid orders:read",
  "act": {
    "sub": "service-a",
    "gis": "source:service-a",
    "act": {
      "sub": "api-gateway",
      "gis": "source:api-gateway"
    }
  }
}
```

Each service in the chain can inspect the `act` claim to understand the full delegation path. The **Maximum Delegation Depth** setting controls how many hops are allowed.

### Service Account Impersonation

An admin service or batch job needs to perform actions as a specific user — for example, a data migration tool updating user profiles, or a support tool accessing a user's resources for troubleshooting. Token Exchange with impersonation lets the service obtain a token that represents the user directly, with a bounded lifetime and narrowed scopes.

**Flow:**

1. The admin service authenticates and obtains the target user's token (e.g., via a prior authorization or admin API).
2. The admin service exchanges the user's token via impersonation to get a new token scoped to only the permissions needed for the task.
3. The issued token represents the user with no `act` claim — downstream services see it as a regular user token.

**Example:**

```bash
curl -X POST https://auth.example.com/your-domain/oauth/token \
  -u "admin-service-id:admin-service-secret" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "grant_type=urn:ietf:params:oauth:grant-type:token-exchange" \
  -d "subject_token=<user-access-token>" \
  -d "subject_token_type=urn:ietf:params:oauth:token-type:access_token" \
  -d "scope=profile:read"
```

The token's lifetime is bounded by the original subject token, and scopes are narrowed to only `profile:read`. The audit trail records the exchange, including the `client_id` of the admin service and the `jti` of the original subject token, even though the issued token itself carries the user's identity.

## Prerequisites

- OAuth2 client must have `urn:ietf:params:oauth:grant-type:token-exchange` grant type enabled
- Domain must have Token Exchange enabled in **Settings > OAuth 2.0 > Token Exchange**
- Subject token must be a valid JWT issued by the domain or a trusted issuer
- Actor token (if provided) must be a valid JWT issued by the domain or a trusted issuer
- Client must have `client_credentials` or equivalent authentication configured
- For trusted issuers: JWKS endpoint must be accessible or PEM certificate must be valid