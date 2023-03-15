---
description: >-
  Learn how to create your Gravitee APIs using the Gravitee Management Console
  UI
---

# How-to

### Create APIs using the API Management (APIM) UI

Gravitee offers two ways to create Gateway APIs using the APIM UI:

* The API creation wizard
* Importing an API

You can also use the API Designer for API creation. However, the API Designer is used to create data models for local or web APIs and not for creating Gateway APIs. Because of this, we have written specific documentation for using the API Designer, and we will focus on only the creation wizard and the API import options in this section.

### Create a Gateway API using the API creation wizard

{% @arcade/embed flowId="gjzRqNfSladxmw4olxSX" url="https://app.arcade.software/share/gjzRqNfSladxmw4olxSX" %}

The API creation wizard is comprised of several steps, each which requires you to define certain sets of information:

* API details
* API architecture
* Entrypoints
* Endpoints
* Security
* Documentation
* Summray

#### Step 1: API details

The API details step is where you can define a name, version number, and description for your API. The name and version number are required, but we also recommend giving your API a description so that it is more easily understood and managed by internal users.

<figure><img src="../../.gitbook/assets/Screen Shot 2023-03-15 at 12.38.10 PM.png" alt=""><figcaption><p>Step 1: define your Gateway API's basic details.</p></figcaption></figure>

#### Step 2: API architecture

The API Architecture component is where you'll define the kind of backend resource that you want to expose. As of now, there are two API architectures:

* **HTTP proxy:** this will be used for "pure" REST, gRPC, SOAP, and WebSocket use cases, where you want to expose a backend REST API as a Gateway REST API, a backend WebSocket Server as a Gateway WebSocket, and so on.
* **Message-based:** this will be used when the kind of backend resource that you want to expose is an event-broker.

What you choose here will dictate the kinds of entrypoints and endpoints that you can select later on.&#x20;

&#x20;

<figure><img src="../../.gitbook/assets/Screen Shot 2023-03-15 at 12.41.03 PM.png" alt=""><figcaption><p>Step 2: selecting your API architecture</p></figcaption></figure>

#### Step 3: Entrypoints

After you select your API Architecture, you'll have to choose your entrypoint(s). You will have different options based on the architecture choice from earlier.&#x20;

If you chose **HTTP Proxy**, the entrypoints step will just require you to define a context path and decide whether or not you want to enable virtual hosts. The context path is just the URL location of your API. So if your URL is `[https://apim-master-gateway.team-apim.gravitee.dev/myAPI]` then `[/myAPI]` is the context path. Please note that the context path must start with a '/' and can only contain uppercase letters, numbers, dashes or underscores.

If you select :heavy\_check\_mark:**Enable virtual hosts**, you'll have to define the following in addition to your context path:

* **Virtual host:** the host that must be set in the HTTP request to access your entrypoint.
* **Override access: e**nable override on the access URL of your Portal using a virtual host.
  * To enable or disable this, simply toggle **Enable** ON or OFF

To disable virtual hosts, just select **X Disable virtual hosts.**&#x20;

<figure><img src="../../.gitbook/assets/HTTP proxy entrypoints.gif" alt=""><figcaption><p>HTTP-Proxy entrypoints</p></figcaption></figure>

If you chose **Message-based,** you get a much different set of entrypoint options:

* **HTTP GET:** allows you to front a chosen backend or data source with a Gateway REST API with support for the HTTP GET request
* **HTTP POST:** allows you to front a chosen backend or data source with a Gateway REST API with support for the HTTP POST request
* **Server-sent Events:** allows you to front a chosen backend or data source with a Gateway SSE API for unidirectional communication between server and client
* **Server-sent Events advanced:** allows you to front a chosen backend or data source with a Gateway SSE API for unidirectional communication between server and client with additional support for Quality of Service (QoS)
* **Webhook**: allows you to front a chosen backend or data source with a Gateway Webhook API. This allows consumers to subscribe to the Gravitee Gateway via Webhook and then retrieve streamed data in real-time from a backend data source, via the Gateway, over the consumer's Webhook callback URL.
* **WebSocket**: allows you to front a chosen backend or data source with a Gateway WebSocket API. This allows for a consumer to retrieve and send streamed events and messages in real-time.

<figure><img src="../../.gitbook/assets/Message-based entrypoints.png" alt=""><figcaption><p>Message-based entrypoints</p></figcaption></figure>

Once you select your entrypoints from the entrypoints page, there will be further configuration required. Please browse the following tabs for more information based on your chosen entrypoint(s).

{% tabs %}
{% tab title="HTTP GET" %}
If you chose HTTP GET as an entrypoint, you will be brought to a page where you can configure:

* The context path: the URL location of your API. So if your URL is `[https://apim-master-gateway.team-apim.gravitee.dev/myAPI]` then `[/myAPI]` is the context path.
* Your HTTP GET characteristics
  * **Limit messages count:** this defines the maximum number of messages to retrieve via HTTP GET. Default is 500. To set a custom limit, enter in your limit as a numerical value in the **Limit messages count** text field.
  * **Limit messages duration:** this defines the maximum duration in milliseconds to wait to retrieve the expected number of messages (See Limit messages count). The effective number of retrieved messages could be less than expected it maximum duration is reached. To set a custom limit, enter in your limit as a numerical value in the **Limit messages count** text field.
  * **HTTP GET permissions:** you can define whether or not to Allow sending messages headers to client in payload or Allow sending messages metadata to client in payload.&#x20;
    * To allow or disallow these actions, toggle either **Allow sending messages headers to client in payload** or **Allow sending messages metadata to client in payload** to either ON or OFF.&#x20;
{% endtab %}

{% tab title="Second Tab" %}

{% endtab %}
{% endtabs %}

#### Endpoints

**Gateway endpoints** define the protocol and configuration by which the gateway API will fetch data from, or post data to, the backend API. Your endpoints will be dictated by the entrypoints that you select.&#x20;
