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

Each rule specifies an action to take when the condition fires. Not all actions are available on every rule — refer to each policy's configuration table for the supported actions per rule.

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

## Configuring rules

### Kafka Produce Rules policy

Intercepts Kafka Produce requests in the **PUBLISH** phase. Enforces rules on producer behavior including acknowledgements, batch size, timestamp type, idempotence, record headers, and compression codec.

| Property | Type | Description | Example |
|:---------|:-----|:------------|:--------|
| `topicPatterns` | `String[]` | Java regex patterns to scope which topic names trigger rule evaluation. Empty = all topics. | `["^prod-.*", "^staging-.*"]` |
| `acks.operator` | `String` | Comparison operator: `GT`, `GTE`, `LT`, `LTE`, `EQ`. Rule fires when: `acks <operator> threshold`. | `LT` |
| `acks.threshold` | `Integer` | Value to compare against. Well-known values: 0 (none), 1 (leader), -1 (all). | `2` |
| `acks.action` | `String` | `FORBID`, `OVERRIDE`, `LOG` | `FORBID` |
| `acks.overrideValue` | `Integer` | Acks value to enforce when action is `OVERRIDE`. Required when action is `OVERRIDE`. | `-1` |
| `batchSize.operator` | `String` | `GT`, `GTE`, `LT`, `LTE`, `EQ` | `GT` |
| `batchSize.threshold` | `Integer` | Batch size in bytes. | `1048576` |
| `batchSize.action` | `String` | `FORBID`, `THROTTLE`, `LOG` | `THROTTLE` |
| `batchSize.throttleMs` | `Integer` | Milliseconds to throttle when action is `THROTTLE`. Default: `1000`. | `5000` |
| `timestampType.expected` | `String` | `CREATE_TIME` or `LOG_APPEND_TIME` | `CREATE_TIME` |
| `timestampType.action` | `String` | `FORBID`, `LOG` | `FORBID` |
| `idempotence.expected` | `String` | `"true"` = rule fires when the batch is idempotent; `"false"` = fires when not idempotent. | `"true"` |
| `idempotence.action` | `String` | `FORBID`, `LOG` | `FORBID` |
| `headers[].namePattern` | `String` | Java regex pattern matched against record header keys. | `^X-Trace-.*` |
| `headers[].matchType` | `String` | `REQUIRED` (fires when header is missing) or `FORBIDDEN` (fires when header is present). | `REQUIRED` |
| `headers[].action` | `String` | `FORBID`, `LOG` | `FORBID` |
| `compression.expected` | `String` | `NONE`, `GZIP`, `SNAPPY`, `LZ4`, `ZSTD` | `ZSTD` |
| `compression.action` | `String` | `FORBID`, `OVERRIDE`, `LOG` | `OVERRIDE` |
| `compression.overrideValue` | `String` | Compression codec to set when action is `OVERRIDE`. Values: `NONE`, `GZIP`, `SNAPPY`, `LZ4`, `ZSTD`. | `ZSTD` |

{% hint style="info" %}
Header rules are evaluated in declaration order. The first rule that fires stops further header evaluation for that record batch.
{% endhint %}

### Kafka Fetch Rules policy

Intercepts Kafka Fetch requests in the **INTERACT** phase. Enforces rules on consumer behavior including isolation level, minimum/maximum bytes, and maximum wait time.

| Property | Type | Description | Example |
|:---------|:-----|:------------|:--------|
| `topicPatterns` | `String[]` | Java regex patterns to scope which topic names trigger rule evaluation. Empty = all topics. | `["^analytics-.*"]` |
| `isolationLevel.expected` | `String` | `READ_UNCOMMITTED` or `READ_COMMITTED` | `READ_COMMITTED` |
| `isolationLevel.action` | `String` | `FORBID`, `OVERRIDE`, `LOG` | `OVERRIDE` |
| `minBytes.operator` | `String` | `GT`, `GTE`, `LT`, `LTE`, `EQ` | `LT` |
| `minBytes.threshold` | `Integer` | Minimum bytes threshold. | `1024` |
| `minBytes.action` | `String` | `FORBID`, `OVERRIDE`, `THROTTLE`, `LOG` | `OVERRIDE` |
| `minBytes.overrideValue` | `Integer` | Value to set when action is `OVERRIDE`. | `1024` |
| `minBytes.throttleMs` | `Integer` | Milliseconds to throttle when action is `THROTTLE`. | `3000` |
| `maxWaitMs.operator` | `String` | `GT`, `GTE`, `LT`, `LTE`, `EQ` | `GT` |
| `maxWaitMs.threshold` | `Integer` | Maximum wait time in milliseconds. | `10000` |
| `maxWaitMs.action` | `String` | `FORBID`, `OVERRIDE`, `THROTTLE`, `LOG` | `OVERRIDE` |
| `maxWaitMs.overrideValue` | `Integer` | Value to set when action is `OVERRIDE`. | `10000` |
| `maxWaitMs.throttleMs` | `Integer` | Milliseconds to throttle when action is `THROTTLE`. | `3000` |
| `maxBytes.operator` | `String` | `GT`, `GTE`, `LT`, `LTE`, `EQ` | `GT` |
| `maxBytes.threshold` | `Integer` | Maximum bytes threshold. | `52428800` |
| `maxBytes.action` | `String` | `FORBID`, `OVERRIDE`, `THROTTLE`, `LOG` | `FORBID` |
| `maxBytes.overrideValue` | `Integer` | Value to set when action is `OVERRIDE`. | `10485760` |
| `maxBytes.throttleMs` | `Integer` | Milliseconds to throttle when action is `THROTTLE`. | `3000` |

