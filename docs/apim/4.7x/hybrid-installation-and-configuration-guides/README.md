# Hybrid Installation & Configuration Guides

## Overview

Hybrid installations use a mix of self-hosted and cloud components to provide flexibility when defining your architecture and deployment. In a Gravitee hybrid installation, the Gravitee platform is split into two deployments that can be hosted independently but must communicate over a network.

A typical Gravitee hybrid installation consists of a SaaS Control Plane and a self-hosted Data Plane. The Control Plane is a Cloud installation that is hosted by Gravitee. Gravitee currently supports both the Classic Cloud and Next-Gen Cloud. The Data Plane is a self-hosted installation that consists of the Gravitee Gateway, Redis, and, for Gravitee Classic Cloud, a log management solution.

If you are using Gravitee Cloud, you can enable multi-tenancy. Gravitee multi-tenancy describes a configuration in which features and data are isolated between tenants. This allows you to register multiple APIM environments and installations, manage environment hierarchies, and promote APIs across higher and lower environments.

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
{% tab title="SaaS control plane components" %}
<table><thead><tr><th width="225.37383177570098" align="center">Component</th><th>Description</th></tr></thead><tbody><tr><td align="center">APIM Console<br>(for API producers)</td><td>A web UI that provides easy access to key APIM Management API services. API publishers can use it to publish APIs. Administrators can configure global platform settings and specific portal settings.</td></tr><tr><td align="center">Management API</td><td>A RESTful API that exposes services to manage and configure the APIM Console and APIM Developer Portal.<br>All exposed services are restricted by authentication and authorization rules.</td></tr><tr><td align="center">Developer Portal<br>(for API consumers)</td><td>A web UI that provides easy access to key APIM API services. API consumers can manage their applications and discover, try out, and subscribe to published APIs.</td></tr><tr><td align="center"><p>[Optional]</p><p>APIM SaaS API Gateways</p></td><td>The APIM Gateway is the core component of the APIM platform. It behaves like a reverse proxy and has the ability to apply <a href="../../4.6/hybrid-deployment/broken-reference/">policies</a> (rules or logic) to both the request and response phases of an API transaction to transform, secure, and monitor traffic.</td></tr><tr><td align="center">Bridge API gateway</td><td>Exposes HTTP services that bridge HTTP calls to the underlying repository, which can be any of Gravitee's supported repositories.</td></tr><tr><td align="center">Config Database</td><td>Contains all the APIM platform management data, such as API definitions, users, applications, and plans.</td></tr><tr><td align="center">S3 Bucket + Analytics Database</td><td>Contains analytics and logs data.</td></tr><tr><td align="center">Gravitee Cloud</td><td>A centralized, multi-environment/organization tool for managing all your Gravitee API Management and Access Management installations in a single place.</td></tr><tr><td align="center">[Optional]<br>API Designer</td><td>Drag-and-Drop graphical API designer to design your APIs (Swagger/OAS) and deploy mocked APIs for quick testing.</td></tr><tr><td align="center">[Optional]<br>Alert Engine</td><td>Provides efficient and flexible APIM/AM platform monitoring, including advanced alerting and notifications sent through preferred channels, e.g., email, Slack, via Webhooks. AE does not require any external components or a database. Events trigger it to send notifications per pre-configured conditions.</td></tr><tr><td align="center">[Optional]<br>Access Management</td><td>Offers a centralized authentication and authorization service to deliver secure access to your applications and APIs from any device.</td></tr></tbody></table>
{% endtab %}

{% tab title="Self-hosted data plane components" %}
<table><thead><tr><th width="172.18918918918916" align="center">Component</th><th>Description</th></tr></thead><tbody><tr><td align="center">APIM Gateway</td><td>The APIM Gateway is the core component of the APIM platform. It behaves like a reverse proxy and has the ability to apply <a href="../../4.6/hybrid-deployment/broken-reference/">policies</a> (rules or logic) to both the request and response phases of an API transaction to transform, secure, and monitor traffic.</td></tr><tr><td align="center">Logstash</td><td>Collects and sends local Gateway logs and metrics to the Gravitee APIM SaaS control plane.</td></tr><tr><td align="center">Redis</td><td>The database used locally for rate limit synchronized counters (RateLimit, Quota, Spike Arrest) and, optionally, as an external cache for the Cache policy.</td></tr></tbody></table>
{% endtab %}
{% endtabs %}

## Architecture

Hybrid architecture refers to a scheme where certain Gravitee API Management components are Gravitee-managed SaaS components while others remain self-hosted by the user on-prem and/or in a private cloud. Gravitee Cloud and API Designer are optional Gravitee-managed components that can be connected to a hybrid API Management installation.

The following diagrams illustrate the component management, design, and self-hosted-to-SaaS connections of a hybrid architecture.

### Hybrid component management

<img src="../.gitbook/assets/file.excalidraw (14).svg" alt="" class="gitbook-drawing">

### Hybrid architecture diagram

<img src="../.gitbook/assets/file.excalidraw (18).svg" alt="" class="gitbook-drawing">

### Self-hosted-to-SaaS connections

<img src="../.gitbook/assets/file.excalidraw (15).svg" alt="Hybrid: SaaS to self-hosted connections" class="gitbook-drawing">

