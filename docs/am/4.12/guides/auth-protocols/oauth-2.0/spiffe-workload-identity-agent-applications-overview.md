# SPIFFE Workload Identity & Agent Applications Overview

## Overview

SPIFFE Workload Identity & Agent Applications introduce AI agents as first-class OAuth/OIDC identities in Access Management. Agents authenticate using SPIFFE JWT-SVIDs issued by SPIRE, enabling per-instance identity attestation with delegation chains. Administrators can create agent applications from Client Identity Metadata Documents (CIMD) or configure them manually, choosing from three agent personas: User-Embedded, Hosted Delegated, and Autonomous.

## Key Concepts

### Agent Application Types

Agent applications are standard OAuth clients with `type=AGENT` and a persona defined by the `subType` field. Three personas are available:

- **User-Embedded**: Agents acting on behalf of an authenticated user within the user's session. Require redirect URIs. Support `authorization_code` grant only.
- **Hosted Delegated**: Agents running in a hosted environment, acting on behalf of users but with their own instance identity. Require redirect URIs. Support `authorization_code` grant only.
- **Autonomous**: Fully independent agents with no user context. Support `client_credentials` grant only.

All agent types prohibit `implicit`, `password`, and `refresh_token` grants.

### SPIFFE Workload Identity

SPIFFE (Secure Production Identity Framework For Everyone) provides cryptographically verifiable workload identities. Access Management validates JWT-SVIDs (SPIFFE Verifiable Identity Documents) issued by SPIRE servers against registered trust domains. Each trust domain defines a JWKS URL, allowed signature algorithms, and a refresh interval for fetching trust bundles.

**Trust Domain properties:**

| Property | Description | Example |
|:---------|:------------|:--------|
| Name | Unique identifier for the trust domain | `am.local` |
| Bundle Source | How the trust bundle is obtained | `JWKS_URL` or `STATIC_JWKS` |
| JWKS URL | Endpoint serving the trust bundle public keys | `http://spire-oidc:8443/keys` |
| Refresh Interval Seconds | Cache duration for fetched bundles | `300` |
| Allowed Algorithms | Permitted JWT signature algorithms | `RS256`, `ES256` |

### SPIFFE Subject Matching

Applications using `spiffe_jwt` authentication configure a SPIFFE subject (the expected SPIFFE ID) and a match mode:

- **Exact Match**: The JWT-SVID `sub` claim must equal the configured subject exactly. Default mode for all applications.
- **Prefix Match**: The JWT-SVID `sub` claim must start with the configured subject. Only allowed for Hosted Delegated and Autonomous agents. The configured subject must end with `/` to ensure path-boundary matching (e.g., `spiffe://acme/hotel-agent/` matches `spiffe://acme/hotel-agent/instance-a` but not `spiffe://acme/hotel-agent-dev/x`).

Prefix matching enables per-instance agent identity: a single blueprint application accepts SVIDs for multiple running instances, each with a unique SPIFFE ID under the blueprint's prefix.

### Client Identity Metadata Document (CIMD)

CIMD allows administrators to create applications by referencing a hosted metadata document URL instead of entering settings manually. Access Management fetches the document, validates it against OAuth/OIDC standards, and pre-populates the application with parsed metadata (redirect URIs, grants, scopes, JWKS, mTLS settings). The CIMD URL becomes the application's `client_id`.

### Agent JWT-Bearer Assertion

Agent applications use a dedicated client assertion type (`urn:ietf:params:oauth:client-assertion-type:agent-jwt-bearer`) to authenticate. The assertion's `iss` claim identifies the blueprint application; the `sub` claim carries the running instance ID. Access Management synthesizes a per-instance client identity and issues tokens with an `act` (actor) delegation chain, where `act.sub` contains the agent instance ID and `act.sub_profile` identifies the agent persona.

## Prerequisites

- Access Management 4.12.0 or later
- For SPIFFE authentication: a SPIRE server deployment with OIDC discovery provider
- For CIMD application creation: domain-level CIMD settings enabled
- For trust domain JWKS URLs: network access from Access Management gateway to the SPIRE OIDC endpoint
- Database migration required (new `sub_type` column in `applications` table; new `trust_domains` table)

## Gateway Configuration

### Trust Domain JWKS Fetch

| Property | Description | Example |
|:---------|:------------|:--------|
| `cimdSettings.allowPrivateIpAddress` | Allow JWKS URLs resolving to private/loopback/link-local addresses | `false` |
| `cimdSettings.fetchTimeoutMs` | Timeout for fetching CIMD documents and JWKS bundles | `5000` |

### SPIFFE JWT-SVID Validation

Access Management validates JWT-SVIDs according to the SPIFFE JWT-SVID specification: `typ` header must be `JWT`, signature algorithm must be in the trust domain's allowed list (no `none` or HMAC), `sub` must be a SPIFFE ID within the configured trust domain, `aud` must contain the token endpoint URL, and `iat`/`exp`/`nbf` must be within acceptable bounds with clock-skew tolerance.
