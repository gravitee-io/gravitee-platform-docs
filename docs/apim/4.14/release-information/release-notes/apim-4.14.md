---
description: >-
  Release notes for Gravitee API Management 4.14, covering new features,
  improvements, breaking changes, and deprecations. Browse the full list of
  changes.
---

# APIM 4.14

## Highlights

* The New Developer Portal lists the AI Workspaces that a user is a member of, with the budget, consumption, endpoint path, API key, and models of each one.
* Gateway reporters and the Management API authenticate to Elasticsearch with an API key, detect Elastic Cloud Serverless, and read and write analytics as data streams.
* A Groovy script reads the body of a v4 HTTP proxy API as bytes or as a base64 string, and returns binary content that arrives unchanged.
* A native Kafka API endpoint group bounds the metadata requests that each Gateway instance sends to the brokers, with **Backend metadata max age (seconds)**.
* The Management API reference lists the Portal API once per Developer Portal: **Next Gen Portal** for the New Developer Portal, the entry to build a custom developer portal on, and **Classic Portal** for the Classic Developer Portal.

## Breaking Changes and deprecations

#### **Alpine Linux images of the Gateway and the Management API are deprecated**

From 4.14.0, the `graviteeio/apim-gateway` and `graviteeio/apim-management-api` images are also published with `-alpine` tags, which point to the same images as the tags without a suffix. The March 2027 release of APIM moves the tags without a suffix, including `latest`, to the Debian image. The June 2027 release stops publishing Alpine Linux images of these two components. To stay on Alpine Linux until then, switch to the `-alpine` tags. To move to Debian, use the `-debian` tags, and check how the Debian image differs before you switch. For more information, see [Breaking Changes and Deprecations](../breaking-changes-and-deprecations.md).

#### **The Gateway and the Management API verify the Elasticsearch certificate**

From 4.14.0, the Gateway reporter and the Management API verify the certificate of an Elasticsearch cluster that they reach over `https`, including its host name. They use the truststore set in `ssl.truststore`, or the default truststore of the JVM. In 4.13 and earlier, they accepted any certificate. A cluster whose certificate is self-signed or signed by an internal authority needs a truststore, or `ssl.trustAll: true` to keep the previous behavior. With Helm, set `es.ssl.truststore` or `es.ssl.trustAll`. For more information, see [Breaking Changes and Deprecations](../breaking-changes-and-deprecations.md).

#### **Message API connections are reported in two documents**

From 4.14.0, the Gateway reports a message API connection in two documents: one when the connection opens, and one when it ends. The new `connection-phase` field tells them apart. The Management API counts a connection from its opening and reads its duration from its end. A Management API earlier than 4.14 counts each connection twice, so upgrade it before or together with the Gateways. Dashboards or queries that read the v4 metrics and v4 log indices directly must apply the same rule. For more information, see [Breaking Changes and Deprecations](../breaking-changes-and-deprecations.md) and [APIM 4.14 Elasticsearch Index Template Changes](../../upgrade-guides/apim-4.14-elasticsearch-index-template-changes.md).

## New Features

APIM 4.14 adds the following features.

#### **AI Workspaces in the New Developer Portal**

* With **Enable AI Workspaces** turned on in the **Portal capabilities** of the Portal Settings, the New Developer Portal shows **My Workspace**, which lists the AI Workspaces that the logged-in user is a member of. The setting is off by default and requires an Enterprise license.
* The details of an AI Workspace show the allocated budget, the tokens, requests, and spend of the last 30 days, the endpoint path, a request snippet for the selected model and client, the user's API key, and the models with their input and output prices.
* A user becomes a member when an administrator adds them to an AI Workspace in Agent Management.
* For more information, see [Show AI Workspaces in the Developer Portal](../../developer-portal/new-developer-portal/show-ai-workspaces-in-the-developer-portal.md).

#### **Binary bodies in the Groovy policy**

