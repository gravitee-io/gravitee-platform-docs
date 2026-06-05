# Agent Application Restrictions and Validation Rules

## Restrictions

The following restrictions apply to agent applications and CIMD-based authentication:

### Agent application restrictions

* **PREFIX subject matching**: Only allowed for Hosted Delegated and Autonomous agent applications.
* **PREFIX subject format**: PREFIX subjects must end with `/` to ensure path-boundary matching.
* **User-Embedded agents**: Cannot use the client credentials grant.
* **Autonomous agents**: Cannot use the authorization code grant.
* **Hosted Delegated agents**: Must support both authorization code and client credentials grants.
* **Prohibited grants**: Agent applications cannot use implicit, password, or refresh token grants.
* **Redirect URI requirement**: User-Embedded and Hosted Delegated agents require at least one redirect URI.

### CIMD authentication restrictions

* **Authentication methods**: CIMD documents must use certificate-based authentication (`private_key_jwt`, `tls_client_auth`, `self_signed_tls_client_auth`). Secret-based methods (`client_secret_basic`, `client_secret_post`, `client_secret_jwt`) are rejected.
* **JWKS URL restrictions**:
  * JWKS URLs resolving to private, loopback, or link-local IP addresses are rejected unless **Allow Private IP Address** is enabled.
  * HTTP (non-TLS) JWKS URLs are rejected unless **Allow Unsecured HTTP URI** is enabled.
* **CIMD URL restrictions**:
  * CIMD URLs resolving to private IPs are rejected unless **Allow Private IP Address** is enabled.
  * HTTP CIMD URLs are rejected unless **Allow Unsecured HTTP URI** is enabled.

### SPIFFE JWT-SVID restrictions

* **Header requirement**: SPIFFE JWT-SVIDs must include a `kid` header.
* **Signing algorithms**: SPIFFE JWT-SVIDs must use allowed signing algorithms. The `none` algorithm and HMAC algorithms are not permitted.
* **Subject format**: SPIFFE subjects must start with `spiffe://<trustDomain>/`.
* **Assertion type**: JWT-SVIDs presented with `client_assertion_type=urn:ietf:params:oauth:client-assertion-type:jwt-bearer` are rejected with error: "SPIFFE JWT-SVID must be sent with client_assertion_type=urn:ietf:params:OAuth:client-assertion-type:jwt-spiffe".
* **Issuer validation**: Standard `jwt-bearer` assertions with `iss != sub` are rejected with error: "assertion is not valid".

### Trust Domain Management

Trust domain management adds a Workload Identity section under domain settings with list, create, edit, and delete views.

### Access Token Claims

Access tokens issued for user-bound agent flows include:
- `act.sub`: Set to the agent instance ID (extracted from the JWT-SVID `sub` claim for SPIFFE flows or the `agent-jwt-bearer` assertion `sub` claim)
- `client_profile`: Agent profile (e.g., `"ai_agent autonomous"`)
- `sub_profile`: Agent subject profile claim

## Related Changes

The following changes have been introduced to support agent applications and trust domains:

### Management Console

* A top-level **Agents** navigation entry has been added with a dedicated agent list and creation flow, separate from the standard Applications area.
* The Applications list now excludes agent applications.
* The application listing endpoint accepts a multi-valued `type` query parameter to filter by application type (e.g., `?type=AGENT` or `?type=WEB&type=NATIVE`).

### Database Schema

* A new `sub_type` column has been added to the `applications` table.
* A new `trust_domains` table has been created.

### CIMD Application Creation

* A Manual / CIMD toggle has been added on step 2 of the agent creation wizard.
* This toggle is shown only when CIMD is enabled on the domain.

### Trust Domain Management

See [Trust Domain Management](#trust-domain-management) above for details.
### Access Token Claims

See [Access Token Claims](#access-token-claims) above for details.
