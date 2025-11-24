---
description: Configuration and setup guide for http get.
---

# HTTP GET

## Configuration

If you chose **HTTP GET** as an entrypoint, you can modify the following configuration parameters.

1. Define the maximum number of messages to retrieve via HTTP GET.
2. Define the maximum duration, in milliseconds, to wait to retrieve the expected number of messages. The effective number of retrieved messages could be less than expected if maximum duration is reached before all messages are retrieved.
3. Choose whether to allow sending message headers to the client in the payload.
4. Choose whether to allow sending message metadata to the client in the payload.
5. Use the drop-down menu to choose between the available options. QoS compatibility is detailed [here](../quality-of-service.md).
