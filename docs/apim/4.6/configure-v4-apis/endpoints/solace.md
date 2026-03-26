---
description: An overview about solace.
---

# Solace

## Overview

This page discusses the [configuration](solace.md#configuration) and [implementation](solace.md#implementation) of the **Solace** endpoint and includes a [reference](solace.md#reference) section.

## Configuration

The **Solace** endpoint allows the Gravitee Gateway to create an API that exposes Solace resources and event APIs via your chosen Gravitee entrypoint(s). Entering a URL and VPN name is required. Modifying any other configuration parameters is optional.

### 1. Initial settings

1. **URL:** Your Solace broker's URL
2. **VPN name:** Provide your VPN name.

### 2. Role

You can tell the Gravitee Gateway's Solace client to act as a producer, a consumer, or both a producer and consumer. Choose **Use Consumer**, **Use Producer**, or **Use Consumer and Producer** from the drop-down menu to do one of the following:

* **Use Producer:** Tells the Gateway Solace client to be prepared to produce messages and send them to the Solace broker that you define as your endpoint
* **Use Consumer:** Tells the Gateway Solace client to be prepared to consume messages from the Solace broker that you define as your endpoint
* **Use Producer and Consumer:** Tells the Gateway Solace client to both **Use Producer** and **Use Consumer**

### 3. Initial security settings

You will define more Gravitee Gateway-specific security settings later on, but this is where you define your Solace-specific authentication flow.

1. Enter the username and password used for authentication.
2. Choose whether to ignore SSL expiration.
3. Choose between **None**, **JKS with location**, and **PKCS12 with location**.

{% tabs %}
{% tab title="None" %}
No further security configuration is necessary.
{% endtab %}

{% tab title="JKS with location" %}
Enter the truststore file's location and SSL password.
{% endtab %}

{% tab title="PKCS12 with location" %}
Enter the truststore file's location and SSL password.
{% endtab %}
{% endtabs %}

### 4. Role settings

If you chose **Use Producer** or **Use Producer and Consumer**, you must define the settings that the Gravitee Gateway Solace client will rely on for producing messages to your backend Solace topic/broker.

If you chose **Use Consumer** or **Use Producer and Consumer**, you must define the settings that the Gravitee Gateway Solace client will rely on to consume messages from your backend Solace topic/broker.

{% tabs %}
{% tab title="Producer" %}
1. Define the topic(s) that the broker uses to filter messages for each connected client.
2. Choose between direct delivery mode and persistent delivery mode.
{% endtab %}

{% tab title="Consumer" %}
Define the **Topics** from which the Gateway Solace client will consume messages.
{% endtab %}
{% endtabs %}

## Implementation

### Common to subscribe and publish

On each incoming request, the endpoint searches an internal cache for an existing Solace messaging service for the API configuration. If not found, the endpoint will create a new one from the API configuration.

### Subscribe

Subscription relies on Message Receiver and Topic.

{% tabs %}
{% tab title="Message Receiver" %}
On each incoming request, the [common messaging service](solace.md#common-to-subscribe-and-publish-1) is used to create a Dedicated Message Receiver. The Solace endpoint consumes messages based on the QoS:

**None**

When the QoS is None, a Direct Message Receiver is created and a shared queue is generated per the format `gravitee-gio-gateway-<clientIdentifier>`.

This allows multiple clients using the same subscription to consume the same topic in parallel. In order to distinguish all clients using the same subscription, the client identifier must be overridden.

**Auto / At-least-Once / At-Most-Once**

A Persistent Message Receiver is created to keep track of messages.

When the entrypoint supports manual ack, the endpoint will use it. Otherwise, the endpoint will use auto-ack for every message received in addition to a Durable Non Exclusive queue that follows the naming format `gravitee/gio-gateway/<clientIdentifier>`.
{% endtab %}

{% tab title="Topic" %}
The topic is retrieved from the API configuration and cannot be overridden via attributes.
{% endtab %}
{% endtabs %}

### Publish

Publication relies on **Direct Message Publisher** and **Topic**.

{% tabs %}
{% tab title="Direct Message Publisher" %}
On each incoming request, the [common messaging service](solace.md#common-to-subscribe-and-publish-1) is used to create a Direct Message Publisher with a backpressure reject mode limited to 10 messages.
{% endtab %}

{% tab title="Topic" %}
The topic is retrieved from the API configuration and cannot be overridden with attributes.
{% endtab %}
{% endtabs %}

## Reference

Refer to the following sections for additional details.

{% hint style="info" %}
Only SMF protocol is supported.
{% endhint %}

* [Compatibility matrix](solace.md#user-content-compatibility-matrix)
* [Endpoint identifier](solace.md#user-content-endpoint-identifier)
* [Endpoint configuration](solace.md#user-content-endpoint-configuration)

### Compatibility matrix <a href="#user-content-compatibility-matrix" id="user-content-compatibility-matrix"></a>

| Plugin version | APIM version  |
| -------------- | ------------- |
| 1.x and up     | 4.x or higher |

### Endpoint identifier <a href="#user-content-endpoint-identifier" id="user-content-endpoint-identifier"></a>

To use this plugin, declare the `solace` identifier when configuring your API endpoints.

### Endpoint configuration <a href="#user-content-endpoint-configuration" id="user-content-endpoint-configuration"></a>

#### General configuration <a href="#user-content-general-configuration" id="user-content-general-configuration"></a>

<table><thead><tr><th width="129">Attributes</th><th width="93">Default</th><th width="121">Mandatory</th><th>Description</th></tr></thead><tbody><tr><td>url</td><td>N/A</td><td>Yes</td><td>Define the URL of the Solace broker. Should begin with either <code>tcp://</code> or <code>tcps://</code> for SMF protocol.</td></tr><tr><td>vpnName</td><td>N/A</td><td>Yes</td><td>Virtual event broker to target</td></tr></tbody></table>

#### Shared Configuration <a href="#user-content-shared-configuration" id="user-content-shared-configuration"></a>

{% tabs %}
{% tab title="Security" %}
Security options are available under `security` attribute.
{% endtab %}

{% tab title="Authentication" %}
Available under `security.auth`:

<table><thead><tr><th width="132">Attributes</th><th width="98">Default</th><th width="123">Mandatory</th><th>Description</th></tr></thead><tbody><tr><td>username</td><td>N/A</td><td>No</td><td>The username to use for the authentication</td></tr><tr><td>password</td><td>N/A</td><td>No</td><td>The password to use for the authentication</td></tr></tbody></table>
{% endtab %}

{% tab title="Consumer" %}
<table><thead><tr><th width="131">Attributes</th><th width="90">Default</th><th width="116">Mandatory</th><th>Description</th></tr></thead><tbody><tr><td>enabled</td><td>false</td><td>No</td><td>Enable or disable the consumer capability</td></tr><tr><td>topics</td><td>N/A</td><td>Yes</td><td>Refers to a list of UTF-8 strings to subscribe to</td></tr></tbody></table>
{% endtab %}

{% tab title="Producer" %}
<table><thead><tr><th width="131">Attributes</th><th width="95">Default</th><th width="118">Mandatory</th><th>Description</th></tr></thead><tbody><tr><td>enabled</td><td>false</td><td>No</td><td>Enable or disable the producer capability</td></tr><tr><td>topics</td><td>N/A</td><td>Yes</td><td>Refers to a list of UTF-8 strings used to publish incoming messages</td></tr></tbody></table>
{% endtab %}
{% endtabs %}

#### Example <a href="#user-content-examples" id="user-content-examples"></a>

The example below shows a full Solace endpoint configuration:

```json
{
    "name": "default",
    "type": "solace",
    "weight": 1,
    "inheritConfiguration": false,
    "configuration": {
        "url": "tcp://localhost:55554",
        "vpnName": "default"
    },
    "sharedConfigurationOverride": {
        "consumer" : {
            "enabled": true,
            "topics": ["topic/subscribe"]
        },
        "producer" : {
            "enabled": true,
            "topics": ["topic/publish"]
        },
        "security" : {
            "auth": {
                "username": "user",
                "password": "password"
            }
        }
    }
}
```
