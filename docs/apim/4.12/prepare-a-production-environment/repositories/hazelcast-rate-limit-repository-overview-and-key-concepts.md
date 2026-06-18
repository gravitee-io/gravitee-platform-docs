---
hidden: true
noIndex: true
---

# Hazelcast Rate-Limit Repository Overview and Key Concepts

## Overview

The Hazelcast rate-limit repository is a distributed rate-limiting backend for Gravitee API Management gateways. It stores rate-limit counters in an embedded Hazelcast cluster, enabling accurate quota enforcement across multiple gateway replicas without requiring external databases. Administrators deploy it by setting `ratelimit.type: hazelcast` and configuring cluster discovery via XML or YAML.

## Key Concepts

### Distributed Counter Storage

Rate-limit counters are stored in a Hazelcast IMap named `rate-limits`, where each entry contains the current counter value, limit, reset time, and subscription identifier. Entries automatically evict when their time window closes (TTL derived from `resetTime - now`, floored at 1ms to prevent infinite retention). When a request increments a counter, the repository checks if the existing entry's reset time is still valid; if expired or missing, it creates a new entry from the policy's default configuration.

### Cluster Independence

The rate-limit Hazelcast instance operates independently of `cluster.type=hazelcast` and `cache.type=hazelcast`. Each subsystem forms its own logical cluster identified by a distinct `<cluster-name>` in the XML configuration (default: `graviteeio-apim-ratelimit`). To avoid port collisions when multiple Hazelcast subsystems run in the same JVM, the rate-limit instance defaults to port 5901 (cluster uses 5701, cache uses 5801), with `auto-increment="true"` enabled.

### Kubernetes Discovery

In Kubernetes deployments, the Helm chart auto-configures Hazelcast to discover peers via the Kubernetes API. It creates a ClusterIP service (`{{ .Release.Name }}-gateway-hz`) and grants the gateway ServiceAccount permissions to list endpoints, pods, nodes, and services in the release namespace. Each gateway pod joins the cluster by querying the service for peer addresses.

## Prerequisites

- Gravitee API Management gateway (version supporting `ratelimit.type=hazelcast`)
- For Kubernetes deployments: `apim.managedServiceAccount: true` in Helm values (or manually grant RBAC permissions for Hazelcast discovery)
- For standalone deployments: Hazelcast XML or YAML configuration file with TCP-IP join configured
