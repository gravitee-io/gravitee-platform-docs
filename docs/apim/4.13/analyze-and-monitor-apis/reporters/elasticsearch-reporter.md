---
description: Configuration guide for the Elasticsearch reporter.
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
