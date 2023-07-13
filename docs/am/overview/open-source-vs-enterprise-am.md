---
description: >-
  This article explores the additional features that you get from the enterprise
  Gravitee Access Management solution.
---

# Gravitee AM Enterprise Edition

## Introduction <a href="#introduction" id="introduction"></a>

Gravitee offers both an open source (OSS) and an enterprise version of its Access Management (AM) platform. This article introduces the additional features, capabilities, hosting options, and support options that are included in the Gravitee Enterprise Edition of API Management.​

{% hint style="info" %}
**Other Gravitee Products**

Gravitee's platform extends beyond just API Management. For information on enterprise versions of other products, please refer to our [platform overview documentation.](https://documentation.gravitee.io/platform-overview/gravitee-essentials/gravitee-offerings-ce-vs-ee)
{% endhint %}

## Enterprise Edition AM <a href="#gravitee-community-edition-api-management-vs-gravitee-enterprise-edition-api-management" id="gravitee-community-edition-api-management-vs-gravitee-enterprise-edition-api-management"></a>

The Gravitee AM Enterprise Edition is available in three different packages, each offering a different level of access to enterprise features and capabilities. For more information, please refer to our [pricing page](https://www.gravitee.io/pricing).

## Enterprise features <a href="#enterprise-features" id="enterprise-features"></a>

The features below are included in the default enterprise API Management distribution and do not require additional enterprise plugins:

* Risk Assessment
* SAML v2
* Geo IP

## Enterprise Identity Provider pack <a href="#enterprise-policy-pack" id="enterprise-policy-pack"></a>

The Enterprise Identity Provider pack enables the use of different IdPs when setting up your Gravitee Access Management OAuth2 server:

* CAS
* Kerberos
* SAML 2.0
* LDAP
* Azure AD
* HTTP Flow
* France Connect
* Salesforce

## Enterprise MFA pack

The Enterprise MFA pack enables advanced authentication factors for MFA:

* Phone Call
* FIDO2
* HTTP
* Recovery Code
* SMS Factor
* Twilio Resource

## Advanced API monitoring <a href="#advanced-api-monitoring" id="advanced-api-monitoring"></a>

While not technically a part of the Access Management product, Gravitee does offer a standalone, enterprise-grade API monitoring solution called Gravitee Alert Engine (AE). AE provides APIM and AM users with efficient and flexible API platform monitoring, including advanced alerting configurations and notifications sent through preferred channels, such as email, Slack and Webhooks. Alert Engine integrates with Gravitee API Management to enable advanced alerting, new dashboards, etc. For more information, please refer to [the Alert Engine documentation](https://documentation.gravitee.io/ae/overview/introduction-to-gravitee-alert-engine).

## Advanced environment management <a href="#advanced-environment-management" id="advanced-environment-management"></a>

Gravitee EE AM enables you to register multiple AM environments and installations using [Gravitee Cloud.](https://documentation.gravitee.io/gravitee-cloud) This allows you to manage environment hierarchies and promote APIs across higher and lower environments.

## Hosting options <a href="#hosting-options" id="hosting-options"></a>

An investment in Gravitee EE is an investment in deployment flexibility, and, optionally, the ability to offload costs associated with maintaining self-hosted AM installations. Gravitee Enterprise supports:

* **Self-hosted deployments**: Install and host AM within your own private cloud/environment.
* **Gravitee-managed deployments**: Gravitee hosts and manages all AM components within its own cloud environments.
* **Hybrid deployment**: Gravitee hosts and manages some AM components in its cloud environment while you manage others in your own private cloud/environment.

For more information, please refer to our [AM Architecture documentation](am-architecture.md).

## Support options <a href="#support-options" id="support-options"></a>

Gravitee offers enterprise-grade support for enterprise customers, available in three different packages: Gold, Platinum, and Diamond. Each has different SLAs, benefits, etc. For more information on each support option, please [refer to our pricing page](https://www.gravitee.io/pricing).
