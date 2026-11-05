---
description: Send API Management 4.13 Gateway events to Elasticsearch with the Elasticsearch reporter. Find the configuration details you need.
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

## Attach index lifecycle policies

The reporter attaches no index lifecycle policy by default. To attach policies to the index templates that the reporter creates, configure the following settings in the Gateway `gravitee.yml` file:

* `reporters.elasticsearch.lifecycle.policies.monitor`, `reporters.elasticsearch.lifecycle.policies.health`, `reporters.elasticsearch.lifecycle.policies.request`, and `reporters.elasticsearch.lifecycle.policies.log`: the name of the lifecycle policy to attach to the corresponding index template.
* `reporters.elasticsearch.lifecycle.policy_property_name`: the index setting through which the policy is referenced. The default is `index.lifecycle.name`, which matches Elasticsearch index lifecycle management. If your cluster manages index lifecycles through a different index setting, set this property to the setting your cluster expects. Refer to your cluster vendor's documentation for the setting name.

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
