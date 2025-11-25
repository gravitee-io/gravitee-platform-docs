---
description: Manage and expose your backend resources with Gravitee
---

# Gateway APIs 101 - Traditional & Message Proxies

{% hint style="warning" %}
Before beginning this guide, you should already have the Gravitee API Management Console up and running. [Start here](./) if you need help!
{% endhint %}

## Overview

Gravitee API Management (APIM) consists of four components:

1. Gateway
2. Console UI
3. Developer Portal
4. Management API

For now, we just need to focus on the Gateway and the Console UI. The Gateway acts as a single, unified entrypoint for all backend services providing centralized security, traffic shaping, monitoring, and observability. The Console is a graphical user interface for configuring all the different components of your Gateway.

The first Gravitee concept you need to understand is Gateway APIs. As the name suggests, Gateway APIs are APIs deployed to the Gateway and are what your API consumers will call or subscribe to in order to retrieve data, functionality, etc., from your backend services or resources. Your backend services are essentially the data source or functionality that you want to expose to your consumers through the Gateway.

<figure><img src="../../../.gitbook/assets/gateway apis_drawing.png" alt=""><figcaption></figcaption></figure>

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

***

## Create a Gateway API

Now that we've detailed the high-level concepts, let's dive into how to actually build an API in the Console UI.

### Access API creation wizard

To get started, you need to access your **APIs** homescreen. This screen displays the status of all the Gateway APIs that have been created in your current environment.

Assuming you have the proper permissions, you can access and modify the configurations of existing APIs, or, in our case, create new APIs.

<figure><img src="../../../.gitbook/assets/apis_homescreen.png" alt=""><figcaption><p>APIs homscreen</p></figcaption></figure>

> * [x] Select **APIs** in the sidebar of the Console UI
> * [x] Next, select **+ Add API** in the top right to create a new API

You will be greeted with several options to create an API. We will be creating a v4 API with the creation wizard.

<figure><img src="../../../.gitbook/assets/options.png" alt=""><figcaption><p>Options to create a new Gateway API</p></figcaption></figure>

> * [x] Select the green **Create =>** button shown next to **Create a V4 API from scratch**

### API details

API details is the first step of the API creation wizard. Provide a name, version, and (optionally) a description for your API. This is the metadata for your API.

<figure><img src="../../../.gitbook/assets/api_details.png" alt=""><figcaption><p>Fill in API details</p></figcaption></figure>

> * [x] Provide a name, version, and (optionally) a description for your API
> * [x] Select **Validate my API details** to move on to the next step

### Proxy selection: Choose your path

This step is where you decide between the [traditional proxy and message proxy](./#traditional-and-message-proxies):

* **Traditional proxy:** Select **Proxy Upstream Protocol** to configure the Gateway API to proxy backend API servers
* **Message proxy**: Select **Introspect Messages From Event-Driven Backend** to configure the Gateway API to proxy event/message brokers

{% hint style="warning" %}
Message proxies require an enterprise license. If you don't have one, you can [schedule a demo](https://www.gravitee.io/demo).
{% endhint %}

In the Console UI, choose which type of proxy you'd like to create based on the backend resource you're most interested in exposing. If you don't have a preference, we recommend trying a traditional proxy first, as it is easier to conceptualize.

<figure><img src="../../../.gitbook/assets/traditional or message.png" alt=""><figcaption><p>Traditional or message proxy selection</p></figcaption></figure>

> * [x] Choose **Proxy Upstream Protocol** or **Introspect Messages from Event-Driven Backend**

Based on your selection in the Console, continue with the applicable guide:

<table data-card-size="large" data-view="cards"><thead><tr><th></th><th data-hidden data-card-target data-type="content-ref"></th></tr></thead><tbody><tr><td><p><strong>Traditional Proxy (Proxy Upstream Protocol)</strong></p><p>Gateway APIs 101 | Proxy backend API servers</p></td><td><a href="broken-reference/">broken-reference</a></td></tr><tr><td><p><strong>Message Proxy (Introspect Messages From Event-Driven Backend)</strong></p><p>Gateway APIs 101 | Proxy event/message brokers</p></td><td><a href="broken-reference/">broken-reference</a></td></tr></tbody></table>
