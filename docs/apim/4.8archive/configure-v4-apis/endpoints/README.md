# Endpoints

## Overview

You can choose to configure either [v4 proxy API endpoints](./#proxy-api-endpoints) or [v4 message API endpoints](./#message-api-endpoints).

## Proxy API endpoints

To configure v4 proxy API endpoints:

1. Select **APIs** from the left nav
2. Select your API&#x20;
3. Select **Endpoints** from the inner left nav
4. Click the pencil icon of the endpoint you want to edit:&#x20;

<figure><img src="../../.gitbook/assets/edit HTTP endpoint.png" alt=""><figcaption><p>Configure the Default HTTP proxy endpoint in the Default HTTP proxy group</p></figcaption></figure>

You can also create additional endpoints in the existing group or in new endpoint groups. Refer to the following sections for step-by-step configuration details per proxy type.

### HTTP proxy APIs

Edit the endpoint's settings under the **General** and **Configuration** tabs.

<figure><img src="../../.gitbook/assets/edit HTTP endpoint settings.png" alt=""><figcaption><p>Define the endpoint's General and Configuration settings</p></figcaption></figure>

{% tabs %}
{% tab title="General" %}
### 1. Define your endpoint name

Enter your endpoint name in the **Endpoint name** text field.

### 2. Define your target URL

Enter your target URL in the **Target URL** text field.

### 3. Configure the load balancer

Use the arrow keys to select a value for the weight.
{% endtab %}

{% tab title="Configuration" %}
### 1. Inherit configuration from the endpoint group

Toggle to ON for the endpoint to inherit its configuration settings from the endpoint group to which it belongs.

### **2. Security configuration**

1. Select the HTTP protocol version to use. HTTP/1.1 and HTTP/2 are supported.
2. Choose to either enable or disable keep-alive by toggling **Enable keep-alive** ON or OFF.
   * If enabled, you'll need to define a numeric timeout value in the **Connect timeout** text field by either entering a numerical value or using the arrow keys.
3. Choose to either enable or disable HTTP pipelining by toggling **Enable HTTP pipelining** ON or OFF.
   * If enabled, you'll need to define a numeric timeout value in the **Read timeout** text field by either entering a numerical value or using the arrow keys.
4. Choose to either enable or disable compression by toggling **Enable compression (gzip, deflate)** ON or OFF.
5. **Idle timeout:** Define, in milliseconds, the maximum time a connection will stay in the pool without being used by entering a numeric value or using the arrow keys in the text field. Once the specified time has elapsed, the unused connection will be closed, freeing the associated resources.
6. Choose whether to follow HTTP redirects by toggling **Follow HTTP redirects** ON or OFF.
7. Define the number of max concurrent connections by entering a numeric value or using the arrow keys in the text field.
8. Enter the **KEY** and **VALUE** of HTTP headers that should be added or overridden by the Gateway before proxying the request to the backend API.

### **3. Proxy options**

Select from the following options.

* **No proxy**
* **Use proxy configured at system level**
* **Use proxy for client connections:** Enter the proxy type (SOCKS4 or SOCKS5), the proxy host and port to connect to, and the proxy username and password (both optional).

### 4. SSL options

1. **Verify Host:** Toggle to enable host name verification
2. **Trust all:** Toggle ON for the Gateway to trust any origin certificates. Use with caution over the Internet. The connection will be encrypted, but this mode is vulnerable to "man in the middle" attacks.
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
{% endtab %}
{% endtabs %}

### TCP proxy APIs

Edit the endpoint's settings under the **General** and **Configuration** tabs.

<figure><img src="../../.gitbook/assets/tcp_endpoints config.png" alt=""><figcaption><p>Define the endpoint's General and Configuration settings</p></figcaption></figure>

{% tabs %}
{% tab title="General" %}
### 1. Define your endpoint name

Enter your endpoint name in the **Endpoint name** text field.

### 2. Target server

1. **Host :** Enter the name or IP of the backend host to connect to
2. **Port:** Enter the number of the backend port
3. **Is target secured:** Toggle to enable SSL to connect to target

### 3. Configure the load balancer

Use the arrow keys to select a value for the weight.
{% endtab %}

{% tab title="Configuration" %}
### 1. Inherit configuration from the endpoint group

Toggle to ON for the endpoint to inherit its configuration settings from the endpoint group to which it belongs.

### 2. SSL options

1. **Verify Host:** Toggle to enable host name verification
2. **Trust all:** Toggle ON for the Gateway to trust any origin certificates. Use with caution over the Internet. The connection will be encrypted, but this mode is vulnerable to "man in the middle" attacks.
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

### 3. TCP client options

1. **Connection timeout:** Enter the timeout in ms to connect to the target
2. **Reconnect attempts:** Enter the number of times to try connecting to the target. 0 means no retry.
3. **Reconnect interval:** Enter the interval in ms between connection retries
4. **Idle timeout (ms):** Enter the maximum time a TCP connection will stay active if no data is received or sent. Once the timeout period has elapsed, the unused connection will be closed and the associated resources freed. Zero means no timeout.
5. **Read idle timeout (ms):** The connection will timeout and be closed if no data is received within the timeout period.
6. **Write idle timeout (ms):** The connection will timeout and be closed if no data is sent within the timeout period.

### 4. Proxy options

Select from the following options.

* **No proxy**
* **Use proxy configured at system level**
* **Use proxy for client connections:** Enter the proxy type (SOCKS4 or SOCKS5), the proxy host and port to connect to, and the proxy username and password (both optional).
{% endtab %}
{% endtabs %}

## Message API endpoints

{% hint style="warning" %}
**Enterprise-only**

The ability to create APIs with message API endpoints is an [Enterprise Edition](../../overview/enterprise-edition.md) capability. To learn more about Gravitee Enterprise Edition and what's included in various enterprise packages:

* [Book a demo](https://app.gitbook.com/o/8qli0UVuPJ39JJdq9ebZ/s/rYZ7tzkLjFVST6ex6Jid/)
* [Check out the pricing page](https://www.gravitee.io/pricing)
{% endhint %}

v4 message APIs currently support the following endpoints:

* **Kafka**: Enables the Gravitee API Gateway to establish a persistent connection with a Kafka topic as a backend resource or target.
* **MQTT 5**: Enables the Gravitee API Gateway to establish a persistent connection with an MQTT topic as a backend resource or target.
* **RabbitMQ**: Enables the Gravitee API Gateway to establish a persistent connection with RabbitMQ as a backend resource or target. This will only work if you are using RabbitMQ and the AMQP 0-9-1 protocol. Because this endpoint supports the AMQP 0-9-1 protocol, it may support other event brokers and message queues that communicate over the AMQP 0-9-1 protocol. However, Gravitee does not guarantee or officially support these implementations.
* **Solace**: Enables the Gravitee API Gateway to establish a persistent connection with Solace as a backend resource or target.
* **Mock**: Enables the Gateway to simulate responses from a server for testing API implementations.

### Configuration and Implementation

To access endpoint configuration:

1. Select **APIs** from the left nav
2. Select your API&#x20;
3. Select **Endpoints** from the inner left nav

The integrations Gravitee uses to enable Kafka, MQTT, RabbitMQ, and Solace endpoints for v4 API definitions rely on the following terminology and functionality:

* **Request-Id**: A Universally Unique Identifier (UUID) generated for any new request. This can be overridden using `X-Gravitee-Request-Id`as a Header or Query parameter.
* **Transaction-Id**: A UUID generated for any new request. This can be overridden using `X-Gravitee-Transaction-Id`as a Header or Query parameter.
* **Client-Identifier**: Inferred from the subscription attached to the request. It is either the subscription ID, or, with a Keyless plan, a hash of the remote address. The **Client-Identifier** can be provided by the client via the header `X-Gravitee-Client-Identifier`. In this case, the value used by Gravitee will be the original inferred value suffixed with the provided overridden value.

Click on the tiles below for specific configuration and implementation details.

<table data-view="cards"><thead><tr><th></th><th></th><th></th><th data-type="content-ref"></th></tr></thead><tbody><tr><td>Kafka</td><td></td><td></td><td><a href="kafka.md">kafka.md</a></td></tr><tr><td>MQTT5</td><td></td><td></td><td><a href="mqtt5.md">mqtt5.md</a></td></tr><tr><td>Solace</td><td></td><td></td><td><a href="solace.md">solace.md</a></td></tr><tr><td>RabbitMQ</td><td></td><td></td><td><a href="rabbitmq.md">rabbitmq.md</a></td></tr><tr><td>Mock</td><td></td><td></td><td><a href="mock.md">mock.md</a></td></tr></tbody></table>

