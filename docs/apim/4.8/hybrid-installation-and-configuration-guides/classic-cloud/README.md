---
description: The technology stacks and deployment methods for a Classic Cloud hybrid API Management 4.8 install. Compare the options available.
---

# Classic Cloud

## Deployment methods

Gravitee APIM can be installed using the following technology stacks and deployment methods.

{% include "../../.gitbook/includes/hybrid-installation-support.md" %}

### Docker

* [docker-compose.md](docker/docker-compose.md "mention")
* Docker CLI

### Kubernetes

* Vanilla Kubernetes
* AWS EKS
* Azure AKS
* [gcp-gke.md](kubernetes/gcp-gke.md "mention")
* OpenShift

### Linux

* RPM
* .ZIP

### Windows

* .ZIP

## Gateway and Bridge compatibility versions

The Bridge and APIM Gateway versions used for your hybrid deployment must be compatible per the tables below.

The following table lists the Gateway versions supported by each Bridge version.

| Bridge version | Supported Gateway versions |
| -------------- | -------------------------- |
| 4.5.x          | 4.3.x to 4.5.x             |
| 4.6.x          | 4.3.x to 4.6.x             |
| 4.7.x          | 4.3.x to 4.7.x             |
| 4.8.x          | 4.3.x to 4.8.x             |

The following table lists the Bridge versions supported by each Gateway version.

| Gateway version | Supported Bridge versions |
| --------------- | ------------------------- |
| 4.5.x           | 4.5.x to 4.8.x            |
| 4.6.x           | 4.6.x to 4.8.x            |
| 4.7.x           | 4.7.x to 4.8.x            |
| 4.8.x           | 4.8.x                     |

## Architecture

<figure><img src="../../.gitbook/assets/hybrid-installation-and-configuration-gu-27-1.png" alt="A diagram splitting the platform into a Gravitee-managed control plane holding Cloud, the console, portal, management API, databases, alert engine, and SaaS gateways, and a customer-managed data plane holding the gateway, rate limit storage, and Logstash."><figcaption></figcaption></figure>

<figure><img src="../../.gitbook/assets/hybrid-installation-and-configuration-gu-28-1.png" alt="A diagram of a hybrid deployment, with a customer-hosted data plane of load-balanced gateways, backend services, Redis, and Logstash on the left, connected over HTTPS to a Gravitee-managed control plane of CloudGate, an S3 bucket, the management API, databases, consoles, and access management on the right."><figcaption></figcaption></figure>
