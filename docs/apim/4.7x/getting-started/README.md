# Getting Started

## How to get started

Set up Gravitee quickly and easily with Gravitee Cloud's 14-day **free** trial.&#x20;

<table data-card-size="large" data-view="cards"><thead><tr><th></th><th data-hidden data-card-target data-type="content-ref"></th></tr></thead><tbody><tr><td>Cloud free trial</td><td><a href="https://eu-auth.cloud.gravitee.io/cloud/register?response_type=code&#x26;client_id=fd45d898-e621-4b12-85d8-98e621ab1237&#x26;state=aFNXUER4ZTJLeVA3cUhZblVpNnI1a0dqT0lFT3Qtd1ZjN0xUMGgyQVU2ZU1Q&#x26;redirect_uri=https%3A%2F%2Feu.cloud.gravitee.io&#x26;scope=openid+profile+email+offline_access&#x26;code_challenge=RawzckmLjFNOvDqrZUPumHbMzXRcIjRRbZFmWlbjLoA&#x26;code_challenge_method=S256&#x26;nonce=aFNXUER4ZTJLeVA3cUhZblVpNnI1a0dqT0lFT3Qtd1ZjN0xUMGgyQVU2ZU1Q&#x26;createUser=true&#x26;hubspotutk=169d02e0ddc1d02ed3202bcac0869f20">https://eu-auth.cloud.gravitee.io/cloud/register?response_type=code&#x26;client_id=fd45d898-e621-4b12-85d8-98e621ab1237&#x26;state=aFNXUER4ZTJLeVA3cUhZblVpNnI1a0dqT0lFT3Qtd1ZjN0xUMGgyQVU2ZU1Q&#x26;redirect_uri=https%3A%2F%2Feu.cloud.gravitee.io&#x26;scope=openid+profile+email+offline_access&#x26;code_challenge=RawzckmLjFNOvDqrZUPumHbMzXRcIjRRbZFmWlbjLoA&#x26;code_challenge_method=S256&#x26;nonce=aFNXUER4ZTJLeVA3cUhZblVpNnI1a0dqT0lFT3Qtd1ZjN0xUMGgyQVU2ZU1Q&#x26;createUser=true&#x26;hubspotutk=169d02e0ddc1d02ed3202bcac0869f20</a></td></tr></tbody></table>

Install the OSS version of Gravitee locally with Docker.

<table data-card-size="large" data-view="cards"><thead><tr><th></th><th data-hidden data-card-target data-type="content-ref"></th></tr></thead><tbody><tr><td>Local Install with Docker</td><td><a href="broken-reference">Broken link</a></td></tr></tbody></table>

## Deployment Options

### Cloud

