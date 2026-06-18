---
description: An overview of APIM 4.12 Elasticsearch index template changes.
metaLinks:
  alternates:
    - apim-4.12-elasticsearch-index-template-changes.md
---

# APIM 4.12 Elasticsearch Index Template Changes

## Overview

APIM 4.12 adds the `api-product-id` field to the following Elasticsearch index templates:

* [v4 API metrics templates](apim-4.12-elasticsearch-index-template-changes.md#template-updates-for-v4-apis) add `api-product-id` as a new keyword field across all supported variants.
* [v4 API log templates](apim-4.12-elasticsearch-index-template-changes.md#template-updates-for-v4-apis) add `api-product-id` as a new keyword field across all supported variants.

Upgrading APIM to 4.12 is a two-step operation:

1. **Template update** — the Elasticsearch reporter registers the updated index templates on startup. Self-managed setups update them manually.
2. **Rollover or reindex** — the current write index must be rolled over (ILM mode) or recreated (daily mode) so it picks up the new mapping. See [Action required for existing indices](apim-4.12-elasticsearch-index-template-changes.md#action-required-for-existing-indices).

Skipping step 2 leaves `api-product-id` incorrectly typed as `text` on the current write index and breaks API Product analytics filtering until that index rolls over on its own.

## Template updates for v4 APIs

The following field must be added to the `properties` section of the v4-metrics and v4-log index templates for all supported Elasticsearch and OpenSearch variants.

{% hint style="warning" %}
If you use the Elasticsearch reporter, APIM automatically applies these template updates during the upgrade. If you manage templates independently, add `api-product-id` to your v4-metrics and v4-log index templates before upgrading to 4.12.

You must still perform the [action required for existing indices](apim-4.12-elasticsearch-index-template-changes.md#action-required-for-existing-indices). Without it, `api-product-id` is dynamically typed as `text` on the current write index, and API Product analytics filters and term aggregations return empty or incorrect results until that index rolls over.
{% endhint %}

The field mapping is identical for every supported engine version — Elasticsearch 7.x, 8.x, and 9.x, and OpenSearch. Add the `api-product-id` keyword field to the `properties` section of each template below.

### v4-metrics template

```json
"api-product-id": {
      "type": "keyword"
  },
```

### v4-log template

```json
"api-product-id": {
      "type": "keyword"
  },
```

## Action required for existing indices

Updating the index template only affects **newly-created** indices. Any Elasticsearch or OpenSearch index that already exists at the time you upgrade — including the current write index — keeps its original mapping. When the upgraded gateway writes `api-product-id` into an existing index for the first time, the search engine falls back to dynamic mapping and types the field as `text` instead of `keyword`.

While the affected index is in this state:

* Console analytics filtered by API Product return empty results for documents in that index.
* REST API log queries that use the `apiProductIds` filter return empty results for those documents.
* Ingestion continues to succeed — `api-product-id` values are still present in `_source` and can be recovered later with a reindex.

Note: This behaviour is the same on Elasticsearch and OpenSearch. The action below applies to both; substitute your OpenSearch endpoint where the examples say Elasticsearch.

Follow the path that matches your reporter configuration.

### If you use ILM mode (`index_mode: ilm`)

This mode covers Elasticsearch clusters using ILM and OpenSearch clusters using ISM (Index State Management). Both are driven by the Gravitee reporter setting `index_mode: ilm`, which tells APIM to write through a rollover alias instead of daily indices.

Force a rollover of the write aliases so a new backing index is created from the updated template:

```
POST gravitee-v4-metrics-write/_rollover
POST gravitee-v4-log-write/_rollover
```

Replace the alias names with the ones configured in your reporter if you have customised them. `_rollover` is supported by both Elasticsearch and OpenSearch.

This operation is zero-downtime and does not drop any data. Previous backing indices stay searchable through the read alias; new writes land in the freshly-rolled index with `api-product-id` mapped as `keyword`.

{% hint style="warning" %}
If you skip this step, the broken mapping persists on the current backing index until your ILM or ISM policy triggers the next rollover.
{% endhint %}

### If you use daily mode (`index_mode: daily`)

In daily mode, the current day's index (`gravitee-v4-metrics-YYYY.MM.DD`, `gravitee-v4-log-YYYY.MM.DD`) must be recreated so it picks up the updated template. Choose one of the two options below.

#### Option A — Delete the current day's index (fastest, loses today's data)

Appropriate for dev clusters, staging, or production clusters where losing today's partial metrics and logs up to the upgrade time is acceptable.

```
DELETE gravitee-v4-metrics-YYYY.MM.DD
DELETE gravitee-v4-log-YYYY.MM.DD
```

Substitute `YYYY.MM.DD` with the current UTC date. Then start the upgraded gateway. A new index is created from the updated template as soon as the first request is reported, and `api-product-id` is mapped as `keyword`.

#### Option B — Reindex the current day's index (preserves data, requires a pause)

Appropriate for production clusters that cannot tolerate losing today's data.

1. Stop all gateway instances, or otherwise pause writes from the Elasticsearch reporter, so no new documents land in the index during the swap.
2. For each of `gravitee-v4-metrics-YYYY.MM.DD` and `gravitee-v4-log-YYYY.MM.DD`, reindex through a temporary index name:

   ```
   POST _reindex
   {
     "source": { "index": "gravitee-v4-metrics-YYYY.MM.DD" },
     "dest":   { "index": "gravitee-v4-metrics-YYYY.MM.DD-tmp" }
   }
   ```

   The temp name matches the `gravitee-v4-metrics*` pattern, so Elasticsearch creates the temp index from the **updated** template and the reindexed documents inherit `api-product-id: keyword`.
3. Verify the temp index mapping:

   ```
   GET gravitee-v4-metrics-YYYY.MM.DD-tmp/_mapping/field/api-product-id
   ```

   Expected response:

   ```json
   {
     "gravitee-v4-metrics-YYYY.MM.DD-tmp": {
       "mappings": {
         "api-product-id": {
           "full_name": "api-product-id",
           "mapping": { "api-product-id": { "type": "keyword" } }
         }
       }
     }
   }
   ```

   No `"fields"` sub-object must be present.
4. Delete the original and reindex back so the final index has the production name:

   **4a.** Delete the original index:

   ```
   DELETE gravitee-v4-metrics-YYYY.MM.DD
   ```

   **4b.** Reindex from the temp index back to the production name:

   ```
   POST _reindex
   {
     "source": { "index": "gravitee-v4-metrics-YYYY.MM.DD-tmp" },
     "dest":   { "index": "gravitee-v4-metrics-YYYY.MM.DD" }
   }
   ```

   **4c.** Delete the temp index:

   ```
   DELETE gravitee-v4-metrics-YYYY.MM.DD-tmp
   ```

5. Repeat steps 2–4 for `gravitee-v4-log-YYYY.MM.DD`.
6. Start the gateway again.

Reindex doubles the affected index's disk usage for the duration of the swap. For a small cluster (less than 1M docs per day) the procedure takes under five minutes. For large clusters (10M+ docs per day) plan for longer and ensure you have the disk headroom.

{% hint style="info" %}
If you skip the action in daily mode, the broken mapping self-heals at the next UTC midnight when the gateway creates the next daily index. Product analytics remain broken for the rest of the current day.
{% endhint %}

### Verification

After the action, confirm the mapping for every current v4-metrics and v4-log index:

```
GET gravitee-v4-metrics-*/_mapping/field/api-product-id
GET gravitee-v4-log-*/_mapping/field/api-product-id
```

Every index in the response must show:

```json
{ "api-product-id": { "type": "keyword" } }
```

If any index shows `"type": "text"` with a `"keyword"` sub-field, that index was written to before the action and must be reindexed (daily mode) or allowed to roll over (ILM mode) before product-analytics queries will work correctly for it.

## Field Description

* `api-product-id`: The API Product identifier associated with the request. Present when the request was processed via an API Product subscription; omitted when the request was made directly against the API.
