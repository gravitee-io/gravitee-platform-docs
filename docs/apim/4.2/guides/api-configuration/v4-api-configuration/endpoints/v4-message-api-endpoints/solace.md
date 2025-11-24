---
description: An overview about Solace.
---

# Solace

## Overview

This page discusses the [configuration](solace.md#configuration) and [implementation](solace.md#implementation) of the **Solace** endpoint

## Configuration

The **Solace** endpoint allows the Gravitee Gateway to create an API that exposes Solace resources and event APIs via your chosen Gravitee entrypoint(s). If you chose this endpoint, you will need to configure the settings in the following sections.

### 1. Initial settings

1. **URL:** Your Solace broker's URL
2. **VPN name**

### 2. Role

You can tell the Gravitee Gateway's Solace client to act as a producer, a consumer, or both a producer and consumer. Choose **Use Consumer**, **Use Producer**, or **Use Consumer and Producer** from the drop-down menu to do one of the following:

* **Use Producer:** Tells the Gateway Solace client to be prepared to produce messages and send them to the Solace broker that you define as your endpoint
* **Use Consumer:** Tells the Gateway Solace client to be prepared to consume messages from the Solace broker that you define as your endpoint
* **Use Producer and Consumer:** Tells the Gateway Solace client to both **Use Producer** and **Use Consumer**

### 3. Initial security settings

You will define more Gravitee Gateway-specific security settings later on, but this is where you define your Solace-specific **Authentication** flow. Gravitee uses TLS to support the **Username** and **Password** you define.

### 4. Role settings

If you chose **Use Producer** or **Use Producer and Consumer**, you must define the settings that the Gravitee Gateway Solace client will rely on for producing messages to your backend Solace topic/broker.

If you chose **Use Consumer** or **Use Producer and Consumer**, you must define the settings that the Gravitee Gateway Solace client will rely on to consume messages from your backend Solace topic/broker.

{% tabs %}
{% tab title="Producer" %}
Define the **Topics** that the broker uses to filter messages for each connected client. **Topics** consists of one or more topic levels. Each topic level is separated by a forward slash (topic level separator).
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
