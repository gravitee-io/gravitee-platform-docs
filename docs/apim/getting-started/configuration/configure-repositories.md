---
description: This article covers how to configure various repositories
---

# Configure Repositories

## Introduction

In Gravitee, repositories are used to store different type of data (different scopes). Repositories are configured in the `gravitee.yml` configuration file and can be different for each scope. For example, you can decide to store management data in MongoDB, rate limiting data in Redis, and analytics data in Elasticsearch.

## Supported storage

The following matrix shows scope and storage compatibility.

<table><thead><tr><th width="317">Scope</th><th>MongoDB</th><th>Redis</th><th>Elasticsearch</th><th>JDBC</th></tr></thead><tbody><tr><td>Management: All the API Management platform management data, such as API definitions, users, applications and plans</td><td>X</td><td>-</td><td>-</td><td>X</td></tr><tr><td>Rate Limit: rate limiting data</td><td>X</td><td>X</td><td>-</td><td><a data-footnote-ref href="#user-content-fn-1">X*</a></td></tr><tr><td>Analytics: analytics data</td><td>-</td><td>-</td><td>X</td><td>-</td></tr></tbody></table>

Please see the sections below that walk through how to configure each kind of repository.

## ElasticSearch

The Elasticsearch connector is based on the HTTP API exposed by ES instances. This connector supports all versions of ES, from 5.x to 7.x, and OpenSearch v1.x.

