---
hidden: false
noIndex: false
description: In a hybrid Gamma deployment, Gravitee hosts the control plane and you run the Gateway. Choose a Docker or Kubernetes deployment method.
---
# Hybrid installation guides

## Overview

In a hybrid Gamma deployment, Gravitee hosts and manages the control plane in Gravitee Cloud, and you run the data plane (the API Gateway) in your own infrastructure. The Gateway connects to your Gravitee Cloud control plane with a Cloud Token and a License Key, and enforces policies close to your backend services.

An APIM 4.13 Gateway also sends traces and payload logs to Gravitee Cloud for the v4 HTTP proxy APIs that have them turned on. The **Tracing** pages show them. For what it sends and how to turn it off, see [Gateways connected to Gravitee Cloud](../../configure-opentelemetry-tracing-and-logs.md#gateways-connected-to-gravitee-cloud).

## Deployment methods

You can deploy a hybrid Gamma Gateway with Docker or Kubernetes.

### Docker

Run the hybrid Gateway on a single host with Docker.

* [Docker Compose](docker/docker-compose.md)
* [Docker CLI](docker/docker-cli.md)

### Kubernetes

Run the hybrid Gateway on a cluster with the Gravitee Helm chart.

* [Vanilla Kubernetes](kubernetes/vanilla-kubernetes.md)
* [AWS EKS](kubernetes/aws-eks.md)
* [Azure AKS](kubernetes/azure-aks.md)
* [OpenShift](kubernetes/openshift.md)
