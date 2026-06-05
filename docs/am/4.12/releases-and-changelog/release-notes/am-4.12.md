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
#### **SPIFFE Workload Identity for AI Agent Applications**

* AI agents can now authenticate as first-class OAuth/OIDC clients using SPIFFE JWT-SVIDs issued by SPIRE, enabling per-instance identity attestation with delegation chains.
* Three agent personas are supported: User-Embedded (acts on behalf of authenticated users), Hosted Delegated (acts both on behalf of users and autonomously), and Autonomous (acts independently without user context).
* Administrators can configure SPIFFE trust domains with JWKS bundle sources and create agent applications from Client Identity Metadata Documents (CIMD) via hosted metadata URLs.
* SPIFFE subject validation supports exact matching or prefix matching (for Hosted Delegated and Autonomous agents only), and all agent types enforce restricted grant type policies.
* Requires Access Management 4.12.0 or later, SPIRE infrastructure, and database migration for new trust domain storage.
<!-- /PIPELINE:AM-7077 -->

## Improvements

## Bug Fixes
