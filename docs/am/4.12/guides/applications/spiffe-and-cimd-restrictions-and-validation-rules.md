# SPIFFE and CIMD Restrictions and Validation Rules

## Restrictions

* **Prefix subject matching**: Only allowed for Hosted Delegated and Autonomous agent applications. User-Embedded agents must use Exact mode.
* **CIMD URLs**: Must use HTTPS unless `allowUnsecuredHttpUri` is enabled. URLs resolving to private IP addresses are rejected unless `allowPrivateIpAddress` is enabled.
* **Autonomous agent grants**: Cannot use `authorization_code`, `implicit`, `password`, or `refresh_token` grants.
* **User-Embedded and Hosted Delegated agent grants**: Cannot use `client_credentials`, `implicit`, `password`, or `urn:ietf:params:oauth:grant-type:jwt-bearer` grants.
* **Redirect URIs**: User-Embedded and Hosted Delegated agents require at least one redirect URI.
* **CIMD authentication methods**: CIMD documents using secret-based token endpoint authentication methods (`client_secret_basic`, `client_secret_post`, `client_secret_jwt`) are rejected.
* **CIMD document size**: CIMD documents exceeding `maxResponseSizeKb` are rejected.
* **SPIFFE JWT-SVID signing algorithms**: Must use allowed signing algorithms configured in the Trust Domain. If the domain uses a FAPI profile, SVIDs must be signed with `PS256`.
* **SPIFFE subject format**: Subjects must start with `spiffe://<trust-domain>/`. For Prefix mode, subjects must end with `/`.
* **Trust bundle refresh**: Controlled by `refreshIntervalSeconds` and `Cache-Control` headers. No manual refresh endpoint is provided.
* **JWKS URL resolution**: JWKS URLs resolving to private or loopback IP addresses are rejected unless the Trust Domain enables `allowPrivateIpAddress`.
* **Agent application templates**: Agent applications can be marked as DCR/CIMD registration templates. This restriction was removed in 4.12.0.

## Related Changes

The **Agents** section appears as a top-level navigation entry in the management console, separate from **Applications**. The Applications list excludes agent-type applications. Trust Domains are managed under **Workload Identity** in domain settings.

The application creation wizard includes a Manual/CIMD toggle when CIMD is enabled. CIMD mode displays a read-only metadata preview before creation. Agent applications include a **Subject Match Mode** selector (Exact or Prefix) when using SPIFFE JWT authentication.

Tokens issued to user-bound agents populate `act.sub` with the agent instance ID when known, enabling per-instance delegation chains. The `type` query parameter on the applications listing endpoint now accepts multiple values for filtering.

New columns added to the `applications` table (`sub_type`) and a new `trust_domains` table. Database migration is required.
