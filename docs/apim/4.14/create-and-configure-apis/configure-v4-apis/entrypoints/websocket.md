---
description: Configure the WebSocket entrypoint parameters for a v4 API Management 4.13 API. Follow the steps to set them for your API.
metaLinks:
  alternates:
    - websocket.md
---

# WebSocket

## Configuration

If you chose **WebSocket** as an entrypoint, you can modify the following configuration parameters.

1. Choose to either enable or disable the publication capability. Disabling it assumes that the application will never be able to publish any message.
2. Choose to enable or disable the subscription capability. Disabling it assumes that the application will never receive any message.
3. **Frame type:** Choose the WebSocket frame type that the subscriber uses to send messages to the client: **BINARY**, the default, or **TEXT**. The configuration key is `subscriber.frameType`. Existing APIs, and any configuration without this field, keep sending binary frames. For the requirements of **TEXT**, see [Text frames](#text-frames).
4. Use the drop-down menu to choose between the available options. QoS compatibility is detailed [here](../quality-of-service.md).

### Text frames

With **TEXT**, the entrypoint sends each message to the client as one UTF-8 text message.

Text frames follow these rules:

* A message whose payload isn't valid UTF-8 closes the connection with status 1007 (Invalid payload data), and the entrypoint doesn't acknowledge it.
* Whether that message is lost or delivered again depends on the endpoint. An endpoint that has already acknowledged the message on its side, such as one that acknowledges on receipt under QoS `AUTO`, doesn't deliver it again.
* An endpoint that delivers unacknowledged messages again sends the message on the next connection, which closes with status 1007 again.

{% hint style="warning" %}
When the endpoint delivers unacknowledged messages again, a message that isn't valid UTF-8 closes every reconnection with status 1007 until the message is removed at the source.
{% endhint %}

Text frames have the following requirements:

* **TEXT** requires APIM 4.14.0 or later.
* Upgrade the Management API first. During the upgrade, gateways that don't run APIM 4.14 yet ignore **Frame type** and keep sending binary frames. **TEXT** takes effect on each gateway once it runs APIM 4.14 or later.
* Don't copy the WebSocket entrypoint that ships with APIM 4.14 into an older gateway. On an APIM 4.13.x gateway, an API with **TEXT** and the subscription capability enabled isn't deployed, and the gateway logs an ERROR. APIs that use **BINARY** are unaffected. APIM 4.12.x and earlier can't load that entrypoint at all, even for APIs that use **BINARY**, and the gateway logs an `UnsupportedClassVersionError`.
