---
description: >-
  This guide covers every supported deployment pattern for the Gravitee APIM
  Console and Portal UIs
---

# Configuring Portal and Console deployments

## Overview

Gravitee APIM consists of four components that communicate as follows:

1. **Management API → Console & Portal URLs** — The Management API requires the public URLs of both UIs to generate correct redirect links, email links, and Cockpit registration. Configure these via the `installation` block.
2. **Console UI → Management API** — The Console UI requires the Management API's `/management` endpoint as its `baseURL`.
3. **Portal UI → Management API** — The Portal UI requires the Management API's `/portal` endpoint as its `baseURL`.

### Helm auto-derivation

When optional overrides like `ui.baseURL`, `portal.baseURL`, or `installation.api.url` are not set, Helm templates automatically derive them from `api.ingress` and UI ingress settings:

| Derived value                           | Source                                                                                             |
| --------------------------------------- | -------------------------------------------------------------------------------------------------- |
| `installation.api.url`                  | `{api.ingress.management.scheme}://{api.ingress.management.hosts[0]}`                              |
| `installation.api.proxyPath.management` | Path extracted from `api.ingress.management.path`                                                  |
| `installation.api.proxyPath.portal`     | Path extracted from `api.ingress.portal.path`                                                      |
| `installation.standalone.console.url`   | `https://{ui.ingress.hosts[0]}{ui.ingress.path}`                                                   |
| `installation.standalone.portal.url`    | `https://{portal.ingress.hosts[0]}{portal.ingress.path}`                                           |
| Console `baseURL`                       | `{api.ingress.management.scheme}://{api.ingress.management.hosts[0]}{api.ingress.management.path}` |
| Portal `baseURL`                        | `{api.ingress.portal.scheme}://{api.ingress.portal.hosts[0]}{api.ingress.portal.path}`             |
| `jwt.cookie-domain`                     | `ui.ingress.hosts[0]`                                                                              |

In the simplest case, configure only `api.ingress` and the UI ingress hosts. All other values are derived automatically.

## Scenario 1: Single domain, path-based routing (default)

All components are served from `apim.example.com` with path-based routing. This is the default Helm chart configuration.

| Component                | URL                                   |
| ------------------------ | ------------------------------------- |
| Console UI               | `https://apim.example.com/console`    |
| Portal UI                | `https://apim.example.com/`           |
| Management API (console) | `https://apim.example.com/management` |
| Management API (portal)  | `https://apim.example.com/portal`     |

### Helm `values.yaml`

With the default values, this scenario works out of the box. The key defaults are:

```yaml
api:
  ingress:
    management:
      enabled: true
      scheme: https
      path: /management
      hosts:
        - apim.example.com
    portal:
      enabled: true
      scheme: https
      path: /portal
      hosts:
        - apim.example.com

ui:
  ingress:
    enabled: true
    path: /console(/.*)?
    hosts:
      - apim.example.com
    annotations:
      nginx.ingress.kubernetes.io/rewrite-target: /$1

portal:
  ingress:
    enabled: true
    path: /
    hosts:
      - apim.example.com
```

No `installation`, `ui.baseURL`, or `portal.baseURL` overrides are needed. All values are auto-derived.

### `gravitee.yml`

For a non-Helm deployment, configure the Management API explicitly:

```yaml
installation:
  type: standalone
  api:
    url: https://apim.example.com
    proxyPath:
      management: /management
      portal: /portal
  standalone:
    console:
      url: https://apim.example.com/console
    portal:
      url: https://apim.example.com/
```

## Scenario 2: Separate domains per component

Each component is hosted on its own domain.

| Component                | URL                                  |
| ------------------------ | ------------------------------------ |
| Console UI               | `https://console.example.com`        |
| Portal UI                | `https://portal.example.com`         |
| Management API (console) | `https://api.example.com/management` |
| Management API (portal)  | `https://api.example.com/portal`     |

### Helm `values.yaml`

When UI hosts differ from API hosts, `ui.baseURL` and `portal.baseURL` must be set explicitly because auto-derivation would produce incorrect cross-origin URLs:

```yaml
api:
  ingress:
    management:
      scheme: https
      path: /management
      hosts:
        - api.example.com
    portal:
      scheme: https
      path: /portal
      hosts:
        - api.example.com

ui:
  baseURL: https://api.example.com/management
  ingress:
    path: /(.*)
    hosts:
      - console.example.com
    annotations:
      nginx.ingress.kubernetes.io/rewrite-target: /$1

portal:
  baseURL: https://api.example.com/portal
  ingress:
    path: /
    hosts:
      - portal.example.com

installation:
  api:
    url: https://api.example.com
  standalone:
    console:
      url: https://console.example.com
    portal:
      url: https://portal.example.com
```

