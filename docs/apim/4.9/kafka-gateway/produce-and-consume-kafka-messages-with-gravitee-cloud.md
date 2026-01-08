---
description: An overview about produce and consume kafka messages with gravitee cloud.
metaLinks:
  alternates:
    - produce-and-consume-kafka-messages-with-gravitee-cloud.md
---

# Produce and Consume Kafka Messages with Gravitee Cloud

## Overview

This guide explains how to produce and consume Kafka messages using Gravitee Cloud.

## Prerequisites

Before you produce and consume Kafka messages, complete the following steps:

* Deploy a Kafka Gateway with Gravitee Cloud. For more information about Deploying a Kafka Gateway with Gravitee Cloud, see [broken-reference](broken-reference/ "mention").

## Produce and Consume Kafka messages with Gravitee Cloud

1.  Sign in to [Gravitee Cloud](https://cloud.gravitee.io/).

    <figure><img src="../.gitbook/assets/image (272) (1).png" alt=""><figcaption></figcaption></figure>
2.  From the **Dashboard**, navigate to the **Gateways** section, and then click the Gateway that you deployed.

    <figure><img src="../.gitbook/assets/image (304) (1).png" alt=""><figcaption></figcaption></figure>
3.  In the **Gravitee Hosted Gateway Details** screen, navigate to the **Gateway Deployment Details** section, and then copy the **Kafka Domain**.

    <figure><img src="../.gitbook/assets/image (305) (1).png" alt=""><figcaption></figcaption></figure>
4.  Use the **Kafka Domain** to produce and consume Kafka messages to a topic like in the following example:

    ```bash
     ./bin/kafka-console-producer.sh \
      --bootstrap-server {apiHost}.dev-org-qa9.qa.eu.kafka-gateway.gravitee.dev:9092 \
      --topic test_topic \
      --producer.config connect.properties
    ```

    * Replace `{apiHost}` with your API entrypoint.
