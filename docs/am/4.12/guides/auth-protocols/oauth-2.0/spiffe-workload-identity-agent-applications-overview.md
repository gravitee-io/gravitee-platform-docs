# SPIFFE Workload Identity & Agent Applications Overview

## Overview

SPIFFE Workload Identity & Agent Applications introduces AI agents as first-class OAuth/OIDC identities in Access Management. Agents authenticate using SPIFFE JWT-SVIDs issued by SPIRE, enabling per-instance identity attestation with delegation chains. This feature supports three agent personas (User-Embedded, Hosted Delegated, and Autonomous) and includes Client Identity Metadata Document (CIMD) bootstrap for automated application provisioning.

## Key Concepts

### Agent Application Types

Agent applications are standard OAuth clients with `type=AGENT` and one of three personas:

| Persona | Description | Redirect URIs | Allowed Grants |
|:--------|:------------|:--------------|:---------------|
| **User-Embedded** | Agent acts on behalf of an authenticated user within a user-facing application | Required | `authorization_code`, `refresh_token` (no `client_credentials`) |
| **Hosted Delegated** | Agent runs in a hosted environment and acts on behalf of users | Required | `authorization_code`, `refresh_token`, `client_credentials` |
| **Autonomous** | Agent operates independently without user context | Not required | `client_credentials` only (no `authorization_code` or `refresh_token`) |

All agent applications forbid `implicit`, `password`, and `urn:ietf:params:oauth:grant-type:uma-ticket` grant types. Tokens issued to agents include a `client_profile` claim (e.g., `"ai_agent autonomous"`) and a `sub_profile` claim for the agent persona. The `act.sub` claim carries the agent instance ID for User-Embedded and Hosted Delegated agents, enabling downstream systems to track the acting agent instance in delegation chains.

### SPIFFE Workload Identity Settings

Applications using SPIFFE authentication configure workload identity settings:

| Property | Description |
|:---------|:------------|
| **Trust Domain** | Registered trust domain name (must exist in the domain's trust domain registry) |
| **Subject** | SPIFFE URI identifying the workload (e.g., `spiffe://example.org/hotel-agent`) |
| **Subject Match Mode** | `EXACT` (default) or `PREFIX` |

**Subject Match Mode** determines how JWT-SVID subjects are validated:

- **Exact Match**: The SVID `sub` claim must exactly equal the configured subject. Used for single-instance workloads and User-Embedded agents.
- **Prefix Match**: The SVID `sub` claim must start with the configured subject (which must end with `/`). Only allowed for Hosted Delegated and Autonomous agents. Enables per-instance identity attestation (e.g., `spiffe://example.org/hotel-agent/instance-a`, `spiffe://example.org/hotel-agent/instance-b`).

When Prefix Match is used with Hosted Delegated or Autonomous agents, each SVID subject becomes a distinct agent instance. The full SPIFFE URI is set as the agent instance ID and propagated to `act.sub` in issued tokens.

### Client Identity Metadata Document (CIMD)

CIMD allows administrators to create applications by referencing a hosted metadata document URL instead of manually entering OAuth settings. The document URL becomes the application's `client_id`. AM fetches the document, validates it against RFC 7591 rules, and pre-populates all OAuth settings (redirect URIs, grants, scopes, JWKS, mTLS, CIBA, software metadata). The document is cached in the gateway on creation. CIMD clients cannot use secret-based authentication methods (`client_secret_basic`, `client_secret_post`, `client_secret_jwt`).
