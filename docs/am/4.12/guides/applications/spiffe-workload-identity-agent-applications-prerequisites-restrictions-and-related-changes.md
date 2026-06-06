# SPIFFE Workload Identity & Agent Applications: Prerequisites, Restrictions, and Related Changes

## Prerequisites

Before configuring SPIFFE Workload Identity and Agent Applications, ensure the following requirements are met:

- Access Management 4.12 or later
- Database migration applied:
  - `4.12.0-applications-add-sub-type` (adds `sub_type` column to `applications` table)
  - `4.12.0-trust-domains-table` (creates `trust_domains` table)
- For SPIFFE authentication: a SPIRE deployment issuing JWT-SVIDs with `aud` containing the Access Management token endpoint URL
- For CIMD: a reachable CIMD document URL serving valid OAuth client metadata (RFC 7591 format)
- For agent applications: [certificate-based client authentication](../auth-protocols/oauth-2.0/cimd.md#cimd-client-identification) configured (JWKS or mTLS)
- `APPLICATION[CREATE]` permission for CIMD validation and application creation endpoints

## SPIFFE Authentication

Configure SPIFFE JWT-SVID authentication for your Gravitee deployment. These properties control JWKS validation, caching, and security constraints for SPIFFE-based authentication.

| Property | Description | Example |
|:---------|:------------|:--------|
| `gravitee.oidc.spiffe.enabled` | Enable SPIFFE JWT-SVID authentication domain-wide | `true` |
| `gravitee.oidc.spiffe.allowPrivateIpAddress` | Allow JWKS URLs resolving to private IP addresses | `false` |
| `gravitee.oidc.spiffe.allowUnsecuredHttpUri` | Allow HTTP (non-TLS) JWKS URLs | `false` |
| `gravitee.oidc.spiffe.cacheMaxEntries` | Maximum JWKS cache entries | `100` |
| `gravitee.oidc.spiffe.cacheTtlSeconds` | JWKS cache time-to-live (in seconds) | `3600` |
| `gravitee.oidc.spiffe.clockSkewSeconds` | Allowed clock skew for JWT validation (in seconds) | `30` |
| `gravitee.oidc.spiffe.defaultAllowedAlgorithms` | Default signing algorithms for trust domains | `["RS256", "ES256"]` |
| `gravitee.oidc.spiffe.fetchTimeoutMs` | HTTP fetch timeout for JWKS/CIMD (in milliseconds) | `5000` |
| `gravitee.oidc.spiffe.maxJwtLifetimeSeconds` | Maximum allowed JWT lifetime (in seconds) | `300` |
| `gravitee.oidc.spiffe.maxResponseSizeKb` | Maximum HTTP response size for JWKS/CIMD (in kilobytes) | `512` |

{% hint style="warning" %}
Set `allowPrivateIpAddress` and `allowUnsecuredHttpUri` to `true` only in development or testing environments. Enabling these options in production may expose your deployment to security risks.
{% endhint %}

### CIMD Creation

1. Navigate to **Agents** and click **Add Agent**.
2. Select **CIMD** on the creation mode step.
3. Enter the **CIMD Document URL** (e.g., `https://cimd.acme.com/agent-billing`).
4. Click **Validate**. Access Management fetches and validates the document server-side.
5. Review the parsed metadata in the read-only CIMD confirm step. If the document lacks a `client_name`, enter an **Application Name**.
6. Click **Create**. The CIMD URL becomes the application's `client_id`.

#### Reference

| Field | Description | Required |
|:------|:------------|:---------|
| CIMD Document URL | URL serving the OAuth client metadata document | Yes |
| Application Name | Human-readable name (auto-filled from `client_name` if present) | Conditional |

### CIMD Validation

Configure CIMD (Client-Initiated Management Data) validation settings to control application creation and URL restrictions.

| Property | Description | Example |
|:---------|:------------|:--------|
| `gravitee.oidc.cimd.enabled` | Enable CIMD application creation | `true` |
| `gravitee.oidc.cimd.allowedDomains` | Allowed domains for CIMD URLs. If empty, all domains are allowed. | `["cimd.acme.com"]` |
| `gravitee.oidc.cimd.allowPrivateIpAddress` | Allow CIMD URLs that resolve to private IP addresses | `false` |
| `gravitee.oidc.cimd.allowUnsecuredHttpUri` | Allow HTTP CIMD URLs (non-HTTPS) | `false` |

{% hint style="warning" %}
Setting **Allow Unsecured HTTP URI** to `true` permits non-HTTPS CIMD URLs, which may expose sensitive data during transmission.
{% endhint %}

### Manual Creation

1. Navigate to **Agents** and click **Add Agent**.
2. Select **Manual** on the creation mode step.
3. Enter an **Application Name** and optional **Description**.
4. Select an **Agent Sub-Type** from the dropdown: User Embedded, Hosted Delegated, or Autonomous.
5. Configure **Redirect URIs** (required for User Embedded and Hosted Delegated; not applicable to Autonomous).
6. Select **Grant Types** appropriate to the agent persona.
7. Choose a **Token Endpoint Auth Method**: Private Key JWT, TLS Client Auth, Self-Signed TLS Client Auth, SPIFFE JWT, or Agent JWT-Bearer.
8. If using SPIFFE JWT, configure **Workload Identity Settings**:
   1. Select a **Trust Domain** from the dropdown.
   2. Enter a **Subject** (SPIFFE URI, e.g., `spiffe://acme.com/billing-agent`).
   3. Select a **Subject Match Mode** (Exact or Prefix). If Prefix, ensure the subject ends with `/`.
9. If using Private Key JWT or Agent JWT-Bearer, provide a **JWKS** or **JWKS URI**.
10. Click **Create**.

#### Configuration Reference

| Field | Description | Required |
|:------|:------------|:---------|
| Application Name | Human-readable agent identifier | Yes |
| Description | Optional agent description | No |
| Agent Sub-Type | Agent persona (User Embedded, Hosted Delegated, Autonomous) | Yes |
| Redirect URIs | OAuth redirect endpoints | Yes (User Embedded, Hosted Delegated) |
| Grant Types | Allowed OAuth grant types | Yes |
| Token Endpoint Auth Method | Client authentication method | Yes |
| Trust Domain | SPIFFE trust domain (SPIFFE JWT only) | Conditional |
| Subject | SPIFFE URI (SPIFFE JWT only) | Conditional |
| Subject Match Mode | Exact or Prefix (SPIFFE JWT only) | Conditional |
| JWKS / JWKS URI | Public keys for signature validation (Private Key JWT, Agent JWT-Bearer) | Conditional |

## Restrictions

- SPIFFE prefix match is restricted to Hosted Delegated and Autonomous agent applications. User Embedded agents must use exact match.
- SPIFFE prefix subjects must end with `/` to ensure path-boundary matching and prevent partial path matches.
- Agent applications cannot use `implicit`, `password`, or `refresh_token` grants.
- Agent applications cannot use secret-based token endpoint authentication (`client_secret_basic`, `client_secret_post`, `client_secret_jwt`).
- User Embedded agents cannot use `client_credentials` grant.
- Autonomous agents cannot use `authorization_code` grant.
- Hosted Delegated agents cannot use `client_credentials` grant.
- User Embedded and Hosted Delegated agents require at least one redirect URI.
- CIMD documents using secret-based `token_endpoint_auth_method` are rejected.
- CIMD documents must include `jwks_uri` or inline `jwks` when using `private_key_jwt` authentication.
- CIMD URLs resolving to private IP addresses are rejected unless `allowPrivateIpAddress=true`.
- HTTP (non-TLS) CIMD and JWKS URLs are rejected unless `allowUnsecuredHttpUri=true`.
- Trust domain JWKS refresh interval is not dynamically adjustable at runtime; changes require updating the trust domain configuration.
- CIMD validation does not support inline JWKS in the metadata document; `jwks_uri` is required.
- Multi-type filtering on `GET /applications?type=...` requires multiple `type` query parameters (e.g., `?type=WEB&type=SERVICE`); comma-separated values are not supported.
- SPIFFE subject validation does not support wildcard or regex patterns; only exact match or prefix match is supported.
- Standard `jwt-bearer` client assertions (`client_assertion_type=urn:ietf:params:oauth:client-assertion-type:jwt-bearer`) with a SPIFFE `sub` are rejected with error: "SPIFFE JWT-SVID must be sent with client_assertion_type=jwt-spiffe".
- Standard `jwt-bearer` assertions now enforce strict RFC 7523 semantics: `iss` must equal `sub` and both must equal `client_id`.
- SVID validation rejects `none` and HMAC signing algorithms; only algorithms in the trust domain's allowed list are accepted.

## Related Changes

The Applications list in the management console now scopes itself to exclude agents. Agents appear in a dedicated Agents area with its own top-level navigation entry and creation wizard. The `/applications` listing endpoint accepts a multi-valued `type` filter so the UI can request "AGENT only" or "everything except AGENT" in one call.

Agent applications can now be marked as DCR/CIMD registration templates.

For user-bound agent flows (User Embedded, Hosted Delegated), issued tokens set `act.sub` to the agent instance ID instead of the blueprint `client_id`, exposing the acting instance in the delegation chain.

Tokens for agent applications include:
- `client_profile` claim: `ai_agent <persona>`
- `sub_profile` claim for client-credentials flows
- `act.sub_profile` claim in the `act` node

All profile claims are propagated through token exchange and ID tokens.

The application model replaces the earlier nested `settings.agent` (AgentSettings) shape with a top-level `subType` field, so the public API, persistence, and UI all read/write a single field.

Database migration is required:
- New `sub_type` column added to the `applications` table
- New `trust_domains` table created
