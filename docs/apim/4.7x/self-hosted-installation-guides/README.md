# Self-Hosted Installation Guides

## Overview

{% hint style="info" %}
**Gravitee Cloud is recommended for new installations to reduce deployment complexity.**\
Let Gravitee run the control plane and database for you. With Gravitee Cloud, you only need to run the data planes. To register for a Gravitee Cloud account, go to the [Gravitee Cloud registration page](https://cloud.gravitee.io/).
{% endhint %}

Self-hosted architecture refers a scheme where all Gravitee API Management components are hosted by the user on-prem and/or in a private cloud. Gravitee Cloud and API Designer are optional Gravitee-managed components that can be connected to a self-hosted API Management installation.

## Deployment methods

Gravitee APIM can be installed using the following technology stacks and deployment methods.

### Docker

* [docker-compose.md](docker/docker-compose.md "mention")
* Docker CLI

### Kubernetes

* [kubernetes](kubernetes/ "mention")
* AWS EKS
* Azure AKS
* GCP GKE
* [openshift.md](kubernetes/openshift.md "mention")

### Linux

* [rpm](rpm/ "mention")
* [.zip.md](.zip.md "mention")

### Windows

* [.zip.md](.zip.md "mention")

## Architecture

The following diagrams illustrate the component management, design, and virtual machine internal/external access deployment of a self-hosted architecture.

### Self-hosted component management

<img src="../.gitbook/assets/file.excalidraw (21).svg" alt="" class="gitbook-drawing">

### Self-hosted architecture diagram

<img src="../.gitbook/assets/file.excalidraw (20).svg" alt="Self-hosted architecture" class="gitbook-drawing">

### Self-hosted VM installation: LAN + DMZ deployment

<img src="../.gitbook/assets/file.excalidraw (19).svg" alt="Self-hosted architecture LAN + DMZ" class="gitbook-drawing">

