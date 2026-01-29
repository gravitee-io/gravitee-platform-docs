---
description: An overview about kafka transform key.
metaLinks:
  alternates:
    - >-
      https://app.gitbook.com/s/bGmDEarvnV52XdcOiV8o/create-and-configure-apis/apply-policies/policy-reference/kafka-transform-key
---

# Kafka Transform Key

## Overview

The Gravitee Kafka Transform Key policy adds a custom Kafka message key to your messages so that you can customize partitioning and perform general actions. For example, ordering the transactions. With this policy, you control the Key of a Kafka record, and the policy enables you to use Expression Language.

## Usage

Use cases for this policy:

#### **Ensure message order for each business entity**

* **Example:** Banking transactions, order processing, user profile updates.
* **Why:** Kafka guarantees ordering within a partition. By assigning a key like `userId` or `accountId`, all related events are routed to the same partition, which ensures that they are processed in order.

#### **Improving partition load-balancing**

* **Example:** High-frequency system logs or telemetry data.
* **Why:** Using a key such as `hostId` or `serviceId` helps distribute messages across partitions, improving throughput and consumer parallelism.

#### **Targeted consumption or filtering**

* **Example:** A consumer that wants messages from only a specific `regionId` or `productType`.
* **Why:** Including such information in the key allows smarter routing or filtering by consumers.

## Phases <a href="#user-content-phases" id="user-content-phases"></a>

This policy can be applied on the Publish and Subscribe phase.

## Compatibility matrix <a href="#user-content-compatibility-with-apim" id="user-content-compatibility-with-apim"></a>

| Plugin version | APIM version    |
| -------------- | --------------- |
| 1.0.x          | 4.8.x or higher |

## Configuration options <a href="#user-content-configuration" id="user-content-configuration"></a>

You can configure the policy with the following options:

| Property                | Required | Description                                                                                           | Type    | Default |
| ----------------------- | -------- | ----------------------------------------------------------------------------------------------------- | ------- | ------- |
| key                     | No       | Custom kafka message key for your messages. Supports EL.                                              | String  |         |
| setUnresolvedKeysToNull | No       | When enabled, and the expression results in an error, set the key to null. Otherwise, throw an error. | Boolean | false   |
