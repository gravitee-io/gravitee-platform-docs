# Proxy Configuration

## Overview

In enterprise environments, Gravitee components often need to communicate through corporate proxy servers. This section covers proxy configuration for self-hosted deployment scenarios.

| Guide                            | Use Case                                                                                |
| -------------------------------- | --------------------------------------------------------------------------------------- |
| Bridge Gateway Proxy             | Configure a Bridge Server to accept Hybrid Gateway connections and proxy outbound calls |
| System Proxy for Backend APIs    | Configure a Gateway to route backend API calls through a system proxy                   |
| Combined Hybrid and Bridge Proxy | Deploy both Hybrid Gateway and Bridge Server with full proxy configuration              |

## Proxy Types

### HTTP Client Proxy

This is used by the Management API for external HTTP calls such as webhooks, API imports, and external notifications.

**Configuration path:** Environment variables `gravitee_httpClient_proxy_*`

### System Proxy

This is used by the Gateway to route API calls to backend services through a centralized proxy. APIs must have `useSystemProxy: true` enabled in their endpoint configuration. The system proxy also applies to JWT plan JWKS retrieval from external identity providers (for example, Microsoft Entra ID) when **Use system proxy** is enabled in the [JWT plan configuration](../../secure-and-expose-apis/plans/jwt.md#jwks-retrieval-through-a-corporate-proxy).

**Configuration path:** Environment variables `gravitee_system_proxy_*`

## Choose the right proxy method

Gravitee supports several proxy configuration approaches. The following table describes each method and when to use it:

| Method | Environment variables | Use case |
| --- | --- | --- |
| **System proxy** | `gravitee_system_proxy_*` | Route Gateway outbound calls through a proxy, including backend API calls and JWKS retrieval from external identity providers. This is the correct method for Helm-based Kubernetes and OpenShift deployments. |
| **HTTP Client proxy** | `gravitee_httpClient_proxy_*` | Route Management API outbound HTTP calls (webhooks, API imports, external notifications) through a proxy. This doesn't affect Gateway traffic. |
| **JVM flags** | `-Dhttp.proxyHost`, `-Dhttps.proxyHost` | Standard Java proxy flags. These aren't used by Gravitee's internal HTTP clients and aren't recommended for Gravitee proxy configuration. |
| **OS environment variables** | `HTTP_PROXY`, `HTTPS_PROXY` | Standard OS-level proxy variables. These aren't used by Gravitee internally and don't configure Gravitee components. |

{% hint style="warning" %}
**Use `gravitee_system_proxy_*` for Gateway proxy configuration**

For Kubernetes and OpenShift Helm deployments, set the `gravitee_system_proxy_*` environment variables in the Gateway section of your `values.yaml`. Alternative approaches such as JVM flags (`-Dhttp.proxyHost`) or OS environment variables (`HTTP_PROXY`/`HTTPS_PROXY`) don't configure Gravitee's Gateway proxy and won't work for routing Gateway traffic, including JWKS retrieval, through a proxy.
{% endhint %}

## Supported Proxy Protocols

All proxy configurations support the following protocols:

| Protocol | Description                                       |
| -------- | ------------------------------------------------- |
| `HTTP`   | Standard HTTP proxy (most common)                 |
| `SOCKS4` | SOCKS version 4 proxy                             |
| `SOCKS5` | SOCKS version 5 proxy with authentication support |
