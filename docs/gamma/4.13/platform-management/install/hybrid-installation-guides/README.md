---
hidden: false
noIndex: false
---
# Hybrid installation guides

## Overview

In a hybrid Gamma deployment, Gravitee hosts and manages the control plane in Gravitee Cloud, and you run the data plane (the API Gateway) in your own infrastructure. The Gateway connects to your Gravitee Cloud control plane with a Cloud Token and a License Key, and enforces policies close to your backend services.

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
