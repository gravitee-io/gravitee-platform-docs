---
description: Gravitee Kubernetes Operator 4.8 Release Notes.
---

# GKO 4.8

**Release Date:** 2025/06/23

## Highlights

**Kubernetes Gateway API Support**: Introduced native support for the Kubernetes Gateway API with GatewayClassParameters custom resource, enabling standardized Kubernetes networking integration alongside existing GKO capabilities to APIM Gateways deployment.

**KafkaRoute for Gateway API**: Introduced the KafkaRoute custom resource that extends the Kubernetes Gateway API to support Kafka messaging, enabling unified gateway management for both HTTP and event-driven communications.

**Notification Support**: Introduced notification capabilities for API definitions resources, enabling automated alerts and status updates for API lifecycle events.

## Product

### New Features

#### Kubernetes Gateway API

Introduced foundational Kubernetes Gateway API support as the first step toward full Gateway API conformance:

- **GatewayClassParameters**: Configuration resource for Gravitee's Gateway API implementation
- **Licensing Integration**: Built-in support for Gravitee licensing within Gateway API resources
- **Kafka Configuration**: Native Kafka cluster connectivity configuration through Gateway API

**Current Limitations**: This initial implementation focuses on core Gateway API functionality. ReferenceGrant and GRPCRoute resources are not yet supported but are planned for future releases as we work toward full Gateway API conformance.

#### KafkaRoute Custom Resource

Added KafkaRoute support that extends Gateway API to Kafka messaging:
- **Gateway API Compliance**: Leverages standard Gateway API patterns for Kafka topic management
- **First-Class Kafka Support**: Treats Kafka message brokers as first-class citizens of the Gateway API

#### Notification Support

Added comprehensive notification capabilities for GKO-managed resources:

- **API Lifecycle Notifications**: Automated alerts for API deployment, updates, and status changes
- **Group Support for Notifications**: Define user groups as notification targets, making it easy to reach multiple recipients at once.
 
### Updates

#### Helm

- **Monitoring & Prometheus Integration**
  
  Refactored the monitoring stack by removing the `kube-rbac-proxy` and now exposing metrics directly via a dedicated metrics service. Authentication is now handled natively by the Operator manager.  
  Prometheus integration can be enabled and customized via Helm values, including automatic generation of `ServiceMonitor` and `PodMonitor` resources.

  Refer our [monitoring quickstart](https://github.com/gravitee-io/gravitee-kubernetes-operator/tree/master/docs/guides/monitoring) for more detailed setup instructions.
