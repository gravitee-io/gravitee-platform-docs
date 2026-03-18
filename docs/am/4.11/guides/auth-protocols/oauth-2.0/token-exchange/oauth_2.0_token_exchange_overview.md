OAuth 2.0 Token Exchange (RFC 8693) enables secure token transformation and delegation for multi-hop architectures, AI agents, and distributed services. Clients exchange an existing token (subject token) for a new token with reduced scope, different type, or delegated authority. This feature supports both impersonation (acting as the user) and delegation (acting on behalf of the user with an auditable actor chain).

### Impersonation vs. delegation

**Impersonation** allows a client to exchange a user's token for a new token representing the same user, typically with reduced scope. The new token contains no `act` claim. Use this when a backend service needs to call another service as the user without introducing an intermediary identity.

**Delegation** requires an `actor_token` parameter and produces a token with an `act` claim identifying the actor (e.g., an AI agent or service). The `act` claim can nest recursively to represent multi-hop chains (user → agent → MCP server → tool). Use this when you need auditable proof of who acted on whose behalf.

| Mode | `actor_token` | `act` claim | Use case |
|:-----|:--------------|:------------|:---------|
| Impersonation | absent | none | Backend service calls API as user |
| Delegation | present | nested JSON | AI agent acts on behalf of user |

### Scope resolution modes

Token exchange enforces scope restrictions to prevent privilege escalation. Two modes control how scopes are granted:

**Downscoping (default):** The granted scopes are the intersection of requested scopes, subject token scopes, and the union of client and resource scopes. Subject token scopes act as a ceiling.

**Example:** Subject has `{read, write}`, client allows `{read, delete}`, request asks for `{read, write}` → granted `{read}`.

**Permissive:** Subject token scopes are ignored. Granted scopes are the intersection of requested scopes and the union of client and resource scopes. Use this when the subject token comes from an external issuer whose scopes don't map directly to your domain.

### Trusted issuers

Trusted issuers allow token exchange with tokens issued by external identity providers. Configure the issuer URL, key resolution method (JWKS URL or PEM certificate), and optional scope mappings to translate external scopes into domain scopes. Enable user binding to resolve external token subjects to domain users via Expression Language criteria (e.g., match `email` claim to user email attribute).
