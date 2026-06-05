# SPIFFE Workload Identity & Agent Applications Overview

## Overview

SPIFFE Workload Identity & Agent Applications introduces AI agents as first-class OAuth/OIDC identities in Access Management. Agents authenticate using SPIFFE JWT-SVIDs issued by SPIRE, enabling per-instance identity attestation with delegation chains. Administrators can create agent applications with three personas (User-Embedded, Hosted Delegated, Autonomous) and bootstrap them from Client Identity Metadata Documents (CIMD).

## Key Concepts

### SPIFFE Subject Matching

SPIFFE subjects are validated using two modes:

- **EXACT**: The JWT-SVID `sub` claim must exactly match the application's configured subject (e.g., `spiffe://acme/billing-agent`).
- **PREFIX**: The JWT-SVID `sub` claim must start with the application's configured subject prefix (e.g., `spiffe://acme/hotel-agent/` matches `spiffe://acme/hotel-agent/instance-a` and `spiffe://acme/hotel-agent/instance-b`). PREFIX mode is only allowed for Hosted Delegated and Autonomous agents. The subject must end with `/` to ensure path-boundary matching.

### Client Identity Metadata Document (CIMD)

CIMD enables application creation from a hosted metadata URL. Administrators provide a document URL; Access Management fetches and validates the metadata, then creates the application with all settings pre-populated. The document URL becomes the application's `client_id`. CIMD documents must use certificate-based authentication (`private_key_jwt`, `tls_client_auth`, `self_signed_tls_client_auth`) — secret-based methods are rejected.
