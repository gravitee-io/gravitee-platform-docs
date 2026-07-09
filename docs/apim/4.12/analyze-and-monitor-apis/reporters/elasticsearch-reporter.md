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
