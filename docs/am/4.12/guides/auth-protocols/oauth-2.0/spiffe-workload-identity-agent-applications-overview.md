# SPIFFE Workload Identity & Agent Applications Overview

## Overview

SPIFFE Workload Identity & Agent Applications introduces AI agents as first-class OAuth/OIDC identities in Access Management. Agents authenticate using SPIFFE JWT-SVIDs issued by SPIRE, enabling per-instance identity attestation with delegation chains. Administrators can create agent applications from hosted metadata documents (CIMD) or configure them manually, choosing from three agent personas that govern grant types and authentication flows.

This feature requires Access Management 4.12.0 or later. Database migration is required (adds `sub_type` column to `applications` table and creates `trust_domains` table).

**Prerequisites:**
- For SPIFFE authentication: a SPIRE server deployment with OIDC discovery provider
- For CIMD: applications must host a `.well-known/client-metadata` document at the CIMD URL

## Key Concepts

### Agent Application Types

Agent applications represent AI agents, automation workflows, or service-to-service integrations. Three agent personas define authentication and authorization behavior:

| Persona | Acts On Behalf Of | Required Grants | Redirect URI Required |
|:--------|:------------------|:----------------|:----------------------|
| **User-Embedded** | End user | `authorization_code`, `refresh_token` | Yes |
| **Hosted Delegated** | End user | `authorization_code`, `refresh_token`, `urn:ietf:params:oauth:grant-type:token-exchange` | Yes |
| **Autonomous** | Itself (service account) | `client_credentials`, `urn:ietf:params:oauth:grant-type:jwt-bearer` | No |

User-Embedded and Hosted Delegated agents require user interaction (authorization code flow). Autonomous agents operate independently using client credentials. Tokens issued to user-bound agents include an `act` (actor) claim chain identifying the agent instance acting on the user's behalf.

### Trust Domains

A Trust Domain represents a SPIFFE trust boundary. Each domain references a JWKS endpoint or static key set used to verify JWT-SVIDs presented by workloads. Trust Domains are scoped to an Access Management domain and configured with:

- **Name**: SPIFFE trust domain identifier (e.g., `prod.example.org`)
- **Bundle Source**: `JWKS_URL` (fetch keys from a URL) or `STATIC_JWKS` (use embedded keys)
- **Allowed Algorithms**: Signing algorithms accepted for SVID verification (e.g., `RS256`, `ES256`)
- **Refresh Interval**: How often to fetch updated trust bundles (seconds)

Trust bundles are cached and refreshed automatically. The service serves the last known good bundle if a fetch fails.

### SPIFFE Subject Matching

Applications using SPIFFE authentication configure a subject (SPIFFE ID) and match mode:

- **Exact**: The SVID `sub` claim must equal the configured subject exactly (e.g., `spiffe://prod.example/agent/billing`).
- **Prefix**: The SVID `sub` must start with the configured subject. The subject must end with `/` (e.g., `spiffe://prod.example/hotel-agent/`). Prefix mode accepts any workload under that path (`spiffe://prod.example/hotel-agent/instance-a`, `spiffe://prod.example/hotel-agent/instance-b`). Only Hosted Delegated and Autonomous agents may use Prefix mode. The full SVID SPIFFE ID becomes the agent instance ID and populates `act.sub` in issued tokens.

### Client Identity Metadata Document (CIMD)

CIMD allows administrators to create applications by referencing a hosted metadata document URL instead of entering settings manually. The CIMD URL becomes the application's `client_id`. Access Management fetches the document, validates it, and populates all OAuth/OIDC settings (redirect URIs, grants, JWKS, mTLS, CIBA, software metadata) from the parsed content. The document is cached to accelerate gateway authentication.
