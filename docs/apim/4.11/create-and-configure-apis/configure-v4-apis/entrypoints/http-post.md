---
description: Configure the HTTP POST entrypoint parameters for a v4 API Management 4.11 API. Follow the steps to set them for your own API.
metaLinks:
  alternates:
    - http-post.md
---

# HTTP POST

## Configuration

If you chose **HTTP POST** as an entrypoint, you can modify the following configuration parameters.

1. Choose whether to add each header from incoming request to the generated message headers.
2. Choose whether to initiate an empty message flow and give policies full access to the context whenever the POST request is made to the entrypoint.
3. Use the drop-down menu to choose between the available options. QoS compatibility is detailed [here](../quality-of-service.md).
