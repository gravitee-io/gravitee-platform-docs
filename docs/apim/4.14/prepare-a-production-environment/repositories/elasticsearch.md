---
description: The Elasticsearch connector for API Management 4.14 uses the HTTP API that Elasticsearch instances expose. Learn how to configure it.
---

# ElasticSearch

## Overview

The Elasticsearch (ES) connector uses the HTTP API exposed by ES instances.

{% hint style="info" %}
**Deprecated support for the native ES client**

Gravitee no longer supports the native ES client. Previous connectors provided by Gravitee are no longer supported.
{% endhint %}

## Supported databases

| Database      | Version tested          |
| ------------- | ----------------------- |
| ElasticSearch | 7.17.x / 8.19.x / 9.5.x |
| OpenSearch    | 1.x / 2.x / 3.x         |

## Prerequisites

The following prerequisites are required for OpenSearch or Elasticsearch integration with Gravitee API Management:

* **Required node roles:** The cluster must have nodes with `master`, `data`, and `ingest` roles. At least one node must have the `ingest` role enabled.
* **Ingest pipelines:** By default, Gravitee configures ingest pipelines (`geoip`, `user_agent`) that are applied during bulk indexing operations.

## Configuration

### APIM API configuration

The Elasticsearch client does not support URL schemes in the format `http://USERNAME:PASSWORD@server.org`. You must provide the username and password using the `analytics.elasticsearch.security.username` and `analytics.elasticsearch.security.password` properties, or an API key using the `analytics.elasticsearch.security.api_key` property.

```yaml
analytics:
  type: elasticsearch
  elasticsearch:
    endpoints:
      - http://localhost:9200
#    index: gravitee
#    index_mode: daily    # "daily" indexes, suffixed with date. Or "ilm" managed indexes, or "data_stream" data streams, both without date
#    flavor: auto         # "auto" detects Elastic Cloud Serverless from the cluster. Or "classic", or "serverless"
#    security:
#       username:
#       password:
#       api_key:          # Instead of username and password. Do not set both.
#    ssl:                        # for https es connection
#      keystore:
#        type: jks               # required. also valid values are "pem", "pfx"
#        path: path/to/jks         # only for only for jks / pkcs12
#        password: <keystore pass> # only for only for jks / pkcs12
#        certs: 'path/to/cert'      # only for pems
#        keys: 'path/to/key'        # only for pems
```

### API Gateway configuration

```yaml
reporters:
  elasticsearch:
    enabled: true # Is the reporter enabled or not (default to true)
    endpoints:
      - http://${ds.elastic.host}:${ds.elastic.port}
#    index: gravitee
#    index_mode: daily    # "daily" indexes, suffixed with date. Or "ilm" managed indexes, without date
#    flavor: auto         # "auto" detects Elastic Cloud Serverless from the cluster. Or "classic", or "serverless"
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
#    security:
#      username:
#      password:
#      api_key:           # Instead of username and password. Do not set both.
#    ssl:                        # for https es connection
#      keystore:
#        type: jks               # required. also valid values are "pem", "pfx"
#        path: path/to/jks         # only for only for jks / pkcs12
#        password: <keystore pass> # only for only for jks / pkcs12
#        certs: 'path/to/cert'      # only for pems
#        keys: 'path/to/key'        # only for pems
```

## Authenticate with an API key

From APIM 4.14, the Gateway reporter and the Management API can authenticate to Elasticsearch with an API key instead of a username and password. For example, use an API key for Elastic Cloud Serverless.

* Set the encoded value of the API key, as Elasticsearch returns it in the `encoded` field, in `reporters.elasticsearch.security.api_key` for the Gateway and in `analytics.elasticsearch.security.api_key` for the Management API.
* An API key and a username and password are mutually exclusive. When both are configured, the Gateway and the Management API don't start.
* The OpenTelemetry traces and logs readers of the Management API accept the same `security.api_key` setting in their own `elasticsearch` configuration.

With Helm, set `es.security.apiKey`. The chart renders it as `security.api_key` for both the Gateway reporter and the Management API, whatever the value of `es.security.enabled`, and it doesn't render `es.security.username` and `es.security.password`. For the OpenTelemetry readers, set `api.otelTraces.elasticsearch.security.apiKey` and `api.otelLogs.elasticsearch.security.apiKey`.

{% hint style="warning" %}
The chart writes the value of `es.security.apiKey` in clear text in the ConfigMap of each component. It doesn't read the API key from a Kubernetes Secret.
{% endhint %}

## Elastic Cloud Serverless

