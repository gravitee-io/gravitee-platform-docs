---
description: Learn how to create your Gravitee APIs using the Gravitee API creation wizard
---

# The API Creation Wizard

### Introduction

The API creation wizard makes it easy to create new Gateway API's from scratch.&#x20;

### Create your Gateway API

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
If you chose **HTTP GET** as an entrypoint, you will be brought to a page where you can configure:

* The context path: the URL location of your API. So if your URL is `[https://apim-master-gateway.team-apim.gravitee.dev/myAPI]` then `[/myAPI]` is the context path.
* Enabling virtual hosts
  * This will then require you to define your **Virtual host** and optionally enable **override access.**
* Your HTTP GET characteristics
  * **Limit messages count:** this defines the maximum number of messages to retrieve via HTTP GET. Default is 500. To set a custom limit, enter in your limit as a numerical value in the **Limit messages count** text field.
  * **Limit messages duration:** this defines the maximum duration in milliseconds to wait to retrieve the expected number of messages (See Limit messages count). The effective number of retrieved messages could be less than expected it maximum duration is reached. To set a custom limit, enter in your limit as a numerical value in the **Limit messages count** text field.
  * **HTTP GET permissions:** you can define whether or not to Allow sending messages headers to client in payload or Allow sending messages metadata to client in payload.&#x20;
    * To allow or disallow these actions, toggle either **Allow sending messages headers to client in payload** or **Allow sending messages metadata to client in payload** to either ON or OFF.&#x20;

<figure><img src="../../.gitbook/assets/HTTP GET entrypoint config.gif" alt=""><figcaption></figcaption></figure>
{% endtab %}

{% tab title="HTTP POST" %}
If you chose **HTTP POST** as an entrypoint, you will be brought to a page where you can configure:

* **The context path:** the URL location of your API. So if your URL is `[https://apim-master-gateway.team-apim.gravitee.dev/myAPI]` then `[/myAPI]` is the context path.
* **Enabling virtual hosts**
  * This will then require you to define your **Virtual host** and optionally enable **override access.**
* **HTTP POST permissions:** here, you can choose to allow add request Headers to the generated message. To do this toggle, **Allow add request Headers to the generated message** ON or OFF**.**

<figure><img src="../../.gitbook/assets/HTTP POST entrypoint config.gif" alt=""><figcaption></figcaption></figure>
{% endtab %}

{% tab title="Server-sent events (SSE) or SSE advanced" %}
If you chose **SSE** as an entrypoint, you will be brought to a page where you can configure:

* **The context path:** the URL location of your API. So if your URL is `[https://apim-master-gateway.team-apim.gravitee.dev/myAPI]` then `[/myAPI]` is the context path.
* **Enabling virtual hosts**
  * This will then require you to define your **Virtual host** and optionally enable **override access.**
* **SSE characteristics and permissions:**&#x20;
  * **Heartbeat intervals:** define the interval in which heartbeats are sent to the client. Intervals must be higher or equal than 2000ms. To configure this, enter a numerical value into the **Define the interval in which heartbeats** **are sent to client** text field either by typing a numerical value or by using the arrows in the text field. Each heartbeat will be sent as extra empty comment: `''`
  * Permissions:
    * Choose to allow or disallow sending messages metadata to client as SSE comments. To allow or disallow this, toggle **Allow sending messages metadata to client as SSE comments** ON or OFF.
    * Choose to allow or disallow sending messages headers to client as SSE comments. To allow or disallow this, toggle **Allow sending messages headers to client as SSE comments** ON or OFF.

<figure><img src="../../.gitbook/assets/SSE entrypoint config.gif" alt=""><figcaption></figcaption></figure>
{% endtab %}

{% tab title="Webhook" %}
If you chose **Webhook** as an entrypoint, you will be brought to a page where you can configure:

* **HTTP Options**
  * **Connect timeout:** maximum time to connect to the webhook in milliseconds. Either type a numerical value or use the arrows on the right of the text field.
  * **Read timeout:** maximum time given to the webhook to complete the request (including response) in milliseconds. Either type a numerical value or use the arrows on the right of the text field.
  * **Idle timeout:** maximum time a connection will stay in the pool without being used in milliseconds. Once the timeout has elapsed, the unused connection will be closed, allowing to free the associated resources. Either type a numerical value or use the arrows on the right of the text field.
