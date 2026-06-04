# Kafka Virtual Cluster & Multi-Cluster Routing Overview

## Overview

Kafka Virtual Cluster & Multi-Cluster Routing enables API administrators to aggregate multiple Kafka clusters behind a single virtual endpoint and route client requests across backend clusters transparently. This feature supports idempotent producer sessions, SASL credential replay for cross-cluster operations, and lifecycle management for deployed clusters. It is designed for platform teams managing multi-region or multi-tenant Kafka infrastructures.

{% hint style="info" %}
**Minimum version**: Gravitee API Management 4.12.0 or later

**Database migration required**: A new `type` column is added to the `clusters` table.
{% endhint %}
