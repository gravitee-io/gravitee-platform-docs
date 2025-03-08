---
description: An overview of Helm charts and Kubernetes operators
---

# Install on Kubernetes

{% hint style="info" %}
This guide assumes familiarity with Kubernetes and its terms.
{% endhint %}

## Overview

Installing Gravitee API Management (APIM) and the Gravitee Kubernetes Operator (GKO) on a Kubernetes cluster is made easy with the help of our Helm chart. Helm is a package manager for Kubernetes that simplifies the deployment and management of applications on Kubernetes clusters. Helm packages are called charts, which are collections of YAML templates that describe the different Kubernetes resources needed to run an application (e.g., deployments, services, ConfigMaps, etc).

If you used Helm to install APIM on Kubernetes, you can continue to use it to manage the APIM installation. Helm allows you to install, upgrade, rollback, and delete applications with just a few commands.&#x20;

Additionally, complex services and applications, like an API management platform, benefit from the advanced automation and management capabilities of a Kubernetes operator. A Kubernetes operator is a [pattern](https://kubernetes.io/docs/concepts/extend-kubernetes/operator/) for building custom [controllers](https://kubernetes.io/docs/concepts/architecture/controller/) that can manage custom resources. Operators are designed to perform actions based on a low-level understanding of the applications they manage.

The GKO can also be installed with Helm and allows you to manage your APIs in a fully declarative fashion.&#x20;

## Install

**The APIM Helm chart supports Gravitee APIM Management (APIM) versions: 3.0.x and higher** and deploys the following:

* APIM Management API
* APIM Management Console
* APIM Developer Portal
* APIM Gateway
* MongoDB replica set or PostgreSQL (optional dependency)
* Elasticsearch Cluster (optional dependency)

The GKO Helm chart is currently installed as a separate component from the standard APIM cluster.

<table data-view="cards"><thead><tr><th></th><th></th><th data-hidden></th><th data-hidden data-type="content-ref"></th><th data-hidden data-card-target data-type="content-ref"></th></tr></thead><tbody><tr><td>APIM Helm Install and Configuration</td><td></td><td></td><td><a href="apim-helm-install-and-configuration.md">apim-helm-install-and-configuration.md</a></td><td><a href="apim-helm-install-and-configuration.md">apim-helm-install-and-configuration.md</a></td></tr><tr><td>Architecture Overview</td><td></td><td></td><td><a href="architecture-overview.md">architecture-overview.md</a></td><td><a href="architecture-overview.md">architecture-overview.md</a></td></tr></tbody></table>