You can find more detail about supported versions of ElasticSearch at [https://www.elastic.co/support/eol](https://www.elastic.co/support/eol).

{% hint style="info" %}
**Deprecated support for the native ES client**

Gravitee no longer supports native ES client. Previous connectors provided by us are no longer supported.
{% endhint %}

### Configuration

#### APIM API configuration

The Elasticsearch client does not support URL schemes in format http://USERNAME:PASSWORD@server.org. You must provide the username and password using the analytics.elasticsearch.security.username and analytics.elasticsearch.security.password properties.

```
analytics:
  type: elasticsearch
  elasticsearch:
    endpoints:
      - http://localhost:9200
#    index: gravitee
#    index_mode: daily    # "daily" indexes, suffixed with date. Or "ilm" managed indexes, without date
#    security:
#       username:
#       password:
#    ssl:                        # for https es connection
#      keystore:
#        type: jks               # required. also valid values are "pem", "pfx"
#        path: path/to/jks         # only for only for jks / pkcs12
#        password: <keystore pass> # only for only for jks / pkcs12
#        certs: 'path/to/cert'      # only for pems
#        keys: 'path/to/key'        # only for pems
```

#### API Gateway configuration

```
reporters:
  elasticsearch:
    enabled: true # Is the reporter enabled or not (default to true)
    endpoints:
      - http://${ds.elastic.host}:${ds.elastic.port}
#    index: gravitee
#    index_mode: daily    # "daily" indexes, suffixed with date. Or "ilm" managed indexes, without date
#    cluster: elasticsearch
#    bulk:
#      actions: 1000           # Number of requests action before flush
#      flush_interval: 5       # Flush interval in seconds
#      concurrent_requests: 5  # Concurrent requests
#    settings:
#      number_of_shards: 5
#      number_of_replicas: 1
#    pipeline:
#      plugins:
#        ingest: geoip
#    ssl:                        # for https es connection
#      keystore:
#        type: jks               # required. also valid values are "pem", "pfx"
#        path: path/to/jks         # only for only for jks / pkcs12
#        password: <keystore pass> # only for only for jks / pkcs12
#        certs: 'path/to/cert'      # only for pems
#        keys: 'path/to/key'        # only for pems
```

### Index management with ES Curator

ES Curator is a great tool for ES administration. For optimizing data footprint and ES performance, you can define a retention window and periodically merge shards into only one segment.

```
/usr/bin/curator --config /opt/curator/curator.yml /opt/curator/action-curator.yml
```

`curator.yml` :

```
client:
  hosts:
    - node1
    - node2
  port: 9200

logging:
  loglevel: INFO
  logfile:
  logformat: default
  blacklist: ['elasticsearch', 'urllib3']
```

`action-curator.yml` :

```
actions:
  1:
    action: forcemerge
    description: "Perform a forceMerge on selected indices to 'max_num_segments' per shard. Merge Days - 1 index for optimize disk space footprint on Elasticsearch TS"
    options:
      max_num_segments: 1
      continue_if_exception: True
      ignore_empty_list: True
    filters:
    - filtertype: pattern
      kind: prefix
      value: '^(gravitee-).*$'
      exclude: False
    - filtertype: age
      source: name
      direction: older
      unit: days
      unit_count: 1
      timestring: '%Y.%m.%d'
  2:
    action: delete_indices
    description: "Delete selected indices older than 15d days"
    options:
      continue_if_exception: True
      ignore_empty_list: True
    filters:
    - filtertype: pattern
      kind: prefix
      value: '^(gravitee-).*$'
      exclude: False
    - filtertype: age
      source: name
      direction: older
      unit: days
      unit_count: 15
      timestring: '%Y.%m.%d'
```

{% hint style="info" %}
**ES curator deployment hint**

If you deploy ES Curator on every ES data node, you need to set master\_only: True in the curator configuration file. This ensures the curator is run only once on the elected current master.
{% endhint %}

### Index management with ES ILM

{% hint style="info" %}
**APIM version compatibility**

To use the ILM feature, you need to use Gravitee version 3.8.5 (for APIM 3.10.x) or version 3.12.1 of the plugin (for APIM 3.15.x and beyond).
{% endhint %}

You can configure Index Lifecycle Management (ILM) policies to automatically manage indices according to your retention requirements. For example, you can use ILM to create a new index each day and archive the previous ones. You can check the documentation [here](https://www.elastic.co/guide/en/elasticsearch/reference/current/set-up-lifecycle-policy.html#ilm-create-policy) for more information.

By default, the `index_mode` configuration value is `daily`: Gravitee suffixes index names with the date.

If you want to let ILM handles that, you can set `index_mode` to `ILM`. Gravitee will no longer add a suffix to index names.

You also need to tell your APIM Gateway which ILM policies to use.

Here’s an example of configuration for APIM Gateway:

```
  elasticsearch:
    enabled: true # Is the reporter enabled or not (default to true)
    endpoints:
      - http://${ds.elastic.host}:${ds.elastic.port}
    lifecycle:
      policies:
        health: hot_delete_health # ILM policy for the gravitee-health-* indexes
        monitor: hot_delete_monitor # ILM policy for the gravitee-monitor-* indexes
        request: hot_delete_request # ILM policy for the gravitee-request-* indexes
        log: hot_delete_log # ILM policy for the gravitee-log-* indexes
    index_mode: ilm         # "daily" indexes, suffixed with date. Or "ilm" managed indexes, without date

```

## MongoDB

Please see the below table for versions of APIM that support using MongoDB as a repository:

| APIM Version    | Version tested        | APIM plugin                                                                                                                                             |
| --------------- | --------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------- |
| 1.30.x to 3.9.x | 3.6 / 4.0 / 4.2       | [Download the same version as your APIM platform](https://download.gravitee.io/#graviteeio-apim/plugins/repositories/gravitee-apim-repository-mongodb/) |
| 3.10.x          | 3.6 / 4.0 / 4.2 / 4.4 |                                                                                                                                                         |

### Configure MongoDB

[MongoDB](https://www.mongodb.org/) is the default repository implementation used by APIM.

#### Mandatory configuration

```
# ===================================================================
# MINIMUM MONGO REPOSITORY PROPERTIES
#
# This is a minimal sample file declared connection to MongoDB
# ===================================================================
management:
  type: mongodb             # repository type
  mongodb:                  # mongodb repository
    dbname:                 # mongodb name (default gravitee)
    host:                   # mongodb host (default localhost)
    port:                   # mongodb port (default 27017)
```

#### Optional configuration

The example above shows the minimum configuration required to get started with a MongoDB database. You can configure the following additional properties to customize the behavior of a MongoDB database:

```
# ===================================================================
# MONGO REPOSITORY PROPERTIES
#
# This is a sample file declared all properties for MongoDB Repository
# ===================================================================
management:
  type: mongodb                 # repository type
  mongodb:                      # mongodb repository
    prefix:                     # collections prefix
    dbname:                     # mongodb name (default gravitee)
    host:                       # mongodb host (default localhost)
    port:                       # mongodb port (default 27017)

## Client settings
    description:                # mongodb description (default gravitee.io)
    username:                   # mongodb username (default null)
    password:                   # mongodb password (default null)
    authSource:                 # mongodb authentication source (when at least a user or a password is defined, default gravitee)
    readPreference:              # possible values are 'nearest', 'primary', 'primaryPreferred', 'secondary', 'secondaryPreferred'
    readPreferenceTags:          # list of read preference tags (https://docs.mongodb.com/manual/core/read-preference-tags/#std-label-replica-set-read-preference-tag-sets)
### Write concern
    writeConcern:               # possible values are 1,2,3... (the number of node) or 'majority' (default is 1)
    wtimeout:                   # (default is 0)
    journal:                    # (default is true)

## Socket settings
    connectTimeout:             # mongodb connection timeout (default 1000)
    socketTimeout:              # mongodb socket timeout (default 1000)

## Cluster settings
    serverSelectionTimeout:     # mongodb server selection timeout (default 1000)
    localThreshold:             # mongodb local threshold (default 15)

## Connection pool settings
    maxWaitTime:                # mongodb max wait time (default 120000)
    maxConnectionLifeTime:      # mongodb max connection life time (default 0)
    maxConnectionIdleTime:      # mongodb max connection idle time (default 0)
    connectionsPerHost:         # mongodb max connections per host (default 100)
    minConnectionsPerHost:      # mongodb min connections per host (default 0)

## Server settings
    heartbeatFrequency:         # mongodb heartbeat frequency (default 10000)
    minHeartbeatFrequency:      # mongodb min heartbeat frequency (default 500)

## SSL settings (Available in APIM 3.10.14+, 3.15.8+, 3.16.4+, 3.17.2+, 3.18+)
    sslEnabled:                 # mongodb ssl mode (default false)
    keystore:
      path:                     # Path to the keystore (when sslEnabled is true, default null)
      type:                     # Type of the keystore, supports jks, pem, pkcs12 (when sslEnabled is true, default null)
      password:                 # KeyStore password (when sslEnabled is true, default null)
      keyPassword:              # Password for recovering keys in the KeyStore (when sslEnabled is true, default null)
    truststore:
      path:                     # Path to the truststore (when sslEnabled is true, default null)
      type:                     # Type of the truststore, supports jks, pem, pkcs12 (when sslEnabled is true, default null)
      password:                 # Truststore password (when sslEnabled is true, default null)
## Deprecated SSL settings that will be removed in 3.19.0
    sslEnabled:                 # mongodb ssl mode (default false)
    keystore:                   # path to KeyStore (when sslEnabled is true, default null)
    keystorePassword:           # KeyStore password (when sslEnabled is true, default null)
    keyPassword:                # password for recovering keys in the KeyStore (when sslEnabled is true, default null)
```

{% hint style="info" %}
**Gravitee version compatiblity**\
From Gravite version 3.10.0 and beyond, Gravitee APIM uses the 4.1.2 version of the Java Driver. Therefore, some settings are no longer available:

* `threadsAllowedToBlockForConnectionMultiplier` and `socketKeepAlive` have been deprecated in 3.12 and removed in 4.0
* `heartbeatConnectTimeout` and `heartbeatSocketTimeout` can’t be used to configure the `MongoClient` object. Instead, `connectTimeout` and `socketTimeout` values are used to configure the heartbeat
* `cursorFinalizerEnabled` has been removed

See:\
[https://mongodb.github.io/mongo-java-driver/3.12/javadoc/com/mongodb/MongoClientOptions.html#getThreadsAllowedToBlockForConnectionMultiplier(](https://mongodb.github.io/mongo-java-driver/3.12/javadoc/com/mongodb/MongoClientOptions.html#getThreadsAllowedToBlockForConnectionMultiplier\())

[https://mongodb.github.io/mongo-java-driver/3.12/javadoc/com/mongodb/MongoClientOptions.html#isSocketKeepAlive(](https://mongodb.github.io/mongo-java-driver/3.12/javadoc/com/mongodb/MongoClientOptions.html#isSocketKeepAlive\())

[https://github.com/mongodb/mongo-java-driver/blob/master/driver-core/src/main/com/mongodb/MongoClientSettings.java#L807-L814](https://github.com/mongodb/mongo-java-driver/blob/master/driver-core/src/main/com/mongodb/MongoClientSettings.java#L807-L814)
{% endhint %}

### Use a custom prefix

From APIM 3.7 and beyond, you can use a custom prefix for your collection names. This is useful if you want to use the same databases for APIM and AM, for example.

#### Use a custom prefix on a new installation

If you are installing APIM for the first time, you need to update the following two values in the APIM Gateway and APIM API `gravitee.yml` files:

* `management.mongodb.prefix`
* `ratelimit.mongodb.prefix`

By default, these values are empty.

#### Migrating an existing installation

Before running any scripts, you must create a dump of your existing database. You need to repeat these steps on both APIM Gateway and APIM API.

To prefix your collections, you need to rename them. You can use [this script](https://gh.gravitee.io/gravitee-io/gravitee-api-management/master/gravitee-apim-repository/gravitee-apim-repository-mongodb/src/main/resources/scripts/3.7.0/1-rename-collections-with-prefix.js), which renames all the collections by adding a prefix and rateLimitPrefix of your choice.

Then, update these values: `management.mongodb.prefix` and `ratelimit.mongodb.prefix` in the `gravitee.yml` file.

### Index

You can create an index using the [script](https://github.com/gravitee-io/gravitee-api-management/blob/master/gravitee-apim-repository/gravitee-apim-repository-mongodb/src/main/resources/scripts/create-index.js) available from our MongoDB GitHub repository. You must use the correct version of this script for the version of APIM you are running. If you use a custom prefix for collections, do not forget to set it on the first line of the script.

### Security

Sometimes, you need to apply specific security constraints and rules to users accessing your database. The following table summarizes how to define fine-grained constraints per collection.

| Component    | Read-only                           | Read-write                       |
| ------------ | ----------------------------------- | -------------------------------- |
| APIM Gateway | apis - keys - subscriptions - plans | events - ratelimit - commands    |
| APIM API     | -                                   | all collections except ratelimit |

[^1]: _\*Using JDBC as a rate limit repository is not recommended. It can lead to inaccuracies in limit calculation, as counter is not shared across concurrent threads._
