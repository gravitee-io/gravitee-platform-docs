---
description: This page provides high-level overview of the Gravitee ecosystem
---

# Gravitee Core Concepts

The API lifecycle includes API design, development, testing, deployment, troubleshooting, monitoring, and security. The challenges imposed by novel architectures and use cases have underscored API complexity and driven the development of comprehensive API management solutions, of which Gravitee is best-in-class.&#x20;

## Overview <a href="#overview-2" id="overview-2"></a>

Gravitee offers an API lifecycle toolset that extends beyond conventional API strategy and implementation. One of Gravitee’s core differentiators is that it's an event-native API solution that provides centralized support for both asynchronous and synchronous APIs. Built on event-driven architecture and implemented with reactive programming, Gravitee also supports the traditional request/response model and can even mediate between sync and async application layer protocols.&#x20;

## Key concepts <a href="#key-concepts-3" id="key-concepts-3"></a>

Key Gravitee concepts and terminology are introduced below as a foundation for more detailed product documentation.

### Gravitee global architecture <a href="#gravitee-global-architecture-4" id="gravitee-global-architecture-4"></a>

The architecture diagrams below offer a high-level conceptualization of the Gravitee ecosystem. The first diagram shows the interactions between and within Gravitee API Management (APIM) and Gravitee Access Management (AM). The second diagram illustrates the function of the Alert Engine (AE).&#x20;

<figure><img src="https://europe1.discourse-cdn.com/business20/uploads/graviteeforum/optimized/2X/b/b014429c2135257d51371e103e78eda7e306277d_2_486x500.png" alt=""><figcaption><p>APIM and AM architecture overview</p></figcaption></figure>

<figure><img src="../.gitbook/assets/ae_architecture.png" alt=""><figcaption><p>AE architecture overview</p></figcaption></figure>

Key takeaways:

* API publishers make requests to the Management API either programmatically or from the Management Console.&#x20;
* The Management API focuses on creating and deploying APIs to the Gateway, which determines how requests are proxied from end users to backend APIs, and exposing backend APIs in a developer portal for access by API consumers.
* A single Gravitee APIM instance is composed of several core Gravitee components.
* An AM instance is deployed separately from APIM. AM and APIM can be linked together or used as standalone products.

### Gravitee Cloud architecture

Each APIM and AM instance is attached to a Gravitee Cloud environment. Gravitee Cloud observes a hierarchy of three entity types:&#x20;

* Account: Top level. Typically a company, not an individual user.
* Organization: Second level. Typically a logical part of the company in a particular context, such as a region or business unit.
* Environment: Lowest level. Typically an environment in an IT infrastructure, such as development or production.

<figure><img src="https://europe1.discourse-cdn.com/business20/uploads/graviteeforum/optimized/2X/7/7bf3116daf4855840784ef9a860641ddf335f924_2_690x230.png" alt=""><figcaption><p>Sample Gravitee Cloud hierarchy</p></figcaption></figure>

### API Gateway <a href="#api-gateway-policies-and-plugins-5" id="api-gateway-policies-and-plugins-5"></a>

API Management encompasses API design, API security and access management, API reliability, API delivery, and API productization. At the core of APIM, the API Gateway is a reverse proxy that sits in front of your APIs. It routes requests to the appropriate backend services while performing various tasks such as rate limiting, authentication, and request or response transformations.

### API policies

The default Gravitee distribution includes policies to control how APIs are consumed. Policies are rules or logic executed by the API Gateway during an API call to enforce security, reliability, proper data transfer, and/or API monetization. &#x20;

Common API policies executed at the Gateway level:

{% tabs %}
{% tab title="Traffic shaping" %}
Policies that strip, shape, or otherwise alter network traffic to make API consumption and data movement more secure, reliable, performant, or efficient.

**Example:** Strip sensitive and nonessential information as data is brokered and sent to the client application to protect confidential data and streamline the message.
{% endtab %}

{% tab title="Authentication/authorization" %}
Policies that enforce certain authentication or authorization methods to ensure that an API consumer can request information from your backend.

