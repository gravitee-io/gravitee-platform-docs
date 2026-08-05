---
description: >-
  This article explores the additional features that you get from the enterprise
  Gravitee Access Management solution.
metaLinks:
  alternates:
    - >-
      https://app.gitbook.com/s/H4VhZJXn1S232OEmh8Wv/overview/open-source-vs-enterprise-am
---

# Gravitee AM Enterprise Edition

## Introduction <a href="#introduction" id="introduction"></a>

Gravitee offers open source (OSS) and enterprise versions of its Access Management (AM) distribution package. This article introduces the additional features, capabilities, hosting options, and support options that are included in the Gravitee Enterprise Edition of Access Management.​

{% hint style="info" %}
**Other Gravitee Products**

Gravitee's platform extends beyond just Access Management. For information on enterprise versions of other products, please refer to our [platform overview documentation.](https://documentation.gravitee.io/apim/readme/enterprise-edition)
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

## Enterprise plugins <a href="#enterprise-policy-pack" id="enterprise-policy-pack"></a>

The following packs consist of Gravitee Enterprise Edition plugins. These are not included in the default distribution and must be manually downloaded [here](https://download.gravitee.io/).

EE plugins are installed from their respective repositories in GitHub. Gravitee’s EE plugin repositories are private and their names are prefixed as `gravitee-io/gravitee-policy-<plugin-name>`. For example, the Data Logging Masking Policy repository is at `https://github.com/gravitee-io/gravitee-policy-data-logging-masking`.

If you have not been granted access to private EE plugin repositories as part of your EE license request process, email [contact@graviteesource.com](mailto:contact@graviteesource.com).

### Enterprise Identity Provider pack <a href="#enterprise-policy-pack" id="enterprise-policy-pack"></a>

The Enterprise Identity Provider pack enables the use of different IDPs when setting up your Gravitee Access Management OAuth2 server:

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

## How AM applies your license

AM reads your Enterprise entitlements from a license. Where that license comes from depends on how AM is deployed.

### Self-hosted deployments

You install a license on each AM node, and each node applies the entitlements in that license. Connecting a self-hosted installation to Gravitee Cockpit for environment management doesn't change this. The installation stays a standalone one and keeps applying its own installed license.

### Gravitee-managed deployments

Gravitee assigns a license to your organization and keeps it in step with your subscription. AM stores that organization license and applies it across both the AM API and the AM Gateway. You don't install or upload this license yourself, and AM Console has no screen to edit it. Your subscription in Gravitee Cloud stays the source of truth.

### What happens when a feature isn't included

On a Gravitee-managed deployment, AM applies the organization license at three points.

AM Console lists every plugin in the catalog. Selecting one your license doesn't include opens an upgrade dialog instead of saving the configuration.

The AM API rejects a request that creates or updates a configuration for such a plugin with `403 Forbidden` and this message:

```
Plugin '<plugin-id>' requires the feature '<feature>' which is not included in your organization's license
```

AM doesn't restrict reading or deleting an existing configuration, so what you already configured stays visible and removable.

At the AM Gateway, a security domain that references such a plugin still deploys. The Gateway skips the unlicensed plugin and keeps serving the rest of the domain's configuration. Plugins that don't require an Enterprise feature always load.

### License expiry and downgrade

An expired license leaves only the plugins that don't require an Enterprise feature enabled. An organization with no license assigned behaves the same way. A downgrade withdraws the features the new subscription drops and leaves the rest in place.

Expiry doesn't interrupt a running Gateway. Security domains that are already deployed keep running with the plugins they loaded, and the new restriction takes effect the next time the domain is updated or the Gateway restarts.

Every license change Gravitee applies to your organization is recorded in the organization audit log. See [Audit Trail](../../guides/audit-trail.md) for the event types and how to view the log.

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

For more information on each, please refer to our [AM Architecture documentation](../am-architecture/README.md).

## Support options

Gravitee offers enterprise-grade support for enterprise customers, available in three different packages: Gold, Platinum, and Diamond. Each has different SLAs, benefits, etc. For more information, please [refer to our pricing page](https://www.gravitee.io/pricing).
