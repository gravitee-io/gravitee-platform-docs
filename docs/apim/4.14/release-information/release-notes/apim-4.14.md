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
* The Data Logging Masking policy masks the logs of LLM Proxy and MCP Proxy APIs, including streamed responses.
* A native Kafka API endpoint group bounds the metadata requests that each Gateway instance sends to the brokers, with **Backend metadata max age (seconds)**.
* The Kafka Gateway and the Kafka endpoint of message APIs use the Apache Kafka 4.4 client libraries, and share groups and the streams groups of Kafka Streams applications go through the Kafka Gateway.
* The Management API reference lists the Portal API once per Developer Portal: **Next Gen Portal** for the New Developer Portal, the entry to build a custom developer portal on, and **Classic Portal** for the Classic Developer Portal.
* The Console and the Management API renew the shared API key of an application with a custom API key.
* The **Entrypoints** menu of a v4 API that clients reach over HTTP has a **Path Mappings** tab, to group the API's analytics by path template, such as `/orders/:orderId`.

## Breaking Changes and deprecations

#### **Alpine Linux images of the Gateway and the Management API are deprecated**

From 4.14.0, the `graviteeio/apim-gateway` and `graviteeio/apim-management-api` images are also published with `-alpine` tags, which point to the same images as the tags without a suffix. The March 2027 release of APIM moves the tags without a suffix, including `latest`, to the Debian image. The June 2027 release stops publishing Alpine Linux images of these two components. To stay on Alpine Linux until then, switch to the `-alpine` tags. To move to Debian, use the `-debian` tags, and check how the Debian image differs before you switch. For more information, see [Breaking Changes and Deprecations](../breaking-changes-and-deprecations.md).

#### **The Gateway and the Management API verify the Elasticsearch certificate**

From 4.14.0, the Gateway reporter and the Management API verify the certificate of an Elasticsearch cluster that they reach over `https`, including its host name. They use the truststore set in `ssl.truststore`, or the default truststore of the JVM. In 4.13 and earlier, they accepted any certificate. A cluster whose certificate is self-signed or signed by an internal authority needs a truststore, or `ssl.trustAll: true` to keep the previous behavior. With Helm, set `es.ssl.truststore` or `es.ssl.trustAll`. For more information, see [Breaking Changes and Deprecations](../breaking-changes-and-deprecations.md).

#### **Message API connections are reported in two documents**

From 4.14.0, the Gateway reports a message API connection in two documents: one when the connection opens, and one when it ends. The new `connection-phase` field tells them apart. The Management API counts a connection from its opening and reads its duration from its end. A Management API earlier than 4.14 counts each connection twice, so upgrade it before or together with the Gateways. Dashboards or queries that read the v4 metrics and v4 log indices directly must apply the same rule. For more information, see [Breaking Changes and Deprecations](../breaking-changes-and-deprecations.md) and [APIM 4.14 Elasticsearch Index Template Changes](../../upgrade-guides/apim-4.14-elasticsearch-index-template-changes.md).

#### **The Management API refuses a v4 path mapping outside the path mapping rules**

From 4.14.0, a path mapping of a v4 API starts with `/`, followed by letters, digits, and the characters `:`, `/`, `.`, `_`, and `-`. The Management API refuses to create, import, or update a v4 API with a path mapping outside these rules, including one the API already holds. In 4.13, it accepted any path mapping that compiled as a regular expression, such as `/users/*`. A v4 API created or updated in 4.13 can hold one, including an API managed with the Gravitee Kubernetes Operator, Terraform, or the Automation API. Fix these path mappings before you upgrade. The same rules block migrating a v2 API whose path mappings all break them, unless its only path mapping is `/`. For more information, see [Breaking Changes and Deprecations](../breaking-changes-and-deprecations.md).

#### **Terraform provider 1.2.0: Set the WebSocket frame type**

From 4.14.0, APIM stores `"frameType": "BINARY"` in the subscriber settings of a WebSocket entrypoint that doesn't set it. With Terraform provider 1.2.0 or earlier, every `terraform plan` of that `apim_apiv4` resource then shows a change. After you upgrade the Management API, set `subscriber.frameType` in the entrypoint configuration. Later versions of the provider need no change. For more information, see [Breaking Changes and Deprecations](../breaking-changes-and-deprecations.md#websocket-entrypoint-set-the-frame-type-in-terraform-configurations).

#### **Data Logging Masking: A rule with a path masks each event of a stream**

From 4.14.0, in a logged request or response with the `text/event-stream` content type, a Data Logging Masking rule that sets a `path` masks the value that the path selects in each event. In 4.13 and earlier, a rule that set only a `path` masked the whole body, and a rule that also set a `type` or a `regex` applied it to the whole body. To keep the `type` or `regex` applied to the whole body, add the same rule without a `path`. For more information, see [Breaking Changes and Deprecations](../breaking-changes-and-deprecations.md).

