# Kafka Governance Rules Policies

## Overview

Kafka Governance Rules Policies enforce compliance and operational standards on Kafka protocol requests flowing through the Gravitee API Gateway. Four policies target Produce, Fetch, CreateTopics, and AlterConfigs requests, validating fields like acknowledgements, batch size, compression, replication factor, and topic configuration against administrator-defined rules. When violations occur, the gateway can forbid the request, override values, throttle the client, or log the event.

## Key Concepts

### Policy Suite

Four policies cover the primary Kafka client operations:

| Policy | Target Request | Governed Fields |
|:-------|:---------------|:----------------|
| **Kafka Produce Rules** | ProduceRequest | `acks`, batch size, timestamp type, idempotence, headers, compression type |
| **Kafka Fetch Rules** | FetchRequest | `isolationLevel`, `minBytes`, `maxWaitMs`, `maxBytes` |
| **Kafka Create Topic Rules** | CreateTopicsRequest | Topic name pattern, `numPartitions`, `replicationFactor`, topic configs (`min.insync.replicas`, `retention.ms`, `segment.bytes`, `max.message.bytes`, `compression.type`, `cleanup.policy`) |
| **Kafka Alter Topic Rules** | AlterConfigsRequest (TOPIC resource) | Topic configs (`min.insync.replicas`, `retention.ms`, `compression.type`, `cleanup.policy`, `segment.bytes`, `max.message.bytes`) |

### Rule Actions

Each rule specifies an action to take when the condition fires:

| Action | Behavior |
|:-------|:---------|
| `FORBID` | Reject the request with Kafka error code `POLICY_VIOLATION` |
| `OVERRIDE` | Rewrite the field value in-place and forward the modified request |
| `THROTTLE` | Pause the client by setting throttle time in the response (Produce/Fetch only) |
| `LOG` | Emit an info-level log entry and pass the request through unchanged |

### Topic Scoping

The `topicPatterns` property (available in all four policies) accepts a list of Java regex patterns. If empty, the policy applies to all topics. If populated, the policy evaluates only requests targeting topics whose names match at least one pattern. For Fetch requests, the gateway persists the scope decision on the connection context when a new fetch session is established (`sessionId == 0`), then reuses that decision for incremental fetches in the same session.

### Rule Evaluation Strategy

All rule conditions are validated first without side effects. If any matched rule has action `FORBID`, the entire request is rejected and all violations are logged. Otherwise, all matched non-blocking rules (`OVERRIDE`, `THROTTLE`, `LOG`) are applied in declaration order.

## Prerequisites

- Gravitee API Gateway with native Kafka reactor enabled
- License feature flag `apim-native-kafka-policy-rules` enabled
- API configured with a Kafka entrypoint (v4 API definition)

## Gateway Configuration

### Policy Installation

The four policy plugins are bundled in the Gravitee APIM distribution as zip artifacts. No manual installation is required when using the official distribution.

### Feature Flag

Enable the Kafka rules policies via license feature flag:

| Feature Flag | Description |
|:-------------|:------------|
| `apim-native-kafka-policy-rules` | Enables all four Kafka governance rules policies |

## Creating a Kafka Governance Rule

Add one or more Kafka rules policies to a Kafka-enabled API plan or flow. Configure the policy by enabling individual rules and setting their parameters. For example, to enforce minimum acknowledgements on produce requests: (1) add the Kafka Produce Rules policy to the plan, (2) enable the `acks` rule, (3) set `operator` to `LT`, `threshold` to `2`, and `action` to `FORBID`. The gateway will reject any ProduceRequest with `acks < 2`. To enforce a topic naming convention: (1) add the Kafka Create Topic Rules policy, (2) enable the `topicNamePattern` rule, (3) set `pattern` to `^[a-z0-9-]+$` and `action` to `FORBID`. The gateway will reject CreateTopicsRequest for any topic name that does not match the pattern.

