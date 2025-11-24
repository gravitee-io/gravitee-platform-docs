---
description: Manage and expose your backend resources with Gravitee
---

# Gravitee Gateway APIs

{% hint style="warning" %}
Before beginning this guide, you should already have the Gravitee API Management Console up and running. For more information about starting the Gravitee API Management Console, see [apim-console](../../apim-console/ "mention").
{% endhint %}

## Overview

Gravitee API Management (APIM) consists of four components:

1. Gateway
2. Console UI
3. Developer Portal
4. Management API

For now, we just need to focus on the Gateway and the Console UI. The Gateway acts as a single, unified entrypoint for all backend services providing centralized security, traffic shaping, monitoring, and observability. The Console is a graphical user interface for configuring all the different components of your Gateway.

The first Gravitee concept you need to understand is Gateway APIs. As the name suggests, Gateway APIs are APIs deployed to the Gateway and are what your API consumers will call or subscribe to in order to retrieve data, functionality, etc., from your backend services or resources. Your backend services are essentially the data source or functionality that you want to expose to your consumers through the Gateway.

<img src="broken-reference" alt="" class="gitbook-drawing">

{% hint style="warning" %}
In this Quickstart Guide, the terms _Gateway API_ and _API_ are often used synonymously. However, when referring to an API server used as a backend service or resource, we use the term _backend API_.
{% endhint %}

### Traditional and message proxies

Since external clients send requests directly to the Gateway, it is often referred to as a reverse proxy. Based on the type of backend resource you want to expose, Gravitee supports two types of reverse proxies:

* **Traditional proxy:** Use this method if you want to use the Gateway to proxy API servers. APIM supports numerous web-friendly protocols like HTTP (including architectural styles like REST, SOAP, GraphQL, etc.), WebSockets, and gRPC.
* **Message proxy:** Use this method if you want to use the Gateway to proxy message/event brokers. APIM supports a number of messaging and streaming solutions like RabbitMQ, Kafka, MQTT, and Solace.

APIM allows you to abstract your backend resource as an API regardless of proxy type. This enables you to manage both resource types within a single, unified platform and expose them to API consumers using a simple, secure, and consistent interface.

### Gateway API components

Gateway API creation is broken into five steps, which we will explain briefly here:

1. **API details:** Provide a name, description, and version for your API.
2. **Gateway entrypoints:** Define the protocol(s) and configuration settings by which the API consumer accesses the API. The Gateway entrypoint dictates how the backend API is exposed through the Gateway.
3. **Gateway endpoints:** Define the protocol(s) and configuration settings by which the Gateway will fetch data/functionality from, and/or post data to, the backend resource.
4. **Security:** Configure a layer of access control through plans. Plans enable the API publisher to secure, monitor, and transparently communicate access details.
5. **Summary:** Review your API configuration. You can then either save your configuration or save and deploy your API, which makes it immediately available on your Gateway.
