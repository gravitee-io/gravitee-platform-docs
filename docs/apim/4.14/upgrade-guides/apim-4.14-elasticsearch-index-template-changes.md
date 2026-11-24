---
description: The Elasticsearch index templates gain a connection-phase field for API Management 4.14 message APIs. Learn which templates change and how.
---

# APIM 4.14 Elasticsearch Index Template Changes

## Overview

From APIM 4.14, the Gateway reports a message API connection in two documents: one when the connection opens, and one when it ends. The `connection-phase` field tells them apart. For more information, see [Message API connections](../analyze-and-monitor-apis/reporters/elasticsearch-reporter.md#message-api-connections).

APIM 4.14 adds the `connection-phase` field to the following Elasticsearch index templates, for Elasticsearch 7.x, 8.x, and 9.x, and OpenSearch:

* The v4-metrics template.
* The v4-log template.

The data stream templates of the `serverless/` folder in the `gravitee-apim-distribution-es-index-mappings` ZIP file include the field too. For more information, see [Read Analytics from Data Streams](../prepare-a-production-environment/repositories/elasticsearch-data-streams.md).

## Template updates for v4 APIs

{% hint style="info" %}
If you use the Elasticsearch reporter, the reporter registers the updated index templates when the Gateway starts. If you manage the templates yourself, add `connection-phase` to your v4-metrics and v4-log index templates before you upgrade to 4.14.
{% endhint %}

The field mapping is identical for every supported engine version. Add the `connection-phase` keyword field to the `properties` section of each template below.

### v4-metrics template

```json
"connection-phase": {
      "type": "keyword"
  },
```

### v4-log template

```json
"connection-phase": {
      "type": "keyword"
  },
```

## Existing indices

Index templates apply when an index is created. The index that the Gateway writes to at the time of the upgrade keeps its previous mapping, and Elasticsearch maps `connection-phase` dynamically as `text` in that index.

The Management API reads this dynamic mapping correctly: connections are counted once and timed as expected, and the logs list each connection once. You don't need to roll over or rebuild the index. The next index that the Gateway creates, the next day's index in daily mode or the next backing index after a rollover in ILM mode, maps `connection-phase` as `keyword`.

## Upgrade the Management API with the Gateway

A Management API earlier than 4.14 doesn't read the `connection-phase` field. It counts each connection that a 4.14 Gateway reports twice, and lists it twice in the logs. Upgrade the Management API to 4.14 before or together with the Gateways.

## Field description

* `connection-phase`: the phase of a message API connection that the document reports. `open` marks the document reported when the connection opens, whose ID is `<request-id>:open`, in the v4-metrics and v4-log indices. `end` marks the document reported when the connection ends, in the v4-metrics index. Documents of other APIs don't have the field.
