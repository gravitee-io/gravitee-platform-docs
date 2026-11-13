---
description: >-
  Release notes for Gravitee API Management 4.14, covering new features,
  improvements, breaking changes, and deprecations. Browse the full list of
  changes.
---

# APIM 4.14

## Highlights

* The New Developer Portal lists the AI Workspaces that a user is a member of, with the budget, consumption, endpoint path, API key, and models of each one.
* The Management API reference lists the Portal API once per Developer Portal: **Next Gen Portal** for the New Developer Portal, the entry to build a custom developer portal on, and **Classic Portal** for the Classic Developer Portal.

## Breaking Changes and deprecations

#### **Alpine Linux images of the Gateway and the Management API are deprecated**

From 4.14.0, the `graviteeio/apim-gateway` and `graviteeio/apim-management-api` images are also published with `-alpine` tags, which point to the same images as the tags without a suffix. The March 2027 release of APIM moves the tags without a suffix, including `latest`, to the Debian image. The June 2027 release stops publishing Alpine Linux images of these two components. To stay on Alpine Linux until then, switch to the `-alpine` tags. To move to Debian, use the `-debian` tags, and check how the Debian image differs before you switch. For more information, see [Breaking Changes and Deprecations](../breaking-changes-and-deprecations.md).

## New Features

APIM 4.14 adds the following features.

#### **AI Workspaces in the New Developer Portal**

* With **Enable AI Workspaces** turned on in the **Portal capabilities** of the Portal Settings, the New Developer Portal shows **My Workspace**, which lists the AI Workspaces that the logged-in user is a member of. The setting is off by default and requires an Enterprise license.
* The details of an AI Workspace show the allocated budget, the tokens, requests, and spend of the last 30 days, the endpoint path, a request snippet for the selected model and client, the user's API key, and the models with their input and output prices.
* A user becomes a member when an administrator adds them to an AI Workspace in Agent Management.
* For more information, see [Show AI Workspaces in the Developer Portal](../../developer-portal/new-developer-portal/show-ai-workspaces-in-the-developer-portal.md).

#### **Elasticsearch: API keys, Elastic Cloud Serverless, and data streams**

* The Gateway reporter and the Management API authenticate to Elasticsearch with an API key, set in `security.api_key`, or in `es.security.apiKey` with Helm. An API key and a username and password are mutually exclusive.
* The Gateway reporter and the Management API detect Elastic Cloud Serverless from the cluster. The `flavor` setting forces the detection with `classic` or `serverless`. At startup, the reporter logs one line with its flavor, authentication, and index mode.
* The Management API reads analytics from data streams named `<index>-<type>` with `analytics.elasticsearch.index_mode: data_stream`, on Elastic Cloud Serverless, where this mode applies by default, and on classic clusters. With Helm, `api.analytics.elasticsearch.index_mode` sets this mode for the Management API alone.
* The `gravitee-apim-distribution-es-index-mappings` ZIP file publishes data stream index templates in its `serverless/` folder.
* The Gateway reporter doesn't write to data streams. It stays inactive on Elastic Cloud Serverless, and rejects `data_stream` on classic clusters. Data streams must be filled by another writer, for example Logstash.
* APIM doesn't migrate existing analytics to data streams, and the Management API doesn't read dated indices and data streams together. On Elastic Cloud Serverless, APIM doesn't set the retention of the data streams.
* For more information, see [Read Analytics from Data Streams](../../prepare-a-production-environment/repositories/elasticsearch-data-streams.md) and [ElasticSearch](../../prepare-a-production-environment/repositories/elasticsearch.md).

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
