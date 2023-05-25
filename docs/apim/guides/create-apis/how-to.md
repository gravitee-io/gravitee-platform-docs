---
description: Learn how to create your Gravitee APIs using the Gravitee API creation wizard
---

# The API Creation Wizard

## Introduction

The API creation wizard makes it easy to create new Gateway API's from scratch.&#x20;

{% @arcade/embed flowId="gjzRqNfSladxmw4olxSX" url="https://app.arcade.software/share/gjzRqNfSladxmw4olxSX" %}

The API creation wizard is comprised of several steps, each which requires you to define certain sets of information:

* API details
* API architecture
* Entrypoints
* Endpoints
* Security
* Documentation
* Summray

## Step 1: API details

The API details step is where you can define a name, version number, and description for your API. The name and version number are required, but we also recommend giving your API a description so that it is more easily understood and managed by internal users.

<figure><img src="../../.gitbook/assets/Screen Shot 2023-03-15 at 12.38.10 PM.png" alt=""><figcaption><p>Step 1: define your Gateway API's basic details.</p></figcaption></figure>

## Step 2: API architecture

The API Architecture component is where you'll define the kind of backend resource that you want to expose. As of now, there are two API architectures:

* **HTTP proxy:** this will be used for "pure" REST, gRPC, SOAP, and WebSocket use cases, where you want to expose a backend REST API as a Gateway REST API, a backend WebSocket Server as a Gateway WebSocket API, and so on.
* **Message-based:** this will be used when the kind of backend resource that you want to expose is an event-broker.

