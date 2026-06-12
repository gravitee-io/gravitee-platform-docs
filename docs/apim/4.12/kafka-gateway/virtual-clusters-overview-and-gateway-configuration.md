# Virtual Clusters Overview and Gateway Configuration

## Overview

Virtual clusters enable a single Kafka API to span multiple backend Kafka clusters, presenting them to clients as one unified cluster. Clients connect to a single bootstrap address and interact with topics distributed across backends without awareness of the underlying topology. This capability is designed for API platform administrators managing multi-region or multi-tenant Kafka deployments.

## Key Concepts

### Virtual Cluster

A virtual cluster is a fan-out wrapper that aggregates two or more backend Kafka clusters into a single logical cluster. It owns a list of backend references, each pairing a Kafka Cluster entity with one of its connections. The gateway merges metadata from all backends, remaps broker IDs to a unified virtual address space, and routes client requests to the appropriate backend based on topic ownership.

### Kafka Cluster Entity

A reusable connection profile to a real Kafka backend. Each Kafka Cluster entity contains one or more connections, each specifying bootstrap servers and security configuration (PLAINTEXT, SSL, SASL_PLAINTEXT, or SASL_SSL). Multiple APIs can reference the same Kafka Cluster entity; updates to the entity propagate to all referencing APIs.

### Backend

A backend is a `(clusterCrossId, connectionCrossId)` pair within a virtual cluster configuration. It identifies one connection from a Kafka Cluster entity. A virtual cluster requires a minimum of two backends to enable multi-cluster routing.

### Virtual Broker ID Mapping

The gateway assigns each backend cluster a non-overlapping broker ID range. Backend cluster 0 uses virtual IDs 10000–19999, cluster 1 uses 20000–29999, and so on. Real broker IDs (0–9999) are remapped to virtual IDs when served to clients. This mapping supports up to 214,748 backend clusters, each with up to 10,000 brokers.

| Backend Cluster Index | Virtual Broker ID Range | Real Broker ID Range |
|:----------------------|:------------------------|:---------------------|
| 0 | 10000–19999 | 0–9999 |
| 1 | 20000–29999 | 0–9999 |
| N | (N+1)×10000 – (N+2)×10000−1 | 0–9999 |

### Topic-to-Cluster Routing

The gateway routes requests to the backend cluster that owns the target topic. Topic ownership is determined by topic ID (UUID) when available, falling back to topic name. When the same topic name exists on multiple backends, the first backend in configuration order wins. Internal topics (names starting with `__`, such as `__consumer_offsets`) are excluded from merged metadata.

### Consumer Group Routing

Consumer groups are routed to the backend cluster that owns the topics in the group's subscription. The gateway caches the `groupId → clusterIndex` mapping after the first successful join.  When a group's subscription spans multiple clusters, the gateway either rejects the request (classic protocol) or multiplexes the group across backends (KIP-848 protocol). Cross-cluster subscriptions in classic protocol mode return `INVALID_REQUEST` with the message:

```
Cross-cluster subscription is not supported in MESH mode (group '{groupId}' subscribes to topics that span clusters {clusters}). Split the subscription into per-cluster groups, mirror the topics, or use single-cluster routing.
```

### Shadow Groups

When multiplexing a consumer group across backends (KIP-848 protocol only), the gateway creates one shadow group per backend cluster. Shadow group IDs follow the format `<clientGroupId>__shadow-c<clusterIndex>`. Client group IDs matching the regex `.*__shadow-c\d+$` are rejected with `INVALID_GROUP_ID` to prevent collisions. Group IDs containing `__shadow-c` without a trailing digit (e.g., `orders__shadow-counter`) are permitted.

### Metadata Merge

The gateway fetches metadata from all backend clusters in parallel and merges the results into a single response. Brokers from all backends are included with virtual ID remapping. Topics are deduplicated by ID; name collisions are resolved by first-cluster-wins. The controller ID is taken from the first backend and remapped to a virtual ID. The cluster ID is a synthetic UUID derived from the virtual cluster's cross-environment identifier.

## Prerequisites

