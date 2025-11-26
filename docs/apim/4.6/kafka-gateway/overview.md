---
description: An overview about overview.
---

# Overview

The Gravitee Kafka Gateway applies Gravitee's API management capabilities directly to native Kafka to address security, cost, and scalability issues that exist in traditional Kafka deployments. Specifically, the Kafka Gateway gives you the ability to:

* Apply [policies](policies/README.md) on Kafka topics at runtime
* [Document](configure-kafka-apis/documentation.md) how clients can connect to Kafka, and publish that information to the Developer Portal
* Manage [subscriptions](subscriptions.md) to Kafka topics via the Developer Portal in a self-service manner

Policies that can be applied at runtime on native Kafka topics are designed for Kafka-specific use cases. For example:

* The ability to "mediate" authentication to provide enhanced security
* Virtual topics and partitions to enable scalable and cost-effective deployments
* A Developer Portal to facilitate topic availability and knowledge sharing

Using these features, you can easily restrict topic access to approved tenants, publish documentation on Kafka topics and infrastructure, or require client certificates for mTLS as an additional security layer, for example.

The Kafka Gateway natively supports the Kafka protocol and is treated like a traditional Kafka broker by consumers and producers. As a Gravitee user, you expose Kafka topics using the Gravitee concept of an API - we call this a [Kafka API](create-kafka-apis.md#introduction) for clarity. However, a consumer and producer see this as a regular client connection to a Kafka bootstrap server, and therefore don't need to change existing application logic.

You can expose multiple Kafka topics within a single Kafka API, and can expose multiple Kafka APIs through the Gravitee Kafka Gateway. With the Kafka Gateway, data is processed in real time.
