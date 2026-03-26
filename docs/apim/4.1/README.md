---
description: Tutorial on Introduction to Gravitee API Management (APIM).
---

# Introduction to Gravitee API Management (APIM)

An API management solution allows an organization to securely and reliably expose its APIs to partners and developers, both internal and external, and offers numerous benefits and advantages. By unlocking the potential of data and services while facilitating the transformation to OpenAPI, an API management solution empowers a company to extend its digital platform, forge new communication channels, and attract new customers.

A growing customer base brings new challenges, e.g., how to:

* Reduce the time taken to enroll new partners
* Identify partners and manage their API consumption
* Measure consumption from the perspective of a consumer and/or producer
* Share and discover existing APIs
* Manage the API lifecycle, versioning, documentation, etc.

Gravitee API Management (APIM) enables businesses to address these challenges seamlessly, across all of their APIs, using a centralized tool.

## Gravitee API Management

Gravitee API Management is a lightweight and performant event-native API management platform that accelerates and streamlines the governance and security of both synchronous and asynchronous APIs.

As a highly flexible and scalable solution, Gravitee APIM seamlessly integrates with a customer's infrastructure and expertly conforms to specific business needs. We’ve designed and developed APIM to be fully extensible using its own internal plugin system: customers can define their own policies, develop their own reporting systems, and more.

Gravitee's consciously aggressive approach to CPU and memory management enables our products to supply high availability through lightning-fast component start-up times. For a typical number of API deployments, it takes **less than 5 seconds** for the API Gateway to be accessible to consumers.

### APIM components

APIM is composed of four main components, all of which are incredibly lightweight:

**APIM Gateway:** The core component of the APIM platform, it is essentially a sophisticated proxy. Unlike a traditional HTTP proxy, APIM Gateway can apply policies (i.e., rules) to both HTTP requests and responses to enhance processing by adding transformations, security, and many other exciting features.

**APIM Management API:** A RESTful API that exposes services to manage and configure the APIM Console and APIM Portal web UIs. All exposed services are restricted by authentication and authorization rules. For more information, see the [API Reference](reference/management-api-reference.md) section.

**APIM Console:** A web UI providing easy access to key APIM API services. It allows API publishers to publish APIs and administrators to configure both global platform settings and specific portal settings.

**APIM Developer Portal:** A web UI providing easy access to key APIM API services. API consumers can use it to manage their applications and search for, view, try out, or subscribe to a published API.

### APIM core concepts

The following concepts are fundamental to APIM:

**Gateway API:** The root concept defined and used by APIM and through which services are exposed to the Gateway.

**API publisher:** The creator, designer, and/or manager of an API.

**API consumer:** The user or application accessing the API. Consumers are granted access to APIs via subscriptions.

**Application:** An intermediary between a consumer and an API. Through applications, consumers are grouped together and the application as a whole subscribes to the API.

### Ant notation

APIM frequently uses Ant notation for path matching:

* `?` matches one character
* `\*` matches zero or more characters
* `**` matches zero or more directories in a path

## First steps

Ready to use Gravitee API Management? Select from the options below to learn more about APIM and get it up and running.

<table data-view="cards"><thead><tr><th></th><th></th><th></th><th data-hidden data-card-target data-type="content-ref"></th></tr></thead><tbody><tr><td></td><td>APIM Architecture</td><td></td><td><a href="overview/apim-architecture.md">apim-architecture.md</a></td></tr><tr><td></td><td>Plugins</td><td></td><td><a href="overview/plugins.md">plugins.md</a></td></tr><tr><td></td><td>Integrations</td><td></td><td><a href="overview/integrations.md">integrations.md</a></td></tr><tr><td></td><td>Open Source vs Enterprise Edition</td><td></td><td><a href="overview/ee-vs-oss/">ee-vs-oss</a></td></tr><tr><td></td><td>Install &#x26; Upgrade Guides</td><td></td><td><a href="getting-started/install-guides/">install-guides</a></td></tr></tbody></table>
