---
description: Configuration guide for hybrid installation & configuration guides.
---

# Hybrid Installation & Configuration Guides

## Deployment Methods

### Next-Gen Cloud

* [docker-compose.md](next-gen-cloud/docker/docker-compose.md "mention")
* [docker-cli.md](next-gen-cloud/docker/docker-cli.md "mention")

#### Kubernetes

* [vanilla-kubernetes](next-gen-cloud/kubernetes/vanilla-kubernetes/ "mention")
* [AWS EKS](next-gen-cloud/kubernetes/aws-eks.md)
* [azure-aks.md](next-gen-cloud/kubernetes/azure-aks.md "mention")
* [OpenShift](next-gen-cloud/kubernetes/openshift.md)
* GCP GKE

#### RPM

* [rpm.md](next-gen-cloud/rpm.md "mention")

#### .ZIP

* [.zip.md](next-gen-cloud/.zip.md "mention")

### Classic cloud

#### Docker

* [docker-compose.md](classic-cloud/docker/docker-compose.md "mention")
* Docker CLI

#### Kubernetes

* Vanilla Kubernetes
* AWS EKS
* Azure AKS
* [gcp-gke.md](classic-cloud/kubernetes/gcp-gke.md "mention")
* OpenShift

#### RPM

* RPM

#### .ZIP

* [.zip.md](classic-cloud/.zip.md "mention")

## Overview

A hybrid Gateway architecture uses a mix of self-hosted and cloud components. The Gravitee platform is split into two deployments that can be hosted independently, but must communicate over a network. The Control Plane provides centralized management and monitoring, while the Data Plane processes API traffic locally within your infrastructure.