### Kafka Create Topic Rules policy

Intercepts Kafka CreateTopics requests in the **INTERACT** phase. Enforces topic naming conventions and configuration standards at creation time.

| Property | Type | Description | Example |
|:---------|:-----|:------------|:--------|
| `topicPatterns` | `String[]` | Java regex patterns to scope which topic names trigger rule evaluation. Empty = all topics. | `[".*"]` |
| `topicNamePattern.pattern` | `String` | Java regex the topic name is validated against. The rule fires when the name doesn't match. | `^[a-z0-9-]+$` |
| `topicNamePattern.action` | `String` | `FORBID`, `LOG` | `FORBID` |
| `numPartitions.operator` | `String` | `GT`, `GTE`, `LT`, `LTE`, `EQ` | `LT` |
| `numPartitions.threshold` | `Integer` | Number of partitions. | `10` |
| `numPartitions.action` | `String` | `FORBID`, `OVERRIDE`, `LOG` | `FORBID` |
| `numPartitions.overrideValue` | `Integer` | Value to set when action is `OVERRIDE`. | `10` |
| `replicationFactor.operator` | `String` | `GT`, `GTE`, `LT`, `LTE`, `EQ` | `LT` |
| `replicationFactor.threshold` | `Integer` | Replication factor. | `3` |
| `replicationFactor.action` | `String` | `FORBID`, `OVERRIDE`, `LOG` | `FORBID` |
| `replicationFactor.overrideValue` | `Integer` | Value to set when action is `OVERRIDE`. | `3` |
| `minInsyncReplicas.operator` | `String` | `GT`, `GTE`, `LT`, `LTE`, `EQ` | `LT` |
| `minInsyncReplicas.threshold` | `Integer` | `min.insync.replicas` topic config. | `2` |
| `minInsyncReplicas.action` | `String` | `FORBID`, `OVERRIDE`, `LOG` | `OVERRIDE` |
| `minInsyncReplicas.overrideValue` | `Integer` | Value to set when action is `OVERRIDE`. | `2` |
| `retentionMs.operator` | `String` | `GT`, `GTE`, `LT`, `LTE`, `EQ` | `GT` |
| `retentionMs.threshold` | `Integer` | `retention.ms` topic config in milliseconds. | `604800000` |
| `retentionMs.action` | `String` | `FORBID`, `OVERRIDE`, `LOG` | `FORBID` |
| `retentionMs.overrideValue` | `Integer` | Value to set when action is `OVERRIDE`. | `604800000` |
| `segmentBytes.operator` | `String` | `GT`, `GTE`, `LT`, `LTE`, `EQ` | `GT` |
| `segmentBytes.threshold` | `Integer` | `segment.bytes` topic config. | `1073741824` |
| `segmentBytes.action` | `String` | `FORBID`, `OVERRIDE`, `LOG` | `FORBID` |
| `segmentBytes.overrideValue` | `Integer` | Value to set when action is `OVERRIDE`. | `1073741824` |
| `maxMessageBytes.operator` | `String` | `GT`, `GTE`, `LT`, `LTE`, `EQ` | `GT` |
| `maxMessageBytes.threshold` | `Integer` | `max.message.bytes` topic config. | `1048576` |
| `maxMessageBytes.action` | `String` | `FORBID`, `OVERRIDE`, `LOG` | `FORBID` |
| `maxMessageBytes.overrideValue` | `Integer` | Value to set when action is `OVERRIDE`. | `1048576` |
| `compressionType.expected` | `String` | `GZIP`, `SNAPPY`, `LZ4`, `ZSTD`, `UNCOMPRESSED`, `PRODUCER` | `PRODUCER` |
| `compressionType.action` | `String` | `FORBID`, `OVERRIDE`, `LOG` | `OVERRIDE` |
| `compressionType.overrideValue` | `String` | Compression type to set when action is `OVERRIDE`. | `PRODUCER` |
| `cleanupPolicy.expected` | `String` | `DELETE`, `COMPACT`, `COMPACT_DELETE` | `DELETE` |
| `cleanupPolicy.action` | `String` | `FORBID`, `OVERRIDE`, `LOG` | `OVERRIDE` |
| `cleanupPolicy.overrideValue` | `String` | Cleanup policy to set when action is `OVERRIDE`. | `DELETE` |

