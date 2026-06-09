# SPIFFE Workload Identity and Agent Applications Overview

## Overview

SPIFFE Workload Identity & Agent Applications introduces AI agents as first-class OAuth/OIDC identities in Access Management 4.12. Agents authenticate using SPIFFE JWT-SVIDs issued by SPIRE, enabling per-instance identity attestation with delegation chains. The feature includes a new AGENT application type with three personas (USER_EMBEDDED, HOSTED_DELEGATED, AUTONOMOUS), CIMD-based application bootstrap from hosted metadata URLs, and trust domain management for SPIFFE workload identities.

## Key Concepts

### Agent Application Types

Agent applications represent AI agents that act on behalf of users or autonomously. Each agent has a persona that determines its OAuth flow and identity model:

| Persona | Description | OAuth Flow | Redirect URI Requirement | Token Subject |
|:--------|:------------|:-----------|:-------------------------|:--------------|
| USER_EMBEDDED | Agents embedded in user-facing applications | `authorization_code` | At least one redirect URI required | End user in `sub`; agent instance in `act.sub` |
| HOSTED_DELEGATED | Agents hosted by the platform that act on behalf of users | `authorization_code` (for user delegation) and `client_credentials` (for autonomous tasks) | At least one redirect URI required | End user in `sub` (authorization_code); agent instance in `sub` (client_credentials) |
| AUTONOMOUS | Fully autonomous agents with no user context | `client_credentials` | No redirect URIs required | Agent instance in `sub` |

All agent applications emit a `client_profile` claim (for example: `"ai_agent autonomous"`) in issued tokens. Agent applications can be marked as DCR/CIMD registration templates via the "Use as DCR / CIMD registration template" toggle. When used as a template, the blueprint application ID is permitted as the `software_id` in dynamic client registration requests.

### SPIFFE Workload Identity

SPIFFE (Secure Production Identity Framework For Everyone) provides cryptographically verifiable workload identities. Agents authenticate to Access Management by presenting a JWT-SVID (SPIFFE Verifiable Identity Document) issued by their SPIRE deployment. AM validates the SVID against a registered trust domain's JWKS bundle and matches the SPIFFE ID against the application's configured subject.

#### SVID Validation Rules

AM validates JWT-SVIDs according to the following rules:

- JWT header `typ` must be `JWT`
- Signing algorithm must be in the trust domain's allowed algorithms list (no `none` or HMAC algorithms)
- `sub` claim must be a SPIFFE ID inside the configured trust domain (format: `spiffe://<trust-domain>/<path>`)
- `aud` claim must include the token endpoint URL
- `iat`, `exp`, and `nbf` claims must be within bounds, with clock-skew tolerance applied

#### Subject Match Modes

| Mode | Behavior | Eligibility |
|:-----|:---------|:------------|
| EXACT | SVID `sub` must exactly match the configured subject | All applications using `spiffe_jwt` |
| PREFIX | SVID `sub` must start with the configured subject (which must end with `/`) | HOSTED_DELEGATED and AUTONOMOUS agents only |

PREFIX matching enables per-instance identity: a blueprint application with subject `spiffe://acme/hotel-agent/` accepts SVIDs like `spiffe://acme/hotel-agent/instance-a` and `spiffe://acme/hotel-agent/instance-b`, synthesizing a unique client identity for each instance. The trailing slash requirement ensures prefixes only match at path boundaries, preventing unintended matches (for example: `spiffe://acme/hotel-agent/` will not match `spiffe://acme/hotel-agentX/`). The instance ID appears in `act.sub` for user-bound flows and `sub` for autonomous flows.

### Trust Domains

A trust domain represents a SPIFFE trust boundary. Each trust domain in AM holds:

- **Name**: Human-readable identifier
- **Bundle Source**: JWKS_URL (fetch from SPIRE OIDC discovery) or STATIC_JWKS (inline keys)
- **JWKS URL**: HTTP(S) endpoint serving the trust bundle (for JWKS_URL source)
- **Refresh Interval**: How often AM refetches the bundle (seconds)
- **Allowed Algorithms**: Signing algorithms accepted for JWT-SVIDs (for example: RS256, ES256)

Trust domains are scoped to an AM domain and managed via the Workload Identity settings page or the Management API.

### CIMD (Client Identity Metadata Document)

CIMD allows administrators to create applications by referencing a hosted metadata document URL instead of manually entering OAuth settings. In CIMD mode, the administrator supplies only the document URL. AM fetches the document, validates it against domain security policies, and pre-populates all application settings (redirect URIs, grants, JWKS, mTLS, etc.). The document URL becomes the application's `client_id`. CIMD is particularly useful for agent applications where metadata is managed externally.

## Prerequisites

- Access Management 4.12.0 or later
- For SPIFFE authentication: a SPIRE deployment with OIDC discovery enabled and reachable JWKS endpoint
- For CIMD: applications must use asymmetric authentication methods (`private_key_jwt`, `tls_client_auth`, or `spiffe_jwt`) — secret-based methods are rejected
- For PREFIX subject matching: application type must be AGENT with persona HOSTED_DELEGATED or AUTONOMOUS
- `APPLICATION[CREATE]` permission required for CIMD validation and application creation endpoints
- CIMD must be enabled for the domain to use CIMD-based application creation
- Database migration required (adds `applications.sub_type` column and creates `trust_domains` table)
