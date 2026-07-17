---
description: An overview about repositories.
metaLinks:
  alternates:
    - ./
---

# Repositories

## Overview

Gravitee uses repositories to store different types of data. They are configured in `gravitee.yml` or the Gravitee Helm chart `values.yml`, where each repository can correspond to a particular scope. For example, configuration/management data can be stored in MongoDB, rate limiting data in Redis, and analytics data in Elasticsearch.

## Management Repository

The Management repository is used to store global configurations such as APIs, applications, and API keys. The default configuration uses MongoDB (single server). Use the tab that matches your deployment method.

{% tabs %}
{% tab title="gravitee.yaml" %}
{% code title="gravitee.yml" %}
```yaml
management:
  type: mongodb
  mongodb:
    dbname: ${ds.mongodb.dbname}
    host: ${ds.mongodb.host}
    port: ${ds.mongodb.port}
#    username:
#    password:
#    connectionsPerHost: 0
#    connectTimeout: 500
#    maxWaitTime: 120000
#    socketTimeout: 500
#    socketKeepAlive: false
#    maxConnectionLifeTime: 0
#    maxConnectionIdleTime: 0
#    serverSelectionTimeout: 0
#    description: gravitee.io
#    heartbeatFrequency: 10000
#    minHeartbeatFrequency: 500
#    heartbeatConnectTimeout: 1000
#    heartbeatSocketTimeout: 20000
#    localThreshold: 15
#    minConnectionsPerHost: 0
#    threadsAllowedToBlockForConnectionMultiplier: 5
#    cursorFinalizerEnabled: true
## SSL settings (Available in APIM 3.10.14+, 3.15.8+, 3.16.4+, 3.17.2+, 3.18+)
#    sslEnabled:
#    keystore:
#      path:
#      type:
#      password:
#      keyPassword:
#    truststore:
#      path:
#      type:
#      password:
## Deprecated SSL settings that will be removed in 3.19.0
#    sslEnabled:
#    keystore:
#    keystorePassword:
#    keyPassword:

# Management repository: single MongoDB using URI
# For more information about MongoDB configuration using URI, please have a look to:
# - http://api.mongodb.org/java/current/com/mongodb/MongoClientURI.html
#management:
#  type: mongodb
#  mongodb:
#    uri: mongodb://[username:password@]host1[:port1][,host2[:port2],...[,hostN[:portN]]][/[database][?options]]

# Management repository: clustered MongoDB
#management:
#  type: mongodb
#  mongodb:
#    servers:
#      - host: mongo1
#        port: 27017
#      - host: mongo2
#        port: 27017
#    dbname: ${ds.mongodb.dbname}
#    connectTimeout: 500
#    socketTimeout: 250
```
{% endcode %}
{% endtab %}

{% tab title=".env" %}
Add the following variables to the `.env` file loaded by your `docker-compose.yml`, or to the `environment:` block of the Management API and Gateway services:

```bash
gravitee_management_type=mongodb
gravitee_management_mongodb_dbname=gravitee
gravitee_management_mongodb_host=mongodb
gravitee_management_mongodb_port=27017
# Single MongoDB using URI:
# gravitee_management_mongodb_uri=mongodb://username:password@host:27017/gravitee
```
{% endtab %}

{% tab title="Helm values.yaml" %}
Set `management.type` and the shared `mongo:` block in your `values.yaml` file. The APIM Helm chart uses the same `mongo:` block to render the Management repository connection in the Management API and Gateway `gravitee.yml` files at install time:

```yaml
management:
  type: mongodb

mongo:
  dbhost: graviteeio-apim-mongodb-replicaset-headless
  dbname: gravitee
  dbport: 27017
  rsEnabled: true
  rs: rs0
  connectTimeoutMS: 30000
  sslEnabled: false
  socketKeepAlive: false
  auth:
    enabled: false
    source: admin
    username:
    password:
  # Single MongoDB using URI (overrides dbhost/dbport/dbname):
  # uri: mongodb://username:password@host:27017/gravitee
  # Clustered MongoDB:
  # servers: |
  #   - host: mongo1
  #     port: 27017
  #   - host: mongo2
  #     port: 27017
```
{% endtab %}
{% endtabs %}

## Analytics Repository

