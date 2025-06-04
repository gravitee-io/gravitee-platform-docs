# Getting Started

## How to get started

Set up Gravitee quickly and easily with Gravitee Cloud's 14-day **free** trial.&#x20;

<table data-card-size="large" data-view="cards"><thead><tr><th></th><th data-hidden data-card-target data-type="content-ref"></th></tr></thead><tbody><tr><td>Cloud free trial</td><td><a href="https://eu-auth.cloud.gravitee.io/cloud/register?response_type=code&#x26;client_id=fd45d898-e621-4b12-85d8-98e621ab1237&#x26;state=aFNXUER4ZTJLeVA3cUhZblVpNnI1a0dqT0lFT3Qtd1ZjN0xUMGgyQVU2ZU1Q&#x26;redirect_uri=https%3A%2F%2Feu.cloud.gravitee.io&#x26;scope=openid+profile+email+offline_access&#x26;code_challenge=RawzckmLjFNOvDqrZUPumHbMzXRcIjRRbZFmWlbjLoA&#x26;code_challenge_method=S256&#x26;nonce=aFNXUER4ZTJLeVA3cUhZblVpNnI1a0dqT0lFT3Qtd1ZjN0xUMGgyQVU2ZU1Q&#x26;createUser=true&#x26;hubspotutk=169d02e0ddc1d02ed3202bcac0869f20">https://eu-auth.cloud.gravitee.io/cloud/register?response_type=code&#x26;client_id=fd45d898-e621-4b12-85d8-98e621ab1237&#x26;state=aFNXUER4ZTJLeVA3cUhZblVpNnI1a0dqT0lFT3Qtd1ZjN0xUMGgyQVU2ZU1Q&#x26;redirect_uri=https%3A%2F%2Feu.cloud.gravitee.io&#x26;scope=openid+profile+email+offline_access&#x26;code_challenge=RawzckmLjFNOvDqrZUPumHbMzXRcIjRRbZFmWlbjLoA&#x26;code_challenge_method=S256&#x26;nonce=aFNXUER4ZTJLeVA3cUhZblVpNnI1a0dqT0lFT3Qtd1ZjN0xUMGgyQVU2ZU1Q&#x26;createUser=true&#x26;hubspotutk=169d02e0ddc1d02ed3202bcac0869f20</a></td></tr></tbody></table>

Install the OSS version of Gravitee locally with Docker.

<table data-card-size="large" data-view="cards"><thead><tr><th></th><th data-hidden data-card-target data-type="content-ref"></th></tr></thead><tbody><tr><td>Install with Docker</td><td><a href="broken-reference">Broken link</a></td></tr></tbody></table>

## Deployment Options

### Cloud