**Example:** An API key policy limits API consumption to a set of client applications that pass a specific, unique API key with each request.
{% endtab %}

{% tab title="Rate limit" %}
Policies that limit and/or throttle the number of requests over a set time period.

**Example:** Limit an API to a maximum of 100 calls/min/consumer.
{% endtab %}

{% tab title="Dynamic routing" %}
Policies that dispatch inbound calls to different targets/endpoints or rewrite URIs.

**Example:** Redirect requests from `http://gateway/apis/store/12/info` to `http://backend_store12/info`.
{% endtab %}
{% endtabs %}

### API plugins

Gravitee plugins are modules or components that add or extend functionality by plugging into the Gravitee ecosystem. A policy is a type of plugin, i.e., a feature or function that is enabled through plugin functionality.&#x20;

{% hint style="info" %}
Browse the current collection of [Gravitee plugins](https://www.gravitee.io/plugins).&#x20;

Refer to Custom Plugins for the instructions to build a plugin.
{% endhint %}

### API Developer Portals & API Productization <a href="#api-developer-portals-api-productization-6" id="api-developer-portals-api-productization-6"></a>

A critical component of API management is the ability to expose APIs to various consumers. Different types of consumers are outlined in the following table:

| Consumer                       | Use case                                                                                                                          |
| ------------------------------ | --------------------------------------------------------------------------------------------------------------------------------- |
| Internal Developer             | APIs are used as internal tools to build products and services or connect systems, data sources, etc.                             |
| External Developer as Customer | APIs are exposed to developers at other companies for use in external products. Avoids duplication of existing API functionality. |
| Partner                        | APIs are exposed to partners when technical partnerships require integrations between certain products and/or feature sets.       |

A developer portal is a centralized catalog where internal and/or external API consumers can discover and subscribe to APIs that are developed, managed, and deployed by API publishers. Developer portals avoid unnecessary duplication of API functionality by ensuring that existing APIs are advertised and securely accessible.

API documentation includes specifications and tutorials that convey the purpose, structure, and capabilities of an API. Including high-quality, comprehensive, and accurate API documentation in the developer portal mitigates implementation challenges and increases API consumption.

An incentive to use developer portals is API monetization. This transforms APIs into self-serve, revenue-generating products with plans to govern how consumers pay for API access and usage, e.g., charging a set amount per message.

### API Access Management <a href="#api-access-management-7" id="api-access-management-7"></a>

As an API-security-forward organization, Gravitee implements API access management as a part of its larger API security and API management strategies.

API access management applies typical access management practices at the API level. For example, API access management could be used to implement step-up authentication, which adds extra layers of authentication to certain APIs or application features that may contain or transport sensitive data, e.g., in addition to MFA at login, calling an API from within an application uses biometrics.

API-level access management enables fine-tuned access control for applications containing sensitive data. Applications and/or APIs can be secured via consumer verification while the customer experience can be optimized by only adding the friction of access control where necessary.

### API Design-First <a href="#api-design-first-8" id="api-design-first-8"></a>

Gravitee's API management strategy includes API design, during which intentional architectural choices that define API client and backend interactions are determined.

Gravitee also implements API design-first methodology, where the API design or data model is developed before the API specification is generated. This approach promotes collaboration with less technical, business stakeholders to build APIs that align with business value.

### Gravitee API Definitions <a href="#gravitee-api-definitions-9" id="gravitee-api-definitions-9"></a>

A [Gravitee API definition](https://www.gravitee.io/blog/gravitee-api-definitions) is the API specification for a Gravitee Gateway_._ It is the JSON representation of the information the Gravitee Gateway requires to manage (proxy, apply policies to, create plans for, etc.) your APIs and their traffic.

The latest API definition is v4. The v4 definition supports advanced protocol mediation (e.g., fronting Kafka with a Webhook, WebSocket, or HTTP API) and can apply Gravitee policies (e.g., authentication and traffic shaping) to asynchronous API traffic at the message level. This is achieved by decoupling the Gateway entrypoints and endpoints:

* Gateway entrypoint: how the consumer “calls” or “subscribes” to the gateway. This essentially defines how a consumer will end up consuming data from a producer/provider
* Gateway endpoint: the data source from/to which the gateway will fetch/post data for/from the consumer that calls or subscribes to the gateway

So, for example, if you wanted to make it possible for an API consumer to consume events from a Kafka topic over a WebSocket connection, you would choose a “Websocket” entrypoint and a “Kafka” endpoint when creating your API in Gravitee. If you wanted to make it possible for an API consumer to POST data onto a Kafka topic via an HTTP API, you would use the Gravitee HTTP POST entrypoint and Kafka endpoint.

### Gravitee API Deployment Options <a href="#gravitee-api-deployment-options-10" id="gravitee-api-deployment-options-10"></a>

When it comes to Gravitee, there are two major categories of deployment: the APIs themselves and the Gravitee infrastructure, which includes the API gateway and management console among other components. While each product has detailed documentation on the deployment and installation of its respective infrastructure, we want to provide a quick overview of the different ways you can deploy APIs with Gravitee.

For Gravitee to be able to support [infrastructure as code (IaC)](https://www.redhat.com/en/topics/automation/what-is-infrastructure-as-code-iac) use cases, deployment needs to be able to be handled “as code,” and APIs need to be able to be pushed to/deployed to the API Gateway, tested, and then promoted across environments (test, dev, prod, etc.) without ever having to step a digital foot into a UI.

Many of our enterprise customers are already implementing an IaC practice using Gravitee. Some enterprise customers start off this way (i.e. customers who are already mature when it comes to GitOps, Kubernetes, etc.), but at least ⅓-½ of our enterprise customers gradually work their way into an IaC-compatible approach. We describe this process through the lens of API “deployment maturity.”

> **Note**: the term “maturity” here is not morally valenced or judgemental. We simply use the term to describe the sequential process that we see _most_ of our enterprise customers move through. There are many reasons for and benefits associated with each of the deployment styles mentioned below.

Traditionally, Gravitee customers progress through three levels of API “deployment maturity”:

#### **Gravitee Console**

The default Gravitee distribution includes an intuitive self-serve UI that an estimated ⅓-½ of our enterprise customers use for API development.

#### **Gravitee Management API**

Every action in the Gravitee Console is tied to a REST API that makes up the Gravitee management API. The management API exposes a complete set of endpoints and is [documented using the OpenAPI spec](https://docs.gravitee.io/apim/3.x/apim\_installguide\_rest\_apis\_documentation.html#apim\_console\_api\_reference). As a result, everything you can do in the UI can be done via REST API calls for developers wanting to script some part of APIM administration. Typically, as enterprise customers start to move into a GitOps world and moving things across higher environments, they use things like GitLab, Jenkins, Bitbucket, GitHub Actions, etc. to manage everything in a data serialization format like JSON or YAML.

#### **Kubernetes-native using the Gravitee Kubernetes Operator**

This approach moves beyond relying on the console/UI and the underlying management API. If you deploy APIs in a Kubernetes cluster, you can describe your API as an API extension of Kubernetes using CRDs (custom resource definitions). Essentially, this means that when you deploy something natively to your K8s cluster, there’s an operator there that can deploy that API to the Gravitee gateway without relying on a proprietary UI or REST API. This is powered by the Kubernetes API and the Gravitee Kubernetes Operator. This is the preferred method of deployment if your organization is set on using Kubernetes.

{% hint style="info" %}
**Kubernetes source of truth**

When you deploy the Kubernetes YAML file and everything deployed to the Gravitee Gateway and is up and running, you can still see the API and API definition in the Gravitee console and complete actions like deploying that API to the developer portal. However, as an administrator, there are some components of the API that you cannot change, as the source of truth is the Kubernetes YAML file. While this may seem like a restriction, this is a feature, not a bug. When implementing IaC, a key principle is to never change something in the “live form,” and instead change it in the code and observe the changes as they manifest in the front end.
{% endhint %}
