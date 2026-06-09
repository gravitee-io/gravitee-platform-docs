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
#### **Automation API for Programmatic Resource Management**

* Provides a machine-oriented HTTP interface for managing AM domains, identity providers, certificates, and reporters through infrastructure-as-code workflows.
* Uses idempotent PUT operations following API Management Automation API conventions, with resources organized under a three-level hierarchy (organizations > environments > domains).
* Supports system resources pre-configured via `gravitee.yml` and user-defined resources identified by immutable keys following the pattern `^[a-z0-9]([a-z0-9-]*[a-z0-9])?$`.
* Requires enabling via `api.http.api.automation.enabled: true` in `gravitee.yml` and authentication using JWT bearer tokens, service-account access tokens, or HTTP Basic credentials.
* OpenAPI specification available at the configured entrypoint (default: `/management/automation`) for integration with automation tools like the Gravitee Terraform provider (currently in technical preview).
<!-- /PIPELINE:AM-6850 -->

## Improvements

## Bug Fixes
