# AM 4.12

## Highlights

## Breaking Changes

#### **Java 25 runtime requirement**

Gravitee AM 4.12 now runs on Java 25. If you deploy AM using the distribution ZIP file or the RPM package, make sure a JRE 25 is installed and available in your environment before upgrading.

#### **Upgrade to Eclipse Vert.x 5**

Gravitee AM now runs on Eclipse Vert.x 5. If you develop custom plugins, make sure they are compatible with this new version before upgrading, as APIs and behaviors may have changed between Vert.x versions.

#### **Resend code on MFA challenge screen**

The behavior of the MFA challenge screen has changed. Previously, refreshing the page would invalidate (end) the existing code; now resending a code is handled explicitly through the resend option. If you use a custom MFA challenge template, it may need to be updated to take advantage of this feature. Refer to the [reference template](https://github.com/gravitee-io/gravitee-access-management/tree/4.12.x/gravitee-am-gateway/gravitee-am-gateway-handler/gravitee-am-gateway-handler-core/src/main/resources/webroot/views/mfa_challenge.html#L93) for the expected markup.

## New Features

#### **Resend code on MFA challenge screen**

* Users can now trigger a resend of their verification code directly from the MFA challenge screen, without refreshing the page.
* Available for email and SMS factors.

#### **New TCP reporter**

* Introduces a new TCP reporter, giving you another option for streaming audits to external systems.

#### **WebAuthn Client-Side Error Monitoring**

* Client-side WebAuthn errors occurring in the browser, such as biometric failure, user cancellation, unsupported device, and security issues, are now captured and sent to the backend for logging and analysis.
* Errors are automatically classified into business-readable categories such as `USER_CANCEL_OR_TIMEOUT`, `AUTHENTICATOR_FAILURE`, `NOT_SUPPORTED`, `SECURITY_ISSUE`, and `INVALID_REQUEST`.
* Each error event is enriched with context, including browser, user agent, correlation ID, and RP ID, and stored as structured JSON—searchable in your logging infrastructure.
* No sensitive data (biometric data, credential IDs) is included in the error payload.
* Improves troubleshooting of passwordless authentication failures, security monitoring, and WebAuthn adoption tracking across major browsers, including Chrome, Edge, Firefox, and Safari.

#### **SAML Assertion Encryption**

* Gravitee AM can now encrypt SAML assertions when acting as a SAML Identity Provider, ensuring sensitive identity attributes are protected end-to-end and only readable by the intended Service Provider.
* Configure encryption per SP: upload the SP's public encryption certificate, and then choose to sign only, encrypt only, or sign and encrypt assertions.
* Supports standard key transport algorithms (`RSA-OAEP`, `RSA1_5`) and data encryption algorithms (`AES-128`, `AES-256`), following modern security recommendations by default.
* When enabled, the `<Assertion>` element is replaced by `<EncryptedAssertion>` in the SAML response; the SP decrypts it using its private key.
* Encryption is disabled by default—existing SAML integrations continue to work without any changes.
* Requires gravitee-am-gateway-handler-saml2-idp plugin in version 5.0 or higher.

#### **Policy Studio on Service Applications**

* The Policy Studio / Flow editor is now available on Service applications, also to Web, SPA, and Native application types.
* The **Design** menu for Service applications exposes the **Flows** tab, allowing policies to be applied on the `TOKEN` flows.
* Policy configuration on Service applications follows the same experience as other application types.

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


<!-- PIPELINE:AM-6980 -->
#### **Application Filtering, Cursor Pagination, and Expand Parameters**

This release includes the following capabilities:

* Filter Applications by a `status` of `enabled` or `disabled`, or by owner email address, using query parameters on the Application list API.
* Expand API responses to include OAuth client IDs with the `expand=clientId` parameter, reducing the need for follow-up API calls.
* Use the cursor-based pagination endpoint `/applications/search/_cursor` for efficient traversal of large Application datasets with opaque Base64-encoded tokens.
* Combine filters with AND logic between `status` and owner, and OR logic within application types, to enable granular Application discovery workflows.
* Requires `DOMAIN_APPLICATION[LIST]` permission for the target domain and `ORGANIZATION_USER[READ]` permission to filter by owner email.
<!-- /PIPELINE:AM-6980 -->
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
