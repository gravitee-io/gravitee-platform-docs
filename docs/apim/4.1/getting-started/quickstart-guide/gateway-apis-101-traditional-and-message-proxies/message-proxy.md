---
description: Use Gravitee to proxy your message and event brokers
---

# Message Proxy

{% hint style="danger" %}
Message proxies require an enterprise license. If you don't have one, you can [schedule a demo](https://www.gravitee.io/demo).
{% endhint %}

## Overview

A message proxy is functionality enabled exclusively by Gravitee API Management's (APIM) event-native Gateway. It allows you to securely expose backend message brokers such as Kafka and MQTT to external clients over web-friendly protocols like HTTP, WebSockets, Webhook, and SSE. This is known as _protocol mediation_.

With APIM, protocol mediation is extremely simple. The complexity of producing to and consuming from the message broker is handled internally by the Gateway.

<img src="../../../.gitbook/assets/file.excalidraw (8) (1).svg" alt="Message proxy example" class="gitbook-drawing">

Let's continue with the API creation wizard to see how easily a message proxy can be created.

<figure><img src="../../../.gitbook/assets/message proxy_create (1).png" alt=""><figcaption><p>Creating a message proxy</p></figcaption></figure>

> * [x] Select **Introspect Messages From Event-Driven Backend**
> * [x] Click **Select my API Architecture** to continue

## Gateway entrypoints and endpoints

The next step is configuring how the Gateway will communicate with clients and backend message brokers. This is done through Gateway entrypoints and endpoints:

* **Gateway entrypoint:** Defines the protocol and configuration settings by which the API consumer communicates with the Gateway. In other words, the Gateway entrypoint dictates how the backend message broker is exposed externally through the Gateway.
* **Gateway endpoint:** Defines the protocol and configuration settings by which the Gateway API will fetch data/functionality from, or post data to, the backend message broker.

<img src="../../../.gitbook/assets/file.excalidraw (7) (1).svg" alt="Gateway entypoints and endpoints" class="gitbook-drawing">

### Entrypoints

Unlike traditional proxies, message proxies perform protocol mediation between the Gateway entrypoints and endpoints.

This allows you to expose your message brokers using one or more web-friendly protocols, based on your requirements and those of your API consumers. Each protocol you select has its own set of configuration options.

<figure><img src="../../../.gitbook/assets/message proxy_entrypoints (1).png" alt=""><figcaption><p>Select your entrypoints</p></figcaption></figure>

> * [x] Select **HTTP GET**
> * [x] Select **Websocket**
> * [x] Click **Select my entrypoints** to continue

#### Entrypoint protocol configuration

You will be able to configure each entrypoint protocol you select, but regardless of your protocol selection, you must provide one or more context-paths.

A context-path is the unique route of the Gateway API. The context-path does not include the fully qualified domain name of the Gateway.

<details>

<summary>Example</summary>

Let's say we provided a context-path of `/qs-message-api`. Once the API is fully configured and deployed to the Gateway, API consumers can reach the API at `https://apim-gateway-server/qs-message-api`for HTTP GET requests or `wss://apim-gateway-server/qs-message-api` for WebSockets connections.

</details>

<figure><img src="../../../.gitbook/assets/message proxy_entrypoint configure (1).png" alt=""><figcaption><p>Configure HTTP GET and WebSockets entrypoints</p></figcaption></figure>

> * [x] Provide a **Context-path**
> * [x] Leave the default configuration for the HTTP GET and WebSockets entrypoints
> * [x] Scroll down and select **Validate my entrypoints** to continue

### Endpoints

Endpoints are how your Gateway API connects to your backend message brokers. Each endpoint option has configuration settings specific to that particular message broker. You can configure multiple endpoint types within the same Gateway API.

For this tutorial, we will select the Mock endpoint, which is ideal for testing and demo purposes. The Mock endpoint allows us to generate data without actually having to run a backend server.

<figure><img src="../../../.gitbook/assets/message proxy_endpoints (1).png" alt=""><figcaption><p>Select your endpoints</p></figcaption></figure>

> * [x] Select the **Mock** endpoint
> * [x] Click **Select my endpoints** to continue

#### Endpoint event broker configuration

Typically, this is where you configure your connection to the backend cluster running your event broker of choice. Gravitee uses this configuration to create an internal broker client and manage the connection to the backend cluster.

The configuration is highly specific to the endpoint you select. For our Mock endpoint, we can configure the specifics of the data being produced. We will leave the default settings, which will produce a message every second with a payload of `mock message` as soon as an API consumer connects to one of the entrypoints.

<figure><img src="../../../.gitbook/assets/mock endpoint config (1).png" alt=""><figcaption><p>Mock endpoint configuration</p></figcaption></figure>

> * [x] Click **Validate my endpoints** to continue

## Security

The next step is to configure your API security with plans. In APIM, a plan provides a service and access layer on top of your API that specifies access limits, subscription validation modes, and other configurations to tailor your API to a specific subset of API consumers. All APIs require one or more plans.

We will be focusing on plans in the next part of the Quickstart Guide. For now, we will use the default keyless plan.