In a typical Gravitee hybrid installation, the Control Plane is hosted by Gravitee Cloud while the Data Plane is self-hosted. Gravitee supports both Gravitee Classic Cloud and Gravitee Next-Gen Cloud, which are compared in [#classic-cloud-vs-next-gen-cloud](./#classic-cloud-vs-next-gen-cloud "mention"). The Data Plane hosted by the customer consists of the Gravitee Gateway, Redis, and, for Gravitee Classic Cloud, a log management solution.

{% hint style="info" %}
Self-hosted software is installed and maintained by the customer and can run in any environment the customer controls, whether on-prem, in a private cloud, or even in a public cloud such as AWS, Azure, or GCP.
{% endhint %}

### Features and benefits

A hybrid installation combines the security and control of self-hosted deployment with the operational convenience of cloud-based management. This provides the following benefits:

* **Data residency and compliance.** You can ensure that data remains in the location where the resource owner resides. This facilitates compliance with data residency regulations.
* **Reduced latency.** A Gateway hosted within your own infrastructure processes API requests closer to your services. This minimizes latency and enhances performance.
* **Full control over traffic.** You can confine API traffic to your own infrastructure to control routing and monitoring. This also lets you enforce security policies unrelated to the policies executed on the Gateway runtime.
* **Scalability and flexibility.** You have full control over your Gateway's scaling.
* **Customization and integration**: You can integrate with your existing infrastructure. You can also customize your deployment to meet specific security, monitoring, or logging requirements.
* **Security.** You can confine sensitive API traffic to your infrastructure to reduce potential exposure to threats and vulnerabilities. You can also directly enforce your organization's security measures at the Data Plane level.

### Multi-tenancy

If you are using Gravitee Cloud, you can enable multi-tenancy. Gravitee multi-tenancy describes a configuration in which features and data are isolated between tenants. This lets you register multiple APIM environments and installations, manage environment hierarchies, and promote APIs across higher and lower environments.

## Classic Cloud vs Next-Gen Cloud

{% hint style="warning" %}
Classic Cloud will be deprecated once Next-Gen Cloud reaches full parity and a transition plan is established.
{% endhint %}

As the name implies, Next-Gen Cloud is the next generation of Gravitee Classic Cloud. Classic Cloud is currently more robust than Next-Gen Cloud, although Next-Gen Cloud will eventually reach full feature parity.

The following table indicates which Gravitee products are currently supported by each version of Gravitee Cloud.

<table><thead><tr><th>Feature</th><th data-type="checkbox">Classic Cloud</th><th data-type="checkbox">Next-Gen Cloud</th></tr></thead><tbody><tr><td>APIM</td><td>true</td><td>true</td></tr><tr><td>Access Management (AM)</td><td>true</td><td>false</td></tr><tr><td>Alert Engine (AE)</td><td>true</td><td>false</td></tr></tbody></table>

## Hybrid Gateway components

The tables below list the Data Plane and Control Plane components that are part of a Gravitee hybrid deployment.

{% tabs %}
{% tab title="SaaS Control Plane components" %}
<table><thead><tr><th width="225.37383177570098" align="center">Component</th><th>Description</th></tr></thead><tbody><tr><td align="center">APIM Console<br>(for API producers)</td><td>A web UI that provides easy access to key APIM Management API services. API publishers can use it to publish APIs. Administrators can configure global platform settings and specific portal settings.</td></tr><tr><td align="center">Management API</td><td>A RESTful API that exposes services to manage and configure the APIM Console and APIM Developer Portal.<br>All exposed services are restricted by authentication and authorization rules.</td></tr><tr><td align="center">Developer Portal<br>(for API consumers)</td><td>A web UI that provides easy access to key APIM API services. API consumers can manage their applications and discover, try out, and subscribe to published APIs.</td></tr><tr><td align="center"><p>[Optional]</p><p>APIM SaaS API Gateways</p></td><td>The APIM Gateway is the core component of the APIM platform. It behaves like a reverse proxy and has the ability to apply <a href="../../4.6/hybrid-deployment/broken-reference/">policies</a> (rules or logic) to both the request and response phases of an API transaction to transform, secure, and monitor traffic.</td></tr><tr><td align="center">Bridge API gateway</td><td>Exposes HTTP services that bridge HTTP calls to the underlying repository, which can be any of Gravitee's supported repositories.</td></tr><tr><td align="center">Config Database</td><td>Contains all the APIM platform management data, such as API definitions, users, applications, and plans.</td></tr><tr><td align="center">Analytics Database ( + S3 Bucket)</td><td>Contains analytics and logs data.<br>The S3 Bucket is only needed for Classic Cloud.</td></tr><tr><td align="center">Gravitee Cloud</td><td>A centralized, multi-organization, multi-environment tool for managing all your Gravitee API Management and Access Management installations in a single place.</td></tr><tr><td align="center">[Optional]<br>API Designer</td><td>Drag-and-drop, low-code, graphical API designer to design your APIs (Swagger/OAS) and deploy mocked &#x26; documented APIs for quick testing.</td></tr><tr><td align="center">[Optional]<br>Alert Engine</td><td>Provides efficient and flexible APIM/AM platform monitoring, including advanced alerting and notifications sent through preferred channels, e.g., email, Slack, via Webhooks. Alert Engine does not require any external components or a database. Events trigger it to send notifications per pre-configured conditions.</td></tr><tr><td align="center">[Optional]<br>Access Management</td><td>Offers a centralized authentication and authorization service to deliver secure access to your applications and APIs from any device.</td></tr></tbody></table>
{% endtab %}

{% tab title="Self-hosted Data Plane components" %}
<table><thead><tr><th width="172.18918918918916" align="center">Component</th><th>Description</th></tr></thead><tbody><tr><td align="center">APIM Gateway</td><td>The APIM Gateway is the core component of the APIM platform. It behaves like a reverse proxy and has the ability to apply <a href="../../4.6/hybrid-deployment/broken-reference/">policies</a> (rules or logic) to both the request and response phases of an API transaction to transform, secure, and monitor traffic.</td></tr><tr><td align="center">Redis</td><td><p>While the Gateway works without Redis, Redis is necessary for:</p><ul><li>Rate Limit, Quota, and Spike Arrest policies. Redis is used to store counters. In high availability deployments where traffic is split between Gateways, Redis enables rate-limiting synchronization via a shared execution context.</li><li>Caching. Subsequent calls can use previous responses that are cached.</li></ul></td></tr><tr><td align="center">Logstash</td><td>[Classic Cloud only] Collects and sends local Gateway logs and metrics to the Gravitee APIM SaaS control plane.</td></tr></tbody></table>

{% hint style="warning" %}
To avoid updates to the Gateway configuration and redeployment, Redis, Logstash, and Fluentd should be configured prior to starting the Gateway.
{% endhint %}

These components are configured differently depending on the deployment method. Each installation guide includes configurations for both the Gateway and Redis. Logstash and Fluentd configurations are also included for Classic Cloud installations.
{% endtab %}
{% endtabs %}

### Redis

In a typical Gravitee hybrid deployment, Redis is one of the self-hosted Data Plane components installed and maintained by the customer.

Redis provides caching and rate limiting capabilities that enable your Gateway to perform efficiently under load while maintaining state consistency across multiple Gateway instances. Redis serves as the high-performance, in-memory data store that enables your Gateway to track rate limiting counters, cache frequently accessed data, and maintain session information across multiple requests. This distributed cache infrastructure supports the horizontal scaling required for enterprise deployments, which ensures consistent performance.

## Architecture

Hybrid architecture refers to a scheme where certain Gravitee API Management components are Gravitee-managed SaaS components while others remain self-hosted by the user on-prem and/or in a private cloud. Gravitee Cloud and API Designer are optional Gravitee-managed components that can be connected to a hybrid API Management installation.

The following diagrams illustrate the component management, design, and self-hosted-to-SaaS connections of a hybrid architecture.

### Hybrid component management

<figure><img src="../.gitbook/assets/image (24).png" alt=""><figcaption></figcaption></figure>

### Hybrid architecture diagram

<figure><img src="../.gitbook/assets/image (25).png" alt=""><figcaption></figcaption></figure>

In a typical hybrid architecture, the customer manages the Data Plane and Gravitee manages the Control Plane.

The Data Plane consists of the API Gateways and other dependent infrastructure such as Redis, which is used for caching and rate-limiting. The Management Control Plane consists of API Management, and, optionally, Gravitee Alert Engine and Gravitee Access Management.

The API Gateways communicate with the Gravitee Cloud Control Plane using an outbound secure connection to the Gravitee CloudGate over HTTPS/443. The API Gateways synchronize API configurations, with the option to publish metrics and logs data.

### Self-hosted-to-SaaS connections

Other non-typical architectural options exist, such as connecting a fully self-hosted Control Plane to Gravitee Cloud.

This configuration enables multi-organization and multi-environment support in a single hierarchy. Users and policies can be configured in Gravitee Cloud, and these configurations proliferate to the child Control Planes.
