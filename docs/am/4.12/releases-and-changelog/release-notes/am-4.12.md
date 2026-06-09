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

* Introduces agent applications as first-class OAuth/OIDC identities for AI agents and autonomous services, supporting three personas: User-Embedded (acts on behalf of authenticated users), Hosted Delegated (maintains own identity in delegation chain), and Autonomous (acts independently).
* Enables authentication using SPIFFE JWT-SVIDs issued by SPIRE or other SPIFFE-compliant workload identity providers, with configurable trust domains that validate workload credentials via JWKS URLs and signing algorithms.
* Supports per-instance identity attestation through prefix matching mode (available for Hosted Delegated and Autonomous agents), allowing multiple workload instances to authenticate under a single application configuration.
* Allows administrators to bootstrap agent applications from Client Identity Metadata Documents (CIMD) by providing a metadata URL, with server-side validation and read-only preview before creation.
* Enforces persona-specific grant type constraints and requires redirect URIs for User-Embedded and Hosted Delegated agents; agent applications can be marked as DCR/CIMD registration templates starting in AM 4.12.0.
<!-- /PIPELINE:AM-7077 -->

## Improvements

## Bug Fixes
