# Introduction to Gravitee API Management (APIM)

An organization requires an API management solution to securely and reliably expose its APIs to external developers, internal developers, and partners. API management unlocks the potential of an organization’s data and services and facilitates the transformation to OpenAPI and OpenData. This leads to numerous benefits and advantages, including the company's ability to extend its digital platform offerings, open new communication channels, and attract new customers.

A growing customer base brings new challenges, e.g., how to:

* Reduce the time taken to enroll new partners
* Identify partners and manage their API consumption
* Measure consumption from the perspective of a consumer and/or producer&#x20;
* Share and discover existing APIs
* Manage the API lifecycle, versioning, documentation, etc.

Gravitee API Management (APIM) enables businesses to address these challenges seamlessly, across all APIs, using a centralized tool.

## Gravitee API Management components

Gravitee API Management is a flexible, lightweight, and performant event-native API management platform that enables organizations to manage, secure, and govern synchronous and asynchronous APIs. APIM is composed of four main components:

* APIM Gateway
* APIM Management API
* APIM Console
* APIM Developer Portal

### APIM Gateway

APIM Gateway is the core component of the APIM platform. You can think of it like a _**smart**_ proxy.

Unlike a traditional HTTP proxy, APIM Gateway has the capability to apply policies (i.e., rules) to both HTTP requests and responses according to your needs. With these policies, you can enhance request and response processing by adding transformations, security, and many other exciting features.

### APIM Management API

This RESTful API exposes services to manage and configure the APIM Console and APIM Portal web UIs. All exposed services are restricted by authentication and authorization rules. For more information, see the [API Reference](reference/management-api-reference/) section.

### APIM Console

This web UI gives easy access to some key APIM API services. API Publishers can use it to publish APIs. Administrators can also configure global platform settings and specific portal settings.

### APIM Developer Portal

This web UI gives easy access to some key APIM API services. API Consumers can use it to search for, view, try out and subscribe to a published API. They can also use it to manage their applications.

## Why Gravitee API Management?

Our goal in launching Gravitee APIM is to provide users with a highly flexible and scalable solution that seamlessly integrates with their infrastructure and expertly conforms to their business needs. We’ve designed and developed APIM to be fully extensible using its own internal plugin system: you can define your own policy, develop your own reporting system, and more.

Additionally, all APIM components (including APIM Gateway and APIM Management API) are incredibly lightweight. Gravitee's consciously aggressive approach to CPU and memory management enables our products to supply high availability through lightning-fast component start-up times. For a typical number of API deployments, it takes **less than 5 seconds** for the API Gateway to be accessible to consumers.

## Core APIM Concepts

### Gateway API

**Gateway API** is the root concept defined and used by APIM. Think of this as the starting point through which services are exposed to the gateway.

### API Publisher

In our platform, we define an **API** **publisher** as the role that declares and manages APIs.

### API Consumer

In our platform, we define an **API** **consumer** as the role that consumes APIs. Consumers get access to APIs by **subscribing** to them.

### Application

An **application** is an intermediate level between a consumer and an API. Through applications, consumers are grouped together and the application as a whole subscribes to the API.

## First steps

Ready to use Gravitee API Management? Let’s get started! Select from the options below to learn more about APIM, or head over to the install guides to get APIM up and running.

<table data-view="cards"><thead><tr><th></th><th></th><th></th><th data-hidden data-card-target data-type="content-ref"></th></tr></thead><tbody><tr><td></td><td>APIM Architecture</td><td></td><td><a href="overview/introduction-to-gravitee-api-management-apim/apim-architecture.md">apim-architecture.md</a></td></tr><tr><td></td><td>Plugins</td><td></td><td><a href="overview/introduction-to-gravitee-api-management-apim/plugins.md">plugins.md</a></td></tr><tr><td></td><td>Integrations</td><td></td><td><a href="overview/integrations/">integrations</a></td></tr><tr><td></td><td>Open Source vs Enterprise Edition</td><td></td><td><a href="overview/introduction-to-gravitee-api-management-apim/ee-vs-oss.md">ee-vs-oss.md</a></td></tr><tr><td></td><td>Install &#x26; Upgrade Guides</td><td></td><td><a href="getting-started/install-and-upgrade/install-guides/">install-guides</a></td></tr></tbody></table>