#### **Data Logging Masking: More bodies are masked as a whole**

From 4.14.0, on a v4 API, the Data Logging Masking policy masks as a whole a complete JSON body that isn't valid JSON, such as concatenated documents or fields in single quotes, where 4.13 masked only the values that a rule's `path` selected. A body masked as a whole uses the `replacer` of the first rule that sets one, where 4.13 always used `*`. For more information, see [Breaking Changes and Deprecations](../breaking-changes-and-deprecations.md).

#### **Kafka Gateway: Clients older than Kafka 2.1 are refused**

From 4.14.0, the Kafka Gateway follows the Kafka 4.x protocol baseline. A client request at a version that the baseline dropped, such as a produce request below version 3 or a fetch request below version 4, closes the connection. The Gateway logs a warning that starts with `Client below the protocol floor` and names the client. Java clients from Kafka 2.1 aren't affected. For more information, see [Breaking Changes and Deprecations](../breaking-changes-and-deprecations.md).

#### **Kafka ACL policy 4.0.0: More requests need an ACL**

From 4.14.0, APIM bundles the Kafka ACL policy 4.0.0. For the same ACLs, it refuses requests that 4.13 let through, such as a `DescribeProducers` request without **Read** on the topic, a subscription with a regular expression without **Describe** on every topic, and a `Metadata` request that would create a topic without **Create**. For more information, see [Breaking Changes and Deprecations](../breaking-changes-and-deprecations.md).

#### **Kafka Topic Mapping and Kafka Namespace policies: Subscriptions with a regular expression**

From 4.14.0, a consumer that sets `group.protocol=consumer` and subscribes with a regular expression is refused by a Kafka Topic Mapping policy that has a mapping. The Kafka Namespace policy confines such a subscription to the namespace. In 4.13, both policies left the regular expression unchanged. For more information, see [Breaking Changes and Deprecations](../breaking-changes-and-deprecations.md).

#### **Virtual Clusters: Cluster administration requests are refused**

From 4.14.0, a Virtual Cluster refuses cluster and quorum administration, delegation tokens, client quotas, SCRAM credentials, and the description and listing of transactions with `UNSUPPORTED_VERSION`, even with a single backend. In 4.13, it forwarded these requests to the backend that the connection was bound to. For more information, see [Breaking Changes and Deprecations](../breaking-changes-and-deprecations.md).

#### **Kafka Gateway: A refused produce from an `acks=0` producer closes the connection**

From 4.14.0, when a policy refuses the produce request of a producer set to `acks=0`, the Kafka Gateway closes the connection. In 4.13, it dropped the request and kept the connection open. For more information, see [Breaking Changes and Deprecations](../breaking-changes-and-deprecations.md).

#### **Kafka Gateway: Probe settings that the Gateway doesn't read stop it from starting**

From 4.14.0, with the Kafka Gateway enabled, the Gateway doesn't start when its configuration holds a Kafka probe setting that it doesn't read, such as `kafka.probe.secured` or a setting under `services.kafka-gateway-probes`. In 4.13, it logged a warning and started. For more information, see [Breaking Changes and Deprecations](../breaking-changes-and-deprecations.md).

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

#### **Data Logging Masking on LLM Proxy and MCP Proxy APIs**