What you choose here will dictate the kinds of entrypoints and endpoints that you can select later on. Please refer to [this documentation](./#api-architectures) for more in-depth information on support.

&#x20;

<figure><img src="../../.gitbook/assets/Screen Shot 2023-03-15 at 12.41.03 PM.png" alt=""><figcaption><p>Step 2: selecting your API architecture</p></figcaption></figure>

## Step 3: Entrypoints

After you select your API Architecture, you'll have to choose your entrypoint(s). You will have different options based on the architecture choice from earlier.&#x20;

### HTTP Proxy entrypoints

If you chose **HTTP Proxy**, the entrypoints step will just require you to define a context path and decide whether or not you want to enable virtual hosts. The context path is just the URL location of your API. So if your URL is `[https://apim-master-gateway.team-apim.gravitee.dev/myAPI]` then `[/myAPI]` is the context path. Please note that the context path must start with a '/' and can only contain uppercase letters, numbers, dashes or underscores.

If you select :heavy\_check\_mark:**Enable virtual hosts**, you'll have to define the following in addition to your context path:

* **Virtual host:** the host that must be set in the HTTP request to access your entrypoint.
* **Override access: e**nable override on the access URL of your Portal using a virtual host.
  * To enable or disable this, simply toggle **Enable** ON or OFF

To disable virtual hosts, just select **X Disable virtual hosts.**&#x20;

<figure><img src="../../.gitbook/assets/HTTP proxy entrypoints.gif" alt=""><figcaption><p>HTTP-Proxy entrypoints</p></figcaption></figure>

### Message-based entrypoints

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

* **The context path:** the URL location of your API. So if your URL is `[https://apim-master-gateway.team-apim.gravitee.dev/myAPI]` then `[/myAPI]` is the context path.
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
[A SOCKS proxy](https://hailbytes.com/how-to-use-socks4-and-socks5-proxy-servers-for-anonymous-web-browsing/) is a type of proxy server that uses the SOCKS protocol to tunnel traffic through an intermediary server.
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

## Step 4: Endpoints

**Gateway endpoints** define the protocol and configuration by which the gateway API will fetch data from, or post data to, the backend API. Your endpoints will be dictated by the API architecture that you selected earlier.&#x20;

### HTTP Proxy endpoints

If you chose the HTTP Proxy option, your endpoint will be an HTTP Proxy. To configure this endpoint, you will be brought to a page where you can:

* **Define your target url:** enter your target url in the **Target url** text field.
* **Define your HTTP options**
  * Choose to either allow or disallow h2c clear text upgrade by toggling **Allow h2c Clear Text Upgrade** ON or OFF.
    * You'll need to select the HTTP protocol version to use. As of now, HTTP/1.1 or HTTP/2 are options.
  * Choose to either enable or disable keep-alive by toggling **Enable keep-alive** ON or OFF
    * If you enable this, you'll need to define a timeout value by entering a numerical value in the **Connect timeout** text field by either typing in a numerical value or using the arrow keys in the text field.
  * Choose to either enable or disable HTTP pipelining by toggling **Enable HTTP pipelining** ON or OFF.&#x20;
    * If you enable this, you'll need to define a read timeout value by entering a numerical value in the **Read timeout** text field by either typing in a numerical value or using the arrow keys in the text field.
  * Choose to either enable or disable compression by toggling **Enable compression (gzip, deflate)** ON or OFF.&#x20;
  * **Configure your idle timeout settings**: defines the maximum time a connection will stay in the pool without being used in milliseconds. Once the timeout has elapsed, the unused connection will be closed, allowing to free the associated resources. To configure this, enter in a numerical value or using the arrow keys in the text field.
  * Choose to follow HTTP redirects or not: toggle **Follow HTTP redirects** ON or OFF.
  * Define the number of max concurrent connections: enter in a numerical value or using the arrow keys in the text field.
  * Choose to propagate client Accept-Encoding header: toggle **Propagate client Accept-Encoding header (no decompression if any)** ON or OFF.
  * Add HTTP headers: select **+ Add HTTP headers** to add headers that the Gateway should add or override before proxying the request to the backend API.
* **Define your Proxy options**
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
* **Define your SSL options**
* **Define your Key store**

### **Message-based endpoints**

If youse chose **Message** as your API architecture, you will be able to choose from the following endpoints:

* Endpoint Mock
* MQTT 5.X
* Kafka

Depending on which endpoint you choose, you will need to further define certain sets of endpoint configurations. Please see the tabs below to learn more about endpoint configuration per each available endpoint:&#x20;

{% tabs %}
{% tab title="Endpoint Mock" %}
The Endpoint Mock endpoint allows you to mock a backend service to emulate the behavior of a typical HTTP server and test processes. If you choose this endpoint, you will need to configure:

* **Interval between messages publication:** this defines the interval between published messages (in ms); the default is 1000
* **Content of published messages:** this defines the content of the message body that will be streamed; the default is "mock message"
* **Count of published messages:** this defines the specific limit of published messages as an integer that you want streamed as a part of the mocking; if not specified, there will be no limit
{% endtab %}

{% tab title="MQTT 5.X" %}
The **MQTT 5.X** endpoint allows the Gateway to open up a persistent connection and/or call a backend MQTT broker, as long as that broker is running on MQTT 5.x. This is done by the Gravitee Gateway setting up an MQTT client. If you choose this endpoint, you will need to configure:

* **How the Gateway will interact the broker:** you can tell the Gravitee Gateway's MQTT client to act as either a producer, a consumer, or both a producer and consumer. To do this, choose either **Use Consumer**, **Use Producer**, or **Use Consumer and Producer** from the drop-down menu. Here is an explanation of what each option will result in:
  * **Use Producer**: tells the Gateway MQTT client to be prepared to produce messages and send them to the MQTT broker that you will define as your endpoint
  * **Use Consumer**: tells the Gateway MQTT client to be prepared to consume messages from the MQTT broker that you will define as your endpoint
  * **Use Producer and Consumer**: tell the Gateway MQTT client to do both of the above
* **Define the Server host**: define the serverHost for the MQTT broker that you are using as your endpoint
* **Define the Server port**: define the serverPort for the MQTT broker that you are using as your endpoint
* **Define Reconnect attempts:** this sets the number of reconnect attemps that the Gateway will initiate if there is any kind of disconnecton between the Gateway MQTT client and the MQTT broker; the maximum is 10
* **Session expiry interval: t**his interval defines the period of time that the broker stores the session information of that particular MQTT client. When the session expiry interval is set to **0** or the CONNECT packet does not contain an expiry value, the session information is immediately removed from the broker as soon as the network connection of the client closes.
* **Enable or disable Clean start:** toggle **Clean start** ON or OFF to enable the **cleanStart** tag. This tag tells the MQTT broker to discard any previous session data and the Gateway MQTT client will start with a fresh session upon connection
* **Define initial security settings:** you will define more Gravitee Gateway-specific security settings later on, but this is where you will define your MQTT-specific authentication flow. Gravitee supports username and password using TLS. You will need to define:
  * Username
  * Password
* **Producer settings** (if you chose **Use Producer** or **Use Producer and Consumer** earlier on): this is where you define the settings that the Gravitee Gateway MQTT client will rely on for producing messages to your backend MQTT topic/broker. You will need to define:
  * Topic: the UTF-8 string that the broker uses to filter messages for each connected client. The topic consists of one or more topic levels. Each topic level is separated by a forward slash (topic level separator).&#x20;
  * **Retain settings**: define if the retain flag must be set for every published messages. The broker stores the last retained message. To define this, toggle **Retained** ON or OFF.
  * **Message expiry interval:** defines the period of time that the broker stores the PUBLISH message for any matching subscribers that are not currently connected. When no message expiry interval is set, the broker must store the message for matching subscribers indefinitely. When the retained=true option is set on the PUBLISH message, this interval also defines how long a message is retained on a topic.
  * **Response topic**: represents the topics on which the responses from the receivers of the message are expected
* **Consumer settings** (if you chose **Use Consumer** or **Use Producer and Consumer** earlier on): this is where you define the settings that the Gravitee Gateway MQTT client will rely on for consuming messages from your backend MQTT topic/broker. You will just need to define the **Topic** from which the Gateway MQTT client will consume messages.
{% endtab %}

{% tab title="Kafka" %}
The **Kafka** endpoint allows the Gateway to open up a persistent connection and/or call a backend Kafka broker. This is done by the Gravitee Gateway setting up a Kafka client. If you choose this endpoint, you will need to configure:

* **How the Gateway will interact the broker:** you can tell the Gravitee Gateway's Kafka client to act as either a producer, a consumer, or both a producer and consumer. To do this, choose either **Use Consumer**, **Use Producer**, or **Use Consumer and Producer** from the drop-down menu. Here is an explanation of what each option will result in:
  * **Use Producer**: tells the Gateway Kafka client to be prepared to produce messages and send them to the Kafka broker that you will define as your endpoint
  * **Use Consumer**: tells the Gateway Kafka client to be prepared to consume messages from the Kafka broker that you will define as your endpoint
  * **Use Producer and Consumer**: tell the Gateway Kafka client to do both of the above
* **Define the Bootstrap servers**: defines the list of host/port pairs, separated by a comma, to use for establishing the initial connection to the Kafka cluster. The client will make use of all servers irrespective of which servers are specified here for bootstrapping—this list only impacts the initial hosts used to discover the full set of servers.
* **Define initial security settings:** you will define more Gravitee Gateway-specific security settings later on, but this is where you will define your Kafka-specific authentication flow. Gravitee supports PLAINTEXT, SASL\_PLAINTEXT, SASL\_SSL, and SSL as protocols. Depending on which you choose, you will need to define:
  * **PLAINTEXT**: no further security config necessary
  * **SASL**
    * **SASL mechanism** used for client connections; this will either be GSSAPI, OAUTHBEARER, PLAIN, SCRAM\_SHA-256, or SCRAM-SHA-512
    * **SASL JAAS Config**: the JAAS login context parameters for SASL connections in the format used by JAAS configuration files.
  * **SASL\_SSL**
    * **SASL mechanism** used for client connections; this will either be GSSAPI, OAUTHBEARER, PLAIN, SCRAM\_SHA-256, or SCRAM-SHA-512
    * **SASL JAAS Config**: the JAAS login context parameters for SASL connections in the format used by JAAS configuration files.
      * SSL Configuration
        * **Truststore**: depending on your Truststore type, you will need to define:
          * **PEM with location**
            * Define the **location of your truststore file**
          * **PEM with certificates**
            * Define the trusted certificates in the format specified by 'ssl.truststore.type'
          * **JKS with location**
            * Define the **location of your truststore file**
            * Define the **SSL truststore password** for the truststore file
          * **JKS with certificates**
            * Define the trusted certificates in the format specified by 'ssl.truststore.type'
            * Define the **SSL truststore password** for the truststore file
          * **PKCS12 with location**
            * Define the **location of your truststore file**
            * Define the **SSL truststore password** for the truststore file
          * **PKCS12 with certificates**
            * Define the **trusted certificates** in the format specified by 'ssl.truststore.type'
            * Define the **SSL truststore password** for the truststore file
          * Keystore:
            * **PEM with location**
              * Define the **SSL keystore certificate chain**
              * Define the location of your keystore file
            * **PEM with Key**
              * **SSL keystore certificate chain**
              * Define the **SSL keystore private key** by defining the **Key** and the **Key password**
            * **JKS with location**
              * Define the **location of your keystore file**
              * Define the **SSL keystore password** for the keystore file
            * **JKS with Key**
              * Define the **SSL keystore private key** by defining the **Key** and the **Key password**
              * Define the **SSL keystore password** for the keystore file
            * **PKCS12 with location**
              * Define the **location of your keystore file**
              * Define the **SSL keystore password** for the keystore file
            * **PKCS12 with Key**
              * Define the **SSL keystore private key** by defining the **Key** and the **Key password**
              * Define the **SSL keystore password** for the keystore file
    * **SSL**
      * SSL Configuration
        * **Truststore**: depending on your Truststore type, you will need to define:
          * **PEM with location**
            * Define the **location of your truststore file**
          * **PEM with certificates**
            * Define the trusted certificates in the format specified by 'ssl.truststore.type'
          * **JKS with location**
            * Define the **location of your truststore file**
            * Define the **SSL truststore password** for the truststore file
          * **JKS with certificates**
            * Define the trusted certificates in the format specified by 'ssl.truststore.type'
            * Define the **SSL truststore password** for the truststore file
          * **PKCS12 with location**
            * Define the **location of your truststore file**
            * Define the **SSL truststore password** for the truststore file
          * **PKCS12 with certificates**
            * Define the **trusted certificates** in the format specified by 'ssl.truststore.type'
            * Define the **SSL truststore password** for the truststore file
          * Keystore:
            * **PEM with location**
              * Define the **SSL keystore certificate chain**
              * Define the location of your keystore file
            * **PEM with Key**
              * **SSL keystore certificate chain**
              * Define the **SSL keystore private key** by defining the **Key** and the **Key password**
            * **JKS with location**
              * Define the **location of your keystore file**
              * Define the **SSL keystore password** for the keystore file
            * **JKS with Key**
              * Define the **SSL keystore private key** by defining the **Key** and the **Key password**
              * Define the **SSL keystore password** for the keystore file
            * **PKCS12 with location**
              * Define the **location of your keystore file**
              * Define the **SSL keystore password** for the keystore file
            * **PKCS12 with Key**
              * Define the **SSL keystore private key** by defining the **Key** and the **Key password**
              * Define the **SSL keystore password** for the keystore file
* **Producer settings** (if you chose **Use Producer** or **Use Producer and Consumer** earlier on): this is where you define the settings that the Gravitee Gateway Kafka client will rely on for producing messages to your backend Kafka topic/broker. You will need to define:
  * **Topic**: the topic that the broker uses to filter messages for each connected client.
*   **Consumer settings** (if you chose **Use Consumer** or **Use Producer and Consumer** earlier on): this is where you define the settings that the Gravitee Gateway Kafka client will rely on for consuming messages from your backend Kafka topic/broker.&#x20;

    You will need to define:

    * **Topic**: the topic(s) from which your Gravitee Gateway client will consume messages
    * **Encode message Id:** Toggle this ON or OFF to allow encoding message ids in base64
    * **Auto offset reset:** You can use the **Auto offset reset** drop down to configure what happens when there is no itial offset in Kafka, or if the current offset does not exist on the server anymore. You have multiple options:
      * **Earliest**: automatically reset the offset to the earliest offset
      * **Latest**: automatically reset the offset to the latest offset
      * **None**: throw exception to the consumer if no previous offset is found for the consumer's group
      * **Anything else:** throw exception to the consumer.
{% endtab %}
{% endtabs %}

## Step 5: Security

## Step 6: Documentation
