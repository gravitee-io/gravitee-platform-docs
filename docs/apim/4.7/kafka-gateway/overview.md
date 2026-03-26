---
description: An overview about overview.
---

# Overview

The Gravitee Kafka Gateway applies Gravitee's API management capabilities directly to native Kafka to address the security, cost, and scalability issues that exist in traditional Kafka deployments.

With the Kafka Gateway, you can apply [policies](configure-kafka-apis/policies/README.md) on native Kafka topics at runtime. These policies are designed for Kafka-specific use cases. For example, you can easily restrict topic access to approved tenants or require client certificates for mTLS as an additional security layer.

The Kafka Gateway is linked to Gravitee's Developer Portal to facilitate topic availability and knowledge sharing. For example, you can publish [documentation](configure-kafka-apis/documentation.md) on Kafka topics, infrastructure, and client connections, or use a self-service mechanism to manage [subscriptions](subscriptions.md) to Kafka topics.

The Kafka Gateway natively supports the Kafka protocol and is treated like a traditional Kafka broker by consumers and producers. As a Gravitee user, you expose Kafka topics using the Gravitee concept of an API, called a [Kafka API](create-kafka-apis.md#introduction). However, consumers and producers see a regular client connection to a Kafka bootstrap server, so don't need to change existing application logic.

You can expose multiple Kafka topics within a single Kafka API, and expose multiple Kafka APIs through the Gravitee Kafka Gateway. Using the Kafka Gateway, data is processed in real time, and virtual topics and partitions enable scalable, cost-effective deployments.
