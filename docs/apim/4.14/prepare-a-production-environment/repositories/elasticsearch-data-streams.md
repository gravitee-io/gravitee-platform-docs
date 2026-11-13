---
description: Read API Management 4.14 analytics from Elasticsearch data streams, on Elastic Cloud Serverless or on a classic cluster. Learn the setup and its limitations.
---

# Read Analytics from Data Streams

## Overview

From APIM 4.14, the Management API can read analytics from Elasticsearch data streams instead of dated or ILM-managed indices. This mode applies by default on Elastic Cloud Serverless, which supports data streams only, and you can turn it on for classic Elasticsearch and OpenSearch clusters.

In APIM 4.14, the Management API reads data streams but the Gateway doesn't write them. The data streams are filled by another writer, for example Logstash.

```
Gateway ──▶ writer (for example, the TCP reporter and Logstash) ──▶ data streams ◀── Management API
```

{% hint style="danger" %}
**The Gateway reporter doesn't write to data streams**

The Elasticsearch reporter doesn't support `index_mode: data_stream`:

* On a classic cluster, the reporter rejects `reporters.elasticsearch.index_mode: data_stream`, logs an error, and stays inactive.
* On Elastic Cloud Serverless, the reporter stays inactive whatever its configuration.

In both cases, the Gateway serves API traffic but doesn't report analytics to Elasticsearch. For more information, see [Elasticsearch Reporter](../../analyze-and-monitor-apis/reporters/elasticsearch-reporter.md#cluster-flavor-and-startup-checks).
{% endhint %}

## Prerequisites

* An Elasticsearch cluster that supports data streams, or Elastic Cloud Serverless. For Elastic Cloud Serverless, you can authenticate with an API key. For more information, see [Authenticate with an API key](elasticsearch.md#authenticate-with-an-api-key).
* A writer that sends the Gateway analytics to the data streams in the document format of the Elasticsearch reporter. For example, the `elasticsearch` output of the [TCP reporter](../../analyze-and-monitor-apis/reporters/tcp-reporter.md) uses the same field names, and Logstash can write its events to the data streams.
* The data stream index templates of your APIM version, registered before the first document is written. For more information, see [Register the index templates](#register-the-index-templates).

## Data stream names

The Management API reads one data stream per type of analytics, named `<index>-<type>`, where `<index>` is the value of `analytics.elasticsearch.index`. The default is `gravitee`.

| Type | Default data stream |
| ---- | ------------------- |
| `request` | `gravitee-request` |
| `log` | `gravitee-log` |
| `health` | `gravitee-health` |
| `monitor` | `gravitee-monitor` |
| `v4-metrics` | `gravitee-v4-metrics` |
| `v4-log` | `gravitee-v4-log` |
| `v4-message-metrics` | `gravitee-v4-message-metrics` |
| `v4-message-log` | `gravitee-v4-message-log` |
| `event-metrics` | `gravitee-event-metrics` |
| `decisions` | `gravitee-decisions` |

The `{orgId}` and `{envId}` placeholders in `analytics.elasticsearch.index` are replaced as in the other index modes. For example, with `index: apim-{orgId}`, the Management API reads `apim-<organization ID>-v4-metrics` for the organization's v4 metrics.

## Register the index templates

Each APIM release publishes the `gravitee-apim-distribution-es-index-mappings-<version>.zip` file to Maven Central. From APIM 4.14, its `serverless/` folder holds the data stream templates:

* `pipeline.json`: the ingest pipeline, identical to the pipeline of the `es9x/` folder.
* `<type>.json`: one index template per type in the table of [Data stream names](#data-stream-names), declared with `data_stream`.

The templates follow the mappings of the APIM version that publishes them. They hold no infrastructure settings: no `number_of_shards`, `number_of_replicas`, or `refresh_interval`, no lifecycle policy, and no `data_retention`. The only settings are the `analysis` settings of the log templates, which the body mappings need.

To register the templates:

1. Download the ZIP file of your APIM version, and extract the `serverless/` folder.
2. In each template, check that `index_patterns` matches your data stream names. The templates match `gravitee-<type>*`. If `analytics.elasticsearch.index` differs from `gravitee`, or if it holds a placeholder, replace `gravitee` in the patterns.
3. Register each template with `PUT _index_template/<name>`.
4. Optional: to enrich the documents with the `geoip` and `user_agent` processors, register the pipeline with `PUT _ingest/pipeline/<name>`, and configure your writer to apply it.
5. Configure your writer to create the documents in the data streams with the `create` operation type, which is the only write operation that data streams accept. Each document needs the `@timestamp` field, which the document format of the Elasticsearch reporter includes.

On each APIM upgrade, register the templates of the new version. Their mappings apply to the backing indices created after a rollover.

## Configure the Management API

On Elastic Cloud Serverless, the Management API reads data streams by default. On a classic cluster, set `index_mode` to `data_stream`:

```yaml
analytics:
  type: elasticsearch
  elasticsearch:
    endpoints:
      - https://my-cluster.example.com:443
    index: gravitee
    index_mode: data_stream
    security:
      api_key: <encoded API key>
```

With Helm, `es.index_mode` applies to both the Gateway reporter and the Management API. Because the reporter rejects `data_stream` on a classic cluster, set the mode of the Management API alone with `api.analytics.elasticsearch.index_mode`:

```yaml
es:
  index_mode: daily # Read by the Gateway reporter, which doesn't write data streams
api:
  analytics:
    elasticsearch:
      index_mode: data_stream # Read by the Management API only
```

When `api.analytics.elasticsearch.index_mode` is set, the chart renders it as `analytics.elasticsearch.index_mode` in the Management API configuration instead of `es.index_mode`. It's unset by default.

In data stream mode, the Management API reads field types with the `_field_caps` API instead of the `_mapping/field` API, which Elastic Cloud Serverless doesn't expose.

## Limitations

| Limitation | Details |
| ---------- | ------- |
| The Gateway reporter doesn't write data streams | The data streams must be filled by another writer, for example Logstash. The reporter stays inactive on Elastic Cloud Serverless, and rejects `data_stream` on a classic cluster. |
| No migration of existing analytics | APIM doesn't move the content of dated or ILM-managed indices to data streams. In data stream mode, the Management API reads only the data streams, not the previous indices. Analytics written before the switch don't appear. |
| Retention isn't managed by APIM on Elastic Cloud Serverless | The templates set no `data_retention`, and the reporter's lifecycle policies don't apply. The writer or the cluster administrator sets the retention of each data stream. |
| GeoIP enrichment has no effect on Elastic Cloud Serverless | Elastic Cloud Serverless accepts an ingest pipeline with the `geoip` processor, but the processor adds no location data. |
| Index pattern of the templates | The templates match `gravitee-<type>*`. Data streams with other names need the patterns edited before registration. |
