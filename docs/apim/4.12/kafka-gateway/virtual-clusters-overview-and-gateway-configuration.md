# Virtual Clusters Overview and Gateway Configuration

## Overview

Kafka Cluster entities and Virtual Cluster entities provide reusable connection profiles to backend Kafka deployments. A Kafka Cluster represents a single backend Kafka cluster with one or more security configurations. A Virtual Cluster spans multiple backend clusters, presenting them as a unified virtual cluster to clients. Multiple APIs can reference the same cluster entity—changes to the cluster propagate to all referencing APIs.

This guide explains how to create and configure Kafka Cluster entities, Virtual Cluster entities, and Native Kafka APIs that reference them.


## Gateway Configuration

The gateway runs in one of two routing modes globally, controlled by the `kafka.routingMode` property:

- **HOST (default)**: Uses a single bootstrap port for all APIs. Routing relies on TLS SNI. mTLS plans require HOST mode because the SNI handshake is required for client certificate validation.
- **PORT**: Assigns each plan a dedicated bootstrap port. Routing is by local listening port.

For detailed configuration and usage instructions, refer to the [Kafka Gateway documentation](../../../kafka-gateway/).