## Configuring Rules

### Kafka Produce Rules Policy

| Property | Type | Description | Example |
|:---------|:-----|:------------|:--------|
| `topicPatterns` | `List<String>` | Java regex patterns to scope which topic names trigger rule evaluation. Empty = all topics. | `["^prod-.*", "^staging-.*"]` |
| `acks.operator` | `String` | Comparison operator: `GT`, `GTE`, `LT`, `LTE`, `EQ`. Rule fires when: `acks <operator> threshold`. | `LT` |
| `acks.threshold` | `Integer` | Value to compare against. | `2` |
| `acks.action` | `String` | `FORBID`, `OVERRIDE`, `LOG` | `FORBID` |
| `acks.overrideValue` | `Integer` | Value to set when action is `OVERRIDE`. | `2` |
| `batchSize.operator` | `String` | `GT`, `GTE`, `LT`, `LTE`, `EQ` | `GT` |
| `batchSize.threshold` | `Integer` | Batch size in bytes. | `1048576` |
| `batchSize.action` | `String` | `FORBID`, `THROTTLE`, `LOG` | `THROTTLE` |
| `batchSize.throttleMs` | `Integer` | Milliseconds to throttle when action is `THROTTLE`. | `5000` |
| `timestampType.expected` | `String` | `CREATE_TIME` or `LOG_APPEND_TIME` | `CREATE_TIME` |
| `timestampType.action` | `String` | `FORBID`, `LOG` | `FORBID` |
| `idempotence.expected` | `Boolean` | `true` = require idempotent batches, `false` = forbid idempotent batches | `true` |
| `idempotence.action` | `String` | `FORBID`, `LOG` | `FORBID` |
| `headers[].namePattern` | `String` | Java regex pattern for header key. | `^X-Trace-.*` |
| `headers[].matchType` | `String` | `REQUIRED` or `FORBIDDEN` | `REQUIRED` |
| `headers[].action` | `String` | `FORBID`, `LOG` | `FORBID` |
| `compression.expected` | `String` | `NONE`, `GZIP`, `SNAPPY`, `LZ4`, `ZSTD` | `ZSTD` |
| `compression.action` | `String` | `FORBID`, `OVERRIDE`, `LOG` | `OVERRIDE` |
| `compression.overrideValue` | `String` | Compression codec to set when action is `OVERRIDE`. | `ZSTD` |

### Kafka Fetch Rules Policy

| Property | Type | Description | Example |
|:---------|:-----|:------------|:--------|
| `topicPatterns` | `List<String>` | Java regex patterns to scope which topic names trigger rule evaluation. | `["^analytics-.*"]` |
| `isolationLevel.expected` | `String` | `READ_UNCOMMITTED` or `READ_COMMITTED` | `READ_COMMITTED` |
| `isolationLevel.action` | `String` | `FORBID`, `OVERRIDE`, `LOG` | `OVERRIDE` |
| `minBytes.operator` | `String` | `GT`, `GTE`, `LT`, `LTE`, `EQ` | `LT` |
| `minBytes.threshold` | `Integer` | Minimum bytes. | `1024` |
| `minBytes.action` | `String` | `FORBID`, `OVERRIDE`, `THROTTLE`, `LOG` | `OVERRIDE` |
| `minBytes.overrideValue` | `Integer` | Value to set when action is `OVERRIDE`. | `1024` |
| `minBytes.throttleMs` | `Integer` | Milliseconds to throttle when action is `THROTTLE`. | `3000` |
| `maxWaitMs.operator` | `String` | `GT`, `GTE`, `LT`, `LTE`, `EQ` | `GT` |
| `maxWaitMs.threshold` | `Integer` | Maximum wait time in milliseconds. | `10000` |
| `maxWaitMs.action` | `String` | `FORBID`, `OVERRIDE`, `THROTTLE`, `LOG` | `OVERRIDE` |
| `maxBytes.operator` | `String` | `GT`, `GTE`, `LT`, `LTE`, `EQ` | `GT` |
| `maxBytes.threshold` | `Integer` | Maximum bytes. | `52428800` |
| `maxBytes.action` | `String` | `FORBID`, `OVERRIDE`, `THROTTLE`, `LOG` | `FORBID` |

