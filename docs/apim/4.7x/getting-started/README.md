# Getting Started

## How to get started

Set up Gravitee quickly and easily with Gravitee Cloud's 14-day **free** trial.&#x20;

## Other ways to get Gravitee

<table data-view="cards"><thead><tr><th></th><th data-hidden data-card-target data-type="content-ref"></th></tr></thead><tbody><tr><td>Install with Docker</td><td><a href="broken-reference">Broken link</a></td></tr><tr><td>Hybrid deployment with Docker</td><td></td></tr></tbody></table>

## Deployment Options

### Cloud

If you are not familiar with Gravitee, the easiest way to get Gravitee is with Gravitee Cloud.&#x20;

With this deployment, Gravitee hosts both your Control plane and your Data plane. For more information about Gravitee Cloud, see [Broken link](broken-reference "mention")

* \[Key features and benefits of Cloud to be entered here].

### Hybrid

With this deployment, Gravitee hosts the Control plane and you host the Data plane. For more information about Hybrid Deployment, see [Broken link](broken-reference "mention")

* \[Key features and benefits of a Hybrid Deployment to be entered here].

### Self-hosted

Control plane and Data Plane self-hosted / installed by you. For more information about self-hosted installations, see [Broken link](broken-reference "mention").

* \[Key features and benefits of a self-hosted deployment to be entered here].

## Community Edition versus Enterprise Edition

{% hint style="info" %}
For a detailed description of the Enterprise Edition of Gravitee, see [open-source-vs-enterprise-edition.md](../introduction/open-source-vs-enterprise-edition.md "mention").
{% endhint %}

Hybrid deployment and self-hosted deployment are available in both Open-Source (OSS) and Enterprise Edition (EE). Here is a table that shows the high-level differences between OSS and EE:

<table><thead><tr><th width="214" align="center">Feature</th><th align="center">Description</th><th align="center">Community Edition</th><th align="center">Enterprise Edition</th></tr></thead><tbody><tr><td align="center"><strong>Audit Trail</strong></td><td align="center">Audit the consumption and activity of your Gravitee APIs per event and type to monitor the behavior of your APIs and platform</td><td align="center">No</td><td align="center">Yes</td></tr><tr><td align="center"><strong>Bridge Gateway</strong></td><td align="center">Deploy a Bridge Gateway, which is a proxy for a repository, to avoid opening a connection between a database and something outside its network. The sync occurs over HTTP instead of the database protocol.</td><td align="center">No</td><td align="center">Yes</td></tr><tr><td align="center"><strong>Custom roles</strong></td><td align="center">Create custom user roles to fit your needs. A role is a functional group of permissions and can be defined at the organization, environment, API, and/or application level.</td><td align="center">No</td><td align="center">Yes</td></tr><tr><td align="center"><strong>DCR</strong></td><td align="center">The dynamic client registration (DCR) protocol allows OAuth client applications to register with an OAuth server through the OpenID Connect (OIDC) client registration endpoint</td><td align="center">No</td><td align="center">Yes</td></tr><tr><td align="center"><strong>Debug mode</strong></td><td align="center">Easily test and debug your policy execution and enforcement</td><td align="center">No</td><td align="center">Yes</td></tr><tr><td align="center"><strong>Enterprise OpenID Connect SSO</strong></td><td align="center">Use OpenId Connect SSO with your API Management platform</td><td align="center">No</td><td align="center">Yes</td></tr><tr><td align="center"><strong>Sharding tags</strong></td><td align="center">Specify which "shard" of the Gateway an API should be deployed to. By tagging Gateways with specific keywords, you can select a tag in the API's proxy settings to control where the API will be deployed.</td><td align="center">No</td><td align="center">Yes</td></tr></tbody></table>
