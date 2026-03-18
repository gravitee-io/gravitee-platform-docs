### Request Examples

**Impersonation:**

**Delegation:**

### Response Examples

**Access Token:**

**ID Token Only:**

### Delegation Token Claims

When delegation is enabled and an `actor_token` is provided, the issued token includes an `act` claim identifying the actor. The `act` claim contains the actor's `sub` and optionally `gis`. If the subject token was already delegated, the subject's `act` claim is nested under the new `act` claim. If the actor token was delegated, the actor's `act` claim is stored in `actor_act`.

**Example:**

Delegation depth is calculated as `1 + max(subject_token_act_depth, actor_token_act_depth)`. If depth exceeds `maxDelegationDepth`, the request is rejected with "Delegation depth exceeds maximum allowed".

### Client Configuration

Clients must be configured with the `urn:ietf:params:oauth:grant-type:token-exchange` grant type. Navigate to **Applications > [Your Application] > Settings > OAuth 2.0 / OIDC** and enable the token exchange grant type. Configure allowed scopes and resource URIs as needed.

### Restrictions

- Token exchange must be enabled at the domain level (`enabled=true`)
- Clients must have the `urn:ietf:params:oauth:grant-type:token-exchange` grant type enabled
- `subject_token_type` must be in `allowedSubjectTokenTypes`
- `requested_token_type` must be in `allowedRequestedTokenTypes`
- `actor_token_type` must be in `allowedActorTokenTypes` (when `actor_token` is present)
- Impersonation requires `allowImpersonation=true`
- Delegation requires `allowDelegation=true`
- Delegation depth cannot exceed `maxDelegationDepth` (1-100, default 25)
- No refresh tokens are issued during token exchange
- ID token-only responses return the ID token in the `access_token` field with `token_type="N_A"`
- Trusted issuer tokens must have a valid signature and matching `iss` claim
- User binding requires exactly one matching user; zero or multiple matches result in an error
- Scope downscoping is enforced by default; permissive mode ignores subject token scopes

### Related Changes

The token exchange feature introduces audit events for `REQUESTED_TOKEN_TYPE`, `SUBJECT_TOKEN` (JTI), `SUBJECT_TOKEN_TYPE`, `ACTOR_TOKEN` (JTI), and `ACTOR_TOKEN_TYPE`. The UI provides a tabbed interface for token exchange settings and trusted issuers, with autocomplete for domain scope selection in scope mappings. The gateway migrated to a unified `TokenRepository` interface, replacing separate `AccessTokenRepository` and `RefreshTokenRepository` interfaces. PRE_TOKEN and POST_TOKEN policies execute during token exchange with an `OAuth2Request` context.
