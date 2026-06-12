# Virtual Clusters Overview and Gateway Configuration

## Overview

Kafka Cluster Management enables API administrators to define reusable connection profiles to Kafka backends and reference them across multiple APIs. Instead of duplicating bootstrap server addresses and security credentials in every API definition, you create a Kafka Cluster entity once and reference it by cross-environment identifier. Virtual Clusters extend this model by aggregating multiple backend clusters into a single logical endpoint for fan-out scenarios.

## Gateway Configuration

### Routing Mode

The gateway operates in one of two routing modes, controlled by the `kafka.routingMode` property:

| Property | Value | Description |
|:---------|:------|:------------|
| `kafka.routingMode` | `HOST` (default) | Single bootstrap port (9092) for all APIs. Routing relies on TLS SNI — the gateway dispatches on `<apiPrefix>.<defaultDomain>` and `broker-<N>-<apiPrefix>.<defaultDomain>`. Requires a wildcard certificate covering `*.<defaultDomain>`. mTLS plans force HOST mode. |
| `kafka.routingMode` | `PORT` | Each plan gets a dedicated bootstrap port and broker-port range (configured at plan level via `bootstrapPort`). Routing is by local listening port; no SNI dispatch. Use when wildcard certificates are not acceptable or when clients cannot perform SNI. |
