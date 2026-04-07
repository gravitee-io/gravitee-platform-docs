---
description: Information about kubernetes.
metaLinks:
  alternates:
    - ./
---

# Kubernetes

## Deployment methods

* [Vanilla Kubernetes](vanilla-kubernetes/)
* [AWS EKS](aws-eks.md)
* [Azure AKS](azure-aks.md)
* [OpenShift](openshift.md)
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

For the full configuration reference including proxy authentication and `gravitee.yml` equivalents, see [Configure Helm values](../proxy-configuration/system-proxy-for-backend-apis.md#configure-helm-values). For an overview of all proxy methods, see [Proxy Configuration](../proxy-configuration/).
