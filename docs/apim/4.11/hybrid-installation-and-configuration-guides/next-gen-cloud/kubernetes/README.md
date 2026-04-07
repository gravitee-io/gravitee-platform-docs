---
description: An overview about kubernetes.
metaLinks:
  alternates:
    - ./
---

# Kubernetes

## Deployment Methods

* [vanilla-kubernetes](vanilla-kubernetes/ "mention")
* [AWS EKS](aws-eks.md)
* [azure-aks.md](azure-aks.md "mention")
* [Openshift](openshift.md)
* GCP GKE

## Proxy configuration

To route Gateway traffic through a corporate proxy (for example, for backend API calls or JWKS retrieval from external identity providers like Microsoft Entra ID), add the following `gravitee_system_proxy_*` environment variables to the Gateway section of your `values.yaml`:

```yaml
gateway:
  env:
    - name: gravitee_system_proxy_enabled
      value: "true"
    - name: gravitee_system_proxy_type
      value: "HTTP"
    - name: gravitee_system_proxy_host
      value: "<proxy-host>"
    - name: gravitee_system_proxy_port
      value: "<proxy-port>"
    - name: gravitee_system_proxy_https_host
      value: "<proxy-host>"
    - name: gravitee_system_proxy_https_port
      value: "<proxy-port>"
```

For the full configuration reference including proxy authentication and `gravitee.yml` equivalents, see [Configure Helm values](../../proxy-configuration/system-proxy-for-backend-apis.md#configure-helm-values). For an overview of all proxy methods, see [Proxy Configuration](../../proxy-configuration/).

## Overview

You can use Kubernetes to install the self-hosted components of a Gravitee API Management (APIM) Next-Gen Cloud hybrid architecture. A Kubernetes installation relies on the `values.yaml` configuration file and the Gravitee Helm chart.

The `values.yaml` configuration file serves as the bridge between your local Kubernetes infrastructure and Gravitee Cloud. It contains all of the parameters that define how your hybrid Gateway operates, connects to Gravitee Cloud, and integrates with supporting services like Redis.

The Helm installation process converts your configuration into running Kubernetes resources. These resources provide your API Gateway with the functionality that maintains secure connectivity with Gravitee Cloud.

The following Kubernetes resources are created with the Gravitee Helm chart:

* Deployment objects that manage your Gateway pods
* Service objects that provide network connectivity
* ConfigMap objects that store non-sensitive configuration data
* Secret objects that securely store authentication credentials
* ServiceAccount objects that provide appropriate cluster permissions