* **Proxy options**
  * **Use proxy:** choose whether or not to use a proxy for client connections. To enable this, toggle Use proxy ON.
    * If you enable Use proxy, you will need to select the Proxy type in the **Proxy type** drop-down. You choose between:
      * HTTP proxy
      * SOCKS4
      * SOCKS5
  * **Use system proxy:** choose to use the proxy configured at system level. If you enable this, you'll need to define the:
    * Proxy host: enter your proxy host in the **Proxy host** text field.
    * Proxy port: enter your proxy port in the **Proxy port** text field.
    * (Optional) Proxy username: enter your proxy username in the **Proxy username** text field.
    * (Optional) Proxy password: enter your proxy password in the **Proxy password** text field.

{% hint style="info" %}
**SOCKS proxy**\
****[A SOCKS proxy](https://hailbytes.com/how-to-use-socks4-and-socks5-proxy-servers-for-anonymous-web-browsing/) is a type of proxy server that uses the SOCKS protocol to tunnel traffic through an intermediary server.
{% endhint %}

<figure><img src="../../.gitbook/assets/Webhook entrypoint config.gif" alt=""><figcaption><p>Webhook entrypoint config</p></figcaption></figure>
{% endtab %}

{% tab title="WebSocket" %}
If you chose **WebSocket** as an entrypoint, you will be brought to a page where you can configure:

* **The context path:** the URL location of your API. So if your URL is `[https://apim-master-gateway.team-apim.gravitee.dev/myAPI]` then `[/myAPI]` is the context path.
* **Enabling virtual hosts**
  * This will then require you to define your **Virtual host** and optionally enable **override access.**
* **WebSocket configuration**
  * **Publisher configuration:** choose to either enable or disable the publication capability. By disabling it, you assume that the application will never be able to publish any message. To do this, toggle **Enable the publication capability** ON or OFF.
  * **Subscriber configuration:** choose to enable or disable the subscription capability. By disabling it, you assume that the application will never receive any message. To do this, toggle **Enable the subscription capability** ON or OFF.

<figure><img src="../../.gitbook/assets/WebSocket entrypoint config.gif" alt=""><figcaption><p>WebSocket entrypoint config</p></figcaption></figure>
{% endtab %}
{% endtabs %}

#### Endpoints

**Gateway endpoints** define the protocol and configuration by which the gateway API will fetch data from, or post data to, the backend API. Your endpoints will be dictated by the API architecture that you selected earlier. If you chose the HTTP Proxy option, your endpoint will be an HTTP Proxy. To configure this endpoint, you will be brough to a page where you can:

* **Define your target url:** enter your target url in the **Target url** text field.
* **Define your HTTP options**
  * Choose to either allow or diallow h2c clear text upgrade by toggling **Allow h2c Clear Text Upgrade** ON or OFF.
    * You'll need to select the HTTP protocol version to use. As of now, HTTP/1.1 or HTTP/2 are options.
  * Choose to either enable or disable keep-alive by toggling **Enable keep-alive** ON or OFF
    * If you enable this, you'll need to define a timeout value by entering a numerical value in the **Connect timeout** text field by either typing in a numerical value or using the arrow keys in the text field.
  * Choose to either enable or disable HTTP pipelining by toggling **Enable HTTP pipelining** ON or OFF.&#x20;
    * If you enable this, you'll need to define a read timeout value by entering a numerical value in the **Read timeout** text field by either typing in a numerical value or using the arrow keys in the text field.
  * Choose to either enable or disable compression by toggling **Enable compression (gzip, deflate)** ON or OFF.&#x20;
  * **Configure your idle timeout settings**: defiens the maximum time a connection will stay in the pool without being used in milliseconds. Once the timeout has elapsed, the unused connection will be closed, allowing to free the associated resources. To configure this, enter in a numerical value or using the arrow keys in the text field.
  * Choose to follow HTTP redirects or not: toggle **Follow HTTP redirects** ON or OFF.
  * Define the number of max concurent connections: enter in a numerical value or using the arrow keys in the text field.
  * Choose to propagate client Accept-Encoding header: toggle **Propagate client Accept-Encoding header (no decompression if any)** ON or OFF.
  * Add HTTP headers: select **+ Add HTTP headers** to add headers that the Gateway should add or override before proxying the request to the backend API.
* **Define your Proxy options**
* **Define your SSL options**
* **Define your Key store**

