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

* Introduces agent applications as first-class OAuth/OIDC identities for AI agents and autonomous workloads, supporting three personas: User Embedded, Hosted Delegated, and Autonomous.
* Agents authenticate using SPIFFE JWT-SVIDs attested by SPIRE or agent-specific JWT-bearer assertions, enabling per-instance identity with delegation chains.
* Trust domains can be configured at the domain level to validate workload identities across distributed systems, with support for JWKS URL-based trust bundles and configurable refresh intervals.
* Agent applications require certificate-based token endpoint authentication (`private_key_jwt`, `tls_client_auth`, `self_signed_tls_client_auth`, `spiffe_jwt`, or `agent-jwt-bearer`) and cannot use secret-based methods or `implicit`, `password`, or `refresh_token` grants.
* Administrators can create agent applications manually or bootstrap them from Client Identity Metadata Documents (CIMD) for streamlined registration.
<!-- /PIPELINE:AM-7077 -->

## Improvements

## Bug Fixes
