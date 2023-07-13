---
description: >-
  This article explores the additional features that you get from the Gravitee
  Enterprise Access Management solution.
---

# Open Source vs Enterprise AM

## Introduction <a href="#introduction" id="introduction"></a>

Gravitee offers both an open source (OSS) and an enterprise version of its Access Management (AM) platform. In this article, we'll discuss the additional features, capabilities, hosting options, and support options that come with the Gravitee Enterprise edition of API Management.​

{% hint style="info" %}
**Other Gravitee Products**

Gravitee's platform extends beyond just API Management. For information on enterprise versions of other products, please refer to our [platform overview documentation.](https://documentation.gravitee.io/platform-overview/gravitee-essentials/gravitee-offerings-ce-vs-ee)
{% endhint %}

## Gravitee Community Edition AM vs Gravitee Enterprise Edition AM <a href="#gravitee-community-edition-api-management-vs-gravitee-enterprise-edition-api-management" id="gravitee-community-edition-api-management-vs-gravitee-enterprise-edition-api-management"></a>

Please see the following features and capabilities that you get with the enterprise version of Gravitee AM. Please be aware that the enterprise version of Gravitee is broken up into three different packaging structures, each with access to different amount of the below enterprise capabilities. For more information on each package, please refer to our [pricing page](https://www.gravitee.io/pricing).

### Enterprise features <a href="#enterprise-features" id="enterprise-features"></a>

The below features are included in the default enterprise API Management distribution and will not require the addition of any enterprise plugins:

* Risk Assessment
* SAML v2
* Geo IP

### Enterprise Identity Provider pack <a href="#enterprise-policy-pack" id="enterprise-policy-pack"></a>

The Enterprise Identity Provider pack enables you to use different IdPs when setting up your Gravitee Access Management Oauth2 server:

* CAS
* Kerberos
* SAML 2.0
* LDAP
* Azure AD
* HTTP Flow
* France Connect
* Salesforce

### Enterprise MFA Factor Pack

The Enterprise MFA Factor Pack enables you to make use of advanced authentication factors for MFA:

* Phone Call
* FIDO2
* HTTP
* Recovery Code
* SMS Factor
* Twilio Resource

### Advanced API Monitoring <a href="#advanced-api-monitoring" id="advanced-api-monitoring"></a>

While not technically a part of the Access Management product, Gravitee does offer a standalone API Monitoring solution called Gravitee Alert Engine. Gravitee Alert Engine (AE) is Gravitee's enterprise grade API Monitoring solution. Alert Engine (AE) provides APIM and AM users with efficient and flexible API platform monitoring, including advanced alerting configuration and notifications sent through their preferred channels, such as email, Slack and Webhooks.Alert Engine integrates with Gravitee API Management to enable advanced alerting, new dashboards, and more. For more information, please refer to [the Alert Engine documentation](https://documentation.gravitee.io/ae/overview/introduction-to-gravitee-alert-engine).

### Advanced environment management <a href="#advanced-environment-management" id="advanced-environment-management"></a>

Gravitee EE AM enables you to register multiple AM environments and installations using [Gravitee Cloud.](https://documentation.gravitee.io/gravitee-cloud) This enables you to manage environment hierarchies and promote APIs across higher and lower environments.

### Hosting options <a href="#hosting-options" id="hosting-options"></a>

An investment in Gravitee EE is an investment in deployment flexibility, and, optionally, the ability to offload costs associated with maintaining self-hosted AM installations. Gravitee Enterprise supports:

* **Self-hosted deployments**: install and host AM within your own private cloud/environment
* **Gravitee-managed deployments**: Gravitee hosts and manages all AM components within its own cloud environments
* **Hybrid deployment**: Gravitee hosts and manages some AM components in its own cloud environment while you manage some components in your own private cloud/environment

For more information on each, please refer to our [AM Architecture documentation](am-architecture.md).

#### Support options <a href="#support-options" id="support-options"></a>

Gravitee offers enterprise-grade support for enterprise customers. Gravitee offers three different support packages: Gold, Platinum, and Diamond. Each has different SLAs, benefits, etc. For more information on each support option, please [refer to our pricing page](https://www.gravitee.io/pricing).