The Analytics repository stores all reporting, metrics, API logs, and health-checks for all APIM Gateway instances. The default configuration uses [Elasticsearch](https://www.elastic.co/products/elasticsearch). Use the tab that matches your deployment method.

{% tabs %}
{% tab title="gravitee.yaml" %}
{% code title="gravitee.yml" %}
```yaml
analytics:
  type: elasticsearch
  elasticsearch:
    endpoints:
      - http://localhost:9200
#    index: gravitee
#    security:
#       username:
#       password:
```
{% endcode %}
{% endtab %}

{% tab title=".env" %}
Add the following variables to the `.env` file loaded by your `docker-compose.yml`, or to the `environment:` block of the Management API and Gateway services:

```bash
gravitee_analytics_type=elasticsearch
gravitee_analytics_elasticsearch_endpoints_0=http://localhost:9200
# gravitee_analytics_elasticsearch_index=gravitee
# gravitee_analytics_elasticsearch_security_username=
# gravitee_analytics_elasticsearch_security_password=
```
{% endtab %}

{% tab title="Helm values.yaml" %}
Set the `es:` block in your `values.yaml` file. The APIM Helm chart renders these values into the `analytics.elasticsearch` section of the Management API and Gateway `gravitee.yml` files at install time:

```yaml
es:
  enabled: true
  endpoints:
    - http://elasticsearch-master:9200
  index: gravitee
  security:
    enabled: false
    # username:
    # password:
  ssl:
    enabled: false
    # keystore:
    #   type: jks
    #   path:
    #   password:
```
{% endtab %}
{% endtabs %}

## Rate Limit Repository

When defining the rate-limiting policy, the Gravitee APIM Gateway needs to store data to share with other APIM Gateway instances.

For Management repositories, you can define a custom prefix for the Rate Limit table or collection name.

Counters can be stored in MongoDB, JDBC, Redis Standalone, or Hazelcast.

{% tabs %}
{% tab title="MongoDB" %}
To store counters in MongoDB:

```yaml
ratelimit:
  type: mongodb
  mongodb:
    uri: mongodb://${ds.mongodb.host}/${ds.mongodb.dbname}
    # With MongoDB authentication enabled:
    # uri: mongodb://username:password@host:27017/gravitee?authSource=gravitee
    prefix: # collection prefix
```

The `ratelimit` repository doesn't inherit the credentials of the `management` repository. If your MongoDB deployment requires authentication, include the credentials in the `ratelimit` section too. For the complete list of connection and authentication properties, see [mongodb.md](mongodb.md#rate-limit-repository-configuration).

If you want to use a custom prefix, you need to follow the following [instructions](mongodb.md#use-a-custom-prefix).
{% endtab %}

{% tab title="JDBC" %}
To store counters in JDBC:

```yaml
ratelimit:
  type: jdbc
  jdbc:
    url: jdbc:postgresql://host:port/dbname
    password: # password
    username: # username
    prefix:   # collection prefix
```

If you want to use a custom prefix, you need to follow these [instructions](jdbc.md#use-a-custom-prefix).
{% endtab %}

{% tab title="Redis Standalone" %}
To store counters in Redis Standalone:

```yaml
ratelimit:
  type: redis
  redis:
    host: 'redis.mycompany'
    port: 6379
    password: 'mysecretpassword'
```

Redis Sentinel and Redis SSL configuration options are presented [here](redis.md#redis).
{% endtab %}

{% tab title="Redis Cluster" %}
To store counters in Redis Cluster:

```yaml
ratelimit:
  type: redis
  redis:
    cluster:
      nodes:
        - host: redis-node-1.example.com
          port: 6379
        - host: redis-node-2.example.com
          port: 6379
        - host: redis-node-3.example.com
          port: 6379
```

Redis Cluster mode is mutually exclusive with Sentinel mode. The gateway enforces **Use Replicas**: NEVER for rate limiting to ensure atomic counter operations are always executed on master nodes.
{% endtab %}

{% tab title="Hazelcast" %}
To store counters in Hazelcast:

```yaml
ratelimit:
  type: hazelcast
  hazelcast:
    config-path: ${gravitee.home}/config/hazelcast-ratelimit.xml
```
{% endtab %}
{% endtabs %}

## Supported storage

The following matrix shows scope and storage compatibility.

<table><thead><tr><th width="270">Scope</th><th width="115" data-type="checkbox">MongoDB</th><th data-type="checkbox">Redis</th><th width="143" data-type="checkbox">ElasticSearch</th><th data-type="checkbox">JDBC</th><th data-type="checkbox">Hazelcast</th></tr></thead><tbody><tr><td><strong>Management</strong><br>All the APIM management data such as API definitions, users, applications, and plans</td><td>true</td><td>false</td><td>false</td><td>true</td><td>false</td></tr><tr><td><strong>Rate Limit</strong><br>Rate limiting data</td><td>true</td><td>true</td><td>false</td><td>true</td><td>true</td></tr><tr><td><strong>Analytics</strong><br>Analytics data</td><td>false</td><td>false</td><td>true</td><td>false</td><td>false</td></tr><tr><td><strong>Distributed Sync</strong><br>Responsible for storing the sync state for a cluster</td><td>false</td><td>true</td><td>false</td><td>false</td><td>false</td></tr><tr><td><strong>Token-Bucket Rate Limit</strong><br>Token-bucket rate limiting data. JDBC: rows persist without native TTL. MongoDB: TTL index auto-created. Redis: Lua script. Hazelcast: on-demand map.</td><td>true</td><td>true</td><td>false</td><td>true</td><td>true</td></tr></tbody></table>

Please choose from the options below to learn how to configure these repositories.

{% hint style="warning" %}
Using JDBC as a rate limit repository is not recommended because concurrent threads do not share a counter. This can result in inaccuracies in limit calculations.
{% endhint %}

<table data-view="cards"><thead><tr><th data-type="content-ref"></th><th></th><th></th><th data-hidden data-card-target data-type="content-ref"></th></tr></thead><tbody><tr><td><a href="mongodb.md">mongodb.md</a></td><td></td><td></td><td><a href="elasticsearch.md">elasticsearch.md</a></td></tr><tr><td><a href="elasticsearch.md">elasticsearch.md</a></td><td></td><td></td><td><a href="mongodb.md">mongodb.md</a></td></tr><tr><td><a href="jdbc.md">jdbc.md</a></td><td></td><td></td><td><a href="jdbc.md">jdbc.md</a></td></tr><tr><td><a href="redis.md">redis.md</a></td><td></td><td></td><td><a href="redis.md">redis.md</a></td></tr></tbody></table>