* In a v4 HTTP proxy API with **Read content** enabled, a Groovy script reads the body of its phase as bytes with `contentAsByteArray`, or as a base64 string with `contentAsBase64`.
* With **Read content** and **Override content** enabled, a script that returns a `byte[]` or a `Buffer` replaces the body with those exact bytes, so binary content such as an image arrives unchanged. A script that returns a `String` works as before.
* In a v2 API, both work in **On-request content script** and **On-response content script**, with **Emulate v4 engine** turned on. In the Publish and Subscribe phases of a message API, the returned value is still written as text.
* The feature also ships in APIM 4.13.6 and 4.12.29.
* For more information, see [Groovy](../../create-and-configure-apis/apply-policies/policy-reference/groovy.md#return-binary-content).

#### **Elasticsearch: API keys, Elastic Cloud Serverless, and data streams**

* The Gateway reporter and the Management API authenticate to Elasticsearch with an API key, set in `security.api_key`, or in `es.security.apiKey` with Helm. An API key and a username and password are mutually exclusive.
* The Gateway reporter and the Management API detect Elastic Cloud Serverless from the cluster. The `flavor` setting forces the detection with `classic` or `serverless`. At startup, the reporter logs one line with its flavor, authentication, and index mode.
* The Management API reads analytics from data streams named `<index>-<type>` with `analytics.elasticsearch.index_mode: data_stream`, on Elastic Cloud Serverless, where this mode applies by default, and on classic clusters. With Helm, `api.analytics.elasticsearch.index_mode` sets this mode for the Management API alone.
* The `gravitee-apim-distribution-es-index-mappings` ZIP file publishes data stream index templates in its `serverless/` folder.
* The Gateway reporter writes analytics to data streams named `<index>-<type>` with `reporters.elasticsearch.index_mode: data_stream`, on Elasticsearch 7.9 or later and on OpenSearch. `daily` stays the default. To move an existing installation, switch every Gateway and the Management API at the same time, as described in [Migrate the Elasticsearch Reporter to Data Streams](../../analyze-and-monitor-apis/reporters/migrate-the-elasticsearch-reporter-to-data-streams.md). On Elasticsearch, `lifecycle.policies.<type>` attaches an ILM policy to the data streams, or the new `lifecycle.retention.<type>` settings set their data stream lifecycle retention, on Elasticsearch 8.14 or later. A type takes either a policy or a retention. On OpenSearch, an ISM policy reaches the data streams through its `ism_template`. With Helm, set `es.index_mode: data_stream` and `es.lifecycle.retention`. For more information, see [Write analytics to data streams](../../analyze-and-monitor-apis/reporters/elasticsearch-reporter.md#write-analytics-to-data-streams).
* The Gateway reporter writes analytics directly to Elastic Cloud Serverless, without Logstash, to data streams named `<index>-<type>`. It sets the retention of each data stream with `lifecycle.retention.<type>`, `45d` by default, and shortens an existing retention only with `lifecycle.retention.allow_decrease: true`. It manages its index templates through their `_meta`, and its setup doesn't block the Gateway. For more information, see [Write analytics to Elastic Cloud Serverless](../../analyze-and-monitor-apis/reporters/elasticsearch-reporter.md#write-analytics-to-elastic-cloud-serverless).
* The Gateway reporter exposes its bulk settings under `reporters.elasticsearch.bulk`: `max_concurrent_send`, `max_memory_size`, and `retry.max_retries`, `retry.initial_delay`, and `retry.max_delay`. The defaults are unchanged. The reporter counts the documents it drops in the `reporter_elasticsearch_dropped_documents` metric, by reason and type. For more information, see [Bulk settings and dropped documents](../../analyze-and-monitor-apis/reporters/elasticsearch-reporter.md#bulk-settings-and-dropped-documents).
* APIM doesn't migrate existing analytics to data streams, and the Management API doesn't read dated indices and data streams together.
* For more information, see [Read Analytics from Data Streams](../../prepare-a-production-environment/repositories/elasticsearch-data-streams.md) and [Elasticsearch](../../prepare-a-production-environment/repositories/elasticsearch.md).

#### **Kafka Gateway**

* A native Kafka API endpoint group can set **Backend metadata max age (seconds)** on its **Configuration** tab. With a value above `0`, each gateway instance sends its own all-topics metadata request to the brokers at most about once per that many seconds, instead of on every new client connection. The field is empty by default, which applies the gateway-wide default of `0`: one request per connection, as before.
* The gateway configuration gains a default max age for the endpoint groups, Kafka clusters, and Virtual Clusters that set none of their own, and a setting that lets Virtual Cluster metadata refreshes reuse one connection per backend. Both are also Helm values.
* With a max age above `0`, a topic that a gateway instance hasn't seen yet is looked up on the brokers the first time a client fetches from it, and gateway instances that share a distributed cache share the topics they learn.
* In Event Stream Management, a Cluster or a Virtual Cluster sets the same max age for every Kafka Service bound to it.
* The feature also ships in APIM 4.13.2.
* For more information, see [Configure native Kafka API endpoints](../../kafka-gateway/create-and-configure-kafka-apis/configure-kafka-apis/endpoints.md#bound-the-gateways-own-metadata-requests) and [Configure the Kafka Client & Gateway](../../kafka-gateway/configure-the-kafka-client-and-gateway.md#set-the-default-backend-metadata-max-age).

#### **Portal API reference for each Developer Portal**

* The **API** selector of the Management API reference lists the Portal API twice. **Next Gen Portal** lists the operations of the New Developer Portal, and **Classic Portal** lists the operations of the Classic Developer Portal. An operation common to both Developer Portals appears in both entries.
* Build a custom developer portal on the **Next Gen Portal** entry. Operations that only the Classic Developer Portal uses, for example API ratings, tickets, and application alerts, appear only under **Classic Portal**.
* A link saved with the single **Portal** entry of earlier versions opens **Next Gen Portal**, unless it points to an operation that only **Classic Portal** lists.
* In the Portal API specification, each operation declares the entry it's listed under in its `x-gravitee-portal` field: `classic`, `next`, or `both`.
* For more information, see [Management API Reference](../../management-api-reference.md).
