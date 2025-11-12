---
description: >-
  This page describes the configuration options of the Server-sent events
  entrypoint
---

# Server-sent Events

## Configuration

If you chose **SSE** as an entrypoint, you will be brought to a page where you can configure:

1. **Heartbeat intervals:** Define the interval in which heartbeats are sent to the client by entering a numeric value into the **Define the interval in which heartbeats** **are sent to client** text field or by using the arrow keys. Intervals must be greater than or equal to 2000ms. Each heartbeat will be sent as an empty comment: `''`.
2. Choose to allow or disallow sending message metadata to the client as SSE comments by toggling **Allow sending messages metadata to client as SSE comments** ON or OFF.
3. Choose to allow or disallow sending message headers to the client as SSE comments by toggling **Allow sending messages headers to client as SSE comments** ON or OFF.
4. **Quality of service:** Use the drop-down menu to choose between the available options. QoS compatibility is detailed [here](docs/apim/4.5/using-the-product/managing-your-apis/api-configuration/v4-api-configuration/quality-of-service.md).
