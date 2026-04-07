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

Used by the Gateway to route API calls to backend services through a centralized proxy. APIs must have `useSystemProxy: true` enabled in their endpoint configuration. The system proxy also applies to JWT plan JWKS retrieval from external identity providers (for example, Microsoft Entra ID) when **Use system proxy** is enabled in the [JWT plan configuration](../../secure-and-expose-apis/plans/jwt.md#jwks-retrieval-through-a-corporate-proxy).

**Configuration path:** Environment variables `gravitee_system_proxy_*`