If you are not familiar with Gravitee, the easiest way to get Gravitee is with Gravitee Cloud. Gravitee Cloud is a simple and secure method of running the Gravitee API Management (APIM). With the Control Plane hosted by Gravitee, you can count on consistent availability, cutting-edge features, and innovations from the Gravitee team. For more information about Gravitee Cloud, see [Cloud.](https://documentation.gravitee.io/gravitee-cloud)&#x20;

Here are the Key benefits of Gravitee's Cloud solution:

* **Cloud Hosted Gateways**. Automatically scales and manages gateways, which reduces operational overhead.
* **Hybrid Deployment Model**. Keeps sensitive data within your infrastructure, which enhances security.
* **Multi-Tenancy Support**. Allows isolated environments and organizations within a single platform, which improves manageability.
* **Centralized API Management Console**. Provides a single place to manage and secure all APIs, which simplifies control.
* **Support for Sync & Async APIs**. Manages both REST and event-driven APIs in one solution, which unifies API governance.
* **Advanced Alerting and Monitoring**. Detects and responds to API issues with real-time alerts, which improves reliability.
* **Enterprise-Grade Access Management**. Controls user access with robust security and identity tools, which strengthens protection.
* **Flexible Hosting Options**. Offers cloud, self-hosted, and hybrid deployment choices, which increases deployment flexibility.

### Hybrid

With this deployment, Gravitee hosts the Control plane and you host the Data plane. For more information about Hybrid Deployment, see [hybrid-installation-and-configuration-guides](../hybrid-installation-and-configuration-guides/ "mention"). Here are the key benefits of a Hybrid deployment:

* **SaaS Control Plane with Self-Hosted Data Plane**. Combines Gravitee's cloud-managed control plane with your self-hosted gateways, which provides centralized management while maintaining control over API traffic. [documentation.gravitee.io](https://documentation.gravitee.io/gravitee-cloud/guides/hybrid?utm_source=chatgpt.com)
* **Bridge Gateway Architecture**. Utilizes a bridge gateway to connect the control plane with on-premises gateways, which enables secure communication without exposing internal databases. [documentation.gravitee.io](https://documentation.gravitee.io/apim/4.1/getting-started/hybrid-deployment?utm_source=chatgpt.com)
* **Cloud Gate and Cloud Tokens**. Employs secure endpoints and tokens for synchronization and analytics reporting, which ensures encrypted and authenticated interactions between components. [documentation.gravitee.io](https://documentation.gravitee.io/gravitee-cloud/guides/hybrid?utm_source=chatgpt.com)
* **Data Residency and Compliance**. Keeps sensitive data within your infrastructure, which helps meet data residency requirements and enhances security. [documentation.gravitee.io](https://documentation.gravitee.io/gravitee-cloud/guides/hybrid?utm_source=chatgpt.com)
* **Reduced Latency**. Processes API requests closer to your services, which minimizes latency and improves performance. [documentation.gravitee.io](https://documentation.gravitee.io/gravitee-cloud/guides/hybrid?utm_source=chatgpt.com)
* **Full Control over Traffic**. Routes all API traffic through your infrastructure, which allows complete oversight of routing, monitoring, and security enforcement. [documentation.gravitee.io](https://documentation.gravitee.io/gravitee-cloud/guides/hybrid?utm_source=chatgpt.com)
* **Scalability and Flexibility**. Provides the ability to scale gateways according to your needs, which offers flexibility in handling varying workloads. [documentation.gravitee.io](https://documentation.gravitee.io/gravitee-cloud/guides/hybrid?utm_source=chatgpt.com)
* **Customization and Integration**. Integrates with your existing systems, which allows customization to meet specific organizational requirements. [documentation.gravitee.io](https://documentation.gravitee.io/gravitee-cloud/guides/hybrid?utm_source=chatgpt.com)
* **Secure Communication**. Ensures all interactions between components are encrypted using TLS, which protects data in transit. [documentation.gravitee.io](https://documentation.gravitee.io/gravitee-cloud/guides/hybrid?utm_source=chatgpt.com)
* **Centralized Analytics and Monitoring**. Aggregates analytics and logs in the cloud control plane, which provides a unified view for monitoring and analysis. [documentation.gravitee.io](https://documentation.gravitee.io/gravitee-cloud/guides/hybrid?utm_source=chatgpt.com)

### Self-hosted

Control plane and Data Plane self-hosted / installed by you. For more information about self-hosted installations, see [self-hosted-installation-guides](../self-hosted-installation-guides/ "mention").

* **Flexible Deployment Options**. Supports various installation methods, including Docker, Kubernetes, RPM packages, and ZIP files, which allows you to choose the best fit for your infrastructure. [documentation.gravitee.io+1documentation.gravitee.io+1](https://documentation.gravitee.io/apim/4.3/getting-started/install-and-upgrade-guides?utm_source=chatgpt.com)
* **Full Control Over Infrastructure**. Enables you to manage and configure all components within your own environment, which ensures compliance with internal policies and regulations. [documentation.gravitee.io](https://documentation.gravitee.io/platform-overview/gravitee-platform/gravitee-offerings-ce-vs-ee?utm_source=chatgpt.com)
* **Customizable Architecture**. Allows integration with existing systems and customization of components, which provides flexibility to meet specific organizational needs.
* **Enhanced Security**. Keeps all data and traffic within your own network, which reduces exposure to external threats and enhances data protection. [documentation.gravitee.io](https://documentation.gravitee.io/platform-overview/gravitee-platform/gravitee-offerings-ce-vs-ee?utm_source=chatgpt.com)
* **Scalability**. Offers the ability to scale components horizontally or vertically, which accommodates growing API traffic and user demands.
* **Multi-Tenancy Support**. Supports multiple organizations and environments within a single installation, which enables efficient resource utilization and management. [documentation.gravitee.io](https://documentation.gravitee.io/apim/install-and-upgrade/multi-tenancy?utm_source=chatgpt.com)
* **Plugin Extensibility**. Provides a plugin system to extend functionality, which allows for the addition of custom policies, connectors, and more. [documentation.gravitee.io](https://documentation.gravitee.io/apim/4.1?utm_source=chatgpt.com)
* **Comprehensive Monitoring and Analytics**. Integrates with tools like Elasticsearch and Logstash, which facilitates detailed monitoring and analysis of API usage and performance.
* **Enterprise Support Options**. Offers enterprise-grade support packages, which provide access to expert assistance and service level agreements. [documentation.gravitee.io](https://documentation.gravitee.io/platform-overview/gravitee-platform/gravitee-offerings-ce-vs-ee?utm_source=chatgpt.com)
* **Open Source and Enterprise Editions**. Available in both open-source and enterprise versions, which allows you to choose based on your feature requirements and budget.

## Community Edition versus Enterprise Edition

{% hint style="info" %}
For a detailed description of the Enterprise Edition of Gravitee, see [open-source-vs-enterprise-edition.md](../introduction/open-source-vs-enterprise-edition.md "mention").
{% endhint %}

Hybrid deployment and self-hosted deployment are available in both Open-Source (OSS) and Enterprise Edition (EE). Here is a table that shows the high-level differences between OSS and EE:

<table><thead><tr><th width="214" align="center">Feature</th><th align="center">Description</th><th align="center">Community Edition</th><th align="center">Enterprise Edition</th></tr></thead><tbody><tr><td align="center"><strong>Audit Trail</strong></td><td align="center">Audit the consumption and activity of your Gravitee APIs per event and type to monitor the behavior of your APIs and platform</td><td align="center">No</td><td align="center">Yes</td></tr><tr><td align="center"><strong>Bridge Gateway</strong></td><td align="center">Deploy a Bridge Gateway, which is a proxy for a repository, to avoid opening a connection between a database and something outside its network. The sync occurs over HTTP instead of the database protocol.</td><td align="center">No</td><td align="center">Yes</td></tr><tr><td align="center"><strong>Custom roles</strong></td><td align="center">Create custom user roles to fit your needs. A role is a functional group of permissions and can be defined at the organization, environment, API, and/or application level.</td><td align="center">No</td><td align="center">Yes</td></tr><tr><td align="center"><strong>DCR</strong></td><td align="center">The dynamic client registration (DCR) protocol allows OAuth client applications to register with an OAuth server through the OpenID Connect (OIDC) client registration endpoint</td><td align="center">No</td><td align="center">Yes</td></tr><tr><td align="center"><strong>Debug mode</strong></td><td align="center">Easily test and debug your policy execution and enforcement</td><td align="center">No</td><td align="center">Yes</td></tr><tr><td align="center"><strong>Enterprise OpenID Connect SSO</strong></td><td align="center">Use OpenId Connect SSO with your API Management platform</td><td align="center">No</td><td align="center">Yes</td></tr><tr><td align="center"><strong>Sharding tags</strong></td><td align="center">Specify which "shard" of the Gateway an API should be deployed to. By tagging Gateways with specific keywords, you can select a tag in the API's proxy settings to control where the API will be deployed.</td><td align="center">No</td><td align="center">Yes</td></tr></tbody></table>
