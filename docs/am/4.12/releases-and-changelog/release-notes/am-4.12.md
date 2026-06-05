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

* Introduces AI agents as first-class OAuth/OIDC identities with three personas: User-Embedded (acting within user sessions), Hosted Delegated (per-instance identity with user context), and Autonomous (independent agents).
* Agents authenticate using SPIFFE JWT-SVIDs issued by SPIRE servers, enabling cryptographically verifiable workload identities with delegation chains tracked via the `act` claim.
* Administrators can create agent applications from Client Identity Metadata Documents (CIMD) or configure them manually, with support for exact or prefix matching of SPIFFE IDs to enable per-instance identity attestation.
* Trust domains must be registered in Access Management with JWKS URLs and allowed signature algorithms to validate JWT-SVIDs against SPIRE trust bundles.
* Agent applications prohibit `implicit`, `password`, and `refresh_token` grants; User-Embedded and Hosted Delegated agents support `authorization_code` only, while Autonomous agents use `client_credentials`.
<!-- /PIPELINE:AM-7077 -->

## Improvements

## Bug Fixes
