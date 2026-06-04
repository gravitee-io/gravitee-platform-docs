# Prerequisites and Gateway Configuration for Kafka Virtual Clusters

## Prerequisites

Before creating Kafka Clusters, Virtual Clusters, or Kafka APIs, complete the following:

* **Database migration**: A migration script adds the `type`, `lifecycleState`, `deployedAt`, and `version` columns to the `clusters` table. This migration runs automatically during the upgrade process.
* **Cluster management permissions**: Users must have the `CLUSTER` environment-scoped permission (READ + UPDATE) to view and manage Kafka Clusters and Virtual Clusters. Grant this permission via **Console → Organization → Roles → USER → check the CLUSTER row**.
* **Native Kafka API logs and analytics permissions**: Grant `NATIVE_LOG` and `NATIVE_ANALYTICS` API-scoped permissions to custom roles. The built-in `OWNER` and `PRIMARY_OWNER` roles are backfilled automatically.
* **HOST routing mode configuration**: Configure `gravitee_kafka_routingHostMode_defaultDomain` via **Console → Organization → Entrypoints & Sharding Tags → Default Kafka Domain**. Each API's host prefix maps to `<prefix>.<defaultDomain>:9092`.
* **mTLS plan certificate**: A wildcard certificate covering `*.<defaultDomain>` is required for mTLS plans. mTLS plans force HOST routing mode.
* **Distributed cache for multi-pod deployments**: Configure a distributed `CacheManager` (Hazelcast or Redis) for multi-pod deployments with idempotent producers. This prevents producer ID session eviction on gateway pod failover.


## Gateway Configuration

No gateway-level configuration is required for Kafka Virtual Clusters.
