# WebSocket

## Configuration

{% hint style="info" %}
You must first configure your Gravitee Gateway to enable Websockets.  More information can be found here: [#enable-websocket-support](../../../prepare-a-production-environment/configure-your-http-server.md#enable-websocket-support "mention")
{% endhint %}

If you chose **WebSocket** as an entrypoint, you can modify the following configuration parameters.

1. Choose to either enable or disable the publication capability. Disabling it assumes that the application will never be able to publish any message.
2. Choose to enable or disable the subscription capability. Disabling it assumes that the application will never receive any message.
3. Use the drop-down menu to choose between the available options. QoS compatibility is detailed [here](../../../../4.10/create-and-configure-apis/configure-v4-apis/quality-of-service.md).
