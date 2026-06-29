---
hidden: false
noIndex: false
---
# Self-hosted installation guides

## Overview

A fully self-hosted Gamma installation runs every component in your own infrastructure: the Management API with Gamma enabled, the API Gateway, the Gamma console, the APIM Console, the Developer Portal, and the MongoDB and Elasticsearch datastores. Choose one of the following deployment methods.

## Deployment methods

You can install a fully self-hosted Gamma platform with Docker or Kubernetes.

### Docker

Run the whole platform on a single host with Docker.

* [Docker Compose](docker/docker-compose.md)
* [Docker CLI](docker/docker-cli.md)

### Kubernetes

Run the platform on a cluster with the Gravitee Helm chart.

* [Vanilla Kubernetes](kubernetes/vanilla-kubernetes.md)
* [AWS EKS](kubernetes/aws-eks.md)
* [Azure AKS](kubernetes/azure-aks.md)
* [OpenShift](kubernetes/openshift.md)
