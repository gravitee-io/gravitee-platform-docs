---
description: This article walks through how to configure Alert Engine
---

# Configure Alert Engine

## Introduction

There are three different ways to configure AE:

* environment variables
* system properties
* `gravitee.yml`

The order in which they are listed above corresponds to their order of precedence. In other words, environment variables override the other two configuration types, and system properties override `gravitee.yml`.

## Configure AE via the `gravitee.yml` file

The `gravitee.yml` file, found in `GRAVITEE_HOME/config/`, is the default way to configure AE.

{% hint style="info" %}
Be aware of sensitivities&#x20;

YAML (`yml`) format is very sensitive to indentation. Ensure you include the correct number of spaces and use spaces instead of tabs.
{% endhint %}

Please see the example below:

```
############################################################################################################
################################## Gravitee Alert Engine - Configuration ################################
############################################################################################################

############################################################################################################
# This file is the general configuration of Gravitee Alert Engine:
# - Properties (and respective default values) in comment are provided for information.
# - You can reference other property by using ${property.name} syntax
# - gravitee.home property is automatically set-up by launcher and refers to the installation path. Do not override it !
#
############################################################################################################

# Ingesters
ingesters:
  ws:
#    instances: 0
#    port: 8072
#    host: 0.0.0.0
#    secured: false
#    alpn: false
#    ssl:
#      clientAuth: false
#      keystore:
#        path: ${gravitee.home}/security/keystore.jks
#        password: secret
#      truststore:
#        path: ${gravitee.home}/security/truststore.jks
#        password: secret
    authentication: # authentication type to be used for HTTP authentication
      type: basic # none to disable authentication / basic for basic authentication
      users:
        admin: adminadmin

# Alert service configurations. Provided values are default values.
# All services are enabled by default. To stop one of them, you have to add the property 'enabled: false'.
services:
  core:
    http:
      enabled: true
      port: 18072
      host: localhost
      authentication:
        # authentication type to be used for the core services
        # - none : to disable authentication
        # - basic : to use basic authentication
        # default is "basic"
        type: basic
        users:
          admin: adminadmin
  metrics:
    enabled: false
    prometheus:
      enabled: true

cluster:
  # Frequency at which Alert Engine will register the latest state of dampenings and buckets
  sync:
    time:
      value: 30
      unit: SECONDS

  hazelcast:
    config:
      path: ${gravitee.home}/config/hazelcast.xml
```

## System properties

You can override the default `gravitee.yml` configuration by defining system properties.

To override this property:

```
cluster:
  sync:
    time:
      value: 30
```

Add this property to the JVM:

```
-Dcluster.sync.time.value=50
```

## Environment variables

You can override the default `gravitee.yml` configuration and system properties by defining environment variables.

To override this property:

```
cluster:
  sync:
    time:
      value: 30
```

Define one of the following variables:

```
GRAVITEE_CLUSTER_SYNC_TIME_VALUE=30
GRAVITEE.CLUSTER.SYNC.TIME.VALUE=30
gravitee_cluster_sync_time_value=30
gravitee.cluster.sync.time.value=30
```

{% hint style="info" %}
**Case sensitivities**&#x20;

Some properties are case sensitive and cannot be written in upper case (for example, `gravitee_security_providers_0_tokenIntrospectionEndpoint`). We advise you to define environment variables in lower case. Ensure you use the correct syntax for each property.
{% endhint %}

{% hint style="info" %}
**Hyphen sensitivities**

In some systems, hyphens are not allowed in variable names. You can replace them with another character such as an underscore (for example, `gravitee_policy_apikey_header` instead of `gravitee_policy_api-key_header`).
{% endhint %}
