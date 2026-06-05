# SPIFFE Workload Identity & Agent Applications Overview

## Overview

SPIFFE Workload Identity & Agent Applications introduces AI agents as first-class OAuth/OIDC identities in Access Management. Agents authenticate using SPIFFE JWT-SVIDs attested by SPIRE, enabling per-instance identity with delegation chains. Administrators can create agent applications manually or bootstrap them from Client Identity Metadata Documents (CIMD), and manage SPIFFE trust domains through the console or Management API.

## Key Concepts

### Agent Application Types

Agent applications use the `AGENT` type with three personas:

| Persona | Description | Redirect URIs | Allowed Grants |
|:--------|:------------|:--------------|:---------------|
| **User-Embedded** | Runs in the user's browser or device; acts on behalf of the authenticated user | Required | `authorization_code` only |
| **Hosted Delegated** | Hosted by a provider; acts on behalf of a delegated user | Required | `authorization_code` OR `client_credentials` (not both) |
| **Autonomous** | Fully autonomous service with no user context | Not required | `client_credentials` only |

All agent applications prohibit `implicit`, `password`, and `refresh_token` grants.

### SPIFFE Workload Identity

SPIFFE workload identity authenticates clients using JWT-SVIDs issued by a SPIRE server. Each application references a **Trust Domain** (a named SPIFFE trust boundary) and declares an expected SPIFFE ID in its **Subject** field. AM verifies the SVID signature against the trust domain's JWKS bundle and matches the SVID's `sub` claim to the application's subject.

**Subject Match Modes:**

| Mode | Behavior | Eligibility |
|:-----|:---------|:------------|
| **Exact Match** | SVID `sub` must equal the application's subject exactly | All application types |
| **Prefix Match** | SVID `sub` must start with the application's subject (which must end with `/`) | `HOSTED_DELEGATED` and `AUTONOMOUS` agents only |

Prefix Match enables per-instance agent identity: a blueprint application with subject `spiffe://am.local/hotel-agent/` accepts SVIDs like `spiffe://am.local/hotel-agent/instance-a` and `spiffe://am.local/hotel-agent/instance-b`. The full SPIFFE ID becomes the agent instance ID in the `act.sub` claim.

### Trust Domains

A Trust Domain represents a SPIFFE trust boundary and holds the JWKS bundle used to verify JWT-SVIDs. Trust domains are scoped to an AM domain and configured with:

| Property | Description |
|:---------|:------------|
| **Name** | Trust domain name (e.g., `am.local`) |
| **Bundle Source** | `JWKS_URL` (fetch from endpoint) or `STATIC_JWKS` (inline JSON) |
| **JWKS URL** | HTTPS endpoint serving the trust bundle (when source is `JWKS_URL`) |
| **Static JWKS** | Inline JWKS JSON (when source is `STATIC_JWKS`) |
| **Allowed Algorithms** | Permitted JWS signature algorithms (e.g., `RS256`, `ES256`) |
| **Refresh Interval Seconds** | How often to refresh the JWKS bundle from the URL |

AM caches trust bundles and serves the last known good bundle on transient fetch errors.

### Client Identity Metadata Documents (CIMD)

CIMD allows administrators to create applications by referencing a hosted metadata document URL instead of entering settings manually. The CIMD URL becomes the application's `client_id`. AM fetches the document, validates it against domain trust policies, and populates the application with parsed OAuth/OIDC metadata (redirect URIs, grants, scopes, JWKS, mTLS settings, software metadata).

<figure><img src="../../../.gitbook/assets/am-cimd-settings-overview.png" alt="CIMD settings overview showing enabled state"><figcaption></figcaption></figure>

### Client Assertion Types

AM routes client assertions by type:

| Assertion Type URN | Routing Logic | Use Case |
|:-------------------|:--------------|:---------|
| `urn:ietf:params:oauth:client-assertion-type:jwt-bearer` | Standard RFC 7523: `iss == sub == client_id` | Non-agent applications with static JWKS |
| `urn:ietf:params:oauth:client-assertion-type:agent-jwt-bearer` | Agent instance assertion: `iss` is blueprint `client_id`, `sub` is agent instance ID | Per-instance agent identity with self-signed JWTs |
| `urn:ietf:params:oauth:client-assertion-type:jwt-spiffe` | SPIFFE JWT-SVID: `iss` is bundle issuer, `sub` is SPIFFE URI | SPIFFE-attested workload identity |

Presenting a SPIFFE JWT-SVID with the standard `jwt-bearer` type is rejected with an error.

### Delegation Claims

Tokens issued to agent applications include an `act` (actor) claim describing the delegation chain:

```json
{
  "sub": "<user_id or agent_instance_id>",
  "act": {
    "sub": "<agent_instance_id or blueprint_client_id>",
    "sub_profile": "<agent_persona_lowercase>"
  },
  "client_profile": "ai_agent <agent_persona_lowercase>"
}
```

For user-bound agents (`USER_EMBEDDED`, `HOSTED_DELEGATED`), `act.sub` carries the agent instance ID when known; otherwise it falls back to the blueprint `client_id`. For `AUTONOMOUS` agents, the top-level `sub` is the agent instance ID.
