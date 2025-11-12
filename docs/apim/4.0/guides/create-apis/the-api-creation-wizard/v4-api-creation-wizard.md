---
description: This article walks through how to use the Gravitee v4 API creation wizard
---

# v4 API creation wizard

{% @arcade/embed flowid="IoH5bZLjSO6ce8UbgMmc" url="https://app.arcade.software/share/IoH5bZLjSO6ce8UbgMmc" %}

## Introduction

The v4 API creation wizard makes it easy to create new Gateway APIs from scratch. The API creation wizard is comprised of several steps, each of which requires you to define certain sets of information:

* [API details](v4-api-creation-wizard.md#step-1-api-details)
* [Entrypoints](v4-api-creation-wizard.md#step-2-entrypoints)
* [Endpoints](v4-api-creation-wizard.md#step-3-endpoints)
* [Security](v4-api-creation-wizard.md#step-4-security)
* [Documentation](v4-api-creation-wizard.md#step-5-documentation)
* [Summary](v4-api-creation-wizard.md#step-6-summary)

## Step 1: API details

The API details step is where you can define a name, version number, and description for your API. The name and version number are required, but we also recommend giving your API a description so that it is more easily understood and managed by internal users.

<figure><img src="../../../.gitbook/assets/Screen Shot 2023-03-15 at 12.38.10 PM.png" alt=""><figcaption><p>Step 1: define your Gateway API's basic details.</p></figcaption></figure>

## Step 2: Entrypoints

### Choose your backend exposure method

The first part of the Entrypoints step is to choose how you want to expose your backend. As of today, Gravitee offers two options:

* **Proxy upstream protocol:** Use this method if you want to use Gravitee to proxy backend REST APIs, SOAP APIs, WebSocket Server, gRPC, or GraphQL. You will not be able to enforce policies at the message level.
* **Introspect messages from event-driven backend:** Use this method if you want to expose backend event brokers, such as Kafka and MQTT.

{% hint style="info" %}
The Gravitee documentation adopts concise terminology to differentiate between these API types:

**Proxy API:** An API created using **Proxy upstream protocol**

**Message API:** An API created using **Introspect messages from event-driven backend**
{% endhint %}

What you choose will dictate the kinds of entrypoints and endpoints that you can select later on. For more in-depth information on the exact support that these two methods offer, please [refer to this documentation](../#backend-exposure-methods).

<figure><img src="../../../.gitbook/assets/Screen Shot 2023-06-08 at 8.39.02 AM.png" alt=""><figcaption><p>v4 API creation wizard: select how you want your backend service exposed</p></figcaption></figure>

After you choose your method of exposure, select **Select my API architecture,** and you'll be taken to the entrypoint selection screen. Please read the following content to learn more about entrypoint selection and configuration, based on your selected exposure method.

### Entrypoint options for the "Proxy upstream protocol" method

If you chose **Proxy upstream protocol**, the Entrypoints step will require you to define a context path and decide whether or not you want to enable virtual hosts. The context path is the URL of your API. Please note that the context path must start with a '/' and can only contain uppercase letters, numbers, dashes or underscores.

If you select :heavy\_check\_mark:**Enable virtual hosts**, you'll have to define the following in addition to your context path:

* **Virtual host:** the host that must be set in the HTTP request to access your entrypoint.
* **Override access:** override the access URL of your Portal using a virtual host.
  * To enable or disable this, toggle **Enable** ON or OFF.

To disable virtual hosts, select **X Disable virtual hosts**.

<figure><img src="../../../.gitbook/assets/HTTP proxy entrypoints.gif" alt=""><figcaption><p>HTTP-Proxy entrypoints</p></figcaption></figure>

### Entrypoint options for the "Introspect messages from Event-driven backend" method

{% hint style="warning" %}
**Enterprise only**

As of Gravitee 4.0, the ability to create APIs with message API entrypoints is an Enterprise Edition capability. To learn more about Gravitee Enterprise, and what's included in various enterprise packages, please:

* [Refer to the EE vs OSS documentation](../../../overview/ee-vs-oss/)
* [Book a demo](https://app.gitbook.com/o/8qli0UVuPJ39JJdq9ebZ/s/rYZ7tzkLjFVST6ex6Jid/)
* [Check out the pricing page](https://www.gravitee.io/pricing)
{% endhint %}

If you chose **Introspect messages from Event-driven backend**, you are presented with a much different set of entrypoint options:

* **HTTP GET:** allows you to front a chosen backend or data source with a Gateway REST API with support for the HTTP GET request.
* **HTTP POST:** allows you to front a chosen backend or data source with a Gateway REST API with support for the HTTP POST request.
* **Server-sent Events:** allows you to front a chosen backend or data source with a Gateway SSE API for unidirectional communication between server and client.
* **Webhook**: allows you to front a chosen backend or data source with a Gateway Webhook API. This allows consumers to subscribe to the Gravitee Gateway via Webhook and then retrieve streamed data in real-time from a backend data source, via the Gateway, over the consumer's Webhook callback URL.
* **WebSocket**: allows you to front a chosen backend or data source with a Gateway WebSocket API. This allows a consumer to retrieve and send streamed events and messages in real-time.

<figure><img src="../../../.gitbook/assets/Screen Shot 2023-06-08 at 8.44.08 AM.png" alt=""><figcaption><p>v4 API creation wizard: event-driven backend entrypoints</p></figcaption></figure>

Once you select your entrypoints from the entrypoints page, additional configuration is required. The following sections outline the necessary configuration per entrypoint.

<details>

<summary>Server-sent Events</summary>

If you chose **SSE** as an entrypoint, you will be brought to a page where you can configure:

* **Context path:** the URL of your API. For example, if your URL is `[https://apim-master-gateway.team-apim.gravitee.dev/myAPI]`, then `[/myAPI]` is the context path.
* **Virtual hosts:** enabling virtual hosts requires you to define your **virtual host** and optionally enable **override access**.
* **SSE characteristics and permissions**
  * **Heartbeat intervals:** define the interval in which heartbeats are sent to the client by entering a numeric value into the **Define the interval in which heartbeats** **are sent to client** text field or by using the arrow keys. Intervals must be greater than or equal to 2000ms. Each heartbeat will be sent as an empty comment: `''`.
  * Choose to allow or disallow sending message metadata to the client as SSE comments by toggling **Allow sending messages metadata to client as SSE comments** ON or OFF.
  * Choose to allow or disallow sending message headers to the client as SSE comments by toggling **Allow sending messages headers to client as SSE comments** ON or OFF.

</details>

<details>

<summary>Webhook</summary>

If you chose **Webhook** as an entrypoint, you will be brought to a page where you can configure:

* **HTTP Options**
  * **Connect timeout:** the maximum time, in milliseconds, to connect to the Webhook. Either enter a numeric value or use the arrows to the right of the text field.
  * **Read timeout:** the maximum time, in milliseconds, allotted for the Webhook to complete the request (including response). Either enter a numeric value or use the arrows to the right of the text field.
  * **Idle timeout:** the maximum time, in milliseconds, a connection will stay in the pool without being used. Once this time has elapsed, the unused connection will be closed, freeing the associated resources. Either enter a numeric value or use the arrows to the right of the text field.
* **Proxy options**
  * Choose whether to use a proxy for client connections by toggling **Use proxy** ON or OFF. If enabled, you will need to select from the proxy types in the **Proxy type** drop-down:
    * HTTP proxy
    * SOCKS4
    * SOCKS5
  * Choose whether to use the proxy configured at system level by toggling **Use system proxy** ON or OFF. If enabled, you will need to define:
    * Proxy host: enter your proxy host in the **Proxy host** text field.
    * Proxy port: enter your proxy port in the **Proxy port** text field.
    * (Optional) Proxy username: enter your proxy username in the **Proxy username** text field.
    * (Optional) Proxy password: enter your proxy password in the **Proxy password** text field.

A [**SOCKS proxy**](https://hailbytes.com/how-to-use-socks4-and-socks5-proxy-servers-for-anonymous-web-browsing/) is a type of proxy server that uses the SOCKS protocol to tunnel traffic through an intermediary server.

Also, when using Webhooks as an entrypoint, you can set up a dead letter queue for storing undelivered messages. When configuring DLQ with Webhook, you redirect all the messages that the Webhook rejects to another location, such as a Kafka topic. To learn more, please refer to he DLQ documentation.

</details>

<details>

<summary>WebSocket</summary>

If you chose **WebSocket** as an entrypoint, you will be brought to a page where you can configure:

* **Context path:** the URL of your API. For example, if your URL is `[https://apim-master-gateway.team-apim.gravitee.dev/myAPI]`, then `[/myAPI]` is the context path.
* **Virtual hosts:** enabling virtual hosts requires you to define your **virtual host** and optionally enable **override access**.
* **WebSocket configuration**
  * **Publisher configuration:** choose to either enable or disable the publication capability by toggling **Enable the publication capability** ON or OFF. Disabling it assumes that the application will never be able to publish any message.
  * **Subscriber configuration:** choose to enable or disable the subscription capability by toggling **Enable the subscription capability** ON or OFF. Disabling it assumes that the application will never receive any message.

</details>

<details>

<summary>HTTP POST</summary>

If you chose **HTTP POST** as an entrypoint, you will be brought to a page where you can configure:

* **Context path:** the URL of your API. For example, if your URL is `[https://apim-master-gateway.team-apim.gravitee.dev/myAPI]`, then `[/myAPI]` is the context path.
* **Virtual hosts:** enabling virtual hosts requires you to define your **virtual host** and optionally enable **override access**.
* **HTTP POST permissions:** allow or disallow add request Headers to the generated message by toggling **Allow add request Headers to the generated message** ON or OFF.

</details>

<details>

<summary>HTTP GET</summary>

If you chose **HTTP GET** as an entrypoint, you will be brought to a page where you can configure:

* **Context path:** the URL of your API. For example, if your URL is `[https://apim-master-gateway.team-apim.gravitee.dev/myAPI]`, then `[/myAPI]` is the context path.
* **Virtual hosts:** enabling virtual hosts requires you to define your **virtual host** and optionally enable **override access**.
* **HTTP GET characteristics**
  * **Limit messages count:** defines the maximum number of messages to retrieve via HTTP GET. The default is 500. To set a custom limit, enter a numeric value in the **Limit messages count** text field.
  * **Limit messages duration:** defines the maximum duration, in milliseconds, to wait to retrieve the expected number of messages (See **Limit messages count**). The effective number of retrieved messages could be less than expected if maximum duration is reached before all messages are retrieved. To set a custom limit, enter a numeric value in the **Limit messages duration** text field.
  * **HTTP GET permissions:** allow or disallow **Allow sending messages headers to client in payload** and **Allow sending messages metadata to client in payload** by toggling these actions ON or OFF.

</details>

## Step 3: Endpoints

Gateway endpoints define the protocol and configuration by which the Gateway API will fetch data from or post data to the backend API. Your endpoints will be dictated by the API architecture that you selected earlier.

### HTTP Proxy endpoints

If you chose the HTTP Proxy option, your endpoint will be an HTTP Proxy. To configure this endpoint, you will be brought to a page where you can:

* **Define your target URL:** enter your target URL in the **Target URL** text field.
* **Define your HTTP options:**
  * Choose to either allow or disallow h2c clear text upgrade by toggling **Allow h2c Clear Text Upgrade** ON or OFF.
    * You'll need to select the HTTP protocol version to use. HTTP/1.1 and HTTP/2 are supported.
  * Choose to either enable or disable keep-alive by toggling **Enable keep-alive** ON or OFF.
    * If enabled, you'll need to define a numeric timeout value in the **Connect timeout** text field by either entering a numerical value or using the arrow keys.
  * Choose to either enable or disable HTTP pipelining by toggling **Enable HTTP pipelining** ON or OFF.
    * If enabled, you'll need to define a numeric timeout value in the **Read timeout** text field by either entering a numerical value or using the arrow keys.
  * Choose to either enable or disable compression by toggling **Enable compression (gzip, deflate)** ON or OFF.
  * **Configure your idle timeout settings:** define, in milliseconds, the maximum time a connection will stay in the pool without being used by entering a numeric value or using the arrow keys in the text field. Once the specified time has elapsed, the unused connection will be closed, freeing the associated resources.
  * Choose whether to follow HTTP redirects by toggling **Follow HTTP redirects** ON or OFF.
  * Define the number of max concurrent connections by entering a numeric value or using the arrow keys in the text field.
  * Choose to propagate client Accept-Encoding header by toggling **Propagate client Accept-Encoding header (no decompression if any)** ON or OFF.
  * Select **+ Add HTTP headers** to add headers that the Gateway should add or override before proxying the request to the backend API.
* **Define your Proxy options:**
  * Choose whether to use a proxy for client connections by toggling **Use proxy** ON of OFF.
    * If enabled, you will need to select from the proxy types in the **Proxy type** drop-down:
      * HTTP proxy
      * SOCKS4
      * SOCKS5
  * **Use system proxy:** choose whether to use the proxy configured at system level. If enabled, you'll need to define the following:
    * Proxy host: enter your proxy host in the **Proxy host** text field.
    * Proxy port: enter your proxy port in the **Proxy port** text field.
    * (Optional) Proxy username: enter your proxy username in the **Proxy username** text field.
    * (Optional) Proxy password: enter your proxy password in the **Proxy password** text field.
* **Define your SSL options**
* **Define your Key store**

### **Introspect messages from event-driven backend endpoints**

{% hint style="warning" %}
**Enterprise only**

As of Gravitee 4.0, the ability to create APIs with message API endpoints is an Enterprise Edition capability. To learn more about Gravitee Enterprise, and what's included in various enterprise packages, please:

* [Refer to the EE vs OSS documentation](../../../overview/ee-vs-oss/)
* [Book a demo](https://app.gitbook.com/o/8qli0UVuPJ39JJdq9ebZ/s/rYZ7tzkLjFVST6ex6Jid/)
* [Check out the pricing page](https://www.gravitee.io/pricing)
{% endhint %}

If you chose **Introspect messages from event-driven backend** as your exposure method, you will be able to choose from the following endpoints:

* Endpoint Mock
* MQTT 5.X
* Kafka
* RabbitMQ
* Solace

Depending on which endpoint you choose, you will need to further define certain sets of endpoint configurations. Please see the expandable sections below to learn more about the endpoint configuration of each available endpoint.

<details>

<summary>Endpoint Mock</summary>

The Endpoint Mock endpoint allows you to mock a backend service to emulate the behavior of a typical HTTP server and test processes. If you chose this endpoint, you will need to configure:

* **Interval between messages publication:** defines, in milliseconds, the interval between published messages. The default is 1000.
* **Content of published messages:** defines the content of the message body that will be streamed. The default is "mock message".
* **Count of published messages:** defines, as an integer, the maximum number of published messages that are streamed as a part of the mocking. If left unspecified, there will be no limit.

</details>

<details>

<summary>MQTT 5.X</summary>

The **MQTT 5.X** endpoint allows the Gateway to open up a persistent connection and/or call a backend MQTT broker, as long as that broker is running on MQTT 5.x, via an MQTT client set up by the Gravitee Gateway. If you chose this endpoint, you will need to configure:

* How the Gateway will interact the broker by instructing the Gravitee Gateway's MQTT client to act as either a producer, a consumer, or both a producer and consumer. Choose either **Use Consumer**, **Use Producer**, or **Use Consumer and Producer** from the drop-down menu to do one of the following:
  * **Use Producer:** tells the Gateway MQTT client to be prepared to produce messages and send them to the MQTT broker that you define as your endpoint.
  * **Use Consumer:** tells the Gateway MQTT client to be prepared to consume messages from the MQTT broker that you define as your endpoint.
  * **Use Producer and Consumer**: tell the Gateway MQTT client to both **Use Producer** and **Use Consumer**.
* **Server host:** define the serverHost for the MQTT broker that you are using as your endpoint.
* **Server port:** define the serverPort for the MQTT broker that you are using as your endpoint.
* **Reconnect attempts:** specify an integer number of reconnect attempts that the Gateway will initiate if the Gateway MQTT client disconnects from the MQTT broker. The maximum is 10.
* **Session expiry interval:** defines the period of time that the broker stores the session information of that particular MQTT client. When the session expiry interval is set to **0** or the CONNECT packet does not contain an expiry value, the session information is immediately removed from the broker when the client network connection closes.
* **Clean start:** toggle **Clean start** ON or OFF to enable or disable the **cleanStart** tag. This tag causes the MQTT broker to discard any previous session data and the Gateway MQTT client to connect with a fresh session.
* **Initial security settings:** you will define more Gravitee Gateway-specific security settings later on, but this is where you define your MQTT-specific authentication flow. Gravitee supports username and password using TLS. You will need to define:
  * Username
  * Password
* **Producer settings** (if you chose **Use Producer** or **Use Producer and Consumer**): define the settings that the Gravitee Gateway MQTT client will rely on for producing messages to your backend MQTT topic/broker. You will need to specify:
  * **Topic:** the UTF-8 string that the broker uses to filter messages for each connected client. The topic consists of one or more topic levels. Each topic level is separated by a forward slash (topic level separator).
  * **Retain settings:** whether the retain flag must be set for every published message by toggling **Retained** ON or OFF. If enabled, the broker stores the last retained message.
  * **Message expiry interval:** defines the period of time that the broker stores the PUBLISH message for any matching subscribers that are not currently connected. When no message expiry interval is set, the broker must store the message for matching subscribers indefinitely. When the "retained=true" option is set on the PUBLISH message, this interval also defines how long a message is retained on a topic.
  * **Response topic:** represents the topics on which the responses from the message receivers are expected.
* **Consumer settings** (if you chose **Use Consumer** or **Use Producer and Consumer**): define the settings that the Gravitee Gateway MQTT client will rely on for consuming messages from your backend MQTT topic/broker. You must define the **Topic** from which the Gateway MQTT client will consume messages.

</details>

<details>

<summary>Kafka</summary>

The **Kafka** endpoint allows the Gateway to open up a persistent connection and/or call a backend Kafka broker via a Kafka client set up by the Gravitee Gateway. If you chose this endpoint, you will need to configure:

* How the Gateway will interact the broker by instructing the Gravitee Gateway's Kafka client to act as either a producer, a consumer, or both a producer and consumer. Choose either **Use Consumer**, **Use Producer**, or **Use Consumer and Producer** from the drop-down menu to do one of the following:
  * **Use Producer:** tells the Gateway Kafka client to be prepared to produce messages and send them to the Kafka broker that you define as your endpoint
  * **Use Consumer:** tells the Gateway Kafka client to be prepared to consume messages from the Kafka broker that you define as your endpoint
  * **Use Producer and Consumer:** tell the Gateway Kafka client to both **Use Producer** and **Use Consumer**
* **Bootstrap servers:** define the comma-separated list of host/port pairs to use for establishing the initial connection to the Kafka cluster. The client will make use of all servers irrespective of which servers the list designates for bootstrapping - this list only pertains to the initial hosts used to discover the full set of servers.
* **Initial security settings:** you will define more Gravitee Gateway-specific security settings later on, but this is where you define your Kafka-specific authentication flow. Gravitee supports PLAINTEXT, SASL\_PLAINTEXT, SASL\_SSL, and SSL as protocols. Depending on which you choose, you will need to define:
  * **PLAINTEXT:** no further security config necessary.
  * **SASL**
    * **SASL mechanism:** used for client connections. This will be GSSAPI, OAUTHBEARER, PLAIN, SCRAM\_SHA-256, or SCRAM-SHA-512.
    * **SASL JAAS Config:** the JAAS login context parameters for SASL connections in the format used by JAAS configuration files.
  * **SSL**
    * **Truststore:** depending on your truststore type, you will need to define:
      * **PEM with location**
        * Define the **location of your truststore file**.
      * **PEM with certificates**
        * Define the trusted certificates in the format specified by 'ssl.truststore.type'.
      * **JKS with location**
        * Define the **location of your truststore file**.
        * Define the **SSL truststore password** for the truststore file.
      * **JKS with certificates**
        * Define the trusted certificates in the format specified by 'ssl.truststore.type'.
        * Define the **SSL truststore password** for the truststore file.
      * **PKCS12 with location**
        * Define the **location of your truststore file**.
        * Define the **SSL truststore password** for the truststore file.
      * **PKCS12 with certificates**
        * Define the **trusted certificates** in the format specified by 'ssl.truststore.type'.
        * Define the **SSL truststore password** for the truststore file.
    * **Keystore:**
      * **PEM with location**
        * Define the **SSL keystore certificate chain**.
        * Define the location of your keystore file.
      * **PEM with Key**
        * Define the **SSL keystore certificate chain**.
        * Define the **SSL keystore private key** by defining the **Key** and the **Key password**.
      * **JKS with location**
        * Define the **location of your keystore file**.
        * Define the **SSL keystore password** for the keystore file.
      * **JKS with Key**
        * Define the **SSL keystore private key** by defining the **Key** and the **Key password**.
        * Define the **SSL keystore password** for the keystore file.
      * **PKCS12 with location**
        * Define the **location of your keystore file**.
        * Define the **SSL keystore password** for the keystore file.
      * **PKCS12 with Key**
        * Define the **SSL keystore private key** by defining the **Key** and the **Key password**.
        * Define the **SSL keystore password** for the keystore file.
* **Producer settings** (if you chose **Use Producer** or **Use Producer and Consumer**): define the settings that the Gravitee Gateway Kafka client will rely on for producing messages to your backend Kafka topic/broker. You will need to define:
  * **Topic:** the topic that the broker uses to filter messages for each connected client.
* **Consumer settings** (if you chose **Use Consumer** or **Use Producer and Consumer**): define the settings that the Gravitee Gateway Kafka client will rely on for consuming messages from your backend Kafka topic/broker. You will need to define:
  * **Topic:** the topic(s) from which your Gravitee Gateway client will consume messages.
  * **Encode message Id:** Toggle this ON or OFF to encode message IDs in base64.
  * **Auto offset reset:** Use the **Auto offset reset** drop-down menu to configure what happens when there is no initial offset in Kafka, or if the current offset no longer exists on the server:
    * **Earliest:** automatically reset the offset to the earliest offset.
    * **Latest:** automatically reset the offset to the latest offset.
    * **None:** throw an exception to the consumer if no previous offset is found for the consumer's group.
    * **Anything else:** throw an exception to the consumer.

**Recovering Kafka messages**

Kafka messages are acknowledged automatically or manually by the consumer to avoid consuming messages multiple times. To read previous messages requires specifying the offset at which the Kafka consumer should start consuming records and the entrypoint must support the **at-least-one** or **at-most-one** QoS.

As an example using SSE as an entrypoint, first define the QoS for the entrypoint:

```
"entrypoints": [
        {
            "type": "sse",
            "qos": "at-least-once",
            "configuration": {
                "heartbeatIntervalInMs": 5000,
                "metadataAsComment": true,
                "headersAsComment": true
            }
        }
    ]
```

The offset information provided during the Gateway connection must be encoded in base64. It can be passed in plain text by setting the `encodeMessageId` to **false** in the consumer configuration of the Kafka plugin.

The offset information has to respect the convention `<topicName>@<partition-id>#<offset>`

If the Kafka endpoint manages multiple topics or partitions, you can define multiple offsets using the following convention with a semicolon as the separator:

```
topic1@0#1
topic1@0#1;anotherTopic@1#10
```

Next, initiate SSE consumption by providing the offsets via the `Last-Event-ID` header:

```bash
# generate the Last-Event-ID
LAST_ID=$(echo -n "demo1@0#0" | base64)
# Start the SSE event stream
curl http://localhost:8082/demo/sse/kafka-advanced/plaintext \n 
    -H'Accept: text/event-stream' \n
    -H"Last-Event-ID: ${LAST_ID}" 
```

For the HTTP-GET entrypoint, the offset must be provided using the `cursor` query parameter `curl http://localhost:8082/messages/get?cursor=${LAST_ID}`

</details>

<details>

<summary>Solace</summary>

Choosing the **Solace** endpoint enables the Gravitee Gateway to create an API that exposes Solace resources and event APIs via your chosen Gravitee entrypoint(s). You will need to configure:

* **URL:** Your Solace broker's URL
* **VPN name**
* **Producer settings** (if you chose **Use Producer** or **Use Producer and Consumer**): Define the settings that the Gravitee Gateway Solace client will rely on for producing messages to your backend Solace topic/broker. You will need to specify:
  * **Topic:** The UTF-8 string that the broker uses to filter messages for each connected client. The topic consists of one or more topic levels. Each topic level is separated by a forward slash (topic level separator).
  * **Retain settings:** Whether the retain flag must be set for every published message by toggling **Retained** ON or OFF. If enabled, the broker stores the last retained message.
  * **Message expiry interval:** Defines the period of time that the broker stores the PUBLISH message for any matching subscribers that are not currently connected. When no message expiry interval is set, the broker must store the message for matching subscribers indefinitely. When the `retained=true` option is set on the PUBLISH message, this interval also defines how long a message is retained on a topic.
  * **Response topic:** Represents the topics on which the responses from the message receivers are expected.
* **Consumer settings** (if you chose **Use Consumer** or **Use Producer and Consumer**): Define the settings that the Gravitee Gateway Solace client will rely on to consume messages from your backend Solace topic/broker.
  * Define the **Topic** from which the Gateway Solace client will consume messages.
  * Toggle Authentication configuration ON or OFF. When OFF, no further configuration is necessary. When ON, you will need to:
    * Define the username used for authentication.
    * Define the password used for authentication.

</details>

<details>

<summary>RabbitMQ</summary>

The **RabbitMQ** endpoint allows the Gateway to open up a persistent connection and/or call a backend RabbitMQ resource, as long as that RabbitMQ resource communicates over AMQP 0-9-1 protocol. If you choose this endpoint, you will need to configure the following:

* **Server host:** define the host of your RabbitMQ resource
* **Server port**: define the port that RabbitMQ is using
* How the Gateway will interact with RabbitMQ by instructing the Gravitee Gateway to act as either a producer, a consumer, or both a producer and consumer. Choose either **Use Consumer**, **Use Producer**, or **Use Consumer and Producer** from the drop-down menu to do one of the following:
  * **Use Producer:** tells the Gateway Gateway to be prepared to produce messages and send them to RabbitMQ that you define as your endpoint
  * **Use Consumer:** tells the Gateway to be prepared to consume messages from RabbitMQ that you define as your endpoint
  * **Use Producer and Consumer:** tell the Gateway to be able to use both **Use Producer** and **Use Consumer** settings
* **Authentication:** define the **userna**me and **password** for RabbitMQ authentication
* **Producer settings** (if you chose **Use Producer** or **Use Producer and Consumer**): define the settings that the Gravitee Gateway Kafka client will rely on for producing messages to your backend Kafka topic/broker. You will need to define:
  * **Exchange name**
  * **Exchange type**
  * Enable or disable **Durable**
  * Enable or disable **Auto Delete**
  * **Routing Key**

- **Consumer settings** (if you chose **Use Consumer** or **Use Producer and Consumer**): define the settings that the Gravitee Gateway Kafka client will rely on for consuming messages from your backend Kafka topic/broker. You will need to define:
  * **Exchange name**
  * **Exchange type**
  * Enable or disable [**Durable**](https://www.rabbitmq.com/tutorials/amqp-concepts.html#exchanges)**:** Durable exchanges survive broker restart
  * Enable or disable [**Auto Delete**](https://www.rabbitmq.com/tutorials/amqp-concepts.html#exchanges)**:** exchange is deleted when last queue is unbound from it
  * **Routing Key**

</details>

## Step 4: Security

Next in the API creation wizard is the Security step, where you will configure:

* **Plan information**: Define a plan that provides the API producer with a method to secure, monitor, and transparently communicate details around access.
* **Configuration**: Define authorization resources, such as Gravitee AM or another OAuth2 resource.
* **Limitations**: Define access limitations, such as rate limiting and quotas.

### Plan information

A plan is essentially an access layer around an API that provides the API producer with a method to secure, monitor, and transparently communicate details around access. If you want to learn more about how plans function in Gravitee, please refer to the [plans documentation](docs/apim/4.0/guides/api-exposure-plans-applications-and-subscriptions/plans.md). You will be able to choose between several different plan types:

* **OAuth2**: A standard designed to allow a website or application to access resources hosted by other web apps on behalf of a user.
* **JWT**: An open standard that defines a compact and URL-safe way to securely transmit information as a JSON object between parties.
* **API Key:** A plan where the API Gateway will reject calls from consumers that aren't able to pass the right API key in their request.
* **Keyless**: A plan that results in no added security via plan configuration. This is considered an "Open" plan.
* **Push plan**: A plan that provides an access layer for the Gateway pushing data to consumers. This is used for subscribers.

<figure><img src="../../../.gitbook/assets/Screen Shot 2023-06-01 at 12.14.02 PM.png" alt=""><figcaption><p>API creation wizard: different Security plan types</p></figcaption></figure>

Depending on which plan you select, the configuration will differ. Please see the expandable sections below to learn more about how to configure each of the different plans.

<details>

<summary>OAuth2 plan</summary>

To configure your OAuth2 plan, select OAuth2 from the **+Add plan** drop-down menu, then define general details, settings, and restrictions. On the **General** screen, define:

* **Name**
* **Description**
* **Characteristics**
* **Subscription:** choose whether to auto-validate subscriptions, require a message from a consumer during subscription, and/or present a message to the consumer upon subscription.
* **Access control:** select any Groups within APIM that you do not want to have access to this API. For more information on Groups, refer to the [Groups documentation](../../administration/#users-and-user-groups).

<img src="../../../.gitbook/assets/image (37).png" alt="" data-size="original">

Select Next to move on to **OAuth2 authentication configuration**. Here, you'll specify:

* Your OAuth2 resource in the **OAuth2 resource** field. This should be the resource that you'll use to validate the token.
* Your cache resource in the **Cache resource** field. This should be the cache resource that you will use to store the tokens.
* (Optional) **Extract an OAuth2 payload:** pushes the token endpoint payload into the oauth.payload context attribute.
* (Optional) **Check scopes:** instructs your authentication method to check required scopes in order to access the resource. If you choose to check scopes, you must define your list of required scopes using the **Required scopes** module.
* Whether strict mode is enabled or disabled. If you choose **Strict**, scopes will be checked against the exact list you provided in the **Required scopes** section.
* Whether to permit authorization headers to target endpoints.
* (Optional) Define additional selection rules. If you are managing multiple plans that share the same type, this will help the plan selection process. You will need to use the Gravitee Expression Language. For more information on the Gravitee Expression Language, please refer to the Expression Language documentation.

<img src="../../../.gitbook/assets/image (51).png" alt="" data-size="original">

Select Next to define any additional restrictions for the plan. These restrictions include:

* **Rate limiting:** specify the maximum number of requests that an application can make within a given number of seconds or minutes, then:
  * Enable or disable **Non-strict mode**: this enables rate limiting to be applied in an asynchronous manner, which results in the distributed counter value not being strict.
  * Enable or disable **Add response headers**.
  * Define your rate limit's **Key**.
  * Define the **max request count** (this can be a static or dynamic count).
  * Define the **time duration** (e.g., a one-second time interval within which to apply the request limitation).
* **Quota:** define a rate limit over a period of hours, days, or months. If you choose this, you will need to define the same settings that are applicable to rate limiting (see above).
* **Resource filtering:** restricts resources based on defined whitelist/allowed and/or blacklist/disallowed settings. These will be defined by path patterns and methods.

<img src="../../../.gitbook/assets/image (43).png" alt="" data-size="original">

</details>

<details>

<summary>JWT plan</summary>

If you chose **JWT**, you will need to specify general details, the authentication configuration, and restrictions. On the **General** screen, define:

* **Name**
* **Description**
* **Characteristics**
* **Subscription:** choose whether to auto-validate subscriptions, require a message from a consumer during subscription, and/or present a message to the consumer upon subscription.
* **Access control:** select any Groups within APIM that you do not want to have access to this API. For more information on Groups, refer to the [Groups documentation](../../administration/#users-and-user-groups).

Once you're done with your general details, select Next to define your JWT authentication configuration. This will require you to:

* Choose a **Signature** to define how your JWT token must be signed. The options are:
  * RSA\_RS256
  * RSA\_RS384
  * RSA\_RS512
  * HMAC\_HS512
  * HMAC\_HS384
  * HMAC\_HS384
* Define your **JWKS resolver**. This defines how your JSON Web Key Set is retrieved.
* Define your Resolver parameter **(secrets must be base-64 encoded)**.
* Choose whether to use a system proxy.
* Choose whether to enable extra JWT claims.
* Choose whether to propagate Authorization headers.
* Define the User claim where users can be extracted.
* Define the Client Id claim where the client can be extracted.
* Define additional selection rules using the Gravitee Expression Language.

Select Next to define any restrictions associated with this plan. Your options include:

* **Rate limiting:** specify the maximum number of requests that an application can make within a given number of seconds or minutes, then:
  * Enable or disable **Non-strict mode**: this enables rate limiting to be applied in an asynchronous manner, which results in the distributed counter value not being strict.
  * Enable or disable **Add response headers**.
  * Define your rate limit's **Key**.
  * Define the **max request count** (this can be a static or dynamic count).
  * Define the **time duration** (e.g., a one-second time interval within which to apply the request limitation).
* **Quota:** define a rate limit over a period of hours, days, or months. If you choose this, you will need to define the same settings that are applicable to rate limiting (see above).
* **Resource filtering:** restricts resources based on defined whitelist/allowed and/or blacklist/disallowed settings. These will be defined by path patterns and methods.

<img src="../../../.gitbook/assets/image (44).png" alt="" data-size="original">

</details>

<details>

<summary>API key</summary>

If you chose API key, you will define general settings, the API key authentication configuration, and restrictions. On the **General** screen, define:

* **Name**
* **Description**
* **Characteristics**
* **Subscription:** choose whether to auto-validate subscriptions, require a message from a consumer during subscription, and/or present a message to the consumer upon subscription.
* **Access control:** select any Groups within APIM that you do not want to have access to this API. For more information on Groups, refer to the [Groups documentation](../../administration/#users-and-user-groups).

Select Next to be taken to the **API key authentication** configuration page. Here, you need to:

* Choose whether to propagate your API key to upstream APIs.
* Define any additional selection rules using the Gravitee Expression Language.

Select Next to be taken to the **Restriction** page to define any additional restrictions that you want to be associated with your plan. Your options include:

* **Rate limiting:** specify the maximum number of requests that an application can make within a given number of seconds or minutes, then:
  * Enable or disable **Non-strict mode**: this enables rate limiting to be applied in an asynchronous manner, which results in the distributed counter value not being strict.
  * Enable or disable **Add response headers**.
  * Define your rate limit's **Key**.
  * Define the **max request count** (this can be a static or dynamic count).
  * Define the **time duration** (e.g., a one-second time interval within which to apply the request limitation).
* **Quota:** define a rate limit over a period of hours, days, or months. If you choose this, you will need to define the same settings that are applicable to rate limiting (see above).
* **Resource filtering:** restricts resources based on defined whitelist/allowed and/or blacklist/disallowed settings. These will be defined by path patterns and methods.

</details>

<details>

<summary>Keyless plan</summary>

If you chose Keyless, you will only need to define general details and restrictions, as there is no authentication to configure (unlike OAuth2, JWT, and API key). On the **General** screen, define:

* **Name**
* **Description**
* **Characteristics**
* **Subscription:** choose whether to auto-validate subscriptions, require a message from a consumer during subscription, and/or present a message to the consumer upon subscription.
* **Access control:** select any Groups within APIM that you do not want to have access to this API. For more information on Groups, refer to the [Groups documentation](../../administration/#users-and-user-groups).

Select Next to be taken to the **Restriction** page to define any additional restrictions that you want to be associated with your plan. Your options include:

* **Rate limiting:** specify the maximum number of requests that an application can make within a given number of seconds or minutes, then:
  * Enable or disable **Non-strict mode**: this enables rate limiting to be applied in an asynchronous manner, which results in the distributed counter value not being strict.
  * Enable or disable **Add response headers**.
  * Define your rate limit's **Key**.
  * Define the **max request count** (this can be a static or dynamic count).
  * Define the **time duration** (e.g., a one-second time interval within which to apply the request limitation).
* **Quota:** define a rate limit over a period of hours, days, or months. If you choose this, you will need to define the same settings that are applicable to rate limiting (see above).
* **Resource filtering:** restricts resources based on defined whitelist/allowed and/or blacklist/disallowed settings. These will be defined by path patterns and methods.

</details>

## Step 5: Documentation

The Documentation step is not currently supported for v4 APIs. This will be added in a future release.

## Step 6: Summary

The final step is to review and then create or deploy your API. Creating your API will create the API as a Gravitee artifact, but not deploy it to the Gateway. If you choose Deploy, the API will be created and deployed to the Gravitee Gateway.

{% hint style="success" %}
Once you create or deploy your API, you are done with the API creation process! At this point, we recommend learning how to further configure your API, and how to design and enforce policies that make your API more secure, reliable, efficient, etc.
{% endhint %}
