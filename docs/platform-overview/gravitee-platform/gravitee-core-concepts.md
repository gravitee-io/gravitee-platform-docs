---
description: This page provides high-level overview of the Gravitee ecosystem
---

# Core Concepts

## Overview

The API lifecycle includes API design, development, testing, deployment, troubleshooting, monitoring, and security. The ever increasing quantity and complexity of APIs has driven the development of comprehensive API management solutions, of which Gravitee is best-in-class.

Gravitee offers an API lifecycle toolset that extends beyond conventional API strategy and implementation. One of Gravitee’s core differentiators is that it's an event-native API solution, built on an event-driven architecture implemented with reactive programming. It fully supports both asynchronous, event-driven APIs and synchronous APIs, even mediating between synchronous and asynchronous protocols.

The following sections provide a high-level overview of Gravitee architecture, concepts, and features:

* [Global architecture](gravitee-core-concepts.md#gravitee-global-architecture-4)
* [Cloud architecture](gravitee-core-concepts.md#gravitee-cockpit-architecture)
* [API Gateway](gravitee-core-concepts.md#api-gateway-policies-and-plugins-5)
* [API policies](gravitee-core-concepts.md#api-policies)
* [API plugins](gravitee-core-concepts.md#api-plugins)
* [Developer Portal](gravitee-core-concepts.md#api-developer-portals-api-productization-6)
* [API access management](gravitee-core-concepts.md#api-access-management-7)
* [API design-first](gravitee-core-concepts.md#api-design-first-8)
* [API definitions](gravitee-core-concepts.md#gravitee-api-definitions-9)
* [API deployment options](gravitee-core-concepts.md#gravitee-api-deployment-options-10)

## Global architecture <a href="#gravitee-global-architecture-4" id="gravitee-global-architecture-4"></a>

The architecture diagrams below offer a high-level conceptualization of the Gravitee ecosystem. The first diagram shows the interactions between and within Gravitee API Management (APIM) and Gravitee Access Management (AM). The second diagram illustrates the function of the Alert Engine (AE).

<figure><img src="../.gitbook/assets/AM-APIM-Architecture.png" alt=""><figcaption><p>APIM and AM architecture overview</p></figcaption></figure>

<figure><img src="../.gitbook/assets/AE-Architecture.png" alt=""><figcaption><p>AE architecture overview</p></figcaption></figure>

* API publishers make requests to the Management API either programmatically or from the Management Console.
* The Management API focuses on creating and deploying APIs to the Gateway, which determines how requests are proxied from clients to backend APIs and how backend APIs are exposed in the Developer Portal for access by API consumers.
* A single Gravitee APIM instance is composed of several core Gravitee components.
* An AM instance is deployed separately from APIM. AM and APIM can be linked together or used as standalone products.

## Cloud architecture

Each APIM and AM instance can be attached to a Gravitee Cloud environment. Gravitee Cloud observes a hierarchy of three entity types:

{% hint style="info" %}
By default, Gravitee-managed deployments are connected to Gravitee Cloud.
{% endhint %}

* **Account:** Top level. Typically a company, not an individual user.
* **Organization:** Second level. Typically a logical part of the company in a particular context, such as a region or business unit.
* **Environment:** Lowest level. Typically an environment in an IT infrastructure, such as development or production.

<figure><img src="https://europe1.discourse-cdn.com/business20/uploads/graviteeforum/optimized/2X/7/7bf3116daf4855840784ef9a860641ddf335f924_2_690x230.png" alt=""><figcaption><p>Sample Gravitee Cloud hierarchy</p></figcaption></figure>

## API Gateway <a href="#api-gateway-policies-and-plugins-5" id="api-gateway-policies-and-plugins-5"></a>

API Management encompasses the design, security and access management, reliability, delivery, and productization of APIs. At the core of APIM, the API Gateway is a reverse proxy that sits in front of your backend APIs and event brokers. It routes requests to the appropriate backend services while performing various tasks such as rate limiting, authentication, and request or response transformations.

## API policies

The default Gravitee distribution includes policies to control how APIs are consumed. Policies are rules or logic executed by the API Gateway during an API call to enforce security, reliability, proper data transfer, and/or API monetization. The following are common API policies executed at the Gateway level:

{% tabs %}
{% tab title="Traffic shaping" %}
Policies that strip, shape, or otherwise alter network traffic to make API consumption and data movement more secure, reliable, performant, or efficient.

**Example:** Strip sensitive and nonessential information as data is brokered and sent to the client application to protect confidential data and streamline the message.
{% endtab %}

{% tab title="Auth" %}
Policies that enforce certain authentication or authorization methods to ensure that an API consumer can request information from your backend.

**Example:** An API key policy limits API consumption to a set of client applications that pass a specific, unique API key with each request.
{% endtab %}

{% tab title="Restrictions" %}
Policies that limit and/or throttle the number of requests over a set time period.

**Example:** Limit an API to a maximum of 100 calls/min/consumer.
{% endtab %}

{% tab title="Routing" %}
Policies that dispatch inbound calls to different targets/endpoints or rewrite URIs.

**Example:** Redirect requests from `http://gateway/apis/store/12/info` to `http://backend_store12/info`.
{% endtab %}

{% tab title="Performance" %}
Policies that cache responses from backend APIs to eliminate the need for subsequent calls.

**Example:** Use a cache policy to cache the response of a particular backend API for one hour or until the user manually bypasses the cache.
{% endtab %}
{% endtabs %}

## API plugins

Gravitee plugins are modules or components that add or extend functionality by plugging into the Gravitee ecosystem. A policy is a type of plugin, i.e., a feature or function that is enabled through plugin functionality.

{% hint style="info" %}
Browse the current collection of [Gravitee plugins](https://www.gravitee.io/plugins).

Refer to the [APIM Plugins](https://documentation.gravitee.io/apim/overview/plugins) guide for more information or to the [Custom Plugins guide](https://documentation.gravitee.io/apim/guides/developer-contributions/dev-guide-plugins) for the instructions to build a plugin.
{% endhint %}

## Developer Portal <a href="#api-developer-portals-api-productization-6" id="api-developer-portals-api-productization-6"></a>

A critical component of API management is the ability to expose APIs to various consumers. Different types of consumers are outlined in the following table:

| Consumer                       | Use case                                                                                                                          |
| ------------------------------ | --------------------------------------------------------------------------------------------------------------------------------- |
| Internal Developer             | APIs are used as internal tools to build products and services or connect systems, data sources, etc.                             |
| External Developer as Customer | APIs are exposed to developers at other companies for use in external products. Avoids duplication of existing API functionality. |
| Partner                        | APIs are exposed to partners when technical partnerships require integrations between certain products and/or feature sets.       |

A Developer Portal is a centralized catalog where internal and/or external API consumers can discover and subscribe to APIs that are developed, managed, and deployed by API publishers. Developer portals avoid unnecessary duplication of API functionality by ensuring that existing APIs are advertised and securely accessible.

API documentation includes specifications and tutorials that convey the purpose, structure, and capabilities of an API. Including high-quality, comprehensive, and accurate API documentation in the Developer Portal mitigates implementation challenges and increases API consumption.

An incentive to use Developer Portals is API monetization. This transforms APIs into self-serve, revenue-generating products with plans to govern how consumers pay for API access and usage, e.g., charging a set amount per message.

## API access management <a href="#api-access-management-7" id="api-access-management-7"></a>

As an API-security-forward organization, Gravitee implements API access management as a part of its larger API security and API management strategies.

API access management applies typical access management practices at the API level. For example, API access management could be used to implement step-up authentication, which adds extra layers of authentication to certain APIs or application features that may contain or transport sensitive data, e.g., in addition to MFA at login, calling an API from within an application uses biometrics.

API-level access management enables fine-tuned access control for applications containing sensitive data. Applications and/or APIs can be secured via consumer verification while the customer experience can be optimized by only adding the friction of access control where necessary.

## API design-first <a href="#api-design-first-8" id="api-design-first-8"></a>

Gravitee's API management strategy includes API design, during which intentional architectural choices that define API client and backend interactions are determined.

Gravitee also implements API design-first methodology, where the API design or data model is developed before the API specification is generated. This approach promotes collaboration with less technical, business stakeholders to build APIs that align with business value.

## API definitions <a href="#gravitee-api-definitions-9" id="gravitee-api-definitions-9"></a>

A [Gravitee API definition](https://www.gravitee.io/blog/gravitee-api-definitions) is the API specification for a Gravitee Gateway. It is the JSON representation of the information the Gravitee Gateway requires to manage (proxy, apply policies to, create plans for...) your APIs and their traffic.

The latest API definition supports advanced protocol mediation (e.g., fronting Kafka with a Webhook, WebSocket, or HTTP API) and can apply Gravitee policies to asynchronous API traffic at the message level.

Mediation and policy enforcement are achieved by decoupling the Gateway entrypoints and endpoints. The Gateway entrypoint dictates how the backend API is exposed by defining the protocol and configuration settings the API consumer uses to access the Gateway API. The Gateway endpoint defines the protocol and configuration settings the Gateway API uses to fetch data from, or post data to, the backend API.

<details>

<summary>Examples of entrypoint/endpoint selection</summary>

**Example 1:** To allow an API consumer to consume events from a Kafka topic over a WebSocket connection, choose the Websocket entrypoint and the Kafka endpoint when creating a v4 API definition.

**Example 2:** To allow an API consumer to POST data onto a Kafka topic via an HTTP API, use the Gravitee HTTP POST entrypoint and the Kafka endpoint.

</details>

## API deployment options <a href="#gravitee-api-deployment-options-10" id="gravitee-api-deployment-options-10"></a>

Gravitee supports two major categories of deployment: the APIs themselves and the Gravitee infrastructure, which includes the API Gateway and Management Console (among other components). To support Infrastructure as Code (IaC) use cases, Gravitee must support API deployment to the API Gateway, testing, and promotion across environments (test, dev, prod, etc.) "as code," i.e., without requiring the use of a UI.

Gravitee customers typically progress through three stages of API deployment:

<details>

<summary>1. Gravitee Console</summary>

The default Gravitee distribution includes an intuitive self-serve web UI that customers use for API development. The Console provides easy access to key APIM API services, allows API publishers to publish APIs, and enables administrators to configure both global platform settings and specific portal settings.

</details>

<details>

<summary>2. Gravitee Management API</summary>

Every interaction with the Gravitee Console corresponds to a REST API, the collection of which comprise the Gravitee Management API. The Management API exposes a complete set of endpoints to manage and configure the APIM Console and APIM Portal web UIs, where all exposed services are restricted by authentication and authorization rules.&#x20;

The Management API is documented using the OpenAPI spec, allowing developers to script APIM administration via calls to REST APIs. As enterprise customers progress with GitOps, they often adopt tools (GitLab, Jenkins, Bitbucket, GitHub Actions, etc.) to manage data in serialization formats like JSON or YAML.

</details>

<details>

<summary>3. <strong>Kubernetes-native using the Gravitee Kubernetes Operator</strong></summary>

This approach eliminates reliance on the Management Console and underlying Management API. An API deployed in a Kubernetes cluster can be described as an API extension of Kubernetes using CRDs (custom resource definitions). Using the Kubernetes API and the Gravitee Kubernetes Operator, an API can be deployed to the Gravitee Gateway without relying on a proprietary UI or REST API. This is the preferred method of deployment for organizations that intend to use K8s.

</details>

{% hint style="info" %}
**Kubernetes source of truth**

Once the Kubernetes YAML file has been deployed, it is the source of truth. The API and API definition remain visible in the Gravitee Console and the API can still be deployed to the Developer Portal, but, in adherence to IaC principles, there are API components that the administrator cannot change.
{% endhint %}
