# SPIFFE Workload Identity & Agent Applications - Restrictions and Related Changes

## Restrictions

- Prefix subject match mode is only allowed for Hosted Delegated or Autonomous agent applications. User-Embedded agents and non-agent applications must use Exact mode.
- Prefix subjects must end with `/` to ensure prefix matching occurs at path boundaries.
- Agent applications cannot use `implicit`, `password`, or `refresh_token` grant types.
- User-Embedded agents cannot use `client_credentials` grant.
- Autonomous agents cannot use `authorization_code` grant.
- Hosted Delegated agents cannot use `urn:ietf:params:oauth:grant-type:token-exchange` grant.
- CIMD clients cannot use `client_secret_basic`, `client_secret_post`, or `client_secret_jwt` as `token_endpoint_auth_method`.
- SPIFFE JWT-SVIDs must be sent with `client_assertion_type=urn:ietf:params:oauth:client-assertion-type:jwt-spiffe`. Sending a SPIFFE JWT-SVID with the standard `jwt-bearer` assertion type is rejected.
- JWKS URLs resolving to private, loopback, or link-local addresses are rejected unless the domain sets `allowPrivateIpAddress`.
- CIMD URLs resolving to private IP addresses (literal or DNS resolution) are rejected unless the domain allows private IPs.
- The SPIRE local-stack overlay (`docker-compose.spire.yml`) is only available in the `dev` local-stack configuration. To enable SPIRE tests in CI, set `RUN_SPIRE_TESTS=true`.
- Trust domain JWKS responses are cached per the `Cache-Control` header or `refreshIntervalSeconds` setting. Externally updated JWKS may not be reflected until the cache expires.
- CIMD URL trust validation (domain allow-lists and private IP restrictions) is enforced only when `CIMDSettings.allowedDomains` or `allowPrivateIpAddress` are configured. If these settings are null or empty, all URLs are accepted (subject to HTTP/HTTPS scheme rules).
- For Prefix mode SPIFFE subjects, the full SPIFFE ID becomes the `agentInstanceId` only for Hosted Delegated and Autonomous agents. User-Embedded agents do not synthesize per-instance clients even when using Prefix mode.

## Related Changes

The following changes support the agent-based authentication model:

### Management Console

The Management Console adds a top-level **Agents** navigation entry with a dedicated agent list and creation flow, separate from the standard **Applications** area. The Applications list now scopes itself to exclude agents.

### Management API

The `/applications` endpoint accepts a multi-valued `type` query parameter for filtering (e.g., `?type=WEB&type=SERVICE`), allowing the UI to request "AGENT only" or "everything except AGENT" in one call.

CIMD validation and application creation are exposed via new Management API endpoints:
- `POST /cimd/validate`
- `POST /cimd/applications`

### Application Configuration

Application forms replace the **Agent Identity Mode** checkbox and nested **Agent Type** dropdown with a top-level **Sub Type** field (visible only when `type=AGENT`). This replaces the earlier nested `settings.agent` (AgentSettings) shape so the public API, persistence, and UI all read/write a single field.

SPIFFE settings are renamed from `settings.spiffe` to `settings.workloadIdentitySettings` and include a new **Subject Match Mode** radio group with the following options:
- Exact
- Prefix

### Database Schema

New columns and tables are added to support agent functionality:
- `sub_type` column added to the `applications` table
- New `trust_domains` table created