### Kafka Create Topic Rules Policy

| Property | Type | Description | Example |
|:---------|:-----|:------------|:--------|
| `topicPatterns` | `List<String>` | Java regex patterns to scope which topic names trigger rule evaluation. | `[".*"]` |
| `topicNamePattern.pattern` | `String` | Java regex pattern. Topic name must match this pattern. | `^[a-z0-9-]+$` |
| `topicNamePattern.action` | `String` | `FORBID`, `LOG` | `FORBID` |
| `numPartitions.operator` | `String` | `GT`, `GTE`, `LT`, `LTE`, `EQ` | `LT` |
| `numPartitions.threshold` | `Integer` | Number of partitions. | `10` |
| `numPartitions.action` | `String` | `FORBID`, `OVERRIDE`, `THROTTLE`, `LOG` | `FORBID` |
| `replicationFactor.operator` | `String` | `GT`, `GTE`, `LT`, `LTE`, `EQ` | `LT` |
| `replicationFactor.threshold` | `Integer` | Replication factor. | `3` |
| `replicationFactor.action` | `String` | `FORBID`, `OVERRIDE`, `THROTTLE`, `LOG` | `FORBID` |
| `minInsyncReplicas.operator` | `String` | `GT`, `GTE`, `LT`, `LTE`, `EQ` | `LT` |
| `minInsyncReplicas.threshold` | `Integer` | `min.insync.replicas` topic config. | `2` |
| `minInsyncReplicas.action` | `String` | `FORBID`, `OVERRIDE`, `THROTTLE`, `LOG` | `OVERRIDE` |
| `retentionMs.operator` | `String` | `GT`, `GTE`, `LT`, `LTE`, `EQ` | `GT` |
| `retentionMs.threshold` | `Long` | `retention.ms` topic config in milliseconds. | `604800000` |
| `retentionMs.action` | `String` | `FORBID`, `OVERRIDE`, `THROTTLE`, `LOG` | `FORBID` |
| `segmentBytes.operator` | `String` | `GT`, `GTE`, `LT`, `LTE`, `EQ` | `GT` |
| `segmentBytes.threshold` | `Integer` | `segment.bytes` topic config. | `1073741824` |
| `segmentBytes.action` | `String` | `FORBID`, `OVERRIDE`, `THROTTLE`, `LOG` | `FORBID` |
| `maxMessageBytes.operator` | `String` | `GT`, `GTE`, `LT`, `LTE`, `EQ` | `GT` |
| `maxMessageBytes.threshold` | `Integer` | `max.message.bytes` topic config. | `1048576` |
| `maxMessageBytes.action` | `String` | `FORBID`, `OVERRIDE`, `THROTTLE`, `LOG` | `FORBID` |
| `compressionType.expected` | `String` | `GZIP`, `SNAPPY`, `LZ4`, `ZSTD`, `UNCOMPRESSED`, `PRODUCER` | `PRODUCER` |
| `compressionType.action` | `String` | `FORBID`, `OVERRIDE`, `LOG` | `OVERRIDE` |
| `compressionType.overrideValue` | `String` | Compression type to set when action is `OVERRIDE`. | `PRODUCER` |
| `cleanupPolicy.expected` | `String` | `DELETE`, `COMPACT`, `COMPACT_DELETE` | `DELETE` |
| `cleanupPolicy.action` | `String` | `FORBID`, `OVERRIDE`, `LOG` | `OVERRIDE` |
| `cleanupPolicy.overrideValue` | `String` | Cleanup policy to set when action is `OVERRIDE`. | `DELETE` |

