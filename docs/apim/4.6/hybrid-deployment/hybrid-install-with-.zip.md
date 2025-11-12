# Hybrid Install with .ZIP

{% include "../.gitbook/includes/installation-guide-note.md" %}

1. Install Gravitee API Management (APIM). For more information about installing Gravitee APIM, see [Install with .ZIP](docs/apim/4.6/install-and-upgrade/.zip.md).
2. Download, and then mount the Redis Repository. This repository is used for the rate limits' synchronized counters. To download this repository, go to [Gravitee.io Downloads](https://download.gravitee.io/#graviteeio-apim/plugins/repositories/gravitee-apim-repository-redis).
3. Download, and then mount the TCP Reporter. This repository is used to push events to Logstash. To download this repository, go to [Gravitee.io Downloads.](https://download.gravitee.io/#graviteeio-ee/apim/plugins/reporters/gravitee-reporter-tcp/)

### **Configuring the connection between the SaaS Control-Plane and the Bridge Gateway**

{% code title="gravitee.yaml" lineNumbers="true" %}
```yaml
management:
  type: http
  http:
    url: https://bridge-gateway-url:bridge-gateway-port
    keepAlive: true
    idleTimeout: 30000
    connectTimeout: 10000
    authentication:
      type: basic
      basic:
        username: bridge-gateway-username
        password: bridge-gateway-password
      # ssl:
      #   ###beware: since 4.4 default is false (see upgrade guide) 
      #   trustall: true
      #   verifyHostname: true
      #   keystore:
      #     type: jks # Supports jks, pem, pkcs12
      #     path: ${gravitee.home}/security/keystore.jks
      #     password: secret
      #   truststore:
      #     type: jks # Supports jks, pem, pkcs12
      #     path: ${gravitee.home}/security/truststore.jks
      #     password: secret
```
{% endcode %}

### **An example of a Self-Hosted Gateway configuration**

{% code title="gravitee.yaml" lineNumbers="true" %}
```yaml
############################################################################################################
#################################### Gravitee.IO Gateway - Configuration ###################################
############################################################################################################

############################################################################################################
# This file is the general configuration of Gravitee.IO Gateway:
# - Properties (and respective default values) in comment are provided for information.
# - You can reference other property by using ${property.name} syntax
# - gravitee.home property is automatically set-up by launcher and refers to the installation path. Do not override it !
#
# Please have a look to http://docs.gravitee.io/ for more options and fine-grained granularity
############################################################################################################

organizations: cockpit-org-hrid
environments: cockpit-env-hrid
tags: your, sharding, tags #example: internal

plugins:
  path:
    - /opt/graviteeio-gateway/plugins
    - /opt/graviteeio-gateway/plugins-ext

management:
  type: http
  http:
    url: https://bridge-gateway-url:bridge-gateway-port
    authentication:
      basic:
        username: bridge-gateway-username
        password: bridge-gateway-password

ratelimit:
  # type: hazelcast
  type: redis
  redis:
    host: redis-host
    port: 6379
    password: redis-password

cache:
  type: ehcache

reporters:
  elasticsearch:
    enabled: false # Is the reporter enabled or not (default to true)
  tcp:
    enabled: true
    host: logstash-host
    port: logstash-port
    output: elasticsearch

services:
  core:
    http:
      enabled: true
      port: 18082
      host: localhost
      authentication:
        type: basic
        users:
          admin: internal-api-password

  sync:
    delay: 5000
    unit: MILLISECONDS
    distributed: false # By enabling this mode, data synchronization process is distributed over clustered API Gateways.
    bulk_items: 100 # Defines the number of items to retrieve during synchronization (events, plans, api keys, ...).

  local:
    enabled: false
    path: ${gravitee.home}/apis # The path to API descriptors

  monitoring:
    delay: 5000
    unit: MILLISECONDS
    distributed: false # By enabling this mode, data monitoring gathering process is distributed over clustered API Gateways.

  metrics:
    enabled: false
    prometheus:
      enabled: true

  tracing:
    enabled: false

api:
  properties:
    encryption:
      secret: your-own-api-32-characters-secret

alerts:
  alert-engine:
    enabled: true
    ws:
      discovery: true
      endpoints:
        - https://alert-engine-url:alert-engine-port
      security:
        username: alert-engine-username
        password: alert-engine-password

classloader:
  legacy:
    enabled: false
```
{% endcode %}
