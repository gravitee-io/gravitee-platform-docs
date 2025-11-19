---
description: This article walks through how to configure v4 API endpoints
---

# Endpoint Configuration

## Introduction

In Gravitee, Gateway endpoints define the protocol and configuration settings by which the Gateway API will fetch data from, or post data to, the backend API.

After you've created your Gateway API and selected your endpoint(s), you can configure them on the **API** page of the Management Console. This article walks through the process for configuring v4 Message API endpoints and v4 Proxy API endpoints.

## Configure v4 message API endpoints

{% hint style="warning" %}
**Enterprise-only**

As of Gravitee 4.0, the ability to create APIs with message API endpoints is an Enterprise Edition capability. To learn more about Gravitee Enterprise Edition and what's included in various enterprise packages, please:

* [Refer to the EE vs OSS documentation](../../../overview/ee-vs-oss/README.md)
* [Book a demo](https://app.gitbook.com/o/8qli0UVuPJ39JJdq9ebZ/s/rYZ7tzkLjFVST6ex6Jid/)
* [Check out the pricing page](https://www.gravitee.io/pricing)
{% endhint %}

v4 APIs currently support the following endpoints:

* **Kafka**: Enables the Gravitee API Gateway to establish a persistent connection with a Kafka topic as a backend resource or target.
* **MQTT 5**: Enables the Gravitee API Gateway to establish a persistent connection with an MQTT topic as a backend resource or target.
* **RabbitMQ**: Enables the Gravitee API Gateway to establish a persistent connection with RabbitMQ as a backend resource or target. This will only work if you are using RabbitMQ and the AMQP 0-9-1 protocol. Because this endpoint supports the AMQP 0-9-1 protocol, it may support other event brokers and message queues that communicate over the AMQP 0-9-1 protocol. However, Gravitee does not guarantee or officially support these implementations.
* **Solace**: Enables the Gravitee API Gateway to establish a persistent connection with Solace as a backend resource or target.
* **Mock**: Enables the Gateway to simulate responses from a server for testing API implementations.

To access endpoint configuration, go to the **API** page in the Developer Portal and select your API. Then, under **Endpoints**, select **Backend services.**

Endpoint configuration may differ depending on which endpoint(s) your API utilizes. Please refer to the following sections for the configuration details of each specific endpoint.

<details>

<summary>Kafka</summary>

The **Kafka** endpoint allows the Gateway to open up a persistent connection to and/or call a backend Kafka broker via a Kafka client set up by the Gravitee Gateway. If you chose this endpoint, you will need to configure:

* How the Gateway will interact with the broker. This is done by instructing the Gravitee Gateway's Kafka client to act as a producer, a consumer, or both a producer and consumer via the drop-down menu:
  * **Use Producer:** Tells the Gateway Kafka client to be prepared to produce messages and send them to the Kafka broker that you define as your endpoint.
  * **Use Consumer:** Tells the Gateway Kafka client to be prepared to consume messages from the Kafka broker that you define as your endpoint.
  * **Use Producer and Consumer:** Tells the Gateway Kafka client to both **Use Producer** and **Use Consumer**.
* **Bootstrap servers:** Define the comma-separated list of host/port pairs used to establish the initial connection to the Kafka cluster. The list only pertains to the initial hosts used to discover the full set of servers. The client will make use of all backend servers irrespective of which servers the list designates for bootstrapping.
*   **Initial security settings:** Define your Kafka-specific authentication flow (you will define additional Gravitee Gateway-specific security settings later). Gravitee supports PLAINTEXT, SASL\_PLAINTEXT, SASL\_SSL, and SSL protocols. Depending on which you choose, you will need to define:

    **PLAINTEXT:** No further security configuration is necessary.

    **SASL**

    * **SASL mechanism:** Choose GSSAPI, OAUTHBEARER, PLAIN, SCRAM\_SHA-256, or SCRAM-SHA-512 for client connections.
    * **SASL JAAS Config:** The JAAS login context parameters for SASL connections in JAAS configuration file format.

    **SSL truststore:** Depending on your truststore type, you will need to define:

    * **PEM with location:** The location of your truststore file.
    * **PEM with certificates:** The trusted certificates, in the format specified by `ssl.truststore.type`.
    * **JKS with location:** The truststore file's location and SSL truststore password.
    * **JKS with certificates**
      * The trusted certificates, in the format specified by `ssl.truststore.type`.
      * The truststore file's SSL truststore password.
    * **PKCS12 with location:** The truststore file's location and SSL truststore password.
    * **PKCS12 with certificates**
      * The trusted certificates, in the format specified by `ssl.truststore.type`.
      * The truststore file's SSL truststore password.

    **SSL keystore:** Depending on your keystore type, you will need to define:

    * **PEM with location**
      * The SSL keystore certificate chain.
      * The location of the keystore file.
    * **PEM with Key**
      * The SSL keystore certificate chain.
      * The SSL keystore private key via defining the Key and the Key password.
    * **JKS with location**
      * The location of the keystore file.
      * The SSL keystore password for the keystore file.
    * **JKS with Key**
      * The SSL keystore private key via defining the Key and the Key password.
      * The SSL keystore password for the keystore file.
    * **PKCS12 with location**
      * The location of your keystore file.
      * The SSL keystore password for the keystore file.
    * **PKCS12 with Key**
      * The SSL keystore private key via defining the Key and the Key password.
      * The SSL keystore password for the keystore file.
* **Producer settings** (if you chose **Use Producer** or **Use Producer and Consumer**): Define the settings that the Gravitee Gateway Kafka client will rely on to produce messages to your backend Kafka topic/broker:
  * **Topic:** The topic that the broker uses to filter messages for each connected client.
* **Consumer settings** (if you chose **Use Consumer** or **Use Producer and Consumer**): Define the settings that the Gravitee Gateway Kafka client will rely on to consume messages from your backend Kafka topic/broker:
  * **Topic:** The topic(s) from which your Gravitee Gateway client will consume messages.
  * **Encode message Id:** Toggle this ON or OFF to encode message IDs in base64.
  * **Auto offset reset:** Use the **Auto offset reset** drop-down menu to configure what happens when there is no initial offset in Kafka, or if the current offset no longer exists on the server:
    * **Earliest:** Automatically reset the offset to the earliest offset.
    * **Latest:** Automatically reset the offset to the latest offset.
    * **None:** Throw an exception to the consumer if no previous offset is found for the consumer's group.
    * **Anything else:** Throw an exception to the consumer.

</details>

<details>

<summary>MQTT5</summary>

The **MQTT 5** endpoint allows the Gateway to open up a persistent connection to and/or call a backend MQTT broker, as long as that broker is running on MQTT 5.x via an MQTT client set up by the Gravitee Gateway. If you chose this endpoint, you will need to configure:

* How the Gateway will interact the broker. This is done by instructing the Gravitee Gateway's MQTT client to act as either a producer, a consumer, or both a producer and consumer via the drop-down menu:
  * **Use Producer:** Tells the Gateway MQTT client to be prepared to produce messages and send them to the MQTT broker that you define as your endpoint.
  * **Use Consumer:** Tells the Gateway MQTT client to be prepared to consume messages from the MQTT broker that you define as your endpoint.
  * **Use Producer and Consumer**: Tells the Gateway MQTT client to both **Use Producer** and **Use Consumer**.
* **Server host:** Define the serverHost for the MQTT broker that you are using as your endpoint.
* **Server port:** Define the serverPort for the MQTT broker that you are using as your endpoint.
* **Reconnect attempts:** Specify an integer number (max 10) of reconnect attempts that the Gateway will initiate if the Gateway MQTT client disconnects from the MQTT broker.
* **Session expiry interval:** Define the period of time that the broker stores the session information of that particular MQTT client. When the session expiry interval is set to 0 or the CONNECT packet does not contain an expiry value, the session information is immediately removed from the broker when the client network connection closes.
* **Clean start:** Toggle **Clean start** ON or OFF to enable or disable the **cleanStart** tag. This tag causes the MQTT broker to discard any previous session data and the Gateway MQTT client to connect with a fresh session.
* **Initial security settings:** Define your MQTT-specific authentication flow (you will define more Gravitee Gateway-specific security settings later). Gravitee uses TLS to support username and password. Define:
  * Username
  * Password
* **Producer settings** (if you chose **Use Producer** or **Use Producer and Consumer**): Define the settings that the Gravitee Gateway MQTT client will rely on to produce messages to your backend MQTT topic/broker:
  * **Topic:** The UTF-8 string that the broker uses to filter messages for each connected client. The topic consists of one or more topic levels. Each topic level is separated by a forward slash (topic level separator).
  * **Retain settings:** Whether the retain flag must be set for every published message by toggling **Retained** ON or OFF. If enabled, the broker stores the last retained message.
  * **Message expiry interval:** Define the period of time that the broker stores the PUBLISH message for any matching subscribers that are not currently connected. When no message expiry interval is set, the broker must store the message for matching subscribers indefinitely. When the `retained=true` option is set on the PUBLISH message, the message expiry interval defines how long a message is retained on a topic.
  * **Response topic:** Define the topics on which the responses from the message receivers are expected.
* **Consumer settings** (if you chose **Use Consumer** or **Use Producer and Consumer**): Define the settings that the Gravitee Gateway MQTT client will rely on to consume messages from your backend MQTT topic/broker. You must define the **Topic** from which the Gateway MQTT client will consume messages.

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

The **RabbitMQ** endpoint allows the Gateway to open up a persistent connection to and/or call a backend RabbitMQ resource, as long as that RabbitMQ resource communicates over the AMQP 0-9-1 protocol. If you chose this endpoint, you will need to configure the following:

* **Server host:** Define the host of your RabbitMQ resource.
* **Server port**: Define the port that RabbitMQ is using.
* How the Gateway will interact with RabbitMQ. This is done by instructing the Gravitee Gateway to act as either a producer, a consumer, or both a producer and consumer via the drop-down menu:
  * **Use Producer:** Tells the Gateway Gateway to be prepared to produce messages and send them to the RabbitMQ that you define as your endpoint.
  * **Use Consumer:** Tells the Gateway to be prepared to consume messages from the RabbitMQ that you define as your endpoint.
  * **Use Producer and Consumer:** Tells the Gateway to be able to use both **Use Producer** and **Use Consumer** settings.
* **Authentication:** Define the username and password for RabbitMQ authentication.
* **Producer settings** (if you chose **Use Producer** or **Use Producer and Consumer**): Define the settings that the Gravitee Gateway Kafka client will rely on to produce messages to your backend Kafka topic/broker:
  * **Exchange name**
  * **Exchange type**
  * Enable or disable [**Durable**](https://www.rabbitmq.com/tutorials/amqp-concepts.html#exchanges): Durable exchanges survive broker restart.
  * Enable or disable [**Auto Delete**](https://www.rabbitmq.com/tutorials/amqp-concepts.html#exchanges): When enabled, the exchange is deleted when the last queue is unbound from it.
  * **Routing Key**
* **Consumer settings** (if you chose **Use Consumer** or **Use Producer and Consumer**): Define the settings that the Gravitee Gateway Kafka client will rely on to consume messages from your backend Kafka topic/broker:
  * **Exchange name**
  * **Exchange type**
  * Enable or disable [**Durable**](https://www.rabbitmq.com/tutorials/amqp-concepts.html#exchanges): Durable exchanges survive broker restart.
  * Enable or disable [**Auto Delete**](https://www.rabbitmq.com/tutorials/amqp-concepts.html#exchanges): When enabled, the exchange is deleted when the last queue is unbound from it.
  * **Routing Key**

</details>

<details>

<summary>Mock</summary>

The **Mock** endpoint allows you to mock a backend service to emulate the behavior of a typical HTTP server and test processes. If you chose this endpoint, you will need to configure:

* **Interval between messages publication:** Define, in milliseconds (default 1000), the interval between published messages.
* **Content of published messages:** Define the content of the message body that will be streamed. The default is "mock message."
* **Count of published messages:** Define, as an integer, the maximum number of published messages that are streamed as a part of the mocking. If left unspecified, there will be no limit.

</details>

## Configure v4 Proxy API endpoints

To access endpoint configuration, go to the **API** page in the Management Console and select your API. Then, under **Endpoints**, select **Backend services.** Next, configure your HTTP Proxy endpoint as follows:

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

### Alter and delete existing endpoints

To alter an existing endpoint, select the <img src="../../../../../../.gitbook/assets/Screen Shot 2023-07-18 at 10.43.13 AM (1).png" alt="" data-size="line"> icon, and then edit your endpoint configuration. You can find more information on v4 Proxy API configuration in the [API creation documentation](../../create-apis/the-api-creation-wizard/v4-api-creation-wizard.md#entrypoint-options-for-the-proxy-upstream-protocol-method).

To delete an existing endpoint, select the <img src="../../../../../../.gitbook/assets/Screen Shot 2023-07-18 at 10.46.30 AM (1).png" alt="" data-size="line">icon underneath **ACTIONS** in the **Endpoints** menu.

### Create new endpoints

To create a new endpoint for your v4 Proxy API, click **Add endpoint**. Configure the endpoint per the instructions in the [API creation documentation](../../create-apis/the-api-creation-wizard/v4-api-creation-wizard.md#entrypoint-options-for-the-proxy-upstream-protocol-method).

When you are done, make sure to redeploy the API for your changes to take effect.
