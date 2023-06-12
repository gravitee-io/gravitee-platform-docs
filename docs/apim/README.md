# Introduction to Gravitee API Management (APIM)

Organizations need API management solutions to publish their APIs to external developers, internal developers, and other partners. API management can unlock the potential of the organization’s data and services, as well as facilitate the transformation to OpenAPI and OpenData, extending the company’s digital platform offerings, opening new communication channels, and finding new customers.

Naturally, a growing customer base brings new challenges, such as:

* How to reduce the time taken to enroll new partners
* How to identify partners and manage their API consumption
* How to measure consumption from a consumer and/or producer point of view
* How to share and discover existing APIs
* How to manage the API lifecycle, versioning, documentation, etc.

So, how can businesses address all these challenges seamlessly, for all APIs, using a centralized tool? Simple – by choosing Gravitee API Management (APIM).

## What Is APIM?

APIM is a flexible, lightweight, and blazing-fast open-source API management solution that gives your organization full control over who accesses your API — when and how. APIM is both simple to use and powerful, acting as a global solution for API management. Gravitee APIM is composed of four main components:

1. APIM Gateway
2. APIM Management API
3. APIM Managment UI
4. APIM Developer Portal

### APIM Gateway

APIM Gateway is the core component of the APIM platform. You can think of it like a _**smart**_ proxy.

Unlike a traditional HTTP proxy, APIM Gateway has the capability to apply [policies](broken-reference) (i.e., rules) to both HTTP requests and responses according to your needs. With these policies, you can enhance request and response processing by adding transformations, security, and many other exciting features.

**Gravitee.io - Internal Gateway**

### APIM Management API

This RESTful API exposes services to manage and configure the [APIM Console](broken-reference) and [APIM Portal](broken-reference) web UIs. All exposed services are restricted by authentication and authorization rules. For more information, see the [API Reference](broken-reference) section.

### APIM Management UI

This web UI gives easy access to some key [APIM API](./#apim-api) services. [API Publishers](broken-reference) can use it to publish APIs. Administrators can also configure global platform settings and specific portal settings.

### APIM Developer Portal

This web UI gives easy access to some key [APIM API](./#apim-api) services. [API Consumers](broken-reference) can use it to search for, view, try out and subscribe to a published API. They can also use it to manage their [applications](broken-reference).

## Why Gravitee API Management?

Our goal in launching Gravitee APIM is to provide users with a highly flexible and scalable solution that integrates with their infrastructure seamlessly and fits their business needs perfectly. We’ve designed and developed APIM to be fully extensible using its own internal plugin system, so you can define your own policy, develop your own reporting system, and more.

Additionally, all APIM components (including APIM Gateway and APIM Management API) are incredibly lightweight. We took a consciously aggressive approach to CPU and memory management with our products to supply high availability through our lightning-fast component start-up times.

Typically, _**it takes less than 5 seconds**_ for the API Gateway to be accessible to consumers (subject to the number of APIs being deployed).

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

Ready to use Gravitee API Management? Let’s get started! Select any options below to learn more about APIM or head over to the install guides to get APIM up and running:

<table data-view="cards"><thead><tr><th></th><th></th><th></th></tr></thead><tbody><tr><td></td><td>APIM Architecture</td><td></td></tr><tr><td></td><td>Install &#x26; Upgrade Guides</td><td></td></tr><tr><td></td><td></td><td></td></tr></tbody></table>
