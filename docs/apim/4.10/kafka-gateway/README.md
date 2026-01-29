---
description: Configuration guide for kafka gateway.
metaLinks:
  alternates:
    - ./
---

# Kafka Gateway

The Gravitee Kafka Gateway applies Gravitee's API management capabilities directly to native Kafka to address the security, cost, and scalability issues that exist in traditional Kafka deployments.

With the Kafka Gateway, you can apply [policies](create-and-configure-kafka-apis/configure-kafka-apis/policies.md) on native Kafka topics at runtime. These policies are designed for Kafka-specific use cases. For example, you can easily restrict topic access to approved tenants or require client certificates for mTLS as an additional security layer.

The Kafka Gateway is linked to Gravitee's Developer Portal to facilitate topic availability and knowledge sharing. For example, you can publish [documentation](create-and-configure-kafka-apis/configure-kafka-apis/documentation.md) on Kafka topics, infrastructure, and client connections, or use a self-service mechanism to manage [subscriptions](subscriptions.md) to Kafka topics.

The Kafka Gateway natively supports the Kafka protocol and is treated like a traditional Kafka broker by consumers and producers. As a Gravitee user, you expose Kafka topics using the Gravitee concept of an API, called a [Kafka API](create-and-configure-kafka-apis/create-kafka-apis.md#introduction). However, consumers and producers see a regular client connection to a Kafka bootstrap server, so don't need to change existing application logic.

You can expose multiple Kafka topics within a single Kafka API, and expose multiple Kafka APIs through the Gravitee Kafka Gateway. Using the Kafka Gateway, data is processed in real time, and virtual topics and partitions enable scalable, cost-effective deployments.

To learn more about the Kafka Gateway, see the following articles:

<table data-view="cards"><thead><tr><th></th><th data-hidden data-card-target data-type="content-ref"></th></tr></thead><tbody><tr><td>Configure the Kafka Client &#x26; gateway</td><td><a href="configure-the-kafka-client-and-gateway.md">configure-the-kafka-client-and-gateway.md</a></td></tr><tr><td>Create &#x26; Configure Kafka APIs</td><td><a href="create-and-configure-kafka-apis/">create-and-configure-kafka-apis</a></td></tr><tr><td>Plans</td><td><a href="plans.md">plans.md</a></td></tr><tr><td>Applications</td><td><a href="applications.md">applications.md</a></td></tr><tr><td>Subscriptions</td><td><a href="subscriptions.md">subscriptions.md</a></td></tr><tr><td>Other ways Gravitee supports Kafka</td><td><a href="other-ways-gravitee-supports-kafka.md">other-ways-gravitee-supports-kafka.md</a></td></tr></tbody></table>