* The Data Logging Masking policy runs in the request and response phases of LLM Proxy and MCP Proxy APIs. In the request phase, it masks the values that its rules select in the logged requests, such as the `Authorization` header and the prompts sent to an LLM. In the response phase, it masks them in the logged responses, such as the completions of an LLM and the text that an MCP tool returns. The requests and responses that pass through the Gateway are unchanged.
* In a logged request or response with the `text/event-stream` content type, a rule that sets a `path` masks the value that the path selects in each event, and the other lines of the events stay as they are.
* On a v4 API, when the Gateway cuts a logged JSON body at its maximum log size, a rule that sets a `path` masks the values it selects in the part that was logged.
* For more information, see [Data Logging Masking](../../create-and-configure-apis/apply-policies/policy-reference/data-logging-masking.md#llm-proxy-and-mcp-proxy-apis).

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

#### **Kafka Gateway and Kafka endpoint on Apache Kafka 4.4**

* The Kafka Gateway and the Kafka endpoint of message APIs use the Apache Kafka 4.4 client libraries that APIM ships, where APIM 4.13 shipped Apache Kafka 3.9.
* Share groups, and the streams groups of Kafka Streams applications, go through the Kafka Gateway when the backend Kafka cluster serves them. On a Virtual Cluster, every backend needs to serve them. The policies that act on consumed records also act on the records that share group consumers receive.
* When a policy interrupts on a record that a consumer fetches, only the partition of that record fails, from that record on, and the consumer receives `CORRUPT_MESSAGE` for it. In 4.13, the whole fetch failed. For more information, see [Policy failures](../../kafka-gateway/create-and-configure-kafka-apis/configure-kafka-apis/policies.md#policy-failures).
* The Kafka endpoint of message APIs adds **Linger time (linger.ms)** to its producer settings. Its default, `0`, sends each record at once. For more information, see [Kafka](../../create-and-configure-apis/configure-v4-apis/endpoints/kafka.md#producer-and-consumer-settings).
* For the backend Kafka clusters and the clients tested with the Kafka Gateway, see [Tested brokers and clients](../../kafka-gateway/README.md#tested-brokers-and-clients).

#### **Path mappings on v4 APIs**

* The **Entrypoints** menu of a v4 API that clients reach over HTTP has a **Path Mappings** tab. Add, edit, and delete the path mappings that group the API's analytics by path template, such as `/orders/:orderId`, or import them from an OpenAPI page of the API on the **Swagger Document** tab of **Add path mapping**.
* A request whose path matches a path mapping is recorded under that path mapping in the API's analytics data. Path mappings take effect the next time you deploy the API.
* An OpenAPI import that creates or updates a v4 API sets the API's path mappings from the paths of the specification when **Create the path mapping for analytics** is enabled.
* Migrating a v2 API to v4 keeps the path mappings that follow the path mapping rules and leaves out the others. When every path mapping of the API breaks the rules, the migration is blocked, and its message lists them. An API whose only path mapping is `/` migrates without path mappings.
* For more information, see [Configure path mappings](../../create-and-configure-apis/configure-v4-apis/path-mappings.md).

#### **Portal API reference for each Developer Portal**

* The **API** selector of the Management API reference lists the Portal API twice. **Next Gen Portal** lists the operations of the New Developer Portal, and **Classic Portal** lists the operations of the Classic Developer Portal. An operation common to both Developer Portals appears in both entries.
* Build a custom developer portal on the **Next Gen Portal** entry. Operations that only the Classic Developer Portal uses, for example API ratings, tickets, and application alerts, appear only under **Classic Portal**.
* A link saved with the single **Portal** entry of earlier versions opens **Next Gen Portal**, unless it points to an operation that only **Classic Portal** lists.
* In the Portal API specification, each operation declares the entry it's listed under in its `x-gravitee-portal` field: `classic`, `next`, or `both`.
* For more information, see [Management API Reference](../../management-api-reference.md).

#### **Shared API keys renewed with a custom API key**

* On the **Shared API Keys** tab of an application, **Renew** opens the **Renew API Key** dialog. With **Allow custom API Key** enabled, the dialog has a **Custom API Key** field for the value of the new key. Left empty, the renewal generates a random key.
* The application-scoped renew operation of the Management API takes the value as `customApiKey` in its body.
* A value of an earlier key of the application, even a revoked or expired one, makes that key valid again. A value of a key of another application in the environment, even a revoked or expired one, or the value of the current key, is refused. Every subscription of the application moves to the new key, and the previous key stays valid for two hours.
* The feature also ships in APIM 4.13.8, 4.12.30, and 4.11.36.
* For more information, see [Manage application subscriptions](../../secure-and-expose-apis/subscriptions/manage-subscriptions.md#renew-with-a-custom-api-key).

#### **WebSocket entrypoint: Text frames**

* APIM 4.14 bundles the WebSocket entrypoint 4.0.0, a new major version of the entrypoint.
* The WebSocket entrypoint can send messages to the client as text frames. With **TEXT**, each message is sent as one UTF-8 text message.
* Set it with the **Frame type** field of the subscriber settings, `subscriber.frameType`: **BINARY**, the default, or **TEXT**. Existing APIs keep sending binary frames.
* A message whose payload isn't valid UTF-8 closes the connection with status 1007 (Invalid payload data). If the endpoint delivers unacknowledged messages again, that message closes every reconnection with status 1007 until it's removed at the source.
* **TEXT** requires APIM 4.14.0 or later. Upgrade the Management API first: gateways that don't run APIM 4.14 yet keep sending binary frames until they're upgraded.
* With Terraform provider 1.2.0 or earlier, set `subscriber.frameType` explicitly. Otherwise, once the 4.14 Management API saves the API, every `terraform plan` shows a change. Later versions of the provider need no change. For more information, see [Breaking changes and deprecations](../breaking-changes-and-deprecations.md#websocket-entrypoint-set-the-frame-type-in-terraform-configurations).
* For more information, see [WebSocket](../../create-and-configure-apis/configure-v4-apis/entrypoints/websocket.md#text-frames).
