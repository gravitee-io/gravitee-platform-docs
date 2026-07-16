# Kafka governance rules policies

## Overview

Kafka governance rules policies enforce compliance and operational standards on Kafka protocol requests flowing through the Gravitee API Gateway. Four policies target Produce, Fetch, CreateTopics, and AlterConfigs requests, validating fields like acknowledgements, batch size, compression, replication factor, and topic configuration against administrator-defined rules. When violations occur, the gateway can forbid the request, override values, throttle the client, or log the event.

{% hint style="info" %}
Kafka governance rules policies require an Enterprise Edition license with the `apim-native-kafka-policy-rules` feature.
{% endhint %}

## Policy suite

Four policies cover the primary Kafka client operations:

| Policy | Kafka API intercepted | Phase | Governed fields |
|:-------|:----------------------|:------|:----------------|
| **Kafka Produce Rules** | Produce (API Key 0) | PUBLISH | `acks`, batch size, timestamp type, idempotence, headers, compression type |
| **Kafka Fetch Rules** | Fetch (API Key 1) | INTERACT | `isolationLevel`, `minBytes`, `maxWaitMs`, `maxBytes` |
| **Kafka Create Topic Rules** | CreateTopics (API Key 19) | INTERACT | Topic name pattern, `numPartitions`, `replicationFactor`, topic configs (`min.insync.replicas`, `retention.ms`, `segment.bytes`, `max.message.bytes`, `compression.type`, `cleanup.policy`) |
| **Kafka Alter Topic Rules** | AlterConfigs (API Key 33) | INTERACT | Topic configs (`min.insync.replicas`, `retention.ms`, `compression.type`, `cleanup.policy`, `segment.bytes`, `max.message.bytes`) |

## Rule actions

Each rule specifies an action to take when the condition fires. Not all actions are available on every rule — refer to each policy's configuration in the APIM Console for the supported actions per rule.

| Action | Behavior |
|:-------|:---------|
| `FORBID` | Reject the request with Kafka error code `POLICY_VIOLATION` (error code 87). A human-readable message describes which rule was violated. |
| `OVERRIDE` | Rewrite the field value in-place and forward the modified request. For enum fields, the value is set to the configured override. For integer fields, an explicit `overrideValue` is required. |
| `THROTTLE` | Pause the client by setting throttle time in the response. Available on Produce batch size and Fetch integer rules only. Requires a `throttleMs` value (milliseconds). |
| `LOG` | Allow the request to pass through unchanged and emit a log entry. |

## Topic scoping

The `topicPatterns` property (available in all four policies) accepts a list of Java regex patterns. If empty, the policy applies to all topics. If populated, the policy evaluates only requests targeting topics whose names match at least one pattern.

## Rule evaluation strategy

All rule conditions are validated first without side effects. If any matched rule has action `FORBID`, the entire request is rejected and all violations are logged. Otherwise, all matched non-blocking rules (`OVERRIDE`, `THROTTLE`, `LOG`) are applied in declaration order.

## Prerequisites

- Gravitee API Gateway with native Kafka reactor enabled
- Enterprise Edition license with the `apim-native-kafka-policy-rules` feature
- API configured with a Kafka entrypoint (v4 API definition)

## Policy details

### Kafka Produce Rules policy

Intercepts Kafka Produce requests in the **PUBLISH** phase. Enforces rules on producer behavior including acknowledgements, batch size, timestamp type, idempotence, record headers, and compression.

{% hint style="info" %}
Header rules are evaluated in declaration order. The first rule that fires stops further header evaluation for that record batch.
{% endhint %}

To view all configurable properties, open a Kafka API in the APIM Console and go to **Policies** (Policy Studio). Add the Kafka Produce Rules policy to a flow and refer to its configuration form.

### Kafka Fetch Rules policy

Intercepts Kafka Fetch requests in the **INTERACT** phase. Enforces rules on consumer behavior including isolation level, minimum/maximum bytes, and maximum wait time.

To view all configurable properties, open a Kafka API in the APIM Console and go to **Policies** (Policy Studio). Add the Kafka Fetch Rules policy to a flow and refer to its configuration form.

### Kafka Create Topic Rules policy

Intercepts Kafka CreateTopics requests in the **INTERACT** phase. Enforces topic naming conventions and configuration standards at creation time.

To view all configurable properties, open a Kafka API in the APIM Console and go to **Policies** (Policy Studio). Add the Kafka Create Topic Rules policy to a flow and refer to its configuration form.

### Kafka Alter Topic Rules policy

Intercepts Kafka AlterConfigs requests in the **INTERACT** phase. Enforces topic configuration standards when altering existing topics. Only evaluates `TOPIC` resource types — broker-level configurations are passed through.

{% hint style="info" %}
Topic naming validation doesn't apply to Alter Topic Rules because AlterConfigs can't rename topics. For topic creation naming enforcement, use the Create Topic Rules policy.
{% endhint %}

To view all configurable properties, open a Kafka API in the APIM Console and go to **Policies** (Policy Studio). Add the Kafka Alter Topic Rules policy to a flow and refer to its configuration form.

## Restrictions

- Invalid regex patterns in `topicPatterns`, `topicNamePattern.pattern`, or `headers[].namePattern` cause policy initialization to fail.
- Compression override (Produce policy) rebuilds record batches, preserving per-batch metadata (magic, producer ID, epoch, sequence, transactional flag) to maintain idempotent and transactional semantics.
