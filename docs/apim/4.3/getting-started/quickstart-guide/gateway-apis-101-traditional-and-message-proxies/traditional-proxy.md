---
description: Use Gravitee to proxy your backend API servers
---

# Traditional Proxy

## Overview

A traditional proxy is the classic API Gateway use case. The Gateway will connect with the client and the backend service using the same protocol.

<img src="../../../../../../.gitbook/assets/file.excalidraw (2) (1).svg" alt="Traditional proxy example" class="gitbook-drawing">

Let's continue with the API creation wizard to see how easily a traditional proxy can be created with Gravitee.

<figure><img src="../../../../4.0/.gitbook/assets/traditional proxy (1).png" alt=""><figcaption><p>Creating a traditional proxy</p></figcaption></figure>

> * [x] Select **Proxy Upstream Protocol**
> * [x] Click **Select my API Architecture** to continue

## Gateway entrypoints and endpoints

The next step is configuring how the Gateway will communicate with clients and backend servers. This is done through Gateway entrypoints and endpoints:

* **Gateway entrypoint:** Provides the means for the API consumer to interact with the Gateway API.
* **Gateway endpoint:** Defines the protocol and configuration settings by which the Gateway API will fetch data/functionality from, or post data to, the backend API server.

<img src="../../../../../../.gitbook/assets/file.excalidraw (3) (1).svg" alt="Gateway entrypoints and endpoints" class="gitbook-drawing">

### Entrypoints

To determine how to route requests from API consumers, the Gateway relies on context-paths. A Gateway API can have one or more context-paths, but they must be unique between all APIs deployed to the same Gateway.

{% hint style="info" %}
For traditional proxies, the Gateway entrypoint will automatically use the same protocol as your API server.
{% endhint %}

There are two important items to note about the context-path:

* The context-path does not include the fully qualified domain name of the Gateway.
* The context-path is stripped before the request is forwarded to the backend service.

<details>

<summary>Example</summary>

Let's say we provided a context-path of `/qs-traditional-api`. Once the API is fully configured and deployed to the Gateway, API consumers can reach the API at `https://apim-gateway-server/qs-traditional-api`. Now, if the consumer sends the following HTTP request to the Gateway:

```
GET https://apim-gateway-server/qs-traditional-api/orders
```

Then the backend API server will receive the following request:

```
GET https://backend-api-server/orders
```

</details>

<figure><img src="../../../../4.0/.gitbook/assets/traditional proxy_context path (1).png" alt=""><figcaption><p>Provide a context-path</p></figcaption></figure>

> * [x] Provide a context-path
> * [x] Select **Validate my entrypoints** to move on to endpoints configuration

### Endpoints

In addition to the standard HTTP configuration options, traditional proxies include several key Gateway endpoint settings. These are discussed in detail below.

#### Target URL