- **Kafka Cluster entities**: At least two Kafka Cluster entities must be configured in the environment, each with at least one connection.
- **Cluster management permissions**: Users must have the `CLUSTER` environment-scoped permission (READ + UPDATE) to create and manage Kafka Cluster and Virtual Cluster entities. Grant this permission via Console → Organization → Roles → [role name] → check the CLUSTER row.
- **API-scoped permissions** (for API owners): `NATIVE_LOG` and `NATIVE_ANALYTICS` permissions on the API scope are required to view native Kafka API logs and analytics. These are automatically granted to built-in `OWNER` and `PRIMARY_OWNER` roles during upgrade; custom roles require manual grants.
- **Default Kafka domain** (HOST routing mode): The gateway must have a default domain configured for SNI-based routing. Set this via Console → Organization → Entrypoints & Sharding Tags → **Default Kafka Domain**. The domain is used to construct SNI hostnames in the format `<apiPrefix>.<defaultDomain>:9092`.
- **Wildcard certificate** (HOST routing mode): A wildcard TLS certificate covering `*.<defaultDomain>` is required when using HOST routing mode (the default). mTLS plans always require HOST mode.

## Gateway Configuration

### Routing Mode

The gateway operates in one of two routing modes, controlled by the `kafka.routingMode` property:

| Property | Value | Description |
|:---------|:------|:------------|
| `kafka.routingMode` | `host` (default) | Single bootstrap port (9092) for all APIs. Routing relies on TLS SNI; the gateway dispatches on `<apiPrefix>.<defaultDomain>` and `broker-<N>-<apiPrefix>.<defaultDomain>`. Requires a wildcard certificate. mTLS plans force HOST mode. |
| `kafka.routingMode` | `port` | Each plan receives a dedicated bootstrap port and broker-port range (configured at plan level via `bootstrapPort`). Routing is by local listening port; no SNI dispatch. No wildcard certificate required. |

### Timeout Configuration

| Property | Default | Description |
|:---------|:--------|:------------|
| `SHADOW_HEARTBEAT_TIMEOUT` | 3 seconds | Per-shadow timeout for cross-cluster ConsumerGroupHeartbeat fan-out (KIP-848 multiplex). |
| `BACKEND_CALL_TIMEOUT` | 5 seconds | Per-call timeout when forwarding requests to a backend cluster (AlterConfigs, CreatePartitions, DeleteGroups, DeleteRecords, DeleteTopics, DescribeConfigs, DescribeGroups, ConsumerGroupDescribe, OffsetDelete). |
| `BACKEND_FORWARD_TIMEOUT` | 10 seconds | Per-call timeout when forwarding gateway-internal requests (probe, FindCoordinator) to a backend. |
| `METADATA_FETCH` | 10 seconds | Metadata fetch timeout per backend cluster. |
| `RETRY_BACKOFF` | 300 milliseconds | Backoff duration between retry attempts on transient coordinator-load errors. |

### Shadow Coordinator Warm-Up

| Property | Default | Description |
|:---------|:--------|:------------|
| `SHADOW_FIND_COORDINATOR_VERSION` | 4 | FIND_COORDINATOR API version used for shadow coordinator warm-up. |
| `SHADOW_WARMUP_MAX_RETRIES` | 5 | Maximum retries for shadow coordinator warm-up. |
| `SHADOW_WARMUP_BACKOFF` | 50 milliseconds | Backoff duration between shadow coordinator warm-up retries. |

### Probe Configuration

| Property | Default | Description |
|:---------|:--------|:------------|
| `PROBE_TIMEOUT_MS` | 5000 | Total timeout for Kafka gateway bind probe. |
| `PROBE_CONNECT_MS` | 500 | Connect timeout for individual probe attempt. |
| `PROBE_RETRY_INTERVAL_MS` | 100 | Interval between probe retry attempts. |

### Integration Test Resources

| Property | Default | Description |
|:---------|:--------|:------------|
| **Test Job Resource Class** | `large` | CircleCI resource class (8 GB RAM) for integration test runners to accommodate parallel ConfluentKafka testcontainers plus gateway under test. |
