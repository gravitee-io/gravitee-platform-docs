---
description: >-
  This article explores the additional features that you get from the enterprise
  Gravitee Access Management solution.
---

# Gravitee AM Enterprise Edition

## Introduction <a href="#introduction" id="introduction"></a>

Gravitee offers open source (OSS) and enterprise versions of its Access Management (AM) distribution package. This article introduces the additional features, capabilities, hosting options, and support options that are included in the Gravitee Enterprise Edition of Access Management.​

{% hint style="info" %}
**Other Gravitee Products**

Gravitee's platform extends beyond just Access Management. For information on enterprise versions of other products, please refer to our [platform overview documentation.](https://documentation.gravitee.io/platform-overview/gravitee-essentials/gravitee-offerings-ce-vs-ee)
{% endhint %}

## Enterprise AM <a href="#gravitee-community-edition-api-management-vs-gravitee-enterprise-edition-api-management" id="gravitee-community-edition-api-management-vs-gravitee-enterprise-edition-api-management"></a>

The Gravitee AM Enterprise Edition is available as three different packages, each offering a different level of access to enterprise features and capabilities. For more information, please refer to our [pricing page](https://www.gravitee.io/pricing).

### Enterprise features <a href="#enterprise-features" id="enterprise-features"></a>

{% hint style="warning" %}
The features below are included in the default enterprise Access Management distribution and do not require additional enterprise plugins
{% endhint %}

* Risk Assessment
* SAML v2
* Geo IP
* Account Linking
* Certificate fallback for JWT signing

#### Certificate fallback for JWT signing

Certificate fallback provides a resilience mechanism for JWT signing operations in multi-tenant environments. When a client's primary certificate fails to load or sign a JWT, the system attempts signing with a domain-level fallback certificate before using the default HMAC certificate or failing completely.

**Certificate selection hierarchy**

The system evaluates certificates in a three-tier priority order:

1. **Client-specific certificate**: Configured in the client settings
2. **Domain-level fallback certificate**: Used when the primary certificate is unavailable or signing fails
3. **Default HMAC certificate**: Used only if `fallbackToHmacSignature` is enabled and no fallback certificate is available

If no certificate succeeds and `fallbackToHmacSignature` is disabled, the system throws a `TemporarilyUnavailableException`.

**Domain isolation**

Certificate access follows domain isolation rules:

- Non-master domains can only access certificates belonging to their own domain ID
- Master domains have cross-domain access for introspection purposes
- The fallback certificate must belong to the same domain unless the domain is configured as a master domain

**Mutual exclusion rule**

The fallback certificate is automatically skipped if its ID matches the primary certificate ID. This prevents infinite loops and ensures the system progresses through the certificate hierarchy correctly.

**Prerequisites**

- A valid certificate deployed in the domain's certificate repository
- `DOMAIN_SETTINGS[UPDATE]` permission on the domain, environment, or organization
-

**Gateway configuration**

Configure the fallback certificate at the domain level using the certificate settings property.

| Property | Type | Default | Description |
|:---------|:-----|:--------|:------------|
| `fallbackCertificate` | String | null | ID of the certificate to use as fallback when primary certificate fails |

**Creating certificate settings**

Use the Management API to configure certificate settings without triggering a full domain reload. Send a PUT request to `/organizations/{organizationId}/environments/{environmentId}/domains/{domain}/certificate-settings` with a JSON body containing the `fallbackCertificate` property set to a valid certificate ID.

The endpoint returns the updated certificate settings object. This operation requires `DOMAIN_SETTINGS[UPDATE]` permission and validates that:

- The fallback certificate exists in the domain's certificate repository
- The fallback certificate belongs to the same domain (unless the domain is a master domain)

**JWT signing with fallback**

When signing a JWT, the system:

1. Attempts to use the client's configured certificate
2. If signing fails, retrieves the fallback certificate from the domain settings
3. Verifies that the fallback certificate ID differs from the primary certificate ID
4. Logs a warning message: `"Failed to sign JWT with certificate: {primary}, attempting fallback using: {fallback}"`
5. Attempts signing with the fallback certificate

If the fallback certificate is unavailable and `fallbackToHmacSignature` is enabled, the system uses the default HMAC certificate and logs: `"Certificate: {primary} not loaded, using default certificate as fallback"`. Otherwise, it throws a `TemporarilyUnavailableException`.

**Architecture notes**

*Event-driven settings updates*

Certificate settings are managed via a new event type (`DomainCertificateSettingsEvent.UPDATE`) that allows runtime updates without requiring a full domain reload. This event-driven approach improves operational efficiency by enabling administrators to update fallback certificate configurations dynamically.

*Logging for observability*

All fallback operations are logged at WARN level with explicit certificate IDs. This provides operational visibility into certificate failures and fallback usage patterns, enabling administrators to identify and resolve certificate availability issues proactively.

*Permission granularity*

The feature introduces three new permission types for finer-grained access control: `PROTECTED_RESOURCE_SETTINGS`, `PROTECTED_RESOURCE_OAUTH`, and `PROTECTED_RESOURCE_CERTIFICATE`. These replace the generic `PROTECTED_RESOURCE[ACTION]` permissions and enable more precise authorization policies for protected resource management.

**Restrictions**

- Fallback certificate must exist in the domain's certificate repository
- Fallback certificate must belong to the same domain (unless domain is master)
- Fallback certificate ID can't match the primary certificate ID
- Requires `DOMAIN_SETTINGS[UPDATE]` permission to modify certificate settings
- System certificates were previously filtered from UI selection but are now available for fallback configuration
- If `fallbackToHmacSignature` is disabled and no fallback certificate is available, authentication fails with `TemporarilyUnavailableException`

**Related changes**

The Management API now includes a dedicated PUT endpoint for certificate settings at `/organizations/{organizationId}/environments/{environmentId}/domains/{domain}/certificate-settings`. The UI certificate settings dialog has been updated to include system certificates in the selection list, which were previously filtered out. Certificate settings updates are validated to ensure the fallback certificate exists and belongs to the correct domain. The system logs all fallback operations with explicit certificate IDs for operational monitoring.

## Enterprise plugins <a href="#enterprise-policy-pack" id="enterprise-policy-pack"></a>

The following packs consist of Gravitee Enterprise Edition plugins. These are not included in the default distribution and must be manually downloaded [here](https://download.gravitee.io/).

EE plugins are installed from their respective repositories in GitHub. Gravitee's EE plugin repositories are private and their names are prefixed as `gravitee-io/gravitee-policy-<plugin-name>`. For example, the Data Logging Masking Policy repository is at `https://github.com/gravitee-io/gravitee-policy-data-logging-masking`.

If you have not been granted access to private EE plugin repositories as part of your EE license request process, email [contact@graviteesource.com](mailto:contact@graviteesource.com).

### Enterprise Identity Provider pack <a href="#enterprise-policy-pack" id="enterprise-policy-pack"></a>

The Enterprise Identity Provider pack enables the use of different IdPs when setting up your Gravitee Access Management OAuth2 server:

* CAS
* Kerberos
* SAML 2.0
* LDAP
* Azure AD
* HTTP Flow
* France Connect
* Salesforce

### Enterprise MFA pack

The Enterprise MFA pack enables advanced authentication factors for MFA:

* Phone Call
* FIDO2
* HTTP
* Recovery Code
* SMS Factor
* Twilio Resource
* MFA Challenge

### Secret Manager pack

The Secret Manager pack enables clients that manage connections, retries, and credentials renewal when connecting to Secret Managers:

* HashiCorp Vault

### Authorization Engine pack

The Authorization Engine pack enables authorization features for MCP Servers:

* OpenFGA
* AuthZen

## Advanced API monitoring <a href="#advanced-api-monitoring" id="advanced-api-monitoring"></a>

Not technically a part of the Access Management product, Gravitee offers a standalone, enterprise-grade API monitoring solution called Gravitee Alert Engine (AE).

AE provides APIM and AM users with efficient and flexible API platform monitoring, including advanced alerting configurations and notifications sent through preferred channels, such as email, Slack and Webhooks. Alert Engine integrates with Gravitee APIM and AM to enable advanced alerting, new dashboards, etc.

For more information, please refer to [the Alert Engine documentation](https://documentation.gravitee.io/alert-engine).

## Advanced environment management

Gravitee APIM EE includes [Gravitee Cockpit](https://documentation.gravitee.io/gravitee-cloud), which you can use to register multiple APIM environments and installations. This allows you to manage environment hierarchies and promote APIs across higher and lower environments.

## Hosting options

An investment in Gravitee EE is an investment in deployment flexibility, and, optionally, the ability to offload costs associated with maintaining self-hosted Access Management installations. Gravitee Enterprise supports:

* **Self-hosted deployments**: Install and host AM within your own private cloud/environment.
* **Gravitee-managed deployments**: Gravitee hosts and manages all AM components within its own cloud environment.
* **Hybrid deployment**: Gravitee hosts and manages some AM components within its cloud environment while you manage others within your private cloud/environment.

For more information on each, please refer to our [AM Architecture documentation](../am-architecture/).

## Support options

Gravitee offers enterprise-grade support for enterprise customers, available in three different packages: Gold, Platinum, and Diamond. Each has different SLAs, benefits, etc. For more information, please [refer to our pricing page](https://www.gravitee.io/pricing).
