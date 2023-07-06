# Introduction to Gravitee API Management (APIM)

An API management solution allows an organization to securely and reliably expose its APIs to partners and developers, both internal and external, and offers numerous benefits and advantages. By unlocking the potential of data and services while facilitating the transformation to OpenAPI, an API management solution empowers a company to extend its digital platform, forge new communication channels, and attract new customers.

A growing customer base brings new challenges, e.g., how to:

* Reduce the time taken to enroll new partners
* Identify partners and manage their API consumption
* Measure consumption from the perspective of a consumer and/or producer&#x20;
* Share and discover existing APIs
* Manage the API lifecycle, versioning, documentation, etc.

Gravitee API Management (APIM) enables businesses to address these challenges seamlessly, across all of its APIs, using a centralized tool.

## Gravitee API Management components

Gravitee API Management is a flexible, lightweight, and performant event-native API management platform that accelerates and streamlines the governance and security of both synchronous and asynchronous APIs. APIM is composed of four main components:

**APIM Gateway:** The core component of the APIM platform, it is essentially a sophisticated proxy. Unlike a traditional HTTP proxy, APIM Gateway can apply policies (i.e., rules) to both HTTP requests and responses to enhance processing by adding transformations, security, and many other exciting features.

**APIM Management API:** A RESTful API that exposes services to manage and configure the APIM Console and APIM Portal web UIs. All exposed services are restricted by authentication and authorization rules. For more information, see the [API Reference](reference/management-api-reference/) section.

**APIM Console:** A web UI providing easy access to key APIM API services. It allows API Publishers to publish APIs and administrators to configure both global platform settings and specific portal settings.

**APIM Developer Portal:** A web UI providing easy access to key APIM API services. API Consumers can use it to manage their applications and search for, view, try out, or subscribe to a published API.

## Why Gravitee API Management?

Our goal in launching Gravitee APIM is to provide users with a highly flexible and scalable solution that seamlessly integrates with their infrastructure and expertly conforms to their business needs. We’ve designed and developed APIM to be fully extensible using its own internal plugin system: you can define your own policy, develop your own reporting system, and more.

Additionally, all APIM components (including APIM Gateway and APIM Management API) are incredibly lightweight. Gravitee's consciously aggressive approach to CPU and memory management enables our products to supply high availability through lightning-fast component start-up times. For a typical number of API deployments, it takes **less than 5 seconds** for the API Gateway to be accessible to consumers.

## Core APIM Concepts

**Gateway API:** The root concept defined and used by APIM and through which services are exposed to the Gateway.

**API Publisher:** Gravitee defines an API publisher as the role that declares and manages APIs.

**API Consumer:** Gravitee defines an API Consumer as the role that consumes APIs. Consumers are granted access to APIs via subscriptions.

### Application

An **application** is an intermediate level between a consumer and an API. Through applications, consumers are grouped together and the application as a whole subscribes to the API.

## First steps

Ready to use Gravitee API Management? Let’s get started! Select from the options below to learn more about APIM, or head over to the install guides to get APIM up and running.

<table data-view="cards"><thead><tr><th></th><th></th><th></th><th data-hidden data-card-target data-type="content-ref"></th></tr></thead><tbody><tr><td></td><td>APIM Architecture</td><td></td><td><a href="overview/introduction-to-gravitee-api-management-apim/apim-architecture.md">apim-architecture.md</a></td></tr><tr><td></td><td>Plugins</td><td></td><td><a href="overview/introduction-to-gravitee-api-management-apim/plugins.md">plugins.md</a></td></tr><tr><td></td><td>Integrations</td><td></td><td><a href="overview/integrations/">integrations</a></td></tr><tr><td></td><td>Open Source vs Enterprise Edition</td><td></td><td><a href="overview/introduction-to-gravitee-api-management-apim/ee-vs-oss.md">ee-vs-oss.md</a></td></tr><tr><td></td><td>Install &#x26; Upgrade Guides</td><td></td><td><a href="getting-started/install-and-upgrade/install-guides/">install-guides</a></td></tr></tbody></table>
