# API Product Analytics and Logging Integration

## Overview

API Product Analytics and Logging Integration extends the analytics engine and environment logs to track and filter requests by API Product. Administrators can filter analytics dashboards and environment logs by API Product, and log entries display the associated API Product name alongside the API name. This feature applies to v4 APIs only.

## Key Concepts

### API Product Facet and Filter

The analytics engine supports `API_PRODUCT` as a facet and filter for all HTTP metrics. The filter accepts API Product IDs and uses the `EQ` (equals) and `IN` (in list) operators. When no query is provided, the filter returns all products in the environment. When a query is provided, the filter performs case-insensitive substring matching against API Product names in the database.

### API Product Fields in Logs

Environment logs include two new fields:

| Field | Type | Presence | Example |
|:------|:-----|:---------|:--------|
| `apiProductId` | string (UUID) | Optional | `f5e6a5a0-1234-4b3a-9c1e-aabbccddeeff` |
| `apiProductName` | string | Optional | `My Partner API Product` |

When an API is not associated with any product, `apiProductId` is `null` and `apiProductName` is set to `"Standalone API"`. When `apiProductId` is present but the product cannot be resolved from the database, `apiProductName` is `null`.

<figure><img src=".gitbook/assets/apim-api-product-analytics-and-logging-integration-step-01.png" alt="Log detail view showing API Product field in the More details section"><figcaption></figcaption></figure>

### Elasticsearch Index Fields

The `api-product-id` field is indexed in Elasticsearch v4 log and v4 metrics templates as a `keyword` type. The field is optional and appears only when the request is associated with an API Product. Existing documents without `api-product-id` continue to function without modification.

## Prerequisites

- Gravitee API Management 4.12 or later
- Elasticsearch 7.x, 8.x, 9.x, or OpenSearch (for analytics and logs storage)
- Updated Elasticsearch index templates for `gravitee-v4.log.*` and `gravitee-v4.metric.*` indices
- v4 APIs (API Product tracking is not supported for v2 APIs)

## Creating API Product Analytics Filters

To filter analytics dashboards by API Product:

1. Navigate to the analytics dashboard.
2. Select **API Product** from the filter dropdown.
3. Enter an API Product name (case-insensitive substring matching) or leave the query empty to display all products in the environment.

    The filter returns API Product IDs that match the query, which are then applied to the analytics query. The `API_PRODUCT` filter supports `EQ` (equals) and `IN` (in list) operators.

    <figure><img src=".gitbook/assets/apim-api-product-analytics-and-logging-integration-step-02.png" alt="Add a filter dialog with API Product field selected and autocomplete suggestions"><figcaption></figcaption></figure>

## Filtering Environment Logs by API Product

To filter environment logs by API Product:

1. Navigate to the environment logs page.
2. Use the `apiProductIds` query parameter. Provide one or more API Product IDs as an array.

    The logs table displays the API name in bold on the first line and the API Product name (or `"Standalone API"`) in a lighter caption font on the second line. The log detail panel includes an **API Product** field in the **More Details** expansion panel, displaying the product name or `—` when no product is associated.

    <figure><img src=".gitbook/assets/apim-api-product-analytics-and-logging-integration-step-03.png" alt="Environment logs page with API Product filter applied showing filtered results"><figcaption></figcaption></figure>

## Restrictions

- API Product IDs are not indexed in v2 request indices. The `api-product-id` field exists only in v4 metrics and v4 log indices.
- The `API_PRODUCT` filter always queries the database and does not fall back to Elasticsearch when no query is provided, unlike `API`, `APPLICATION`, and `PLAN` filters.
- API Product name resolution requires database access. If the `ApiProductQueryService` is unavailable, `apiProductName` will be `null` for logs with a `apiProductId`.
- The `"Standalone API"` label is applied at the use case layer and is not stored in the database or Elasticsearch.
- Filter value search is case-insensitive and substring-based. Exact-match or regex filtering is not supported.
- The `apiProductIds` query parameter in the logs API is only supported for v4 APIs.
- Streaming APIs (message logs, message metrics) do not support `api-product-id` tracking.

## Related Changes

The Datadog reporter now emits an `apiproductid` tag when the request is made through an API Product subscription. The tag is absent for standalone API access, and null values are suppressed. The CSV reporter now includes an `api-product-id` column in v4 exports, which writes an empty string for non-product requests. Elasticsearch index templates for `gravitee-v4.log.*` and `gravitee-v4.metric.*` must be updated to include the `api-product-id` keyword field. Existing deployments require index template upgrades and may need to roll over indices created before version 4.12. The `gravitee-reporter-api` dependency is upgraded from 2.1.0 to 2.2.0 to support the `apiProductId` field in reporter models.
