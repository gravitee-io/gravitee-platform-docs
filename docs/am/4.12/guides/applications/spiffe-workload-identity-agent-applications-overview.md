# SPIFFE Workload Identity & Agent Applications Overview

## Overview

SPIFFE Workload Identity & Agent Applications introduces AI agents as first-class OAuth/OIDC identities in Access Management. Agents authenticate using SPIFFE JWT-SVIDs issued by SPIRE, enabling per-instance identity attestation with delegation chains. Administrators can create agent applications with three personas (User Embedded, Hosted Delegated, Autonomous), register SPIFFE trust domains, and bootstrap applications from Client Identity Metadata Documents (CIMD). This feature is designed for API platform administrators managing AI agent workloads and developers integrating autonomous services.

## Key Concepts

### Agent Application Types

Agent applications represent AI agents or autonomous services that act on behalf of users or independently. Three agent personas define the authentication and authorization model:

- **User Embedded**: Agent acts on behalf of an end-user. Requires `authorization_code` grant and at least one redirect URI. The issued token's `sub` is the end user; the agent instance ID appears in `act.sub`.
- **Hosted Delegated**: Agent acts on behalf of an end-user in a hosted environment. Requires `authorization_code` grant and at least one redirect URI. Supports per-instance identity via SPIFFE PREFIX subject matching.
- **Autonomous**: Agent acts independently without user context. Uses `client_credentials` grant. No redirect URIs required. The agent instance ID becomes the token's `sub`.

All agent types forbid `implicit`, `password`, and `refresh_token` grants. User Embedded and Hosted Delegated agents cannot use `client_credentials`; Autonomous agents cannot use `authorization_code`. Agent applications can be marked as DCR/CIMD registration templates; the blueprint ID is permitted as `software_id` in DCR flows.

### SPIFFE Workload Identity

SPIFFE (Secure Production Identity Framework For Everyone) provides cryptographically verifiable workload identity. A workload presents a JWT-SVID (SPIFFE Verifiable Identity Document) issued by its SPIRE server. Access Management validates the SVID against a registered trust domain and authenticates the client.

**Trust Domain**: A named entity scoped to an Access Management domain. Contains a JWKS URL, allowed signature algorithms, and a refresh interval. Trust bundles are cached per domain and refreshed at the configured interval. The trust bundle service serves the last known good bundle on transient fetch errors.

**JWT-SVID Validation**: The SVID must have `typ=JWT`, use an allowed signing algorithm (no `none` or HMAC), contain a `sub` claim formatted as a SPIFFE URI within the configured trust domain, include the token endpoint in `aud`, and have valid `iat`, `exp`, and `nbf` timestamps (with clock-skew tolerance). Signature verification uses the trust domain's JWKS.

**Subject Matching Modes**:
- **Exact** (default): The SVID `sub` must exactly match the application's configured `subject`.
- **Prefix**: The SVID `sub` must start with the application's `subject`. The subject must end with `/` to ensure prefixes only match at path boundaries. Only allowed for Hosted Delegated and Autonomous agents. The full SPIFFE ID from the SVID becomes the agent instance ID and populates `act.sub` in issued tokens.

### Client Identity Metadata Document (CIMD)

CIMD enables application creation by referencing a hosted metadata document URL instead of manual configuration. In CIMD mode, the administrator supplies only the Document URL. Access Management fetches and validates the document server-side, then displays a read-only preview (a "CIMD confirm" step) of parsed metadata (redirect URIs, grants, scopes, JWKS, mTLS, CIBA, software metadata) before creation. The CIMD URL becomes the application's `client_id`. The document's `client_name` auto-fills the application name; if absent, the administrator must provide one during creation.

CIMD documents using secret-based token endpoint authentication methods (`client_secret_basic`, `client_secret_post`, `client_secret_jwt`) are rejected. Documents specifying `private_key_jwt` without `jwks` or `jwks_uri` are rejected. Unreachable, oversized, or slow (timeout) documents are rejected.

### Agent JWT-Bearer Assertion

Agent applications authenticate using a distinct client-assertion type: `urn:ietf:params:oauth:client-assertion-type:agent-jwt-bearer`. The blueprint (registered agent application) is resolved from the JWT's `iss` claim; the running instance ID is carried in `sub`. Standard `jwt-bearer` assertions (RFC 7523) require `iss == sub == client_id`. FAPI signing-algorithm checks apply to agent JWTs when the domain's FAPI profile is enabled.

Issued tokens include a `client_profile` claim (`ai_agent <persona>`) and a `sub_profile` claim for agent subjects. These claims propagate through `act` delegation chains in token exchange, ID tokens, and audit logs. For User Embedded and Hosted Delegated agents, `act.sub` is set to the agent instance ID when known; otherwise it falls back to the blueprint `client_id`. Autonomous agents already carry the instance ID in the top-level `sub`.

### Application Schema Changes

The agent persona is stored in a top-level `subType` field (optional string) on the Application object, replacing the earlier nested `settings.agent` (AgentSettings) shape. The public API, persistence layer, and UI all read and write this single field. The database migration adds a nullable `sub_type` column to the `applications` table (JDBC) and a `subType` field to the `applications` collection (MongoDB).

## Prerequisites

- Access Management 4.12.0 or later
- SPIRE server and agent infrastructure (for SPIFFE workload identity)
- Database migration required (JDBC: `4.12.0-applications-add-sub-type.yml`, `4.12.0-trust-domains-table.yml`; MongoDB: automatic on first write)
- Domain-level OIDC settings configured with SPIFFE and CIMD enabled
- `APPLICATION[CREATE]` permission for CIMD application creation and validation
