---
description: Tutorial on Installing a Gravitee Gateway with a Hybrid Deployment.
---

# Installing a Gravitee Gateway with a Hybrid Deployment

## Introduction to Hybrid Deployments

Hybrid architecture is the deployment of a Gravitee Gateway using self-hosted and cloud deployments.

The Gravitee Gateway hybrid deployment uses hybrid components to provide flexibility when you define your architecture and deployment.

This page explains how to install a Self-Hosted Data-Plane in a Hybrid deployment, which consists of a SaaS Control-Plane and a Self-Hosted Data-Plane. The control plane signifies the Bridge and the data-plane signifies the Gateway.

The Gravitee Gateway needs the following two components:

* An HTTP _Bridge_ server that exposes extra HTTP services for bridging HTTP calls to the underlying repositories. For example, MongoDB and JDBC.
* A _standard_ API Management (APIM) Gateway. You must switch the default repository plugin to the bridge repository plugin.

### Before you begin

* Ensure that you understand the various components of a Hybrid deployment. For more information about the components of a Hybrid architecture, see [Components of Hybrid architecture](./#components-of-hybrid-architecture).
* Ensure that the Bridge and Gateway versions that you use for your Hybrid deployment are compatible. For more information about Gateway and Bridge compatibility versions, see [Gateway and Bridge compatibility versions](gateway-and-bridge-compatibility-versions.md).

<img src="../../../.gitbook/assets/file.excalidraw (4).svg" alt="Hybrid deployment architecture" class="gitbook-drawing">

<img src="../../../.gitbook/assets/file.excalidraw (15) (1).svg" alt="Hybrid architecture connections" class="gitbook-drawing">

## Components of Hybrid Architecture

The components of a Hybrid architecture are divided into two parts:

* [SaaS Control-Plane components](./#saas-components)
* [Self-hosted Data-Plan components](./#on-prem-private-cloud-components)

### SaaS Control-Plane components <a href="#saas-components" id="saas-components"></a>

<table><thead><tr><th width="225.37383177570098" align="center">Component</th><th>Description</th></tr></thead><tbody><tr><td align="center">APIM Console<br>(for API producers)</td><td>This web UI gives easy access to some key APIM Management API services. <a href="../../../#api-publisher">API publishers</a> can use it to publish APIs.<br>Administrators can also configure global platform settings and specific portal settings.</td></tr><tr><td align="center">APIM Management API</td><td>This RESTful API exposes services to manage and configure the APIM Console and APIM Developer Portal web UIs.<br>All exposed services are restricted by authentication and authorization rules. For more information, see the<a href="../../../using-the-product/using-the-gravitee-api-management-components/general-configuration-1/management-api-reference.md"> Management API Reference</a> section.</td></tr><tr><td align="center">APIM Developer Portal<br>(for API consumers)</td><td>This web UI gives easy access to some key APIM API services. It allows <a href="../../../#api-consumer">API Consumers</a> to <a href="../../../using-the-product/managing-your-apis-with-gravitee-api-management/api-exposure-plans-applications-and-subscriptions/#applications">manage their applications</a> and search for, view, try out, and subscribe to a published API.</td></tr><tr><td align="center"><p>[Optional]</p><p>APIM SaaS API Gateways</p></td><td>APIM Gateway is the core component of the APIM platform. You can think of it like a smart reverse proxy.<br>Unlike a traditional HTTP proxy, APIM Gateway has the capability to apply <a href="../../../using-the-product/managing-your-apis-with-gravitee-api-management/policy-studio/">policies</a> (i.e., rules or logic) to both the request and response phases of an API transaction. With these policies, you can transform, secure, monitor, etc., your APIs.</td></tr><tr><td align="center">Bridge Server</td><td>A <em>bridge</em> API Gateway exposes extra HTTP services for bridging HTTP calls to the underlying repository (which can be any of our supported repositories: MongoDB, JDBC, etc.)</td></tr><tr><td align="center">Config Database</td><td>All the API Management platform management data, such as API definitions, users, applications, and plans.</td></tr><tr><td align="center">S3 Bucket + Analytics Database</td><td>Analytics and logs data.</td></tr><tr><td align="center">Gravitee Cockpit</td><td>Gravitee Cockpit is a centralized, multi-environments / organizations tool for managing all your Gravitee API Management and Access Management installations in a single place.</td></tr><tr><td align="center">[Optional]<br>API Designer</td><td>Drag-and-Drop graphical (MindMap) API designer to quickly and intuitively design your APIs (Swagger / OAS) and deploy mocked APIs for quick testing.</td></tr><tr><td align="center">[Optional]<br>Alert Engine</td><td>Alert Engine (AE) provides APIM and AM users with efficient and flexible API platform monitoring, including advanced alerting configuration and notifications sent through their preferred channels, such as email, Slack and using Webhooks.<br>AE does not require any external components or a database as it does not store anything. It receives events and sends notifications under the conditions which have been pre-configured upstream with triggers.</td></tr></tbody></table>

### Self-Hosted Data-Plane components <a href="#on-prem-private-cloud-components" id="on-prem-private-cloud-components"></a>

<table><thead><tr><th width="172.18918918918916" align="center">Component</th><th>Description</th></tr></thead><tbody><tr><td align="center">APIM Gateway</td><td>APIM Gateway is the core component of the APIM platform. You can think of it like a smart reverse proxy.<br><br>Unlike a traditional HTTP proxy, APIM Gateway has the capability to apply <a href="../../../using-the-product/managing-your-apis-with-gravitee-api-management/policy-studio/">policies</a> (i.e., rules or logic) to both the request and response phases of an API transaction. With these policies, you can transform, secure, monitor, etc., your APIs.</td></tr><tr><td align="center">Logstash</td><td>Collect and send local Gateway logs and metrics to the Gravitee APIM SaaS Control Plane.</td></tr><tr><td align="center">Redis</td><td>The database used locally for rate limit synchronized counters (RateLimit, Quota, Spike Arrest) and, optionally, as an external cache for the Cache policy.</td></tr></tbody></table>

## Installation Options

You can install a Gravitee Gateway using the following Hybrid deployment methods:

<table data-card-size="large" data-view="cards"><thead><tr><th data-type="content-ref"></th><th></th></tr></thead><tbody><tr><td><a href="../../../getting-started/install-gravitee-api-management/installing-a-gravitee-gateway-with-a-hybrid-deployment/advanced-hybrid-deployment.md">advanced-hybrid-deployment.md</a></td><td>With this method, you install a Gravitee Gateway on your own infrastructure that connects to a control plane hosted in the Gravitee Cloud environment</td></tr><tr><td><a href="hybrid-deployment-on-kubernetes.md">hybrid-deployment-on-kubernetes.md</a></td><td>With this method, you install a Gravitee Gateway and cloud deployments using Kubernetes Helm charts to create your API Management platform.</td></tr></tbody></table>
