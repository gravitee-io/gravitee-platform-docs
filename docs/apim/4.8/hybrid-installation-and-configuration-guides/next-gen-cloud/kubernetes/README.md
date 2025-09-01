# Kubernetes

## Deployment Methods

{% include "../../../.gitbook/includes/hybrid-installation-support.md" %}

*
* [AWS EKS](aws-eks.md)
* [azure-aks.md](azure-aks.md "mention")
* GCP EKS
* [openshift.md](openshift.md "mention")

## Overview

You can use Kubernetes to install the self-hosted components of a Gravitee API Management (APIM) Next-Gen Cloud hybrid architecture. A Kubernetes installation relies on the `values.yaml` configuration file and the Gravitee Helm chart.

The `values.yaml` configuration file serves as the bridge between your local Kubernetes infrastructure and Gravitee Cloud. It contains all of the parameters that define how your hybrid Gateway operates, connects to Gravitee Cloud, and integrates with supporting services like Redis.

The Helm installation process converts your configuration into running Kubernetes resources. These resources provide your API Gateway with the functionality that maintains secure connectivity with Gravitee Cloud.&#x20;

The following Kubernetes resources are created with the Gravitee Helm chart:

* Deployment objects that manage your Gateway pods
* Service objects that provide network connectivity
* ConfigMap objects that store non-sensitive configuration data
* Secret objects that securely store authentication credentials
* ServiceAccount objects that provide appropriate cluster permissions
