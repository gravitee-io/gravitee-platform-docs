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

This is used by the Gateway to route API calls to backend services through a centralized proxy. APIs must have `useSystemProxy: true` enabled in their endpoint configuration.

**Configuration path:** Environment variables `gravitee_system_proxy_*`

## Supported Proxy Protocols

All proxy configurations support the following protocols:

| Protocol | Description                                       |
| -------- | ------------------------------------------------- |
| `HTTP`   | Standard HTTP proxy (most common)                 |
| `SOCKS4` | SOCKS version 4 proxy                             |
| `SOCKS5` | SOCKS version 5 proxy with authentication support |
