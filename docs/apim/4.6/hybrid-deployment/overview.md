---
description: An overview about overview.
---

# Overview

Hybrid installations use a mix of self-hosted and cloud components to provide flexibility when defining your architecture and deployment. A Gravitee hybrid installation consists of a SaaS control plane and a self-hosted data plane.

In this deployment, a bridge gateway acts as the control plane and the Gravitee Gateway acts as the data plane. The Bridge exposes HTTP services that bridge HTTP calls to the underlying repositories, e.g., MongoDB and JDBC. The Gravitee Gateway is a standard API Management (APIM) Gateway. You must replace the default repository plugin with the bridge repository plugin.

## Hybrid gateway components

{% tabs %}
{% tab title="SaaS control plane components" %}
<table><thead><tr><th width="225.37383177570098" align="center">Component</th><th>Description</th></tr></thead><tbody><tr><td align="center">APIM Console<br>(for API producers)</td><td>A web UI that provides easy access to key APIM Management API services. API publishers can use it to publish APIs. Administrators can configure global platform settings and specific portal settings.</td></tr><tr><td align="center">Management API</td><td>A RESTful API that exposes services to manage and configure the APIM Console and APIM Developer Portal.<br>All exposed services are restricted by authentication and authorization rules.</td></tr><tr><td align="center">Developer Portal<br>(for API consumers)</td><td>A web UI that provides easy access to key APIM API services. API consumers can manage their applications and discover, try out, and subscribe to published APIs.</td></tr><tr><td align="center"><p>[Optional]</p><p>APIM SaaS API Gateways</p></td><td>The APIM Gateway is the core component of the APIM platform. It behaves like a reverse proxy and has the ability to apply <a href="broken-reference/">policies</a> (rules or logic) to both the request and response phases of an API transaction to transform, secure, and monitor traffic.</td></tr><tr><td align="center">Bridge API gateway</td><td>Exposes HTTP services that bridge HTTP calls to the underlying repository, which can be any of Gravitee's supported repositories.</td></tr><tr><td align="center">Config Database</td><td>Contains all the APIM platform management data, such as API definitions, users, applications, and plans.</td></tr><tr><td align="center">S3 Bucket + Analytics Database</td><td>Contains analytics and logs data.</td></tr><tr><td align="center">Gravitee Cloud</td><td>A centralized, multi-environment/organization tool for managing all your Gravitee API Management and Access Management installations in a single place.</td></tr><tr><td align="center">[Optional]<br>API Designer</td><td>Drag-and-Drop graphical API designer to design your APIs (Swagger/OAS) and deploy mocked APIs for quick testing.</td></tr><tr><td align="center">[Optional]<br>Alert Engine</td><td>Provides efficient and flexible APIM/AM platform monitoring, including advanced alerting and notifications sent through preferred channels, e.g., email, Slack, via Webhooks. AE does not require any external components or a database. Events trigger it to send notifications per pre-configured conditions.</td></tr></tbody></table>
{% endtab %}

{% tab title="Self-hosted data plane components" %}
<table><thead><tr><th width="172.18918918918916" align="center">Component</th><th>Description</th></tr></thead><tbody><tr><td align="center">APIM Gateway</td><td>The APIM Gateway is the core component of the APIM platform. It behaves like a reverse proxy and has the ability to apply <a href="broken-reference/">policies</a> (rules or logic) to both the request and response phases of an API transaction to transform, secure, and monitor traffic.</td></tr><tr><td align="center">Logstash</td><td>Collects and sends local Gateway logs and metrics to the Gravitee APIM SaaS control plane.</td></tr><tr><td align="center">Redis</td><td>The database used locally for rate limit synchronized counters (RateLimit, Quota, Spike Arrest) and, optionally, as an external cache for the Cache policy.</td></tr></tbody></table>
{% endtab %}
{% endtabs %}

## Gateway and Bridge compatibility versions

The Bridge and APIM Gateway versions used for your hybrid deployment must be compatible per the tables below.

The following table lists the Gateway versions supported by each Bridge version.

| Bridge version | Supported Gateway versions |
| -------------- | -------------------------- |
| 4.3.x          | 4.3.x                      |
| 4.4.x          | 4.3.x to 4.4.x             |
| 4.5.x          | 4.3.x to 4.5.x             |
| 4.6.x          | 4.3.x to 4.6.x             |

The following table lists the Bridge versions supported by each Gateway version.

| Gateway version | Supported Bridge versions |
| --------------- | ------------------------- |
| 4.3.x           | 4.3.x to 4.6.x            |
| 4.4.x           | 4.4.x to 4.6.x            |
| 4.5.x           | 4.5.x to 4.6.x            |
| 4.6.x           | 4.6.x                     |

## Architecture

![Hybrid deployment architecture](<../.gitbook/assets/file.excalidraw (4) (1).svg>)

<figure><img src="../.gitbook/assets/image (135).png" alt="Diagram showing the hybrid architecture"><figcaption><p>Hybrid architecture connections</p></figcaption></figure>
