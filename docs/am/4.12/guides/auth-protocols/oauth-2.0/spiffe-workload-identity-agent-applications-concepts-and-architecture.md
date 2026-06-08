# SPIFFE Workload Identity & Agent Applications: Concepts and Architecture

## Overview

SPIFFE Workload Identity & Agent Applications introduces AI agents as first-class OAuth/OIDC identities in Gravitee Access Management. Agents authenticate using SPIFFE JWT-SVIDs issued by SPIRE, enabling per-instance identity attestation with delegation chains. Administrators can create agent applications with three personas (User-Embedded, Hosted Delegated, Autonomous) and bootstrap applications from Client Identity Metadata Documents (CIMD).

## Key Concepts

### Trust Domains

A trust domain is an entity scoped to an Access Management domain, holding a name, JWKS URL, allowed signature algorithms, and a refresh interval. Each trust domain represents a SPIFFE trust boundary. Trust domains are managed via the domain settings "Workload Identity" section and the Management API. The trust bundle service caches bundles per domain, honors the configured refresh interval, and serves the last known good bundle on transient fetch errors.

| Property | Description |
|:---------|:------------|
| **Name** | Trust domain identifier (e.g., `prod.example`) |
| **Bundle Source** | JWKS URL or Static JWKS |
| **JWKS URL** | URL for fetching the trust bundle (when source is JWKS URL) |
| **Refresh Interval (seconds)** | Cache TTL for the trust bundle |
| **Allowed Algorithms** | Permitted signing algorithms for JWT-SVID validation |

### Agent Application Types

Agent applications are standard applications with `type=AGENT` and one of three personas. The agent persona is stored in the top-level `subType` field. The public API, persistence layer, and UI all read and write this single field.

| Persona | Description | Redirect URIs | Grants | Auth Method |
|:--------|:------------|:--------------|:-------|:------------|
| **User-Embedded** | Agent embedded in user-facing applications | Required | `authorization_code`, `refresh_token` (no `client_credentials`) | `none` (public client) |
| **Hosted Delegated** | Agent hosted by the platform, acting on behalf of users | Required | `authorization_code`, `refresh_token` (no `client_credentials`) | `private_key_jwt` (confidential) |
| **Autonomous** | Agent acting independently without user context | Not required | `client_credentials`, `refresh_token` (no `authorization_code`) | `private_key_jwt` (confidential) |

User-Embedded and Hosted Delegated agents require at least one redirect URI. Agent applications cannot use `implicit`, `password`, or `urn:ietf:params:oauth:grant-type:saml2-bearer` grants. Agent applications can be marked as DCR/CIMD registration templates using the existing "Use as DCR / CIMD registration template" toggle. The blueprint application ID is permitted as the `software_id` in DCR flows.

### SPIFFE JWT-SVID Authentication

SPIFFE JWT-SVID is a client authentication method using workload identities attested by SPIRE. Clients present a JWT-SVID with `client_assertion_type=urn:ietf:params:oauth:client-assertion-type:jwt-spiffe`. Access Management resolves the trust domain from the SVID `iss` claim, fetches the trust bundle, verifies the signature using the `kid`, and validates claims (`sub`, `aud`, `exp`, `iat`, `nbf`) per the SPIFFE JWT-SVID specification. The SVID `sub` must be a SPIFFE ID within the configured trust domain, and the `aud` must contain the token endpoint URL.

### Subject Matching Modes

| Mode | Behavior | Eligibility |
|:-----|:---------|:------------|
| **Exact** | SVID `sub` must equal the configured subject exactly | All applications |
| **Prefix** | SVID `sub` must start with the configured subject (which must end with `/`) | Hosted Delegated and Autonomous agents only |

Prefix mode enables per-instance agent identity: a blueprint with subject `spiffe://acme/hotel-agent/` accepts SVIDs like `spiffe://acme/hotel-agent/instance-a` and `spiffe://acme/hotel-agent/instance-b`. Prefix matching requires a trailing slash so prefixes only match at path boundaries. The full SVID `sub` becomes the agent instance ID, populating the `act.sub` claim in issued tokens.

### Client Identity Metadata Document (CIMD)

CIMD allows administrators to create applications by providing a metadata document URL instead of entering settings manually. In CIMD mode, the administrator supplies only the document URL. Access Management fetches and validates the document server-side, then shows a read-only preview (a "CIMD confirm" step) of the parsed metadata before creation. The CIMD URL becomes the application's `client_id`. Access Management validates the document against domain trust rules (allowed domains, private IP restrictions, unsecured HTTP restrictions) and parses OAuth/OIDC metadata (redirect URIs, grants, scopes, JWKS, mTLS, CIBA, software metadata). Secret-based token endpoint authentication methods (`client_secret_basic`, `client_secret_post`, `client_secret_jwt`) are rejected.

### Agent JWT-Bearer Assertion

Agent JWT-Bearer is a client assertion type (`urn:ietf:params:oauth:client-assertion-type:agent-jwt-bearer`) for agent applications. The blueprint application is resolved from the JWT `iss` claim, and the running instance ID is carried in the `sub` claim. Access Management verifies the signature against the blueprint's JWKS and synthesizes a per-instance client. Issued tokens include a `client_profile` claim (`"ai_agent <persona>"`) and a `sub_profile` claim (lowercase persona name, e.g., `"hosted_delegated"`). For user-bound agents (User-Embedded, Hosted Delegated), the token's top-level `sub` is the end-user ID, and `act.sub` is the agent instance ID. For Autonomous agents, the top-level `sub` is the agent instance ID.
