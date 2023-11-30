---
description: Manage and expose your backend resources with Gravitee
---

# Gateway APIs 101 - Traditional & Message Proxies

{% hint style="warning" %}
Before beginning this guide, you should already have the Gravitee API Management Console up and running. [Start here](../) if you need help!
{% endhint %}

## Overview

Gravitee API Management (APIM) consists of four components:

1. Gateway
2. Console UI
3. Developer Portal
4. Management API

For now, we just need to focus on the Gateway and the Console UI. The Gateway acts as a single, unified entrypoint for all backend services providing centralized security, traffic shaping, monitoring, and observability. The Console is a graphical user interface for configuring all the different components of your Gateway.

The first Gravitee concept you need to understand is Gateway APIs. As the name suggests, Gateway APIs are APIs deployed to the Gateway and are what your API consumers will call or subscribe to, in order to retrieve data, functionality, etc., from your backend services or resources. Your backend services are essentially the data source or functionality that you want to expose to your consumers through the Gateway.

<img src="../../../.gitbook/assets/file.excalidraw (11).svg" alt="" class="gitbook-drawing">

{% hint style="warning" %}
In this quick start guide, Gateway APIs and APIs are often used synonymously. However, when referring to an API server being used as a backend service or resource, we will be explicit and say backend API.
{% endhint %}

### Traditional and Message Proxies

Since the external clients send requests directly to the Gateway, it is often referred to as a reverse proxy. Based on the type of backend resource you want to expose, Gravitee supports two types of reverse proxies:

* **Traditional Proxy:** Use this method if you want to use the Gateway to proxy API servers. APIM supports numerous web-friendly protocols like HTTP (including architectural styles like REST, SOAP, GraphQL, etc.), WebSockets, and gRPC.
* **Message Proxy:** Use this method if you want to use the Gateway to proxy message/event brokers. APIM supports a number of messaging and streaming solutions like RabbitMQ, Kafka, MQTT, and Solace.

Regardless of the proxy type, APIM allows you to abstract your backend resource as an API. This allows you to manage both types of resources under a single, unified platform and expose them to API consumers in a simple, secure, and consistent interface.

### Gateway API components

Gateway API creation is broken into five steps - which we will explain briefly here:

1. **API details:** Provide a name, description, and version for your API.&#x20;
2. **Gateway Entrypoints:** Defines the protocol(s) and configuration settings by which the API consumer accesses the API. The Gateway entrypoint dictates how the backend API is exposed through the Gateway.
3. **Gateway Endpoints:** Defines the protocol(s) and configuration settings by which the Gateway will fetch data/functionality from, and/or post data to, the backend resource.
4. **Security:** Configure a layer of access control through plans. Plans are the means by which the API publisher can secure, monitor, and transparently communicate access details.
5. **Summary:** Review your API configuration. From here, you can save your configuration, or save and deploy your API which makes it immediately available on your Gateway.

***

## Create a Gateway API

Now that we've detailed the high-level concepts, let's dive into how to actually build one in the Console UI.

### Access API creation wizard

To get started, you need to access your APIs home screen. This screen contains the status of all the Gateway APIs that have been created in your current environment.

Assuming you have the proper permissions, you can access and modify the configuration of existing APIs, or, in our case, create new APIs.

{% hint style="info" %}
Note, that if you see APIs you did not create, this is because the free trial includes some preconfigured APIs. Ignore these for now.
{% endhint %}

<figure><img src="../../../.gitbook/assets/Screenshot 2023-11-09 at 5.39.37 PM.png" alt=""><figcaption><p>APIs homscreen</p></figcaption></figure>

> * [x] Select **APIs** in the sidebar of the Console UI
> * [x] Next, select **+ Add API** in the top right to create a new API

You will be greeted with several options to create an API. We will be creating a v4 API with the creation wizard and ignoring the other options for now.&#x20;

<figure><img src="../../../.gitbook/assets/Screenshot 2023-11-09 at 5.47.49 PM.png" alt=""><figcaption><p>Options to create a new Gateway API</p></figcaption></figure>

> * [x] Select the green **Create =>** button shown next to **Create a V4 API from scratch**

### API Details

API details is the first step of the API creation wizard. Simply provide a name, version, and (optionally) a description for your API. This is the metadata for your API.

<figure><img src="../../../.gitbook/assets/Screenshot 2023-11-09 at 7.38.00 PM.png" alt=""><figcaption><p>Fill in API details</p></figcaption></figure>

> * [x] Provide a name, version, and (optionally) a description for your API
> * [x] Select **Validate my API details** to move on to the next step

### Proxy selection - Choose your path

This step is where you decide between the aforementioned [traditional proxy and message proxy](./#traditional-and-message-proxies):

* **Traditional proxy:** Select **Proxy Upstream Protocol** to configure the Gateway API to proxy backend API servers
* **Message proxy**: select **Introspect Messages From Event-Driven Backend** to configure the Gateway API to proxy event/message brokers

{% hint style="warning" %}
Message proxies require an enterprise license. If you don't have one, you can always [start a free trial](../../install-guides/free-trial.md) or [schedule a demo](https://www.gravitee.io/demo).
{% endhint %}

In the Console UI, choose which type of proxy you'd like to create based on the backend resource you're most interested in exposing. If you don't have a preference, we recommend trying a traditional proxy first, as it is easier to conceptualize.

<figure><img src="../../../.gitbook/assets/Screenshot 2023-11-09 at 7.40.50 PM.png" alt=""><figcaption><p>Traditional or message proxy selection</p></figcaption></figure>

> * [x] Choose **Proxy Upstream Protocol or** **Introspect Messages from Event-Driven Backend**

Based on your selection in the Console, continue with the applicable guide:

<table data-card-size="large" data-view="cards"><thead><tr><th></th><th data-hidden data-card-target data-type="content-ref"></th></tr></thead><tbody><tr><td><p><strong>Traditional Proxy (Proxy Upstream Protocol)</strong></p><p></p><p>Gateway APIs 101 | Proxy backend API servers</p></td><td><a href="traditional-proxy.md">traditional-proxy.md</a></td></tr><tr><td><p><strong>Message Proxy (Introspect Messages From Event-Driven Backend)</strong></p><p></p><p>Gateway APIs 101 | Proxy event/message brokers</p></td><td><a href="message-proxy.md">message-proxy.md</a></td></tr></tbody></table>
