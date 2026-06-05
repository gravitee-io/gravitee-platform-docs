# AM 4.12

## Highlights

## Breaking Changes

## New Features


<!-- PIPELINE:AM-6833 -->
#### **SAML Assertion Attribute Mapping**

* Customize NameID and assertion attributes in SAML responses using Expression Language (EL) expressions for flexible service provider integration.
* Configure custom NameID mapping to override the default internal user ID, with automatic fallback to email address when the service provider requests EMAIL format.
* Define custom assertion attributes as name-value pairs to replace the default attribute set (sub, preferred_username, email, given_name, family_name, name).
* Omit custom attribute mappings to maintain backward compatibility with the standard attribute set from previous versions.
<!-- /PIPELINE:AM-6833 -->


<!-- PIPELINE:AM-6906 -->
#### **Client ID Metadata Document (CIMD) Support**

* Enables OAuth clients to use a URL as their `client_id` and retrieve configuration dynamically from that URL, eliminating the need for pre-registration.
* The gateway fetches a JSON metadata document from the client_id URL, validates it against SSRF protection rules, and synthesizes client configuration by merging it with a designated template application.
* Supports automatic token revocation when remote metadata changes are detected, with configurable in-memory caching.
* Requires a template application configured in the domain and CIMD enabled in domain OIDC settings with SSRF protection configured (private IP blocking, HTTPS enforcement, domain allowlists).
* Designed for AI agents and Model Context Protocol (MCP) clients requiring agent-driven authentication workflows without manual registration.
<!-- /PIPELINE:AM-6906 -->


<!-- PIPELINE:AM-7077 -->
#### **SPIFFE Workload Identity and Agent Applications**

* Introduces AI agents as first-class OAuth/OIDC identities with three personas: User-Embedded (browser-based), Hosted Delegated (provider-hosted), and Autonomous (service-only).
* Agents authenticate using SPIFFE JWT-SVIDs attested by SPIRE, with per-instance identity support through prefix matching (e.g., `spiffe://am.local/hotel-agent/instance-a`).
* Trust Domains manage SPIFFE trust boundaries and JWKS bundles for SVID verification, configurable via console or Management API with automatic bundle refresh.
* Client Identity Metadata Documents (CIMD) enable application bootstrapping from hosted metadata URLs, automatically populating OAuth/OIDC settings including redirect URIs, grants, and JWKS.
* Agent applications restrict grant types by persona and prohibit `implicit`, `password`, and `refresh_token` grants for security.
<!-- /PIPELINE:AM-7077 -->

## Improvements

## Bug Fixes