Gravitee Cloud is a simple and secure method of running Gravitee API Management (APIM). With this full-SaaS solution, you can count on consistent availability and cutting-edge features. For more information about Gravitee Cloud, see [Cloud.](https://documentation.gravitee.io/gravitee-cloud)&#x20;

Here are the key benefits of Gravitee's Cloud solution:

* **Cloud Hosted Gateways** are automatically scaled and managed, reducing operational overhead.
* The **Hybrid Deployment Model** keeps sensitive data secure within your infrastructure.
* With **Multi-Tenancy Support**, isolated environments and organizations are managed independently.
* The **API Management Console** simplifies control through centralized API management.
* **Sync & Async API Support** unifies the governance of both REST and event-driven APIs.
* **Advanced Alerting & Monitoring** detects and responds to issues with real-time alerts.
* **Enterprise-Grade Access Management** integrates with robust security and identity tools.
* **Flexible Hosting Options** include cloud, self-hosted, and hybrid deployments.

### Hybrid

A typical hybrid deployment consists of a Gravitee-hosted cloud installation and a self-hosted Gravitee Gateway. For more information, see [hybrid-installation-and-configuration-guides](../hybrid-installation-and-configuration-guides/ "mention"). Here are the key benefits of a hybrid deployment:

* **SaaS Control Plane & Self-Hosted Data Plane** centralize management while you control API traffic.
* **Bridge Gateway Architecture** to secure communication without exposing internal databases.&#x20;
* **Cloud Gate & Cloud Tokens** encrypts and authenticates interactions between components.
* **Data Residency & Compliance** keeps sensitive data within your infrastructure.&#x20;
* **Reduced Latency** by processing API requests closer to your services.&#x20;
* **API traffic within your infrastructure** for routing oversight, monitoring, and security enforcement.&#x20;
* **Scalability & Flexibility** by sizing Gateways to handle varying workloads.&#x20;
* **Customization & Integration** to interface with existing systems and meet specialized requirements.&#x20;
* **Secure Communication** uses TLS encryption for component interactions to protect data in transit.&#x20;
* **Centralized Analytics & Monitoring** aggregates analytics and logs in the cloud for a unified view.

### Self-hosted

In a self-hosted deployment, both the Control Plane and Data Plane are installed and maintained by you. For more information about self-hosted installations, see [self-hosted-installation-guides](../self-hosted-installation-guides/ "mention").

* **Flexible Deployment Options** let you to choose the best fit for your infrastructure.
* **Full Control Over Infrastructure** guarantees compliance with internal policies and regulations.&#x20;
* **Customizable Architecture** to interface with existing systems and meet specific requirements.
* **Enhanced Security** by keeping all data and traffic within your own network.&#x20;
* **Horizontal & Vertical Scalability** to accommodate increasing API traffic and user demands.
* **Multi-Tenancy Support** isolates organizations and environments to manage resources efficiently.&#x20;
* **Plugin Extensibility** to augment functionality through custom policies and connectors.&#x20;
* **Monitoring & Analytics** integrate with 3rd-party tools to capture usage and performance metrics.
* **Enterprise Support Options** provide access to expert assistance and service level agreements.&#x20;
* **Open Source and Enterprise Editions**. Available in both open-source and enterprise versions, which allows you to choose based on your feature requirements and budget.

## Community Edition versus Enterprise Edition

{% hint style="info" %}
For a detailed description of Gravitee Enterprise Edition, see [apim-enterprise-edition.md](../introduction/apim-enterprise-edition.md "mention").
{% endhint %}

The Gravitee distribution is available as both Open-Source (OSS) and Enterprise Edition (EE). Here is a table that shows the high-level differences between OSS and EE:

<table><thead><tr><th width="214">Feature</th><th>Description</th><th align="center">Community Edition</th><th align="center">Enterprise Edition</th></tr></thead><tbody><tr><td><strong>Audit Trail</strong></td><td>Audit the consumption and activity of your Gravitee APIs per event and type to monitor the behavior of your APIs and platform</td><td align="center">No</td><td align="center">Yes</td></tr><tr><td><strong>Bridge Gateway</strong></td><td>Deploy a Bridge Gateway, which is a proxy for a repository, to avoid opening a connection between a database and something outside its network. The sync occurs over HTTP instead of the database protocol.</td><td align="center">No</td><td align="center">Yes</td></tr><tr><td><strong>Custom roles</strong></td><td>Create custom user roles to fit your needs. A role is a functional group of permissions and can be defined at the organization, environment, API, and/or application level.</td><td align="center">No</td><td align="center">Yes</td></tr><tr><td><strong>DCR</strong></td><td>The dynamic client registration (DCR) protocol allows OAuth client applications to register with an OAuth server through the OpenID Connect (OIDC) client registration endpoint</td><td align="center">No</td><td align="center">Yes</td></tr><tr><td><strong>Debug mode</strong></td><td>Easily test and debug your policy execution and enforcement</td><td align="center">No</td><td align="center">Yes</td></tr><tr><td><strong>Enterprise OpenID Connect SSO</strong></td><td>Use OpenId Connect SSO with your API Management platform</td><td align="center">No</td><td align="center">Yes</td></tr><tr><td><strong>Sharding tags</strong></td><td>Specify which "shard" of the Gateway an API should be deployed to. By tagging Gateways with specific keywords, you can select a tag in the API's proxy settings to control where the API will be deployed.</td><td align="center">No</td><td align="center">Yes</td></tr></tbody></table>
