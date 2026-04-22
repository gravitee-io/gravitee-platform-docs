# Proxy Configuration

## Overview

In enterprise environments, Gravitee components often communicate through corporate proxy servers. This section covers proxy configuration for hybrid deployment scenarios.

| Guide                         | Use Case                                                                                   |
| ----------------------------- | ------------------------------------------------------------------------------------------ |
| Hybrid Gateway Proxy          | Configure a Hybrid Gateway to connect to a Bridge Server or Gravitee Cloud through a proxy |
| System Proxy for Backend APIs | Configure a Gateway to route backend API calls through a system proxy                      |

## Proxy Types

### HTTP Repository Proxy

This is used by Hybrid Gateways to connect to the Management API Bridge or Gravitee Cloud Platform.

**Configuration path:** `gateway.management.http.proxy`

### Cloud Reporter Proxy

This is used by Gateways to send metrics and logs to Gravitee Cloud through a proxy.

**Configuration path:** Environment variables `gravitee_cloud_client_proxy_*`

#### System Proxy

Used by the Gateway to route API calls to backend services through a centralized proxy. APIs must have useSystemProxy: true enabled in their endpoint configuration. The system proxy also applies to JWT plan JWKS retrieval from external identity providers (for example, Microsoft Entra ID, Google, or Okta) when **Use system proxy** is enabled in the [JWT plan configuration](../../secure-and-expose-apis/plans/jwt.md#jwks-retrieval-through-a-corporate-proxy).

**Configuration path:** Environment variables `gravitee_system_proxy_*`

## Choose the right proxy method

Gravitee supports several proxy configuration approaches. The following table describes each method and when to use it:

| Method | Environment variables | Use case |
| --- | --- | --- |
| **System proxy** | `gravitee_system_proxy_*` | Route Gateway outbound calls through a proxy, including backend API calls and JWKS retrieval from external identity providers. This is the correct method for Helm-based Kubernetes and OpenShift deployments. |
| **HTTP Repository proxy** | `gateway.management.http.proxy` | Route Hybrid Gateway connections to the Bridge Server or Gravitee Cloud Platform through a proxy. |
| **Cloud Reporter proxy** | `gravitee_cloud_client_proxy_*` | Route Gateway metrics and log reporting to Gravitee Cloud through a proxy. |
| **HTTP Client proxy** | `gravitee_httpClient_proxy_*` | Route Management API outbound HTTP calls (webhooks, API imports, external notifications) through a proxy. This doesn't affect Gateway traffic. |
| **JVM flags** | `-Dhttp.proxyHost`, `-Dhttps.proxyHost` | Standard Java proxy flags. These aren't used by Gravitee's internal HTTP clients and aren't recommended for Gravitee proxy configuration. |
| **OS environment variables** | `HTTP_PROXY`, `HTTPS_PROXY` | Standard OS-level proxy variables. These aren't used by Gravitee internally and don't configure Gravitee components. |

{% hint style="warning" %}
**Use `gravitee_system_proxy_*` for Gateway proxy configuration**

For Kubernetes and OpenShift Helm deployments, set the `gravitee_system_proxy_*` environment variables in the Gateway section of your `values.yaml`. Alternative approaches such as JVM flags (`-Dhttp.proxyHost`) or OS environment variables (`HTTP_PROXY`/`HTTPS_PROXY`) don't configure Gravitee's Gateway proxy and won't work for routing Gateway traffic, including JWKS retrieval, through a proxy.
{% endhint %}