The first and most important option is the **Target url**. This is the root-level URL of your backend API server. Continuing our previous [entrypoint example](traditional-proxy.md#example), the target URL would be `https://backend-api-server/`. By default, all resources under this URL would be accessible through the Gateway.

<details>

<summary>Example continued</summary>

Let's imagine your backend API server, `https://backend-api-server/`, has two resources: `orders` and `customers`. After setting the Gateway API's target URL to `https://backend-api-server/`, an API consumer would send API requests to the following URLs to reach these resources through the Gateway:

* Access the `orders/1` resource at `https://apim-gateway-server/qs-traditional-api/orders/1`
* Access the `customers/1` resource at `https://apim-gateway-server/qs-traditional-api/customers/1`

</details>

For this guide, you are using `https://api.gravitee.io/echo` as your Target URL, and therefore, your backend service. This is a very simple public API server that, as the name suggests, echoes back some basic information about your API request, like the headers and the size of the request body. Feel free to test out the endpoint directly in your terminal or your browser.

<figure><img src="../../../../4.0/.gitbook/assets/traditional proxy_endpoint config (1).png" alt=""><figcaption><p>Endpoint configuration</p></figcaption></figure>

> * [x] Input `https://api.gravitee.io/echo` as your **Target url**

#### Additional endpoint options

The majority of the remaining configuration options are standard HTTP configuration options that you would generally pass as HTTP request headers to manage connection timeouts, pipelining, redirects, etc. We will leave the default value for each of these settings.

{% hint style="info" %}
**SSL Options**

To clarify, the SSL options shown here are for the connection between the Gateway and your backend server. Configuring a custom truststore and keystore will have no impact on client connections to the Gateway. mTLS between clients and the Gateway are [configured at the Gateway level](../../configuration/apim-gateway/general-configuration.md), not the API level.
{% endhint %}

<figure><img src="../../../../4.0/.gitbook/assets/traditional proxy_finish config (1).png" alt=""><figcaption><p>Finish endpoints configuration</p></figcaption></figure>

> * [x] Scroll all the way down and select **Validate my endpoints** to continue to security

## Security

The next step is to configure your API security via plans. In APIM, a plan provides a service and access layer on top of an API to specify access limits, subscription validation modes, and other configurations to tailor your API to a specific subset of API consumers. All APIs require one or more plans.

We will be focusing on plans in the next part of the Quickstart Guide. For now, leave the default keyless plan.

<figure><img src="../../../../4.0/.gitbook/assets/message proxy_security (1).png" alt=""><figcaption><p>Gateway API security</p></figcaption></figure>

> * [x] Leave defaults and select **Validate my plans** to continue to the final step

{% hint style="danger" %}
By default, a keyless plan provides unrestricted access to your backend services.

* If you’re deploying an API to the Gateway that proxies sensitive information, ensure it does not include a keyless plan.
* For production Gateways, keyless plans can be disabled entirely.
{% endhint %}

## Summary

The final step in creating an API is to review and then save your configuration. The API creation wizard presents you with two options:

* **Save API:** This option will save your API, but it will not be available on the Gateway. This is useful if you'd like to complete some more advanced configuration (e.g., adding policies) before starting the API.
* **Save & Deploy API:** This option will save your API and immediately start it on the Gateway.

<figure><img src="../../../../4.0/.gitbook/assets/traditional proxy_summary (1).png" alt=""><figcaption><p>Gateway API summary page</p></figcaption></figure>

> * [x] Select **Save & Deploy API** so we can begin testing immediately

## Manage your API

You will be greeted with a screen that confirms the creation of your new API and includes several shortcuts to help you start managing it.

<figure><img src="../../../../4.0/.gitbook/assets/message proxy_confirmation (1).png" alt=""><figcaption><p>API creation confirmation</p></figcaption></figure>

> * [x] Select **Open my API in API Management** to see how to manage your API

This will take you straight to the **General Info** page that contains high-level metadata about your API, as well as important API management actions in the **Danger Zone**.

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

From this page, you can manage every aspect of your Gateway API by selecting different tabs from the inner sidebar. We'll be diving into some of these options later in the Quickstart Guide.

<figure><img src="../../../../4.0/.gitbook/assets/traditional proxy_general (1).png" alt=""><figcaption><p>API General Info page</p></figcaption></figure>

## Test your API

Your first API is now started on the Gateway. Since we are using a keyless plan, you can immediately test it by opening your terminal and sending the request below, after modifying the relevant portions:

* `<your-gateway-server>` should be replaced with the fully qualified domain name of your Gateway's server. Remember, your Gateway will be on a different domain than the Console UI.
  * For an enterprise trial, the Console URL in your browser's address bar typically looks something like `https://trial.apim.<your-account-id-here>.gravitee.xyz/console`. The Gateway server is just `trial.apim.<your-account-id-here>.gravitee.xyz`.
  * For the default local Docker deployment, the Console UI is available at `localhost:8084` and the Gateway server is `localhost:8082`.
* `<your-context-path>` should be replaced by the context-path of the Gateway API you just deployed. You can always find the context-path under **Entrypoints**.

{% hint style="warning" %}
Ensure you use the proper protocol! For example, the default local Docker installation of APIM would use `http` instead of `https`, as SSL must be manually enabled.
{% endhint %}

{% code overflow="wrap" %}
```sh
curl -X GET -i "https://<your-gateway-server>/<your-context-path>" -d 'APIM Quickstart Guide=Hello World'
```
{% endcode %}

You should receive the HTTP `200 OK` success status response code, along with your headers echoed back and a `"bodySize":33` in the response body.

{% hint style="success" %}
Congrats! You have successfully deployed your first API to the Gateway and sent your first request!
{% endhint %}

## Next Steps

You should now have a basic understanding of Gravitee APIM's most fundamental concept: Gateway APIs. The Quickstart Guide will build on that knowledge by diving into the real power of APIM: Plans and Policies.

<table data-card-size="large" data-view="cards"><thead><tr><th></th><th></th><th></th><th data-hidden data-card-target data-type="content-ref"></th></tr></thead><tbody><tr><td></td><td><strong>Plans and Policies 101</strong></td><td></td><td><a href="../plans-and-policies-101.md">plans-and-policies-101.md</a></td></tr></tbody></table>
