# SPIFFE Workload Identity & Agent Applications: Concepts

## Key Concepts

### Agent Application Types

Agent applications represent autonomous or user-delegated AI workloads. Three agent personas define the operational model:

| Persona | Description | Redirect URI Required | Allowed Grants |
|:--------|:------------|:---------------------|:---------------|
| **User Embedded** | Agent acts on behalf of an authenticated user within a user session | Yes | `authorization_code`, `urn:ietf:params:oauth:grant-type:jwt-bearer` |
| **Hosted Delegated** | Agent acts on behalf of a user but runs in a separate hosting environment | Yes | `authorization_code`, `urn:ietf:params:oauth:grant-type:jwt-bearer` |
| **Autonomous** | Agent acts independently without user delegation | No | `client_credentials`, `urn:ietf:params:oauth:grant-type:jwt-bearer` |

Agent applications cannot use `implicit`, `password`, or `refresh_token` grants. User Embedded and Hosted Delegated agents require at least one redirect URI. Token endpoint authentication must use certificate-based methods (`private_key_jwt`, `tls_client_auth`, `self_signed_tls_client_auth`, `spiffe_jwt`, or `agent-jwt-bearer`) — secret-based methods are forbidden. Agent applications can be marked as DCR/CIMD registration templates; the blueprint `client_id` is permitted as `software_id` in DCR requests.

### Trust Domains

A trust domain is a domain-scoped entity holding a name, JWKS URL, allowed signature algorithms, and a refresh interval. Each trust domain configuration specifies how Access Management validates JWT-SVIDs issued by a SPIRE deployment. Trust domains are managed through the Workload Identity settings area under domain settings.

| Property | Description | Example |
|:---------|:------------|:--------|
| **Name** | Human-readable trust domain identifier | `production.acme.com` |
| **Bundle Source** | How the trust bundle is obtained | JWKS URL, Static JWKS |
| **JWKS URL** | Remote endpoint serving the trust bundle (when Bundle Source is JWKS URL) | `https://spire.acme.com/keys` |
| **Refresh Interval (seconds)** | How often to fetch the trust bundle from the JWKS URL | `3600` |
| **Allowed Algorithms** | Permitted JWT signing algorithms for SVIDs from this trust domain | `RS256`, `ES256` |

The trust bundle service caches bundles per trust domain, honors the per-domain refresh interval, and serves the last known good bundle on transient fetch errors.

### SPIFFE Subject Matching

SPIFFE subject matching determines how an application's configured subject is compared to the SVID `sub` claim:

**Exact** (default): The SVID `sub` must exactly match the configured subject (e.g., `spiffe://acme.com/billing-agent`). Use for single-instance workloads or when the SPIRE deployment issues one SVID per registered application.

**Prefix**: The SVID `sub` must start with the configured subject. The configured subject must end with `/` to ensure path-boundary matching and prevent partial path matches (e.g., `spiffe://acme.com/hotel-agent/` matches `spiffe://acme.com/hotel-agent/instance-42` but not `spiffe://acme.com/hotel-agent-v2`). Prefix mode is restricted to Hosted Delegated and Autonomous agent applications. When a prefix match succeeds, Access Management synthesizes a per-instance client identity with `agentInstanceId` set to the full SVID `sub`, enabling per-instance delegation chains in issued tokens.

### SVID Validation

SPIFFE JWT-SVID validation enforces the following rules: `typ` header must be `JWT`; signing algorithm must be in the trust domain's allowed algorithms list (no `none` or HMAC algorithms); `sub` must be a SPIFFE ID inside the configured trust domain; `aud` must contain the Access Management token endpoint URL; `iat`, `exp`, and `nbf` claims must be within clock-skew tolerance and maximum lifetime bounds. These rules implement the SPIFFE JWT-SVID specification.

### Client Identity Metadata Document (CIMD)

CIMD allows administrators to create applications by referencing a hosted metadata document instead of manually entering OAuth/OIDC settings. A Manual / CIMD toggle appears on step 2 of the application creation wizard, shown only when CIMD is enabled on the domain. In CIMD mode the administrator supplies only the Document URL. Access Management fetches and validates the document server-side, then shows a read-only preview (a "CIMD confirm" step) of the parsed metadata before creation. The CIMD URL becomes the application's `client_id`.

Access Management validates the document against the same trust rules applied at runtime:

| Rule | Condition | Error Message |
|:-----|:----------|:--------------|
| CIMD enabled | Domain `oidc.cimdSettings.enabled=false` | "CIMD is not enabled for this domain." |
| URL shape | URL does not match `^https?://` | "CIMD url must be an http(s) URL." |
| Unsecured HTTP | `allowUnsecuredHttpUri=false` AND scheme is `http` | "Unsecured HTTP CIMD url is not allowed." |
| Allowed domains | `allowedDomains` non-empty AND host not in list | "CIMD url host is not in allowed domains." |
| Private IP | `allowPrivateIpAddress=false` AND host is private IP literal | "CIMD url resolves to a private or reserved IP address." |
| Private IP | `allowPrivateIpAddress=false` AND DNS resolves to private IP | "CIMD url resolves to a private or reserved IP address." |
| Secret-based auth | CIMD metadata `token_endpoint_auth_method` in {`client_secret_basic`, `client_secret_post`, `client_secret_jwt`} | "Secret-based token_endpoint_auth_method is not allowed for CIMD clients." |
| Max response size | Response exceeds `maxResponseSizeKb` | (HTTP fetch fails) |
| Fetch timeout | Fetch exceeds `fetchTimeoutMs` | (HTTP fetch fails) |

Access Management pre-populates all application settings (redirect URIs, grants, scopes, JWKS, mTLS, CIBA, software metadata) and caches the document to accelerate first-request authentication. The application name is auto-filled from the document's `client_name`; if absent, the confirm step prompts for one.

### Agent JWT-Bearer Assertion

Agent applications authenticate using `client_assertion_type=urn:ietf:params:oauth:client-assertion-type:agent-jwt-bearer`. The assertion's `iss` identifies the registered agent application (the blueprint), and `sub` carries the running instance identifier. Access Management resolves the blueprint from `iss`, validates the assertion signature against the blueprint's JWKS, and synthesizes a per-instance client identity.

Issued tokens include a `client_profile` claim (`ai_agent <persona>`) and an `act` delegation chain with `act.sub` set to the agent instance ID for user-bound flows (User Embedded, Hosted Delegated). For Autonomous agents in client-credentials flows, `act.sub` is set to the blueprint `client_id`. The `act` node includes an `act.sub_profile` claim carrying the lowercase agent persona.
