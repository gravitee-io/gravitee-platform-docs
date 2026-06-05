# Agent Applications Restrictions and Related Changes

## Restrictions

- SPIRE local-stack testing requires Docker Compose 2.x; `docker-compose` v1 is not supported.
- CIMD document fetches are subject to the domain-level `cimdSettings.fetchTimeoutMs` timeout (default 5000ms); slow endpoints may time out.
- Trust domain JWKS bundles are cached per `refreshIntervalSeconds`; manual refresh requires updating the trust domain or evicting the cache.
- Prefix match mode is only allowed for Hosted Delegated and Autonomous agents; User-Embedded agents must use Exact Match mode.
- Applications created from CIMD documents cannot use `client_secret_basic`, `client_secret_post`, or `client_secret_jwt` authentication methods.
- For User-Embedded agents, the `act.sub` claim uses the agent instance ID when known; if the instance ID is unavailable (e.g., no SPIFFE assertion), `act.sub` falls back to the blueprint `client_id`.
- Agent applications prohibit `implicit`, `password`, and `refresh_token` grant types.
- User-Embedded and Hosted Delegated agents require at least one redirect URI.
- Autonomous agents cannot use the `authorization_code` grant.
- User-Embedded agents cannot use the `client_credentials` grant.
- JWKS URLs resolving to private, loopback, or link-local IP addresses are rejected unless the domain sets `allowPrivateIpAddress`.

## Related Changes

AM 4.12 introduces the following changes to support AI agent authentication:

### Database Schema
- A new `sub_type` column is added to the `applications` table.
- A new `trust_domains` table is created.

### Management Console UI
- A top-level **Agents** navigation entry is added, providing a dedicated agent list and creation wizard separate from the **Applications** area.
- The **Applications** list now excludes agent-type applications.
- A new **Workload Identity** section is available under **Domain Settings** to manage trust domains.
- The application creation wizard includes a **Manual / CIMD** toggle on step 2 when CIMD is enabled. A CIMD confirmation step displays a read-only metadata preview.

### Application Configuration
- Agent applications can now be marked as DCR/CIMD registration templates. The previous restriction preventing this configuration is removed.

### Token Claims
Tokens issued for Hosted Delegated and User-Embedded agents include the following claims:

- `act.sub`: Set to the agent instance ID when available.
- `act.sub_profile`: Identifies the agent persona.
- `client_profile`: Emits `"ai_agent <persona>"` (e.g., `"ai_agent autonomous"`).

### Authentication Assertion Types
- **SPIFFE JWT-SVID authentication**: Uses the assertion type `urn:ietf:params:oauth:client-assertion-type:jwt-spiffe`.
- **Agent JWT-bearer authentication**: Uses the assertion type `urn:ietf:params:oauth:client-assertion-type:agent-jwt-bearer`.
- **Standard `jwt-bearer` assertions**: Now strictly follow RFC 7523, requiring `iss == sub == client_id`.

### FAPI Compliance
FAPI signing-algorithm checks now apply to agent JWTs.

