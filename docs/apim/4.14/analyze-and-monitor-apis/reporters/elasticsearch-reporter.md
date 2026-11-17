---
description: Send API Management 4.14 Gateway events to Elasticsearch with the Elasticsearch reporter. Find the configuration details you need.
metaLinks:
  alternates:
    - elasticsearch-reporter.md
---

# Elasticsearch Reporter

Configuration details for the Elasticsearch reporter are available in the [Elasticsearch Repository](../../prepare-a-production-environment/repositories/elasticsearch.md#elasticsearch) documentation.

## Analytics events dropped when the ingest pipeline isn't registered

At startup, the reporter registers an ingest pipeline named `gravitee_pipeline` in Elasticsearch. The `reporters.elasticsearch.pipeline.plugins.ingest` setting controls the ingest processors in the pipeline and defaults to `geoip, user_agent`.

When the pipeline registration fails, or when analytics events arrive before the registration completes, the reporter fails to format every event. Each failed event writes an `Unable to format incoming reportable` warning to the Gateway log with a `NullPointerException` stack trace, and the event isn't delivered to Elasticsearch. On a busy Gateway these warnings fill the log, and analytics data stops appearing even though API traffic is served normally.

To diagnose and resolve the state:

* Search the Gateway startup log for `An error occurs while creating index mapping template`. This entry records why the registration against your Elasticsearch cluster failed.
* Confirm that your Elasticsearch cluster accepts the configured ingest processors.
* After you resolve the cluster-side issue, restart the Gateway. The reporter registers the pipeline only at startup.

To stop the warnings while you investigate, set `reporters.elasticsearch.enabled` to `false` in the Gateway `gravitee.yml` file. This setting disables all analytics reporting to Elasticsearch until you re-enable it and restart the Gateway.

## Cluster flavor and startup checks

From APIM 4.14, the reporter reads the flavor of the cluster at startup: a classic Elasticsearch or OpenSearch cluster, or Elastic Cloud Serverless. By default, `reporters.elasticsearch.flavor` is `auto` and the reporter detects the flavor from the cluster. Set it to `classic` or `serverless` to skip the detection. For more information, see [Elastic Cloud Serverless](../../prepare-a-production-environment/repositories/elasticsearch.md#elastic-cloud-serverless).

When it starts, the reporter writes one `INFO` line that summarizes its configuration:

```
Elasticsearch reporter: flavor [classic] (detected), authentication [api_key], index mode [daily], disabled by the flavor [none]
```

* `flavor`: `classic` or `serverless`, followed by `detected` or `configured`.
* `authentication`: `api_key`, `basic`, or `none`.
* `index mode`: the index mode the reporter applies.
* `disabled by the flavor`: the settings the flavor ignores. On Elastic Cloud Serverless, these are the index settings (`number_of_shards`, `number_of_replicas`, `refresh_interval`) and the lifecycle policies.

The reporter stays inactive, and logs an `ERROR` line that names the setting at fault, in the following cases:

| Case | Error |
| ---- | ----- |
| `reporters.elasticsearch.flavor` has a value other than `auto`, `classic`, or `serverless` | `Unknown value [<value>] for 'reporters.elasticsearch.flavor': expected one of auto, classic, serverless.` |
| `reporters.elasticsearch.index_mode` is `data_stream` on an Elasticsearch cluster earlier than 7.9 | `data_stream` needs Elasticsearch 7.9 or later |
| A `reporters.elasticsearch.lifecycle.retention.*` setting is set with `index_mode: data_stream` on an Elasticsearch cluster earlier than 8.14 | The retention needs the data stream lifecycle of Elasticsearch 8.14 or later |
| With `index_mode: data_stream`, a type has both a `reporters.elasticsearch.lifecycle.policies.*` and a `reporters.elasticsearch.lifecycle.retention.*` setting | The data streams of the type take either the ILM policy or the retention |
| A `reporters.elasticsearch.lifecycle.policies.*` or `reporters.elasticsearch.lifecycle.retention.*` setting is set with `index_mode: data_stream` on OpenSearch | OpenSearch doesn't apply the setting to data streams |
| `reporters.elasticsearch.index_mode` is `data_stream` and an alias named `<index>-<type>` exists, as the `ilm` index mode leaves | Elasticsearch would write the documents to the indices of the alias instead of the data stream |
| `reporters.elasticsearch.index_mode` is `daily` or `ilm` on Elastic Cloud Serverless | Elastic Cloud Serverless manages indices itself |
| A `reporters.elasticsearch.lifecycle.policies.*` setting is set on Elastic Cloud Serverless | Elastic Cloud Serverless manages data retention itself |
| Any other configuration on Elastic Cloud Serverless | `The Elastic Cloud Serverless index setup is not available in this version yet.` |

For the data stream cases, see [Write analytics to data streams](#write-analytics-to-data-streams). For the alias case, see [Migrate the Elasticsearch Reporter to Data Streams](migrate-the-elasticsearch-reporter-to-data-streams.md#migrate-from-the-ilm-index-mode).

{% hint style="danger" %}
In APIM 4.14, the reporter doesn't write to Elastic Cloud Serverless. When the reporter is inactive, the Gateway serves API traffic but doesn't report analytics to Elasticsearch. To fill data streams on Elastic Cloud Serverless, use another writer. For more information, see [Read Analytics from Data Streams](../../prepare-a-production-environment/repositories/elasticsearch-data-streams.md).
{% endhint %}

## Write analytics to data streams

From APIM 4.14, the reporter can write analytics to data streams instead of dated or ILM-managed indices, on Elasticsearch 7.9 or later, including Elasticsearch 8 and 9, and on OpenSearch. `daily` stays the default index mode.

The reporter writes each type of analytics to one data stream named `<index>-<type>`, for example `gravitee-request` or `gravitee-v4-log`. At startup, it registers one index template per data stream, with the same mappings as the templates of the other index modes. The data streams have no date suffix and no rollover alias.

{% hint style="info" %}
This section describes a new installation. To move an installation that already writes dated or ILM-managed indices, see [Migrate the Elasticsearch Reporter to Data Streams](migrate-the-elasticsearch-reporter-to-data-streams.md).
{% endhint %}

### Set up a new installation

1.  In the `gravitee.yml` file of every Gateway, set `reporters.elasticsearch.index_mode` to `data_stream`:

    ```yaml
    reporters:
      elasticsearch:
        index: gravitee
        index_mode: data_stream
    ```
2.  In the `gravitee.yml` file of the Management API, set `analytics.elasticsearch.index_mode` to `data_stream`, with the same `index`. For more information, see [Read Analytics from Data Streams](../../prepare-a-production-environment/repositories/elasticsearch-data-streams.md#configure-the-management-api). With Helm, `es.index_mode` sets both. For more information, see [Configure data streams with Helm](#configure-data-streams-with-helm).
3.  Set the lifecycle of each type with a lifecycle policy or a retention, as described in [Set the lifecycle of the data streams](#set-the-lifecycle-of-the-data-streams). On OpenSearch, create the ISM policies with an `ism_template` instead, as described in [Data streams on OpenSearch](#data-streams-on-opensearch).

### Set the lifecycle of the data streams

The reporter attaches no lifecycle to the data streams by default, so their documents are never deleted. Set the lifecycle per type with the following keys:

| Key | Default data streams |
| --- | -------------------- |
| `request` | `gravitee-request`, `gravitee-v4-metrics`, `gravitee-v4-message-metrics` |
| `log` | `gravitee-log`, `gravitee-v4-log`, `gravitee-v4-message-log` |
| `monitor` | `gravitee-monitor` |
| `health` | `gravitee-health` |
| `event_metrics` | `gravitee-event-metrics` |
| `decisions` | `gravitee-decisions` |

For each key, set one of the following settings, but not both:

* `reporters.elasticsearch.lifecycle.policies.<key>`: the name of an index lifecycle management (ILM) policy that you created in Elasticsearch. The reporter attaches it to the index templates of the data streams, through the index setting set in `reporters.elasticsearch.lifecycle.policy_property_name`.
* `reporters.elasticsearch.lifecycle.retention.<key>`: the retention of the data stream lifecycle, as an Elasticsearch time value, for example `7d` or `12h`. The reporter writes it to the `data_retention` of the index templates. This setting requires Elasticsearch 8.14 or later.

None of these keys has a default value. The reporter reads the `lifecycle.retention` settings only with `index_mode: data_stream`. With `daily` or `ilm`, it ignores them without a warning.

The following example deletes the requests and logs through ILM policies, and sets a retention on the other types:

```yaml
reporters:
  elasticsearch:
    index_mode: data_stream
    lifecycle:
      policies:
        request: hot_delete_request
        log: hot_delete_log
      retention:
        monitor: 7d
        health: 3d
        event_metrics: 30d
        decisions: 30d
```

At startup, the reporter checks the lifecycle settings:

* When a key has both a policy and a retention, the reporter stops at startup, on every Elasticsearch version. Keep either the policy or the retention.
* On an Elasticsearch cluster earlier than 8.14, a `lifecycle.retention` setting stops the reporter. Use a lifecycle policy instead.
* When a key has neither a policy nor a retention, the reporter logs a warning that names the data streams whose documents are never deleted.

The reporter sets the lifecycle in the index templates only, so a change doesn't reach the existing data streams at once:

* A new lifecycle policy applies to the backing indices created after the change, from the next rollover. A data stream without a lifecycle doesn't roll over by itself: roll it over with the `POST <name>/_rollover` API of Elasticsearch.
* A new retention applies to the data streams created after the change. To change the retention of an existing data stream, update its lifecycle with the `PUT _data_stream/<name>/_lifecycle` API of Elasticsearch.

### Data streams on OpenSearch

On OpenSearch, Index State Management (ISM) doesn't apply a policy referenced in the index settings of a data stream, and OpenSearch has no data stream retention. With `index_mode: data_stream`, leave the `lifecycle.policies` and `lifecycle.retention` settings unset: the reporter stops at startup when one of them is set. At each startup, the reporter logs a warning that it attaches no lifecycle to the data streams.

To delete the documents, create the ISM policy with an `ism_template` whose `index_patterns` match the data streams, before the data streams are created. The following example deletes the request analytics after 30 days:

```json
PUT _plugins/_ism/policies/hot_delete_request
{
  "policy": {
    "description": "Delete the request analytics after 30 days",
    "default_state": "hot",
    "states": [
      { "name": "hot", "actions": [], "transitions": [ { "state_name": "delete", "conditions": { "min_index_age": "30d" } } ] },
      { "name": "delete", "actions": [ { "delete": {} } ], "transitions": [] }
    ],
    "ism_template": [ { "index_patterns": [ "gravitee-request", "gravitee-v4-metrics", "gravitee-v4-message-metrics" ], "priority": 100 } ]
  }
}
```

### Configure data streams with Helm

With the Helm chart, set the following values:

* `es.index_mode`: `data_stream`. The chart renders this value for both the Gateway reporter and the Management API, unless `api.analytics.elasticsearch.index_mode` sets another mode for the Management API.
* `es.lifecycle.enabled` and `es.lifecycle.policies.<key>`: the lifecycle policies, with the keys `monitor`, `request`, `health`, `log`, `eventMetrics`, and `decisions`. Don't set them on OpenSearch.
* `es.lifecycle.retention.<key>`: the retention, with the same keys. The chart renders these keys whatever the value of `es.lifecycle.enabled`, only the keys that you set, and none is set by default. Don't set them on OpenSearch.

```yaml
es:
  index_mode: data_stream
  lifecycle:
    retention:
      request: 30d
      log: 7d
      monitor: 7d
      health: 3d
      eventMetrics: 30d
      decisions: 30d
```

{% hint style="warning" %}
When `es.lifecycle.enabled` is `true`, for example in values kept from APIM 4.13, the chart renders the six `lifecycle.policies` keys. `monitor`, `request`, `health`, and `log` default to `my_policy`. A type with both a policy and a retention stops the reporter at startup, so with `es.lifecycle.retention` set for one of these keys, the reporter stays inactive.

To use `es.lifecycle.retention`, set `es.lifecycle.enabled` to `false`, or set to `""` the policy of each type that has a retention.
{% endhint %}

## Authenticate with an API key

From APIM 4.14, the reporter authenticates with an API key when `reporters.elasticsearch.security.api_key` is set. An API key and a username and password are mutually exclusive. When the cluster rejects the credentials with a `401` response, the reporter logs `Elasticsearch authentication failed (401)` and names the settings to check. For more information, see [Authenticate with an API key](../../prepare-a-production-environment/repositories/elasticsearch.md#authenticate-with-an-api-key).

## Message API connections

From APIM 4.14, the Gateway reports a message API connection in two documents in the v4 metrics and v4 log indices:

* When the connection opens, a document with the ID `<request-id>:open` and the field `connection-phase` set to `open`.
* When the connection ends, a document with the request ID. In the v4 metrics index, it has `connection-phase` set to `end`.

The Management API reads both documents as one connection:

* Counts, for example the number of requests, include a connection from its opening. A connection that's still open is counted.
* Durations, for example the response time, are read from the end of the connection. A connection that's still open has no duration yet, instead of a duration of 0 ms.
* The logs list a connection once: by its opening while it's open, and by its end after it ends.

Connections reported before APIM 4.14 have one document only, and the Management API reads them as before. The index templates of APIM 4.14 map `connection-phase` as a `keyword`. For more information, see [APIM 4.14 Elasticsearch Index Template Changes](../../upgrade-guides/apim-4.14-elasticsearch-index-template-changes.md).

## Attach index lifecycle policies

The reporter attaches no index lifecycle policy by default. To attach policies to the index templates that the reporter creates, configure the following settings in the Gateway `gravitee.yml` file:

* `reporters.elasticsearch.lifecycle.policies.monitor`, `reporters.elasticsearch.lifecycle.policies.health`, `reporters.elasticsearch.lifecycle.policies.request`, and `reporters.elasticsearch.lifecycle.policies.log`: the name of the lifecycle policy to attach to the corresponding index template.
* `reporters.elasticsearch.lifecycle.policy_property_name`: the index setting through which the policy is referenced. The default is `index.lifecycle.name`, which matches Elasticsearch index lifecycle management. If your cluster manages index lifecycles through a different index setting, set this property to the setting your cluster expects. Refer to your cluster vendor's documentation for the setting name.

With `index_mode: data_stream`, these policies apply to the data streams. For more information, see [Set the lifecycle of the data streams](#set-the-lifecycle-of-the-data-streams).

## Secure the connection with a client keystore

To present a client certificate to Elasticsearch, configure `reporters.elasticsearch.ssl.keystore.type`, `reporters.elasticsearch.ssl.keystore.path`, and `reporters.elasticsearch.ssl.keystore.password` in the Gateway `gravitee.yml` file. None of these settings has a default value.

## Content length mapping in index templates

From APIM 4.11.0, the request and v4 metrics index templates map the `request-content-length` and `response-content-length` fields as `long` instead of `integer`. Index templates apply when an index is created, so existing indices keep their previous mapping until a new index is created.

## Report on applications and plans by name

The reporter records the application and the plan of a request by ID:

* For a v2 API, the reporter writes the application ID to `application` and the plan ID to `plan` in the request index (`gravitee-request-*` by default). It doesn't write the name of either.
* For a v4 API, the reporter writes the application ID of an HTTP request to `application-id` and the plan ID to `plan-id` in the v4 metrics index (`gravitee-v4-metrics-*` by default). When the request matches a subscription, the reporter also writes the application's name at the time of the request to `application-name`. A request through a Keyless plan doesn't match a subscription, so it has no `application-name`.

A request that isn't tied to an application has the application ID `1`. This applies to a request through a Keyless plan, and to a request that the Gateway rejects because no plan accepts it. The reporter doesn't write a plan's name to any index.

To report on applications and plans by name, use one of the following methods.

### Look up names with the Management API

List the IDs and names of your applications and plans with the Management API, and then match them to the IDs in your reporting tool. Make the calls as an organization administrator, so that the lists include every application and plan in the environment.

*   To list the applications of an environment, make the following call:

    ```http
    GET /management/organizations/{orgId}/environments/{envId}/applications/_paged
    ```

    Each item in `data` has the application's `id` and `name`. By default, the list includes active applications only. To list archived applications, add `status=ARCHIVED`. Use `page` and `size` to page through the results, with up to 200 applications per page.
*   To list the plans of an API, including staging, deprecated, and closed plans, make the following call with the API ID that the reporter writes to `api` for a v2 API, or to `api-id` for a v4 API:

    ```http
    GET /management/v2/environments/{envId}/apis/{apiId}/plans?statuses=STAGING,PUBLISHED,DEPRECATED,CLOSED
    ```

    Each item in `data` has the plan's `id` and `name`. Without `statuses`, the list includes published plans only. Use `page` and `perPage` to page through the results.
*   For a v4 API, a document with an `api-product-id` records a plan of that API Product in `plan-id`. To list the plans of an API Product, make the following call:

    ```http
    GET /management/v2/environments/{envId}/api-products/{apiProductId}/plans?statuses=STAGING,PUBLISHED,DEPRECATED,CLOSED
    ```

### Record application names with the Assign metrics policy

For a v2 API that has **Emulate v4 engine** turned on in its [general settings](../../create-and-configure-apis/configure-v2-apis/general-settings.md), the [Assign metrics](../../create-and-configure-apis/apply-policies/policy-reference/assign-metrics.md) policy records the application's name in the request index. The `{#subscription}` object that the metric reads is only available with **Emulate v4 engine** turned on. The policy requires [Gravitee's Enterprise Edition](../../introduction/enterprise-edition.md).

In the [v2 API Policy Studio](../../create-and-configure-apis/apply-policies/v2-api-policy-studio.md), add the **Assign metrics** policy to a flow of the API with the following metric:

* **Name**: `application-name`
* **Value**: `{#subscription.applicationName}`

For each request that matches a subscription, the reporter then writes the application's name to `custom.application-name` in the request index. A request through a Keyless plan has no application name, so it has no `custom.application-name`.

No Expression Language object exposes a plan's name, so this method records application names only. For more information about `{#subscription}`, see [Subscription](../../gravitee-expression-language.md#subscription).

### Add names in a Logstash pipeline

If your Gateways send analytics to Logstash with the [TCP reporter](tcp-reporter.md), add the names in your Logstash pipeline. Build a lookup of IDs and names with the calls in [Look up names with the Management API](#look-up-names-with-the-management-api), and then add a Logstash filter that adds the matching name for each application and plan ID. With the TCP reporter's `elasticsearch` output, the events use the same field names as the Elasticsearch reporter. For the filters that Logstash provides, see [Filter plugins](https://www.elastic.co/docs/reference/logstash/plugins/filter-plugins) in the Elastic documentation.