From APIM 4.14, the Gateway reporter and the Management API detect whether they connect to Elastic Cloud Serverless or to a classic cluster, and adapt to it. This is the cluster flavor.

### Set the flavor

The `flavor` setting accepts the following values:

| Value | Behavior |
| ----- | -------- |
| `auto` | Default. The flavor is read from the `build_flavor` that the cluster returns. `serverless` means Elastic Cloud Serverless. Any other value means a classic cluster. |
| `classic` | The cluster is treated as a classic Elasticsearch or OpenSearch cluster, without detection. |
| `serverless` | The cluster is treated as Elastic Cloud Serverless, without detection. |

Set it in `reporters.elasticsearch.flavor` for the Gateway and in `analytics.elasticsearch.flavor` for the Management API. With any other value, the Gateway reporter stays inactive and logs an error, and the Management API doesn't start.

### Gateway reporter on Elastic Cloud Serverless

{% hint style="danger" %}
In APIM 4.14, the Elasticsearch reporter doesn't write to Elastic Cloud Serverless. When the cluster is Elastic Cloud Serverless, the reporter stays inactive: the Gateway serves API traffic, but it doesn't report analytics to Elasticsearch. To send analytics to Elastic Cloud Serverless, use another writer, for example the [TCP reporter](../../analyze-and-monitor-apis/reporters/tcp-reporter.md) with Logstash. For more information, see [Read analytics from data streams](elasticsearch-data-streams.md).
{% endhint %}

For the startup checks of the reporter, see [Elasticsearch Reporter](../../analyze-and-monitor-apis/reporters/elasticsearch-reporter.md#cluster-flavor-and-startup-checks).

### Management API on Elastic Cloud Serverless

On Elastic Cloud Serverless, the Management API always reads analytics from data streams, whatever the value of `analytics.elasticsearch.index_mode`. When `index_mode` is set to `daily` or `ilm`, the Management API ignores it and logs a warning. To remove the warning, remove the setting or set it to `data_stream`.

Elastic Cloud Serverless doesn't expose the `_mapping/field` API. In data stream mode, the Management API reads field types with the `_field_caps` API instead.

## Read analytics from data streams

From APIM 4.14, the Management API can read analytics from data streams instead of dated or ILM-managed indices. This works on Elastic Cloud Serverless and on classic Elasticsearch and OpenSearch clusters. Set `analytics.elasticsearch.index_mode` to `data_stream`. On Elastic Cloud Serverless, this mode applies by default.

In this mode, the Management API reads the data stream named `<index>-<type>` for each type of analytics, for example `gravitee-v4-metrics`. The `{orgId}` and `{envId}` placeholders in `analytics.elasticsearch.index` are replaced as in the other modes.

The Gateway reporter doesn't write to data streams. The data streams must be filled by another writer. For the setup and the limitations, see [Read analytics from data streams](elasticsearch-data-streams.md).

## Index management with ES Curator

ES Curator is a tool for ES administration. To optimize the data footprint and ES performance, define a retention window and periodically merge shards into only one segment.

{% code overflow="wrap" %}
```sh
/usr/bin/curator --config /opt/curator/curator.yml /opt/curator/action-curator.yml
```
{% endcode %}

{% code title="curator.yml" %}
```yaml
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
{% endcode %}

{% code title="action-curator.yml " %}
```yaml
actions:
  1:
    action: forcemerge
    description: "Perform a forceMerge on selected indices to 'max_num_segments' per shard. Merge Days - 1 index for optimize disk space footprint on ElasticSearch TS"
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
{% endcode %}

{% hint style="info" %}
**ES curator deployment hint**

If you deploy ES Curator on every ES data node, set `master_only: True` in the curator configuration file. This ensures the curator is run only once on the elected current master.
{% endhint %}

## Index management with ES ILM

You can configure Index Lifecycle Management (ILM) policies to automatically manage indices according to your retention requirements. For example, you can use ILM to create a new index each day and archive the previous ones. See this [documentation](https://www.elastic.co/guide/en/elasticsearch/reference/current/set-up-lifecycle-policy.html#ilm-create-policy) for more information.

By default, the `index_mode` configuration value is `daily`, where Gravitee suffixes index names with the date. To let ILM handle indexing, you can set `index_mode` to `ILM`. Gravitee will no longer add a suffix to index names. You also need to tell your APIM Gateway which ILM policies to use.

Here’s an example configuration for APIM Gateway:

```yaml
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
        event_metrics: hot_delete_event_metrics # ILM policy for the gravitee-event-metrics-* indexes
    index_mode: ilm         # "daily" indexes, suffixed with date. Or "ilm" managed indexes, without date
```
