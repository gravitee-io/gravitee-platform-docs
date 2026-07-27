---
description: Configuration guide for http post.
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

## Message and record mapping

Each POST request to the entrypoint produces exactly one message, built from the request body. The entrypoint doesn't split a JSON array or a multi-line body into separate messages, and it accepts no batch publishing format. To publish several records, send one request per record.

Publishing that message through a [Kafka endpoint](../endpoints/kafka.md) writes one Kafka record for each topic the producer is configured with. With a single configured topic, one request writes one record.

A request with an empty body produces no message at all, unless **Produce Empty Message Flow When Called** is enabled.