### Kafka Alter Topic Rules policy

Intercepts Kafka AlterConfigs requests in the **INTERACT** phase. Enforces topic configuration standards when altering topic configs. Only evaluates `TOPIC` resource types — broker-level configs are passed through.

{% hint style="info" %}
Topic naming validation doesn't apply to Alter Topic Rules because AlterConfigs can't rename topics. For topic creation naming enforcement, use the Create Topic Rules policy.
{% endhint %}

| Property | Type | Description | Example |
|:---------|:-----|:------------|:--------|
| `topicPatterns` | `String[]` | Java regex patterns to scope which topic names trigger rule evaluation. Empty = all topics. | `["^prod-.*"]` |
| `minInsyncReplicas.operator` | `String` | `GT`, `GTE`, `LT`, `LTE`, `EQ` | `LT` |
| `minInsyncReplicas.threshold` | `Integer` | `min.insync.replicas` topic config. | `2` |
| `minInsyncReplicas.action` | `String` | `FORBID`, `OVERRIDE`, `LOG` | `FORBID` |
| `minInsyncReplicas.overrideValue` | `Integer` | Value to set when action is `OVERRIDE`. | `2` |
| `retentionMs.operator` | `String` | `GT`, `GTE`, `LT`, `LTE`, `EQ` | `LT` |
| `retentionMs.threshold` | `Integer` | `retention.ms` topic config in milliseconds. | `86400000` |
| `retentionMs.action` | `String` | `FORBID`, `OVERRIDE`, `LOG` | `FORBID` |
| `retentionMs.overrideValue` | `Integer` | Value to set when action is `OVERRIDE`. | `86400000` |
| `compressionType.expected` | `String` | `GZIP`, `SNAPPY`, `LZ4`, `ZSTD`, `UNCOMPRESSED`, `PRODUCER` | `PRODUCER` |
| `compressionType.action` | `String` | `FORBID`, `OVERRIDE`, `LOG` | `FORBID` |
| `compressionType.overrideValue` | `String` | Compression type to set when action is `OVERRIDE`. | `LZ4` |
| `cleanupPolicy.expected` | `String` | `DELETE`, `COMPACT`, `COMPACT_DELETE` | `DELETE` |
| `cleanupPolicy.action` | `String` | `FORBID`, `OVERRIDE`, `LOG` | `FORBID` |
| `cleanupPolicy.overrideValue` | `String` | Cleanup policy to set when action is `OVERRIDE`. | `DELETE` |
| `segmentBytes.operator` | `String` | `GT`, `GTE`, `LT`, `LTE`, `EQ` | `GT` |
| `segmentBytes.threshold` | `Integer` | `segment.bytes` topic config. | `1073741824` |
| `segmentBytes.action` | `String` | `FORBID`, `OVERRIDE`, `LOG` | `FORBID` |
| `segmentBytes.overrideValue` | `Integer` | Value to set when action is `OVERRIDE`. | `1073741824` |
| `maxMessageBytes.operator` | `String` | `GT`, `GTE`, `LT`, `LTE`, `EQ` | `GT` |
| `maxMessageBytes.threshold` | `Integer` | `max.message.bytes` topic config. | `1048576` |
| `maxMessageBytes.action` | `String` | `FORBID`, `OVERRIDE`, `LOG` | `FORBID` |
| `maxMessageBytes.overrideValue` | `Integer` | Value to set when action is `OVERRIDE`. | `1048576` |

## Restrictions

- Invalid regex patterns in `topicPatterns`, `topicNamePattern.pattern`, or `headers[].namePattern` cause policy initialization to fail.
- Compression override (Produce policy) rebuilds record batches, preserving per-batch metadata (magic, producer ID, epoch, sequence, transactional flag) to maintain idempotent and transactional semantics.
