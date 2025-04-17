# v4 API Creation Wizard

## Overview

The v4 API creation wizard makes it easy to create new Gateway APIs from scratch. To access the v4 API creation wizard:

1. Log in to your APIM Console
2. Click on **APIs** in the left nav
3. In the Create New API , click on **Create V4 API**.

<figure><img src="../.gitbook/assets/image (140).png" alt=""><figcaption></figcaption></figure>

The API creation wizard comprises several steps, each of which requires you to define certain sets of information.

## API details

Define a name, version number, and description for your API.

The name and version number are required, but we also recommend giving your API a description so that it is more easily understood and managed by internal users.

<figure><img src="../.gitbook/assets/v4 wizard_step 1.png" alt=""><figcaption></figcaption></figure>

## Entrypoints

Choose how you want to expose your backend.

* [**Proxy Generic Protocol**](v4-api-creation-wizard.md#generic-proxy-entrypoints)**:** Use this method if you want to use Gravitee to proxy backend REST APIs, SOAP APIs, WebSocket Server, gRPC, or GraphQL over HTTP or TCP. You will not be able to enforce policies at the message level.
* [**Protocol Mediation**](v4-api-creation-wizard.md#protocol-mediation-entrypoints)**:** Use this method if you want to expose backend event brokers, such as Kafka and MQTT.
* **Kafka Protocol:** Refer to the [Kafka documentation](../kafka-gateway/create-kafka-apis.md) if you want to proxy the native Kafka protocol with the Gravitee Gateway acting as a Kafka broker to Kafka clients.

{% hint style="info" %}
The Gravitee documentation adopts concise terminology to differentiate between these API types:

**HTTP proxy API:** An API created using **Proxy Generic Protocol** and called over HTTP

**TCP proxy API:** An API created using **Proxy Generic Protocol** and called over TCP

**Message API:** An API created using **Protocol Mediation**
{% endhint %}

<figure><img src="../.gitbook/assets/v4 step 2.png" alt=""><figcaption></figcaption></figure>

### Generic proxy entrypoints

If you chose **Proxy Generic Protocol**, select either HTTP Proxy or TCP Proxy as your entrypoint.

<figure><img src="../.gitbook/assets/v4 3.png" alt=""><figcaption></figcaption></figure>

The configuration details for each proxy entrypoint selection are discussed below.

<details>

<summary>HTTP Proxy</summary>

* **Context path:** The URL of your API. For example, if your URL is `[https://apim-master-gateway.team-apim.gravitee.dev/myAPI]`, then `[/myAPI]` is the context path.
* **Virtual hosts:** Enabling virtual hosts requires you to define your **virtual host** and optionally enable **override access**.

</details>

<details>

<summary>TCP Proxy</summary>

* **Host:** The name of the host. Duplicate hostnames cannot be entered for the current API.

</details>

### Protocol mediation entrypoints

{% hint style="warning" %}
**Enterprise only**

The ability to create APIs with message API entrypoints is an [Enterprise Edition](../overview/enterprise-edition.md) capability. To learn more about Gravitee Enterprise and what's included in various enterprise packages:

* [Book a demo](https://app.gitbook.com/o/8qli0UVuPJ39JJdq9ebZ/s/rYZ7tzkLjFVST6ex6Jid/)
* [Check out the pricing page](https://www.gravitee.io/pricing)
{% endhint %}

Gravitee supports several different types of entrypoints that cater to different protocols and use cases:

<table><thead><tr><th width="198">Entrypoint</th><th>Description</th></tr></thead><tbody><tr><td><a href="v4-api-creation-wizard.md#http-get">HTTP GET</a></td><td>Front a backend or data source with a Gateway REST API that supports the HTTP GET request.</td></tr><tr><td><a href="v4-api-creation-wizard.md#http-post">HTTP POST</a></td><td>Front a backend or data source with a Gateway REST API that supports the HTTP POST request.</td></tr><tr><td><a href="v4-api-creation-wizard.md#server-sent-events">Server-sent events</a></td><td>Front a backend or data source with a Gateway SSE API for unidirectional communication between server and client.</td></tr><tr><td><a href="v4-api-creation-wizard.md#webhook">Webhook</a></td><td>Front a backend or data source with a Gateway Webhook API. This allows consumers to subscribe to the Gravitee Gateway via Webhook and then retrieve streamed data in real-time from a backend data source, via the Gateway, over the consumer's Webhook callback URL.</td></tr><tr><td><a href="v4-api-creation-wizard.md#websocket">WebSocket</a></td><td>Front a backend or data source with a Gateway WebSocket API. This allows a consumer to retrieve and send streamed events and messages in real-time.</td></tr></tbody></table>

<figure><img src="../.gitbook/assets/v4 wizard_step 2 message entrypoints.png" alt=""><figcaption></figcaption></figure>

Once you select your entrypoint(s), configure the fields common to all entrypoints:

1. **Context path:** The URL of your API. For example, if your URL is `[https://apim-master-gateway.team-apim.gravitee.dev/myAPI]`, then `[/myAPI]` is the context path.
2. **Virtual hosts:** Enabling virtual hosts requires you to define your **virtual host** and optionally enable **override access**.

The following sections describe the additional configuration settings for each protocol mediation entrypoint type.

<details>

<summary>HTTP GET</summary>

Modifying the following configuration parameters is optional.

1. Define the maximum number of messages to retrieve via HTTP GET.
2. Define the maximum duration, in milliseconds, to wait to retrieve the expected number of messages. The effective number of retrieved messages could be less than expected if maximum duration is reached before all messages are retrieved.
3. Choose whether to allow sending message headers to the client in the payload.
4. Choose whether to allow sending message metadata to the client in the payload.
5. Use the drop-down menu to choose between the available options. QoS compatibility is detailed [here](../configure-v4-apis/quality-of-service.md).

</details>

<details>

<summary>HTTP POST</summary>

Modifying the following configuration parameters is optional.

1. Choose whether to add each header from incoming request to the generated message headers.
2. Choose whether to initiate an empty message flow and give policies full access to the context whenever the POST request is made to the entrypoint.
3. Use the drop-down menu to choose between the available options. QoS compatibility is detailed [here](../configure-v4-apis/quality-of-service.md).

</details>

<details>

<summary>Server-sent events</summary>

Modifying the following configuration parameters is optional.

1. Define the interval at which heartbeats are sent to the client. Intervals must be greater than or equal to 2000ms. Each heartbeat will be sent as an empty comment: `''`.
2. Choose to allow or disallow sending message metadata to the client as SSE comments.
3. Choose to allow or disallow sending message headers to the client as SSE comments.
4. Use the drop-down menu to select a Quality of Service option. QoS compatibility is detailed [here](../configure-v4-apis/quality-of-service.md).

</details>

<details>

<summary>Webhook</summary>

Modifying the following configuration parameters is optional.

1. Choose whether to interrupt message consumption if the request to the callback URL ends with a 5xx error.
2. Choose whether to interrupt message consumption if the request to the callback URL ends with an exception.
3. Define the maximum time, in milliseconds, to connect to the Webhook.
4. Define the maximum time, in milliseconds, allotted for the Webhook to complete the request (including response).
5. Define the maximum time, in milliseconds, a connection will stay in the pool without being used. Once this time has elapsed, the unused connection will be closed, freeing the associated resources.
6. Use the drop-down menu to select a proxy option: **No proxy**, **Use proxy configured at system level**, or **Use proxy for client connections**.
   * If you chose **Use proxy for client connections**, define the following:
     * **Proxy type:** Choose between HTTP, SOCKS4 and SOCKS5.
     * **Proxy host:** Enter your proxy host in the text field.
     * **Proxy port:** Enter your proxy port in the text field.
     * (Optional) **Proxy username:** Enter your proxy username in the text field.
     * (Optional) **Proxy password:** Enter your proxy password in the text field.
7. Use the drop-down menu to choose between the available options. QoS compatibility is detailed [here](../configure-v4-apis/quality-of-service.md).

</details>

<details>

<summary>WebSocket</summary>

Modifying the following configuration parameters is optional.

1. Choose to either enable or disable the publication capability. Disabling it assumes that the application will never be able to publish any message.
2. Choose to enable or disable the subscription capability. Disabling it assumes that the application will never receive any message.
3. Use the drop-down menu to choose between the available options. QoS compatibility is detailed [here](../configure-v4-apis/quality-of-service.md).

</details>

## Endpoints

Gateway endpoints define the protocol and configuration by which the Gateway API will fetch data from or post data to the backend API. Your endpoints will be dictated by the API architecture that you selected earlier.

* [Proxy Generic Protocol](v4-api-creation-wizard.md#generic-proxy-endpoints)
* [Protocol Mediation](v4-api-creation-wizard.md#protocol-mediation-endpoints)

{% hint style="info" %}
The endpoint configuration will determine the endpoint group’s default configuration. By default, the endpoint will inherit the configuration of the group.

By default, the endpoint group will be named **Default \<endpoint type> group** and the endpoint will be named **Default \<endpoint type>**, e.g., **Default TCP proxy group** and **Default TCP proxy**.
{% endhint %}

### Generic proxy endpoints

The HTTP proxy and TCP proxy endpoint configurations are described in detail below.

<details>

<summary>HTTP Proxy</summary>

#### Define your target URL

Enter your target URL in the **Target URL** text field.

#### Define your HTTP options

1. Select the HTTP protocol version to use. HTTP/1.1 and HTTP/2 are supported.\
   If you selected HTTP/2, choose to either allow or disallow h2c clear text upgrade.
2. Choose to either enable or disable keep-alive.If enabled, you'll need to define a numeric timeout value in the **Connect timeout** text field.
3. Choose to either enable or disable HTTP pipelining. If enabled, you'll need to define a numeric timeout value in the **Read timeout** text field.
4. Choose to either enable or disable compression .
5. Choose to either enable or disable header propagation. **Propagate client Accept-Encoding header (no decompression if any)** can only be enabled if **Enable compression (gzip, deflate)** is disabled.
6. Define, in milliseconds, the maximum time a connection will stay in the pool without being used. Once the specified time has elapsed, the unused connection will be closed, freeing the associated resources.
7. Choose whether to follow HTTP redirects.
8. Define the number of max concurrent connections.
9. Enter key-value pairs to create headers that the Gateway should add or override before proxying the request to the backend API.

#### Define your Proxy options

Choose between **No proxy**, **Use proxy configured at system level**, or **Use proxy for client connections**.

If **Use proxy for client connections** is selected, you'll need to define the following:

* **Proxy type:** Select between **HTTP**, **SOCKS4**, and **SOCKS5**
* **Proxy host:** Enter your proxy host in the text field.
* **Proxy port:** Enter your proxy port in the text field.
* (Optional) **Proxy username:** Enter your proxy username in the text field.
* (Optional) **Proxy password:** Enter your proxy password in the text field.

#### Define your SSL options

1. Toggle **Verify Host** to enable or disable host verification.
2. Toggle **Trust all** to ON to trust any origin certificates.
3. **Truststore:** Select from the following options. PEM format does not support truststore password.
   * **None**
   * **JKS with path:** Enter the truststore password and path to the truststore file
   * **JKS with content:** Enter the truststore password and binary content as base64
   * **PKCS#12 / PFX with path:** Enter the truststore password and path to the truststore file
   * **PKCS#12 / PFX with content:** Enter the truststore password and binary content as base64
   * **PEM with path:** Enter the truststore password and path to the truststore file
   * **PEM with content:** Enter the truststore password and binary content as base64
4. **Key store:** Select from the following options.
   * **None**
   * **JKS with path:** Enter the key store password, key alias, key password, and path to the key store file
   * **JKS with content:** Enter the key store password, key alias, key password, and binary content as base64
   * **PKCS#12 / PFX with path:** Enter the key store password, key alias, key password, and path to the key store file
   * **PKCS#12 / PFX with content:** Enter the key store password, key alias, key password, and binary content as base64
   * **PEM with path:** Enter the paths to the certificate and private key files
   * **PEM with content:** Enter the certificate and private key

</details>

<details>

<summary>TCP Proxy</summary>

#### Target server

* **Host :** Name or IP of the backend host to connect to
* **Port:** Number of the backend port
* **Is target secured:** Toggle to enable SSL to connect to target

#### SSL Options

1. **Verify Host:** Toggle to enable host name verification
2. **Trust all:** Toggle ON for the Gateway to trust any origin certificates.
3. **Truststore:** Select from the following options. PEM format does not support truststore password.
   * **None**
   * **JKS with path:** Enter the truststore password and path to the truststore file
   * **JKS with content:** Enter the truststore password and binary content as base64
   * **PKCS#12 / PFX with path:** Enter the truststore password and path to the truststore file
   * **PKCS#12 / PFX with content:** Enter the truststore password and binary content as base64
   * **PEM with path:** Enter the truststore password and path to the truststore file
   * **PEM with content:** Enter the truststore password and binary content as base64
4. **Key store:** Select from the following options.
   * **None**
   * **JKS with path:** Enter the key store password, key alias, key password, and path to the key store file
   * **JKS with content:** Enter the key store password, key alias, key password, and binary content as base64
   * **PKCS#12 / PFX with path:** Enter the key store password, key alias, key password, and path to the key store file
   * **PKCS#12 / PFX with content:** Enter the key store password, key alias, key password, and binary content as base64
   * **PEM with path:** Enter the paths to the certificate and private key files
   * **PEM with content:** Enter the certificate and private key

#### TCP client options

1. **Connection timeout:** Enter the timeout in ms to connect to the target
2. **Reconnect attempts:** Enter the number of times to try connecting to the target. 0 means no retry.
3. **Reconnect interval:** Enter the interval in ms between connection retries
4. **Idle timeout (ms):** Enter the maximum time a TCP connection will stay active if no data is received or sent. Once the timeout period has elapsed, the unused connection will be closed and the associated resources freed. Zero means no timeout.
5. **Read idle timeout (ms):** The connection will timeout and be closed if no data is received within the timeout period.
6. **Write idle timeout (ms):** The connection will timeout and be closed if no data is sent within the timeout period.

#### Proxy options

Choose between **No proxy**, **Use proxy configured at system level**, or **Use proxy for client connections**.

If **Use proxy for client connections** is selected, you'll need to define the following:

* **Proxy type:** Select between **HTTP**, **SOCKS4**, and **SOCKS5**
* **Proxy host:** Enter your proxy host in the text field.
* **Proxy port:** Enter your proxy port in the text field.
* (Optional) **Proxy username:** Enter your proxy username in the text field.
* (Optional) **Proxy password:** Enter your proxy password in the text field.

</details>

### **Protocol mediation endpoints**

{% hint style="warning" %}
**Enterprise only**

The ability to create APIs with message API endpoints is an [Enterprise Edition](../overview/enterprise-edition.md) capability. To learn more about Gravitee Enterprise and what's included in various enterprise packages:

* [Book a demo](https://app.gitbook.com/o/8qli0UVuPJ39JJdq9ebZ/s/rYZ7tzkLjFVST6ex6Jid/)
* [Check out the pricing page](https://www.gravitee.io/pricing)
{% endhint %}

Gravitee supports several different types of endpoints that cater to different protocols and use cases:

<table><thead><tr><th width="245">Endpoint</th><th>Description</th></tr></thead><tbody><tr><td><a href="v4-api-creation-wizard.md#azure-service-bus">Azure Service Bus</a></td><td>Publish and subscribe to events in Azure Service Bus using web-friendly protocols such as HTTP or WebSocket. The Gateway mediates the protocol between the client and the backend.</td></tr><tr><td><a href="v4-api-creation-wizard.md#kafka">Kafka</a></td><td>The Gateway opens up a persistent connection and/or sets up a Kafka client to call a backend Kafka broker.</td></tr><tr><td><a href="v4-api-creation-wizard.md#mock">Mock</a></td><td>The Gateway mocks a backend service to emulate the behavior of a typical HTTP server and test processes.</td></tr><tr><td><a href="v4-api-creation-wizard.md#mqtt-5.x">MQTT 5.x</a></td><td>The Gateway opens up a persistent connection and/or sets up an MQTT client to call a backend MQTT broker. The broker must run on MQTT 5.x.</td></tr><tr><td><a href="v4-api-creation-wizard.md#rabbitmq">RabbitMQ</a></td><td>The Gateway opens up a persistent connection and/or calls a backend RabbitMQ resource. The resource must communicate using the AMQP 0-9-1 protocol.</td></tr><tr><td><a href="v4-api-creation-wizard.md#solace">Solace</a></td><td>The Gateway creates an API that exposes Solace resources and event APIs via your chosen entrypoint(s).</td></tr></tbody></table>

<figure><img src="../.gitbook/assets/a v4 00.png" alt=""><figcaption></figcaption></figure>

Protocol mediation endpoint configurations are described in detail below.

<details>

<summary>Azure Service Bus</summary>

Modifying the following configuration parameters is optional.

1. Enter the fully qualified name for your Service Bus namespace.
2. Use the drop-down menu to instruct the Gateway Kafka client to **Use Consumer**, **Use Producer**, or **Use Consumer and Producer**.
3. Enter the connection string for your Azure Service Bus authentication flow.
4. (If applicable) Define the producer settings that the Gravitee Gateway client will rely on for producing messages to your backend Azure Service Bus topic/broker:
   1. Define the name of the queue for which to create a producer.
   2. Enter the name of the topic.
5. (If applicable) Define the consumer settings that the Gravitee Gateway client will rely on for consuming messages from your backend Azure Service Bus topic/broker:
   1. Define the name of the queue for which to create a receiver.
   2. Enter the name of the topic.
   3. Enter the name of the subscription to listen to in the topic.

</details>

<details>

<summary>Kafka</summary>

Entering a host/port pair (and a list of topics for a producer) is required. Modifying any other configuration parameters is optional.

1. Define the comma-separated list of host/port pairs to use for establishing the initial connection to the Kafka cluster.
2. Use the drop-down menu to instruct the Gateway Kafka client to **Use Consumer**, **Use Producer**, or **Use Consumer and Producer**.
3. Select **PLAINTEXT**, **SASL\_PLAINTEXT**, **SASL\_SSL**, or **SSL** from the drop-down menu to define your Kafka-specific authentication flow:
   * **PLAINTEXT:** No further security config necessary.
   * **SASL\_PLAINTEXT:** Choose GSSAPI, OAUTHBEARER, PLAIN, SCRAM\_SHA-256, or SCRAM-SHA-512 and enter the JAAS login context parameters.
   *   **SSL:** Use the drop-down menu to configure a truststore type

       * **PEM with location:** Enter the location of your truststore file.
       * **PEM with certificates:** Enter the certificates.
       * **JKS with location:** Enter the truststore file's location and the SSL password.
       * **JKS with certificates:** Enter the certificates and SSL password.
       * **PKCS12 with location:** Enter the truststore file's location and the SSL password.
       * **PKCS12 with certificates:** Enter the certificates and SSL password.

       and a keystore type

       * **PEM with location:** Enter the SSL keystore certificate chain and the keystore file's location.
       * **PEM with key:** Enter the SSL keystore certificate chain and the SSL keystore private key credentials.
       * **JKS with location:** Enter the keystore file's location and the SSL password.
       * **JKS with key:** Enter the SSL keystore private key credentials and the SSL password.
       * **PKCS12 with location:** Enter the keystore file's location and the SSL password.
       * **PKCS12 with key:** Enter the SSL keystore private key credentials and the SSL password.
   * **SASL\_SSL:** Configure for both SASL\_PLAINTEXT and SSL.
4. (If applicable) Define the producer settings that the Gravitee Gateway Kafka client will rely on for producing messages to your backend Kafka topic/broker:
   1. The topic(s) that the broker uses to filter messages for each connected client.
   2. Choose the compression type for all data generated by the producer: none, gzip, snappy, lz4, or zstd (anything else will throw an exception to the consumer).
5. (If applicable) Define the consumer settings that the Gravitee Gateway Kafka client will rely on for consuming messages from your backend Kafka topic/broker:
   1. Choose whether to encode message IDs in base64.
   2. Choose an **Auto offset reset** to control what happens when there is no initial offset in Kafka, or if the current offset no longer exists on the server. You can select to automatically reset to the earliest or latest offset; other values throw an exception.
   3. Choose whether to check if a topic exists before trying to consume messages from it.
   4. Choose whether to remove the Confluent header from the message content (for topics linked to a Confluent schema registry).
   5. Either specify a list of the topics from which your Gravitee Gateway client will consume messages or provide a Java regular expression to consume only messages from Kafka topics that match it.

</details>

<details>

<summary>Mock</summary>

Modifying the following configuration parameters is optional.

1. Define, in milliseconds, the interval between published messages.
2. Define the content of the message body that will be streamed.
3. Define, as an integer, the maximum number of published messages that are streamed as a part of the mocking. If left unspecified, there will be no limit.
4. Add static headers to the message for downstream consumption.
5. Add static metadata to the message for downstream consumption.

</details>

<details>

<summary>MQTT 5.X</summary>

Entering a host, port, and producer/consumer topic(s) is required. Modifying any other configuration parameters is optional.

1. Define the host for the MQTT broker that you are using as your endpoint.
2. Define the port for the MQTT broker that you are using as your endpoint.
3. Use the drop-down menu to instruct the Gateway MQTT client to **Use Consumer**, **Use Producer**, or **Use Consumer and Producer**.
4. Specify the number of reconnect attempts that the Gateway will initiate if the MQTT client disconnects from the MQTT broker.
5. Define the period of time that the broker stores the session information of that particular MQTT client.
6. Select **No Security Configuration**, **Authentication configuration**, **SSL configuration**, or **Authentication with SSL configuration** from the drop-down menu to define your MQTT-specific authentication flow:
   * **No Security Configuration:** No further security config necessary.
   * **Authentication configuration:** Enter your username and password.
   *   **SSL configuration:** Choose whether to enable host name verification, then use the drop-down menu to configure a truststore type

       * **None**
       * **PEM with content:** Enter binary content as base64.
       * **PEM with path:** Enter the path to the truststore file.
       * **JKS with content:** Enter binary content as base64 and the truststore password.
       * **JKS with path:** Enter the truststore file path and password.
       * **PKCS12 with content:** Enter binary content as base64 and the truststore password.
       * **PKCS12 with path:** Enter the truststore file path and password.

       and a keystore type

       * **None**
       * **PEM with content:** Enter the certificate content and key content.
       * **PEM with path:** Enter the certificate path and key path.
       * **JKS with content:** Enter binary content as base64 and the keystore password.
       * **JKS with path:** Enter the keystore file path and password.
       * **PKCS12 with content:** Enter binary content as base64 and the keystore password.
       * **PKCS12 with path:** Enter the keystore file path and password.
   * **Authentication with SSL configuration:** Configure for both **Authentication configuration** and **SSL configuration**.
7. (If applicable) Define the producer settings that the Gravitee Gateway MQTT client will rely on for producing messages to your backend MQTT topic/broker:
   1. The topic(s) that the broker uses to filter messages for each connected client.
   2. Choose whether the retain flag must be set for every published message.
   3. The period of time that the broker stores the PUBLISH message for any matching subscribers that are not currently connected.
   4. Topics on which responses from the receivers of the message are expected.
8. (If applicable) Define the consumer topic(s) from which your Gravitee Gateway client will consume messages.

</details>

<details>

<summary>RabbitMQ</summary>

Entering a host and port is required. Modifying any other configuration parameters is optional.

1. **Server host:** Define the host of your RabbitMQ resource.
2. **Server port:** Define the port that RabbitMQ is using.
3. **Virtual host:** Define the virtual host to use.
4. Use the drop-down menu to instruct the Gateway Kafka client to **Use Consumer**, **Use Producer**, or **Use Consumer and Producer**.
5. **Authentication:** Define the **username** and **password** for RabbitMQ authentication.
6.  Choose whether to enable host name verification, then use the drop-down menu to configure a truststore type

    * **None**
    * **PEM with content:** Enter binary content as base64.
    * **PEM with path:** Enter the path to the truststore file.
    * **JKS with content:** Enter binary content as base64 and the truststore password.
    * **JKS with path:** Enter the truststore file path and password.
    * **PKCS12 with content:** Enter binary content as base64 and the truststore password.
    * **PKCS12 with path:** Enter the truststore file path and password.

    and a keystore type

    * **None**
    * **PEM with content:** Enter the certificate content and key content.
    * **PEM with path:** Enter the certificate path and key path.
    * **JKS with content:** Enter binary content as base64 and the keystore password.
    * **JKS with path:** Enter the keystore file path and password.
    * **PKCS12 with content:** Enter binary content as base64 and the keystore password.
    * **PKCS12 with path:** Enter the keystore file path and password.
7. (If applicable) Define the producer settings that the Gravitee Gateway RabbitMQ client will rely on for producing messages to your backend RabbitMQ topic/broker:
   1. Enter the exchange name.
   2. Enter the exchange type.
   3. Choose whether to enable [durable exchanges](https://www.rabbitmq.com/tutorials/amqp-concepts.html#exchanges) that will survive broker restart.
   4. Choose whether to enable [auto delete](https://www.rabbitmq.com/tutorials/amqp-concepts.html#exchanges) to delete the exchange when the last queue is unbound from it.
   5. Enter the routing key.
8. (If applicable) Define the consumer settings that the Gravitee Gateway RabbitMQ client will rely on for consuming messages from your backend RabbitMQ topic/broker:
   1. Enter the exchange name.
   2. Enter the exchange type.
   3. Choose whether to enable [durable exchanges](https://www.rabbitmq.com/tutorials/amqp-concepts.html#exchanges) that will survive broker restart.
   4. Choose whether to enable [auto delete](https://www.rabbitmq.com/tutorials/amqp-concepts.html#exchanges) to delete the exchange when the last queue is unbound from it.
   5. Enter the routing key.

</details>

<details>

<summary>Solace</summary>

Entering a URL and VPN name is required. Modifying any other configuration parameters is optional.

1. **URL:** Define your Solace broker's URL.
2. **VPN name:** Provide your VPN name.
3. Use the drop-down menu to instruct the Gateway MQTT client to **Use Consumer**, **Use Producer**, or **Use Consumer and Producer**.
4. Enter the username and password used for authentication.
5. Choose whether to ignore SSL expiration.
6. Select **None**, **JKS with location**, or **PKCS12 with location** from the drop-down menu to define your Solace-specific authentication flow:
   * **None**
   * **JKS with location:** Enter the truststore file's location and SSL password.
   * **PKCS12 with location:** Enter the truststore file's location and SSL password.
7. (If applicable) Define the producer settings that the Gravitee Gateway Solace client will rely on for producing messages to your backend Solace topic/broker:
   1. The topic(s) that the broker uses to filter messages for each connected client.
   2. Choose between direct delivery mode and persistent delivery mode.
8. (If applicable) Define the consumer topic(s) that the broker uses to filter messages for each connected client.

</details>

## Security

Define a plan to secure, monitor, and transparently communicate information on how to access your API. This includes the configuration of authorization resources, such as Gravitee AM or another OAuth2 resource, and access limitations, such as rate limiting and quotas.

<figure><img src="../.gitbook/assets/a v4 1.png" alt=""><figcaption></figcaption></figure>

Gravitee automatically assigns each API a Default Keyless plan, which grants public access.

{% hint style="info" %}
Gravitee automatically assigns a Default PUSH plan to certain entrypoint/endpoint combinations of message APIs.
{% endhint %}

Click **+ Add plan** to create additional plans. The plan types offered by Gravitee and the API types they apply to are summarized below:

<table><thead><tr><th width="165">Plan</th><th width="399">Description</th><th>API compatibility</th></tr></thead><tbody><tr><td>API Key</td><td>The API Gateway rejects calls from consumers that do not pass the correct API key in a request.</td><td><ul class="contains-task-list"><li><input type="checkbox" checked>HTTP proxy</li><li><input type="checkbox">TCP proxy</li><li><input type="checkbox">Message API</li></ul></td></tr><tr><td>JWT</td><td>An open standard that defines a compact and URL-safe way to securely transmit information, in the form of a JSON object, between parties.</td><td><ul class="contains-task-list"><li><input type="checkbox" checked>HTTP proxy</li><li>TCP proxy</li><li>Message API</li></ul></td></tr><tr><td>Keyless (public)</td><td>When configured, this plan does not add security. It is considered an "open" plan.</td><td><ul class="contains-task-list"><li><input type="checkbox" checked>HTTP proxy</li><li><input type="checkbox" checked>TCP proxy</li><li><input type="checkbox">Message API</li></ul></td></tr><tr><td>mTLS</td><td></td><td><ul class="contains-task-list"><li><input type="checkbox" checked>HTTP proxy</li><li>TCP proxy</li><li>Message API</li></ul></td></tr><tr><td>OAuth2</td><td>A standard designed to allow a website or application to access resources hosted by other web apps on behalf of a user.</td><td><ul class="contains-task-list"><li><input type="checkbox" checked>HTTP proxy</li><li>TCP proxy</li><li>Message API</li></ul></td></tr><tr><td>Push</td><td>Provides an access layer for the Gateway pushing data to consumers. This is used for subscribers.</td><td><ul class="contains-task-list"><li><input type="checkbox">HTTP proxy</li><li><input type="checkbox">TCP proxy</li><li><input type="checkbox" checked>Message API</li></ul></td></tr></tbody></table>

{% hint style="info" %}
To learn more about how plans function in Gravitee, refer to the [plans](../expose-apis/plans/) documentation.
{% endhint %}

Individual plan configurations as they pertain to each API type are described in detail below.

### HTTP proxy API

<details>

<summary>API Key</summary>

Select **API Key** from the **+ Add plan** drop-down menu, then define general details, configuration settings, and restrictions.

#### General

You must enter a value in the **Name** field. Modifying the other configuration parameters is optional.

1. **Name**
2. **Description**
3. **Characteristics**
4. **Conditions:** Select a pre-existing page of general conditions
5. **Subscriptions:** Choose whether to auto-validate subscriptions, require a message from a consumer during subscription, and/or present a message to the consumer upon subscription.
6. **Deployment:** Select sharding tags
7. **Access control:** Select any Groups within APIM that you do not want to have access to this API.

#### Configuration

* (Optional) Choose whether to propagate your API key to upstream APIs.
* (Optional) Use the [Gravitee Expression Language](../getting-started/gravitee-expression-language.md) to define additional selection rules. If you are managing multiple plans that share the same type, this will help the plan selection process.

#### Restrictions

Choose to enable any of the following.

* **Rate limiting:** Specify the maximum number of requests that an application can make within a given number of seconds or minutes, then:
  * Enable or disable **Non-strict mode**: this enables rate limiting to be applied in an asynchronous manner, which results in the distributed counter value not being strict.
  * Enable or disable **Add response headers**.
  * Define your rate limit's **Key**.
  * Choose whether to use the custom key to identify the consumer, regardless of subscription and plan.
  * Define the **max request count** (this can be a static or dynamic count).
  * Define the **time duration** (e.g., a one-second time interval within which to apply the request limitation).
  * Define the **time unit**.
* **Quota:** Define a rate limit over a period of hours, days, or months. If you choose this, you will need to define the same settings that are applicable to rate limiting (see above).
* **Resource filtering:** Restricts resources based on defined whitelist/allowed and/or blacklist/disallowed settings. These are defined by path patterns and methods.

</details>

<details>

<summary>JWT</summary>

Select **JWT** from the **+ Add plan** drop-down menu, then define general details, configuration settings, and restrictions.

#### General

You must enter a value in the **Name** field. Modifying the other configuration parameters is optional.

1. **Name**
2. **Description**
3. **Characteristics**
4. **Conditions:** Select a pre-existing page of general conditions
5. **Subscriptions:** Choose whether to auto-validate subscriptions, require a message from a consumer during subscription, and/or present a message to the consumer upon subscription.
6. **Deployment:** Select sharding tags
7. **Access control:** Select any Groups within APIM that you do not want to have access to this API.

#### Configuration

Only the **Signature** and **JWKS resolver** selections are required. Modifying the other configuration parameters is optional.

1. Choose a **Signature** to define how your JWT token must be signed. The options are:
   * RSA\_RS256
   * RSA\_RS384
   * RSA\_RS512
   * HMAC\_HS512
   * HMAC\_HS384
   * HMAC\_HS384
2. Define your **JWKS resolver**. This defines how your JSON Web Key Set is retrieved. The options are:
   * GIVEN\_KEY
   * GATEWAY\_KEYS
   * JWKS\_URL
3. Define your Resolver parameter. This field supports the [Gravitee Expression Language](../getting-started/gravitee-expression-language.md).
4. If your resolver is **JWKS\_URL**, set the **JWKS URL connect timeout**.
5. If your resolver is **JWKS\_URL**, set the **JWKS URL request timeout**.
6. Choose whether to use a system proxy.
7. Choose whether to extract JWT claims.
8. Choose whether to propagate authorization headers.
9. Define the user claim where users can be extracted.
10. Define the client Id claim where the client can be extracted.
11. Choose whether to ignore CNF validation if the token doesn't contain any CNF information.
12. Choose whether to validate the certificate thumbprint extracted from the access\_token with the one provided by the client.
13. Choose whether to extract the client certificate from the request header.
14. If the client certificate is extracted from the request header, enter the name of the header under which to find the client certificate.
15. Choose whether to validate the token type extracted from the access\_token with the one provided by the client.
16. Choose whether to ignore token type validation if the token doesn't contain any token type information.
17. Enter a list of expected token types. JWT is included by default.
18. Choose whether to ignore the case of the token type when comparing the expected values.
19. Use the Gravitee Expression Language to define additional selection rules. If you are managing multiple plans that share the same type, this will help the plan selection process.

#### Restrictions

Choose to enable any of the following.

* **Rate limiting:** Specify the maximum number of requests that an application can make within a given number of seconds or minutes, then:
  * Enable or disable **Non-strict mode**: this enables rate limiting to be applied in an asynchronous manner, which results in the distributed counter value not being strict.
  * Enable or disable **Add response headers**.
  * Define your rate limit's **Key**.
  * Choose whether to use the custom key to identify the consumer, regardless of subscription and plan.
  * Define the **max request count** (this can be a static or dynamic count).
  * Define the **time duration** (e.g., a one-second time interval within which to apply the request limitation).
  * Define the **time unit**.
* **Quota:** Define a rate limit over a period of hours, days, or months. If you choose this, you will need to define the same settings that are applicable to rate limiting (see above).
* **Resource filtering:** Restricts resources based on defined whitelist/allowed and/or blacklist/disallowed settings. These are defined by path patterns and methods.

</details>

<details>

<summary>Keyless</summary>

Select **Keyless (public)** from the **+ Add plan** drop-down menu, then define general details and restrictions.

#### General

You must enter a value in the **Name** field. Modifying the other configuration parameters is optional.

1. **Name**
2. **Description**
3. **Characteristics**
4. **Conditions:** Select a pre-existing page of general conditions
5. **Subscriptions:** Choose whether to auto-validate subscriptions, require a message from a consumer during subscription, and/or present a message to the consumer upon subscription.
6. **Deployment:** Select sharding tags
7. **Access control:** Select any Groups within APIM that you do not want to have access to this API.

#### Restrictions

Choose to enable any of the following.

* **Rate limiting:** Specify the maximum number of requests that an application can make within a given number of seconds or minutes, then:
  * Enable or disable **Non-strict mode**: this enables rate limiting to be applied in an asynchronous manner, which results in the distributed counter value not being strict.
  * Enable or disable **Add response headers**.
  * Define your rate limit's **Key**.
  * Choose whether to use the custom key to identify the consumer, regardless of subscription and plan.
  * Define the **max request count** (this can be a static or dynamic count).
  * Define the **time duration** (e.g., a one-second time interval within which to apply the request limitation).
  * Define the **time unit**.
* **Quota:** Define a rate limit over a period of hours, days, or months. If you choose this, you will need to define the same settings that are applicable to rate limiting (see above).
* **Resource filtering:** Restricts resources based on defined whitelist/allowed and/or blacklist/disallowed settings. These are defined by path patterns and methods.

</details>

<details>

<summary>mTLS</summary>

Select **mTLS** from the **+ Add plan** drop-down menu, then define general details, configuration settings, and restrictions.

#### General

You must enter a value in the **Name** field. Modifying the other configuration parameters is optional.

1. **Name**
2. **Description**
3. **Characteristics**
4. **Conditions:** Select a pre-existing page of general conditions
5. **Subscriptions:** Choose whether to auto-validate subscriptions, require a message from a consumer during subscription, and/or present a message to the consumer upon subscription.
6. **Deployment:** Select sharding tags
7. **Access control:** Select any Groups within APIM that you do not want to have access to this API.

#### Configuration

(Optional) Use the [Gravitee Expression Language](../getting-started/gravitee-expression-language.md) to define additional selection rules. If you are managing multiple plans that share the same type, this will help the plan selection process.

#### Restrictions

Choose to enable any of the following.

* **Rate limiting:** Specify the maximum number of requests that an application can make within a given number of seconds or minutes, then:
  * Enable or disable **Non-strict mode**: this enables rate limiting to be applied in an asynchronous manner, which results in the distributed counter value not being strict.
  * Enable or disable **Add response headers**.
  * Define your rate limit's **Key**.
  * Choose whether to use the custom key to identify the consumer, regardless of subscription and plan.
  * Define the **max request count** (this can be a static or dynamic count).
  * Define the **time duration** (e.g., a one-second time interval within which to apply the request limitation).
  * Define the **time unit**.
* **Quota:** Define a rate limit over a period of hours, days, or months. If you choose this, you will need to define the same settings that are applicable to rate limiting (see above).
* **Resource filtering:** Restricts resources based on defined whitelist/allowed and/or blacklist/disallowed settings. These are defined by path patterns and methods.

</details>

<details>

<summary>OAuth2</summary>

Select **OAuth2** from the **+ Add plan** drop-down menu, then define general details, configuration settings, and restrictions.

#### General

You must enter a value in the **Name** field. Modifying the other configuration parameters is optional.

1. **Name**
2. **Description**
3. **Characteristics**
4. **Conditions:** Select a pre-existing page of general conditions
5. **Subscriptions:** Choose whether to auto-validate subscriptions, require a message from a consumer during subscription, and/or present a message to the consumer upon subscription.
6. **Deployment:** Select sharding tags
7. **Access control:** Select any Groups within APIM that you do not want to have access to this API.

#### Configuration

Only the **OAuth2 resource** and **Cache resource** fields are required. Modifying the other configuration parameters is optional.

1. Define your OAuth2 resource in the **OAuth2 resource** field. This is the resource that you'll use to validate the token.
2. Define your cache resource in the **Cache resource** field. This is the cache resource that you will use to store the tokens.
3. Choose whether to push the token endpoint payload into the oauth.payload context attribute.
4. Choose whether to instruct your authentication method to check required scopes in order to access the resource. If you choose to check scopes, you must define your list of required scopes using the **Required scopes** module.
5. Choose whether strict mode is enabled or disabled. If you choose **Strict**, scopes will be checked against the exact list you provided in the **Required scopes** section.
6. Choose whether to permit authorization headers to target endpoints.
7. Use the [Gravitee Expression Language](../getting-started/gravitee-expression-language.md) to define additional selection rules. If you are managing multiple plans that share the same type, this will help the plan selection process.

#### Restrictions

Choose to enable any of the following.

* **Rate limiting:** Specify the maximum number of requests that an application can make within a given number of seconds or minutes, then:
  * Enable or disable **Non-strict mode**: this enables rate limiting to be applied in an asynchronous manner, which results in the distributed counter value not being strict.
  * Enable or disable **Add response headers**.
  * Define your rate limit's **Key**.
  * Choose whether to use the custom key to identify the consumer, regardless of subscription and plan.
  * Define the **max request count** (this can be a static or dynamic count).
  * Define the **time duration** (e.g., a one-second time interval within which to apply the request limitation).
  * Define the **time unit**.
* **Quota:** Define a rate limit over a period of hours, days, or months. If you choose this, you will need to define the same settings that are applicable to rate limiting (see above).
* **Resource filtering:** Restricts resources based on defined whitelist/allowed and/or blacklist/disallowed settings. These are defined by path patterns and methods.

</details>

### TCP proxy API

<details>

<summary>Keyless</summary>

Select **Keyless (public)** from the **+ Add plan** drop-down menu, then define general details and restrictions.

#### General

You must enter a value in the **Name** field. Modifying the other configuration parameters is optional.

1. **Name**
2. **Description**
3. **Characteristics**
4. **Access control:** Select any Groups within APIM that you do not want to have access to this API.

</details>

### Message API

<details>

<summary>API Key</summary>

Select **API Key** from the **+ Add plan** drop-down menu, then define general details, configuration settings, and restrictions.

#### General

You must enter a value in the **Name** field. Modifying the other configuration parameters is optional.

1. **Name**
2. **Description**
3. **Characteristics**
4. **Conditions:** Select a pre-existing page of general conditions
5. **Subscriptions:** Choose whether to auto-validate subscriptions, require a message from a consumer during subscription, and/or present a message to the consumer upon subscription.
6. **Access control:** Select any Groups within APIM that you do not want to have access to this API.

#### Configuration

* (Optional) Choose whether to propagate your API key to upstream APIs.
* (Optional) Use the [Gravitee Expression Language](../getting-started/gravitee-expression-language.md) to define additional selection rules. If you are managing multiple plans that share the same type, this will help the plan selection process.

#### Restrictions

Choose to enable any of the following.

* **Rate limiting:** Specify the maximum number of requests that an application can make within a given number of seconds or minutes, then:
  * Enable or disable **Non-strict mode**: this enables rate limiting to be applied in an asynchronous manner, which results in the distributed counter value not being strict.
  * Enable or disable **Add response headers**.
  * Define your rate limit's **Key**.
  * Choose whether to use the custom key to identify the consumer, regardless of subscription and plan.
  * Define the **max request count** (this can be a static or dynamic count).
  * Define the **time duration** (e.g., a one-second time interval within which to apply the request limitation).
  * Define the **time unit**.
* **Quota:** Define a rate limit over a period of hours, days, or months. If you choose this, you will need to define the same settings that are applicable to rate limiting (see above).
* **Resource filtering:** Restricts resources based on defined whitelist/allowed and/or blacklist/disallowed settings. These are defined by path patterns and methods.

</details>

<details>

<summary>JWT</summary>

Select **JWT** from the **+ Add plan** drop-down menu, then define general details, configuration settings, and restrictions.

#### General

You must enter a value in the **Name** field. Modifying the other configuration parameters is optional.

1. **Name**
2. **Description**
3. **Characteristics**
4. **Conditions:** Select a pre-existing page of general conditions
5. **Subscriptions:** Choose whether to auto-validate subscriptions, require a message from a consumer during subscription, and/or present a message to the consumer upon subscription.
6. **Access control:** Select any Groups within APIM that you do not want to have access to this API.

#### Configuration

Only the **Signature** and **JWKS resolver** selections are required. Modifying the other configuration parameters is optional.

1. Choose a **Signature** to define how your JWT token must be signed. The options are:
   * RSA\_RS256
   * RSA\_RS384
   * RSA\_RS512
   * HMAC\_HS512
   * HMAC\_HS384
   * HMAC\_HS384
2. Define your **JWKS resolver**. This defines how your JSON Web Key Set is retrieved. The options are:
   * GIVEN\_KEY
   * GATEWAY\_KEYS
   * JWKS\_URL
3. Define your Resolver parameter. This field supports the [Gravitee Expression Language](../getting-started/gravitee-expression-language.md).
4. If your resolver is **JWKS\_URL**, set the **JWKS URL connect timeout**.
5. If your resolver is **JWKS\_URL**, set the **JWKS URL request timeout**.
6. Choose whether to use a system proxy.
7. Choose whether to extract JWT claims.
8. Choose whether to propagate authorization headers.
9. Define the user claim where users can be extracted.
10. Define the client Id claim where the client can be extracted.
11. Choose whether to ignore CNF validation if the token doesn't contain any CNF information.
12. Choose whether to validate the certificate thumbprint extracted from the access\_token with the one provided by the client.
13. Choose whether to extract the client certificate from the request header.
14. If the client certificate is extracted from the request header, enter the name of the header under which to find the client certificate.
15. Choose whether to validate the token type extracted from the access\_token with the one provided by the client.
16. Choose whether to ignore token type validation if the token doesn't contain any token type information.
17. Enter a list of expected token types. JWT is included by default.
18. Choose whether to ignore the case of the token type when comparing the expected values.
19. Use the Gravitee Expression Language to define additional selection rules. If you are managing multiple plans that share the same type, this will help the plan selection process.

#### Restrictions

Choose to enable any of the following.

* **Rate limiting:** Specify the maximum number of requests that an application can make within a given number of seconds or minutes, then:
  * Enable or disable **Non-strict mode**: this enables rate limiting to be applied in an asynchronous manner, which results in the distributed counter value not being strict.
  * Enable or disable **Add response headers**.
  * Define your rate limit's **Key**.
  * Choose whether to use the custom key to identify the consumer, regardless of subscription and plan.
  * Define the **max request count** (this can be a static or dynamic count).
  * Define the **time duration** (e.g., a one-second time interval within which to apply the request limitation).
  * Define the **time unit**.
* **Quota:** Define a rate limit over a period of hours, days, or months. If you choose this, you will need to define the same settings that are applicable to rate limiting (see above).
* **Resource filtering:** Restricts resources based on defined whitelist/allowed and/or blacklist/disallowed settings. These are defined by path patterns and methods.

</details>

<details>

<summary>Keyless</summary>

Select **Keyless (public)** from the **+ Add plan** drop-down menu, then define general details and restrictions.

#### General

You must enter a value in the **Name** field. Modifying the other configuration parameters is optional.

1. **Name**
2. **Description**
3. **Characteristics**
4. **Access control:** Select any Groups within APIM that you do not want to have access to this API.

#### Restrictions

Choose to enable any of the following.

* **Rate limiting:** Specify the maximum number of requests that an application can make within a given number of seconds or minutes, then:
  * Enable or disable **Non-strict mode**: this enables rate limiting to be applied in an asynchronous manner, which results in the distributed counter value not being strict.
  * Enable or disable **Add response headers**.
  * Define your rate limit's **Key**.
  * Choose whether to use the custom key to identify the consumer, regardless of subscription and plan.
  * Define the **max request count** (this can be a static or dynamic count).
  * Define the **time duration** (e.g., a one-second time interval within which to apply the request limitation).
  * Define the **time unit**.
* **Quota:** Define a rate limit over a period of hours, days, or months. If you choose this, you will need to define the same settings that are applicable to rate limiting (see above).
* **Resource filtering:** Restricts resources based on defined whitelist/allowed and/or blacklist/disallowed settings. These are defined by path patterns and methods.

</details>

<details>

<summary>mTLS</summary>

Select **mTLS** from the **+ Add plan** drop-down menu, then define general details, configuration settings, and restrictions.

#### General

You must enter a value in the **Name** field. Modifying the other configuration parameters is optional.

1. **Name**
2. **Description**
3. **Characteristics**
4. **Subscriptions:** Choose whether to auto-validate subscriptions, require a message from a consumer during subscription, and/or present a message to the consumer upon subscription.
5. **Access control:** Select any Groups within APIM that you do not want to have access to this API.

#### Configuration

(Optional) Use the [Gravitee Expression Language](../getting-started/gravitee-expression-language.md) to define additional selection rules. If you are managing multiple plans that share the same type, this will help the plan selection process.

#### Restrictions

Choose to enable any of the following.

* **Rate limiting:** Specify the maximum number of requests that an application can make within a given number of seconds or minutes, then:
  * Enable or disable **Non-strict mode**: this enables rate limiting to be applied in an asynchronous manner, which results in the distributed counter value not being strict.
  * Enable or disable **Add response headers**.
  * Define your rate limit's **Key**.
  * Choose whether to use the custom key to identify the consumer, regardless of subscription and plan.
  * Define the **max request count** (this can be a static or dynamic count).
  * Define the **time duration** (e.g., a one-second time interval within which to apply the request limitation).
  * Define the **time unit**.
* **Quota:** Define a rate limit over a period of hours, days, or months. If you choose this, you will need to define the same settings that are applicable to rate limiting (see above).
* **Resource filtering:** Restricts resources based on defined whitelist/allowed and/or blacklist/disallowed settings. These are defined by path patterns and methods.

</details>

<details>

<summary>OAuth2</summary>

Select **OAuth2** from the **+ Add plan** drop-down menu, then define general details, configuration settings, and restrictions.

#### General

You must enter a value in the **Name** field. Modifying the other configuration parameters is optional.

1. **Name**
2. **Description**
3. **Characteristics**
4. **Subscriptions:** Choose whether to auto-validate subscriptions, require a message from a consumer during subscription, and/or present a message to the consumer upon subscription.
5. **Access control:** Select any Groups within APIM that you do not want to have access to this API.

#### Configuration

Only the **OAuth2 resource** and **Cache resource** fields are required. Modifying the other configuration parameters is optional.

1. Define your OAuth2 resource in the **OAuth2 resource** field. This is the resource that you'll use to validate the token.
2. Define your cache resource in the **Cache resource** field. This is the cache resource that you will use to store the tokens.
3. Choose whether to push the token endpoint payload into the oauth.payload context attribute.
4. Choose whether to instruct your authentication method to check required scopes in order to access the resource. If you choose to check scopes, you must define your list of required scopes using the **Required scopes** module.
5. Choose whether strict mode is enabled or disabled. If you choose **Strict**, scopes will be checked against the exact list you provided in the **Required scopes** section.
6. Choose whether to permit authorization headers to target endpoints.
7. Use the [Gravitee Expression Language](../getting-started/gravitee-expression-language.md) to define additional selection rules. If you are managing multiple plans that share the same type, this will help the plan selection process.

#### Restrictions

Choose to enable any of the following.

* **Rate limiting:** Specify the maximum number of requests that an application can make within a given number of seconds or minutes, then:
  * Enable or disable **Non-strict mode**: this enables rate limiting to be applied in an asynchronous manner, which results in the distributed counter value not being strict.
  * Enable or disable **Add response headers**.
  * Define your rate limit's **Key**.
  * Choose whether to use the custom key to identify the consumer, regardless of subscription and plan.
  * Define the **max request count** (this can be a static or dynamic count).
  * Define the **time duration** (e.g., a one-second time interval within which to apply the request limitation).
  * Define the **time unit**.
* **Quota:** Define a rate limit over a period of hours, days, or months. If you choose this, you will need to define the same settings that are applicable to rate limiting (see above).
* **Resource filtering:** Restricts resources based on defined whitelist/allowed and/or blacklist/disallowed settings. These are defined by path patterns and methods.

</details>

<details>

<summary>Push</summary>

Select **Push** from the **+ Add plan** drop-down menu, then define general details and restrictions.

#### General

You must enter a value in the **Name** field. Modifying the other configuration parameters is optional.

1. **Name**
2. **Description**
3. **Characteristics**
4. **Subscriptions:** Choose whether to auto-validate subscriptions, require a message from a consumer during subscription, and/or present a message to the consumer upon subscription.
5. **Access control:** Select any Groups within APIM that you do not want to have access to this API.

#### Restrictions

Choose to enable any of the following.

* **Rate limiting:** Specify the maximum number of requests that an application can make within a given number of seconds or minutes, then:
  * Enable or disable **Non-strict mode**: this enables rate limiting to be applied in an asynchronous manner, which results in the distributed counter value not being strict.
  * Enable or disable **Add response headers**.
  * Define your rate limit's **Key**.
  * Choose whether to use the custom key to identify the consumer, regardless of subscription and plan.
  * Define the **max request count** (this can be a static or dynamic count).
  * Define the **time duration** (e.g., a one-second time interval within which to apply the request limitation).
  * Define the **time unit**.
* **Quota:** Define a rate limit over a period of hours, days, or months. If you choose this, you will need to define the same settings that are applicable to rate limiting (see above).
* **Resource filtering:** Restricts resources based on defined whitelist/allowed and/or blacklist/disallowed settings. These are defined by path patterns and methods.

</details>

## Documentation

See [Documentation](../configure-v4-apis/documentation.md) to learn how to create documentation for a v4 API.

## Summary

Review your API configuration and choose between the following:

* **Save API:** Creates your API as a Gravitee artifact, but does not deploy it to the Gateway.
* **Save & Deploy API:** Creates your API as a Gravitee artifact and deploys it to the Gateway.
