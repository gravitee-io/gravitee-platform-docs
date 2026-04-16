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

## Template updates for v4 APIs

The following field must be added to the `properties` section of the v4-metrics and v4-log index templates for all supported Elasticsearch and OpenSearch variants.

{% hint style="warning" %}
If you use the Elasticsearch reporter, APIM automatically applies these template updates during the upgrade. If you manage templates independently, add `api-product-id` to your v4-metrics and v4-log index templates before upgrading to 4.12.
{% endhint %}

Add the following field to your existing templates:

1. [#elasticsearch-7.x-v4-metrics-template](apim-4.12-elasticsearch-index-template-changes.md#elasticsearch-7.x-v4-metrics-template "mention")
2. [#elasticsearch-7.x-v4-log-template](apim-4.12-elasticsearch-index-template-changes.md#elasticsearch-7.x-v4-log-template "mention")
3. [#elasticsearch-8.x-v4-metrics-template](apim-4.12-elasticsearch-index-template-changes.md#elasticsearch-8.x-v4-metrics-template "mention")
4. [#elasticsearch-8.x-v4-log-template](apim-4.12-elasticsearch-index-template-changes.md#elasticsearch-8.x-v4-log-template "mention")
5. [#elasticsearch-9.x-v4-metrics-template](apim-4.12-elasticsearch-index-template-changes.md#elasticsearch-9.x-v4-metrics-template "mention")
6. [#elasticsearch-9.x-v4-log-template](apim-4.12-elasticsearch-index-template-changes.md#elasticsearch-9.x-v4-log-template "mention")
7. [#opensearch-v4-metrics-template](apim-4.12-elasticsearch-index-template-changes.md#opensearch-v4-metrics-template "mention")
8. [#opensearch-v4-log-template](apim-4.12-elasticsearch-index-template-changes.md#opensearch-v4-log-template "mention")

### Elasticsearch 7.x v4 Metrics Template

For the Elasticsearch 7.x v4 Metrics Template, add the following field mapping to the `properties` section:

```json
"api-product-id": {
    "type": "keyword"
}
```

### Elasticsearch 7.x v4 Log Template

For the Elasticsearch 7.x v4 Log Template, add the following field mapping to the `properties` section:

```json
"api-product-id": {
    "type": "keyword"
}
```

### Elasticsearch 8.x v4 Metrics Template

For the Elasticsearch 8.x v4 Metrics Template, add the following field mapping to the `properties` section:

```json
"api-product-id": {
    "type": "keyword"
}
```

### Elasticsearch 8.x v4 Log Template

For the Elasticsearch 8.x v4 Log Template, add the following field mapping to the `properties` section:

```json
"api-product-id": {
    "type": "keyword"
}
```

### Elasticsearch 9.x v4 Metrics Template

For the Elasticsearch 9.x v4 Metrics Template, add the following field mapping to the `properties` section:

```json
"api-product-id": {
    "type": "keyword"
}
```

### Elasticsearch 9.x v4 Log Template

For the Elasticsearch 9.x v4 Log Template, add the following field mapping to the `properties` section:

```json
"api-product-id": {
    "type": "keyword"
}
```

### OpenSearch v4 Metrics Template

For the OpenSearch v4 Metrics Template, add the following field mapping to the `properties` section:

```json
"api-product-id": {
    "type": "keyword"
}
```

### OpenSearch v4 Log Template

For the OpenSearch v4 Log Template, add the following field mapping to the `properties` section:

```json
"api-product-id": {
    "type": "keyword"
}
```

### Field Description

* `api-product-id`: The API Product identifier associated with the request. Present when the request was processed via an API Product subscription; omitted when the request was made directly against the API.
