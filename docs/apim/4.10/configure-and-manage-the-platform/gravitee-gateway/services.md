---
description: Configuration guide for services.
metaLinks:
  alternates:
    - services.md
---

# Services

You can update the default APIM Gateway default values. All services are enabled by default. To stop a service, you need to add the property '`enabled: false`' (you can see an example in the '`local`' service).

```yaml
services:
  # Synchronization daemon used to keep the Gateway state in sync with the configuration from the management repository
  # Be aware that, by disabling it, the Gateway will not be sync with the configuration done through Management API and Management Console
  sync:
    # Synchronization is done each 5 seconds
    cron: '*/5 * * * * *'

  # Service used to store and cache api-keys from the management repository to avoid direct repository communication
  # while serving requests.
  apikeyscache:
    delay: 10000
    unit: MILLISECONDS
    threads: 3 # Threads core size used to retrieve api-keys from repository.

  # Local registry service.
  # This registry is used to load API Definition with json format from the file system. By doing so, you do not need
  # to configure your API using the web console or the rest API (but you need to know and understand the json descriptor
  # format to make it work....)
  local:
    enabled: false
    path: ${gravitee.home}/apis # The path to API descriptors

  # Gateway monitoring service.
  # This service retrieves metrics like os / process / jvm metrics and send them to an underlying reporting service.
  monitoring:
    delay: 5000
    unit: MILLISECONDS

  # Endpoint healthcheck service.
  healthcheck:
    threads: 3 # Threads core size used to check endpoint availability
    jitterInMs: 900 # Random offset (0-5000 ms) applied per API to prevent health checks from firing simultaneously

  # Tenant configuration for Kafka endpoint selection.
  # When a tenant is configured, the gateway selects Kafka endpoints that either have no tenant configuration
  # or have a tenant configuration matching the gateway's tenant.
  tenant:
    # Tenant identifier used for Kafka endpoint selection
#   value: my-tenant
```

### Health-check jitter

When many APIs have health checks enabled, all checks can fire at the same cron boundary. This thundering herd of simultaneous outbound requests can temporarily increase API response times.

The `jitterInMs` property adds a deterministic, per-API scheduling offset to spread health check executions over time. Each API and endpoint combination receives a fixed offset within the `[0, jitterInMs]` window, so checks no longer cluster on the same instant.

| Property                          | Description                                                                                                  | Default | Required |
| --------------------------------- | ------------------------------------------------------------------------------------------------------------ | ------- | -------- |
| `services.healthcheck.jitterInMs` | Maximum random scheduling offset in milliseconds applied per API health check. Set to `0` to disable jitter. | `900`   | No       |

The accepted range is `0` to `5000`. If a value outside this range is configured, the gateway logs a warning and falls back to the default of `900`.

This setting applies to both v2 and v4 proxy API health checks.

{% hint style="info" %}
For Helm-based deployments, configure this value with `gateway.services.healthcheck.jitterInMs` in your `values.yaml`.
{% endhint %}

You can configure APIM API to start only the Management or Portal API. You can also change the API endpoints from their default values of `/management` and `/portal`.

```yaml
http:
  api:
    # Configure the listening path for the API. Default to /
#    entrypoint: /
    # Configure Management API.
#    management:
#      enabled: true
#      entrypoint: ${http.api.entrypoint}management
#      cors: ...
    # Configure Portal API.
#    portal:
#      enabled: true
#      entrypoint: ${http.api.entrypoint}portal
#      cors: ...
```
