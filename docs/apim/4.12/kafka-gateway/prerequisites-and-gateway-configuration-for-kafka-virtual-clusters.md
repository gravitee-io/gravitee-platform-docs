# Prerequisites and Gateway Configuration for Kafka Virtual Clusters

## Prerequisites

Before enabling Kafka Virtual Cluster & Multi-Cluster Routing, ensure the following requirements are met:

* Gravitee API Management 4.12.0 or later
* Database migration completed (adds a new `type` column to the `clusters` table)
* For idempotent producer support: distributed `CacheManager` (Hazelcast or Redis) configured in `gravitee.yml`
* For SASL delegate replay: backend clusters must accept the `PLAIN` mechanism