<figure><img src="../../../.gitbook/assets/message proxy_security (1).png" alt=""><figcaption><p>Gateway API security</p></figcaption></figure>

> * [x] Leave defaults and select **Validate my plans** to continue to the final step

{% hint style="danger" %}
By default, a keyless plan provides unrestricted access to your backend resources.

* If you’re deploying an API to the Gateway that proxies sensitive information, ensure it does not include a keyless plan.
* For production Gateways, keyless plans can be disabled entirely.
{% endhint %}

## Summary

The final step in creating an API is to review and then save your configuration. The API creation wizard presents you with two options:

* **Save API:** This option will save your API, but it will not be available on the Gateway. This is useful if you'd like to complete some more advanced configuration (e.g., adding policies) before starting the API on the Gateway.
* **Save & Deploy API:** This option will save your API and immediately start it on the Gateway.

<figure><img src="../../../.gitbook/assets/message proxy_summary (1).png" alt=""><figcaption><p>Gateway API summary page</p></figcaption></figure>

> * [x] Select **Save & Deploy API** so we can begin testing immediately

## Manage your API

You will be greeted with a screen that confirms the creation of your new API and includes several shortcuts to help you start managing it.

<figure><img src="../../../.gitbook/assets/message proxy_confirmation (1).png" alt=""><figcaption><p>API creation confirmation</p></figcaption></figure>

> * [x] Select **Open my API in API Management** to see how to manage your API

This will bring you to the **General Info** page that contains high-level metadata about your API, as well as important API management actions in the **Danger Zone**.

<details>

<summary>Danger Zone deep dive</summary>

The **Danger Zone** should be self-descriptive. Use these actions with caution in production.

Below is a short summary of the different actions, each of which alters the state of your API. Some of these may not make sense until you complete the entire Quickstart Guide, so you may want to reference this later.

* **Stop the API/Start the API:** This action behaves like a toggle, stopping an active API or starting an inactive API. When stopped, all requests to the API will result in the client receiving an HTTP `404 Not Found` response status code.
* **Publish the API/Unpublish the API:** This action behaves like a toggle, publishing an unpublished API or unpublishing a published API. Publishing makes the API visible to members in the Developer Portal (also commonly referred to as an API catalog).
* **Make Public/Make Private:** This action behaves like a toggle, but only impacts published APIs. By default, published APIs can only be seen in the Developer Portal by members of that API. Making a published API public allows anybody with access to the Developer Portal to see the API.
* **Deprecate:** This action permanently blocks any new subscription requests. However, active subscriptions will continue to function unless the API is stopped or deleted.
* **Delete:** This action permanently deletes an API. To delete an API, it must be stopped and all plans must be deleted.

</details>

On this page, you can manage every aspect of your Gateway API by selecting different tabs from the inner sidebar. We'll be diving into some of these options later in the Quickstart Guide.

<figure><img src="../../../.gitbook/assets/message proxy_general info (1).png" alt=""><figcaption><p>API General Info page</p></figcaption></figure>

## Test your API

Your first API is now started on the Gateway. Since we are using a keyless plan, you can immediately test it by opening your terminal and sending either of the requests below, after modifying the relevant portions:

* `your-gateway-server` should be replaced with the fully qualified domain name of your Gateway's server. Remember, your Gateway will be on a different domain than the Console UI. For example, the default local Docker deployment has the Console UI on `localhost:8084` and the Gateway on `localhost:8082`.
* `your-context-path` should be replaced by the context-path of the Gateway API you just deployed. You can always find the context-path under **Entrypoints**.

{% hint style="warning" %}
`websocat` is a CLI tool for establishing WebSockets connections that must be [installed on your machine](https://github.com/vi/websocat#installation).
{% endhint %}

{% hint style="warning" %}
Ensure you use the proper protocol! For example, the default local Docker installation of APIM would use `http` and `ws` instead of `https` and `wss`, respectively, as SSL must be manually enabled.
{% endhint %}

{% code overflow="wrap" %}
```sh
$ curl -X GET -i "https://your-gateway-server/your-context-path"
$ websocat "wss://your-gateway-server/your-context-path"
```
{% endcode %}

For the `curl` request to the HTTP GET entrypoint, you should receive the HTTP `200 OK` success status response code and four JSON messages returned with the content of `"mock message"`. This is because the Mock endpoint is configured to produce a message every second and the HTTP GET entrypoint is configured to receive messages for a maximum of five seconds.

For the `websocat` request, a WebSockets connection should be established that continues to receive a message every second with a payload of `mock message` until you close the connection.

{% hint style="success" %}
Congrats! You have successfully deployed your first API to the Gateway and sent your first request!
{% endhint %}

## Next Steps

You should now have a basic understanding of Gravitee APIM's most fundamental concept: Gateway APIs. The Quickstart Guide will build on that knowledge by diving into the real power of APIM: Plans and Policies.

<table data-card-size="large" data-view="cards"><thead><tr><th></th><th></th><th></th><th data-hidden data-card-target data-type="content-ref"></th></tr></thead><tbody><tr><td></td><td><strong>Plans and Policies 101</strong></td><td></td><td><a href="../plans-and-policies-101.md">plans-and-policies-101.md</a></td></tr></tbody></table>
