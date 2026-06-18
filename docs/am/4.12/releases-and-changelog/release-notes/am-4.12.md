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


<!-- PIPELINE:AM-6850 -->
#### **Automation API for Declarative Resource Management**

* Introduces a machine-oriented HTTP API for managing AM domains, identity providers, certificates, and reporters using stable, user-defined keys instead of database-generated IDs.
* Enables infrastructure-as-code workflows through idempotent PUT operations and an OpenAPI specification served at the configured entrypoint (default: `/management/automation`).
* Supports system resources that inherit configuration from `gravitee.yml`, allowing centralized management of default identity providers and reporters.
* Requires AM Gateway 4.12+ and must be explicitly enabled via `gravitee.http.api.automation.enabled: true` in gateway configuration.
* Resources created through the Automation API are isolated from those created via the Management REST API or Console UI.
<!-- /PIPELINE:AM-6850 -->
<!-- PIPELINE:AM-7077 -->
#### **SPIFFE Workload Identity and Agent Applications**

* AM now supports SPIFFE workload identity authentication, enabling secure machine-to-machine communication using cryptographically verifiable identities instead of static credentials.
* Configure SPIFFE trust domains to validate JWT-SVIDs from external workload identity providers like SPIRE, with support for JWKS URL or static bundle sources.
* Create Agent applications with three persona types: Autonomous (self-contained AI agents), Hosted Delegated (platform-hosted agents acting on behalf of users), and User-Embedded (agents embedded in user-facing applications).
* Enable Client ID Metadata Document (CIMD) support to allow dynamic client registration and metadata discovery with built-in SSRF protection for private IP addresses and unsecured URIs.
* SPIFFE authentication uses the `spiffe_jwt` token endpoint authentication method and requires trust domain configuration at the security domain level.
<!-- /PIPELINE:AM-7077 -->

## Improvements

## Bug Fixes
