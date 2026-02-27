---
description: An overview about kafka message filtering.
metaLinks:
  alternates:
    - kafka-message-filtering.md
---

# Kafka Message Filtering

[Kafka Message Filtering](https://download.gravitee.io/#graviteeio-ee/apim/plugins/policies/gravitee-policy-kafka-message-filtering/): Lets you filter Kafka messages before they are propagated.

## Overview

You can use the `kafka-message-filtering` policy to filter the messages before they are propagated.

The Kafka Message Filtering policy uses configurable filter expressions to provide fine-grained control over which Kafka messages should be delivered to consumers. It is especially useful when multiple subscribers are interested in different subsets of messages.

This policy uses an Expression Language to evaluate each message and decide whether to propagate or discard it. This provides flexibility in filtering based on message content, headers, or subscription metadata.

## Usage

#### Example 1: Filter Messages by Header Value

**Goal:** Only allow messages where the Kafka header `eventType` equals `"order.created"`.

**Policy Configuration:**

**Filter:** `#message.headers['eventType'] == 'order.created'`

Only messages with the header `eventType=order.created` will be sent to the subscriber. Others will be discarded. If the header is missing or invalid, and `excludeMessagesOnError` is `true`, the message is not delivered.

## Phases <a href="#user-content-phases" id="user-content-phases"></a>

| onRequest | onMessageRequest | onResponseContent | onMessageResponse |
| --------- | ---------------- | ----------------- | ----------------- |
|           |                  |                   | X                 |

## Compatibility matrix <a href="#user-content-compatibility-matrix" id="user-content-compatibility-matrix"></a>

| Plugin version | APIM version  |
| -------------- | ------------- |
| 1.x            | 4.8 to latest |

## Configuration options <a href="#user-content-configuration" id="user-content-configuration"></a>

You can configure the policy with the following options:

| Property               | Required | Description                                                                                                                                                                                                                                                                                                                           | Type                         | Default |
| ---------------------- | -------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ---------------------------- | ------- |
| filter                 | X        | The filtering expression that determines which messages to include. The expression should evaluate to a boolean value. When the expression evaluates to 'true', the message is propagated; otherwise, the message is filtered out. You can use the Expression Language to access message content, headers, and subscription metadata. | string (Expression Language) | -       |
| excludeMessagesOnError |          | In case of error when evaluating filter condition, message is not sent.                                                                                                                                                                                                                                                               | boolean                      | false   |

## Examples <a href="#user-content-example" id="user-content-example"></a>

If my message looks like:

```json
{
    "key": "1234",
    "value": "any value"
}
```

I can filter messages by subscriptions metadata `keyword` using the following policy configuration:

```json
 {
    "name": "Key filter",
    "description": "Filter messages based on subscription metadata key",
    "enabled": true,
    "policy": "kafka-message-filtering",
    "configuration": {
        "filter": "#message.content.contains('#subscription.metadata.keyword')",
        "excludeMessagesOnError": false
    }
}
```
