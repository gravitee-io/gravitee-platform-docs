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
```

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
