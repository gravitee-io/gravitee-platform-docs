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
3. **Frame type:** Choose the WebSocket frame type that the subscriber uses to send messages to the client: **Binary** (`BINARY`), the default, or **Text** (`TEXT`). The configuration key is `subscriber.frameType`. Existing APIs, and any configuration without this field, keep sending binary frames. For the requirements of Text, see [Text frames](#text-frames).
4. Use the drop-down menu to choose between the available options. QoS compatibility is detailed [here](../quality-of-service.md).

### Text frames

With **Text**, the entrypoint sends each message to the client as one UTF-8 text message.

Text frames follow these rules:

* A message whose payload isn't valid UTF-8 closes the connection with status 1007 (Invalid payload data), and the entrypoint doesn't acknowledge it.
* Whether that message is lost or delivered again depends on the endpoint. An endpoint that has already acknowledged the message on its side, such as one that acknowledges on receipt under QoS `AUTO`, doesn't deliver it again.
* An endpoint that delivers unacknowledged messages again sends the message on the next connection, which closes with status 1007 again.

{% hint style="warning" %}
When the endpoint delivers unacknowledged messages again, a message that isn't valid UTF-8 closes every reconnection with status 1007 until the message is removed at the source.
{% endhint %}

Text has the following requirements:

* Text requires APIM 4.14.0 or later and the WebSocket entrypoint 4.x.
* On an APIM 4.13.x gateway with entrypoint 4.x installed, an API with **Text** and the subscription capability enabled isn't deployed, and the gateway logs an ERROR. APIs that use **Binary** are unaffected.
* Upgrade the Management API first. During the upgrade, gateways that don't run APIM 4.14 yet still run entrypoint 3.x, which ignores `frameType` and keeps sending binary frames. Text takes effect on each gateway once it runs APIM 4.14 or later.

### Compatibility matrix

| Plugin version | APIM version |
| -------------- | ------------ |
| 2.x            | 4.9.x to 4.10.x |
| 3.x            | 4.11.x to 4.13.x |
| 4.x            | 4.14.x to latest |

Entrypoint 4.x is built for Java 25 and doesn't load at all on APIM 4.12.x or earlier, even for APIs that use **Binary**. The gateway logs an `UnsupportedClassVersionError`. Stay on entrypoint 3.x until you upgrade APIM.
