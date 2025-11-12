# Azure Service Bus

## Overview

This article details the [configuration](azure-service-bus.md#configuration) of the **Azure Service Bus** endpoint and includes a [reference](azure-service-bus.md#reference) section.

## Configuration

The **Azure Service Bus** endpoint allows you to publish and subscribe to events in Azure Service Bus using web-friendly protocols such as HTTP or WebSocket, where the Gravitee Gateway mediates the protocol between the client and the backend. Modifying the following configuration parameters is optional.

### 1. Initial settings

Enter the fully qualified name for your Service Bus namespace.

### 2. Role

You can tell the Gravitee Gateway's Azure Service Bus client to act as a producer, a consumer, or both a producer and consumer. Choose **Use Consumer**, **Use Producer**, or **Use Consumer and Producer** from the drop-down menu to do one of the following:

* **Use Producer:** Tells the Gateway Azure Service Bus client to be prepared to produce messages and send them to the Azure Service Bus broker that you define as your endpoint
* **Use Consumer:** Tells the Gateway Azure Service Bus client to be prepared to consume messages from the Azure Service Bus broker that you define as your endpoint
* **Use Producer and Consumer:** Tells the Gateway Azure Service Bus client to both **Use Producer** and **Use Consumer**

### 3. Initial security settings

You will define more Gravitee Gateway-specific security settings later on, but this is where you enter the connection string for your Azure Service Bus authentication flow.

### 4. Role settings

If you chose **Use Producer** or **Use Producer and Consumer**, you must define the settings that the Gravitee Gateway Azure Service Bus client will rely on for producing messages to your backend Azure Service Bus topic/broker.&#x20;

If you chose **Use Consumer** or **Use Producer and Consumer**, you must define the settings that the Gravitee Gateway Azure Service Bus client will rely on for consuming messages from your backend Azure Service Bus topic/broker.&#x20;

{% tabs %}
{% tab title="Producer" %}
Define the following:

1. Define the name of the queue for which to create a producer.
2. Enter the name of the topic.
{% endtab %}

{% tab title="Consumer" %}
Define the following:

1. Define the name of the queue for which to create a receiver.
2. Enter the name of the topic.
3. Enter the name of the subscription to listen to in the topic.
{% endtab %}
{% endtabs %}

### Tenants

You can configure tenants to specify which users can proxy requests to this endpoint. Tenants ensure that certain groups of users receive information from only specific APIs. For more information about configuring tenants, see [tenants.md](docs/apim/4.7/gravitee-gateway/tenants.md "mention").

## Reference

Refer to the following sections for additional details.

### Compatibility matrix <a href="#user-content-compatibility-matrix" id="user-content-compatibility-matrix"></a>

| Plugin version | APIM version |
| -------------- | ------------ |
| 0.x            | 4.4 minimum  |

### Endpoint identifier <a href="#user-content-endpoint-identifier" id="user-content-endpoint-identifier"></a>

To use this plugin, declare the `asb` identifier when configuring your API endpoints.

### Endpoint configuration <a href="#user-content-endpoint-configuration" id="user-content-endpoint-configuration"></a>

#### General configuration <a href="#user-content-general-configuration" id="user-content-general-configuration"></a>

<table><thead><tr><th width="241">Attributes</th><th width="97">Default</th><th width="124">Mandatory</th><th>Description</th></tr></thead><tbody><tr><td>fullyQualifiedNamespace</td><td></td><td>Yes</td><td>Fully qualified namespace in the format <code>NAMESPACENAME.servicebus.windows.net</code></td></tr></tbody></table>

#### Shared Configuration <a href="#user-content-shared-configuration" id="user-content-shared-configuration"></a>

{% tabs %}
{% tab title="Security" %}
<table><thead><tr><th width="234">Attributes</th><th width="92">Default</th><th width="117">Mandatory</th><th>Description</th></tr></thead><tbody><tr><td>connectionString</td><td></td><td>No</td><td>The connection string to the Azure Service Bus</td></tr></tbody></table>
{% endtab %}

{% tab title="Producer" %}
<table><thead><tr><th width="204">Attributes</th><th width="99">Default</th><th width="121">Mandatory</th><th>Description</th></tr></thead><tbody><tr><td>enabled</td><td>false</td><td>Yes</td><td>Allow enabling or disabling the producer capability</td></tr><tr><td>queueName</td><td></td><td>No</td><td>Sets the name of the queue for which to create a producer</td></tr><tr><td>topicName</td><td></td><td>No</td><td>Sets the name of the topic for which to create a producer</td></tr></tbody></table>
{% endtab %}

{% tab title="Consumer" %}
<table><thead><tr><th width="204">Attributes</th><th width="99">Default</th><th width="121">Mandatory</th><th>Description</th></tr></thead><tbody><tr><td>enabled</td><td>false</td><td>Yes</td><td>Allow enabling or disabling the producer capability</td></tr><tr><td>queueName</td><td></td><td>No</td><td>Sets the name of the queue for which to create a receiver</td></tr><tr><td>topicName</td><td></td><td>No</td><td>Sets the name of the subscription to listen to in the topic. <code>subscriptionName</code> must also be set.</td></tr><tr><td>subscriptionName</td><td></td><td>No</td><td>Sets the name of the subscription to listen to in the topic. <code>topicName</code> must also be set.</td></tr></tbody></table>
{% endtab %}
{% endtabs %}

#### **Examples**

{% tabs %}
{% tab title="Produce messages" %}
{% code title="Produce messages" %}
```json
{
  "name": "default",
  "type": "asb",
  "weight": 1,
  "inheritConfiguration": false,
  "configuration": {},
  "sharedConfigurationOverride": {
      "security": {
        "connectionString": "Endpoint=sb://example.servicebus.windows.net/;SharedAccessKeyName=ExampleSharedAccessKeyName;SharedAccessKey=ExampleSharedAccessKey"
      },
      "producer": {
        "queueName": "queue-name",
        "enabled": true
    }
  }
}
```
{% endcode %}
{% endtab %}

{% tab title="Consume messages" %}
{% code title="Consume messages" %}
```json
{
  "name": "default",
  "type": "asb",
  "weight": 1,
  "inheritConfiguration": false,
  "configuration": {},
  "sharedConfigurationOverride": {
      "security": {
        "connectionString": "Endpoint=sb://example.servicebus.windows.net/;SharedAccessKeyName=ExampleSharedAccessKeyName;SharedAccessKey=ExampleSharedAccessKey"
      },
      "consumer": {
        "queueName": "queue-name",
        "enabled": true
      }
  }
}
```
{% endcode %}
{% endtab %}
{% endtabs %}