### Kafka Alter Topic Rules Policy

| Property | Type | Description | Example |
|:---------|:-----|:------------|:--------|
| `topicPatterns` | `List<String>` | Java regex patterns to scope which topic names trigger rule evaluation. | `["^prod-.*"]` |
| `minInsyncReplicas.operator` | `String` | `GT`, `GTE`, `LT`, `LTE`, `EQ` | `LT` |
| `minInsyncReplicas.threshold` | `Integer` | `min.insync.replicas` topic config. | `2` |
| `minInsyncReplicas.action` | `String` | `FORBID`, `OVERRIDE`, `THROTTLE`, `LOG` | `FORBID` |
| `retentionMs.operator` | `String` | `GT`, `GTE`, `LT`, `LTE`, `EQ` | `LT` |
| `retentionMs.threshold` | `Long` | `retention.ms` topic config in milliseconds. | `86400000` |
| `retentionMs.action` | `String` | `FORBID`, `OVERRIDE`, `THROTTLE`, `LOG` | `FORBID` |
| `compressionType.expected` | `String` | `GZIP`, `SNAPPY`, `LZ4`, `ZSTD`, `UNCOMPRESSED`, `PRODUCER` | `PRODUCER` |
| `compressionType.action` | `String` | `FORBID`, `OVERRIDE`, `LOG` | `FORBID` |
| `cleanupPolicy.expected` | `String` | `DELETE`, `COMPACT`, `COMPACT_DELETE` | `DELETE` |
| `cleanupPolicy.action` | `String` | `FORBID`, `OVERRIDE`, `LOG` | `FORBID` |
| `segmentBytes.operator` | `String` | `GT`, `GTE`, `LT`, `LTE`, `EQ` | `GT` |
| `segmentBytes.threshold` | `Integer` | `segment.bytes` topic config. | `1073741824` |
| `segmentBytes.action` | `String` | `FORBID`, `OVERRIDE`, `THROTTLE`, `LOG` | `FORBID` |
| `maxMessageBytes.operator` | `String` | `GT`, `GTE`, `LT`, `LTE`, `EQ` | `GT` |
| `maxMessageBytes.threshold` | `Integer` | `max.message.bytes` topic config. | `1048576` |
| `maxMessageBytes.action` | `String` | `FORBID`, `OVERRIDE`, `THROTTLE`, `LOG` | `FORBID` |

## End-User Configuration

No end-user configuration is required for Kafka Governance Rules Policies.

## Restrictions

- Requires Gravitee API Gateway with native Kafka reactor enabled
- Requires license feature flag `apim-native-kafka-policy-rules`
- Only applies to v4 APIs with Kafka entrypoints
- Header rules (Produce policy) are evaluated in declaration order; the first matching rule fires and stops further evaluation
- Compression override (Produce policy) rebuilds record batches, preserving per-batch metadata (magic, producer ID, epoch, sequence, transactional flag) to maintain idempotent and transactional semantics
- Fetch session scoping: for incremental fetch requests (empty topic list, `sessionId != 0`), the gateway looks up the scope decision from the connection context; if the session is not found, the request is considered out of scope and skipped
- Invalid regex patterns in `topicPatterns`, `topicNamePattern.pattern`, or `headers[].namePattern` will cause policy initialization to fail
- Unrecognized compression type or cleanup policy values in topic configs are logged as violations but do not halt request processing unless action is `FORBID`

## Related Changes

The four policies are packaged as separate zip artifacts and included in the Gravitee APIM distribution. The shared module `gravitee-policy-kafka-rules-shared` provides common rule types, validation logic, topic scoping, and throttle actions. Integration tests in `gravitee-reactor-native-kafka` validate all four policies against a live Kafka broker. The license model in `gravitee-node` was updated to include the `apim-native-kafka-policy-rules` feature flag. No UI or console changes are included in the manifest.