### `gravitee.yml`

```yaml
installation:
  type: standalone
  api:
    url: https://api.example.com
    proxyPath:
      management: /management
      portal: /portal
  standalone:
    console:
      url: https://console.example.com
    portal:
      url: https://portal.example.com
```

### CORS

When the Console/Portal UIs are on different domains from the Management API, the browser enforces CORS (Cross-Origin Resource Sharing). The Management API enables CORS by default. Verify that the `http.api.management.cors` and `http.api.portal.cors` settings in `gravitee.yml` allow the UI origins:

```yaml
http:
  api:
    management:
      cors:
        allow-origin: https://console.example.com
    portal:
      cors:
        allow-origin: https://portal.example.com
```

### JWT cookie domain

Ensure the JWT cookie domain covers both the Console UI and the Management API. When they share a parent domain, set the cookie domain to the common suffix:

**Helm:**

```yaml
jwt:
  cookie:
    domain: .example.com
```

**`gravitee.yml`:**

```yaml
jwt:
  cookie-domain: .example.com
```

If `jwt.cookie.domain` is not set in Helm, it defaults to `ui.ingress.hosts[0]`. With separate domains, this auto-derived value is likely too narrow. Always set it explicitly.

## Scenario 3: Behind a reverse proxy with custom base paths

Components are behind a corporate reverse proxy at non-standard paths, such as `https://corp.example.com/apim/management`.

### X-Forwarded headers

The Management API includes a JAX-RS `@PreMatching` filter (`UriBuilderRequestFilter`) that rewrites incoming request URIs based on proxy headers. Configure your reverse proxy to forward these headers so the API constructs correct public-facing URLs.

#### Required headers

| Header                      | Purpose                                                               |
| --------------------------- | --------------------------------------------------------------------- |
| `X-Forwarded-Proto`         | Scheme used by the client (`http` or `https`)                         |
| `X-Forwarded-Host`          | Public-facing hostname (and port if non-standard)                     |
| `X-Forwarded-Port`          | Public-facing port (ignored when `X-Original-Forwarded-Host` is used) |
| `X-Forwarded-Prefix`        | Path prefix prepended to API paths (for example, `/apim`)             |
| `X-Original-Forwarded-Host` | Overrides `X-Forwarded-Host` in chained-proxy scenarios               |
| `X-Forwarded-For`           | Client IP for audit logs                                              |

#### Header processing priority

1. **Static configuration takes precedence** — When `installation.api.url` is set in `gravitee.yml`, it determines the bootstrap API URL. Headers augment but do not override the static base.
2. **When static config is absent**, headers are used to reconstruct the public URL:
   * **Scheme**: `X-Forwarded-Proto` overrides the request scheme. If absent, the scheme from the configured API URL is used.
   * **Host**: `X-Original-Forwarded-Host` > `X-Forwarded-Host` > configured API URL host. When the header contains a comma-separated list (multiple proxies), only the first entry is used. If the value contains a port (for example, `host:8443`), it is split into host and port.
   * **Port**: `X-Forwarded-Port` is applied only when `X-Original-Forwarded-Host` was not used (to avoid mixing headers from different proxy hops).
   * **Path prefix**: `X-Forwarded-Prefix` is prepended to the request path. If absent, the filter applies the configured proxy path from `installation.api.proxyPath.*`.
3. **Client IP**: `X-Forwarded-For` — the first comma-delimited value is used as the client IP. Falls back to the TCP remote address.

### Path prefix configuration

When the Management API is served behind a custom path prefix (for example, `/apim/management` instead of `/management`), configure the proxy paths so the API generates correct URLs in responses:

**Helm:**

```yaml
installation:
  api:
    url: https://corp.example.com
    proxyPath:
      management: /apim/management
      portal: /apim/portal

api:
  ingress:
    management:
      path: /apim/management
      annotations:
        nginx.ingress.kubernetes.io/rewrite-target: /management/$1
    portal:
      path: /apim/portal
      annotations:
        nginx.ingress.kubernetes.io/rewrite-target: /portal/$1
```

**`gravitee.yml`:**

```yaml
installation:
  api:
    url: https://corp.example.com
    proxyPath:
      management: /apim/management
      portal: /apim/portal
```

The proxy path values are used by `UriBuilderRequestFilter` to rewrite local paths (`/management`, `/portal`) to public-facing paths when `X-Forwarded-Prefix` is not present.
