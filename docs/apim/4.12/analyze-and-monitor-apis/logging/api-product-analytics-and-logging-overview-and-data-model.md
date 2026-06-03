# API Product Analytics and Logging: Overview and Data Model

## Overview

API Product analytics and logging integration enables administrators to track and filter API requests by API Product association. Logs, metrics, and analytics dashboards now include API Product identifiers and names, allowing operators to monitor usage patterns and troubleshoot issues at the product level.

{% hint style="info" %}
This feature requires Gravitee API Management 4.12 or later and applies to v4 APIs only. API Product filtering is not supported for v2 APIs.
{% endhint %}

## Key Concepts

### API Product Association in Logs

Every log entry for a v4 API request includes `apiProductId` and `apiProductName` fields:

* **API Product subscription requests**: Both fields identify the associated product.
* **Standalone API access**: Requests not associated with any API Product display `apiProductId` as null and `apiProductName` as `"Standalone API"`.
* **Deleted API Products**: When an API Product is deleted after logs are recorded, the `apiProductId` remains but `apiProductName` becomes null.

### API Product Filtering

The `API_PRODUCT` filter is available in analytics dashboards and logs queries:

* **No search query**: Returns all API Products in the environment from the database.
* **With search query**: Filters products by name using case-insensitive substring matching.
* **Logs API**: The `apiProductIds` query parameter allows filtering by one or more product IDs. <!-- SME-REQUIRED: Add hyperlink to Logs API reference documentation -->

{% hint style="warning" %}
API Product IDs are not indexed in analytics log records. The `API_PRODUCT` filter always queries the database, not Elasticsearch, even when no query string is provided.
{% endhint %}

### Reporter Data Fields

Reporters emit API Product identifiers in logs and metrics according to the following behavior:

| Reporter Type | Field/Tag Name | Behavior |
|:--------------|:---------------|:---------|
| Datadog | `apiproductid` | Tag present when request uses API Product subscription; absent for standalone API access; null values suppressed |
| CSV | `api-product-id` | Column always present; empty string when no API Product subscription used |
| Elasticsearch/File/TCP | `apiProductId` | Field present in log payload when API Product associated; absent otherwise |

{% hint style="info" %}
Streaming APIs (message logs and message metrics) do not support `api-product-id` fields. This feature applies to request/response APIs only.
{% endhint %}

{% hint style="warning" %}
Existing Elasticsearch indices created before require manual rollover or reindexing to include the `api-product-id` keyword field. The reporter applies updated index templates automatically on startup, but existing indices are not retroactively updated.
{% endhint %}
