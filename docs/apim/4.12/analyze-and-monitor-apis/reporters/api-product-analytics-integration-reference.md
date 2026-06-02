# API Product Analytics Integration Reference

## Analytics API

The Analytics API supports the `API_PRODUCT` filter name and facet name. Use this filter to query logs and metrics by API Product ID. The filter is only supported for v4 APIs.

### Query Parameter

The `apiProductIds` parameter accepts an array of API Product IDs:

```
GET /environments/{envId}/apis/{apiId}/logs?apiProductIds=f5e6a5a0-1234-4b3a-9c1e-aabbccddeeff
```

{% hint style="warning" %}
The `apiProductIds` parameter is only supported for v4 APIs. Filtering by API Product on v2 APIs will return no results.
{% endhint %}

## Datadog reporter tags

The Datadog reporter emits an `apiproductid` tag when the request is made through an API Product subscription. The tag value is the API Product ID (e.g., `3fa85f64-5717-4562-b3fc-2c963f66afa6`). The tag is absent for standalone API access; null values are suppressed.

## CSV Reporter Columns

The v4 CSV reporter includes an `api-product-id` column. When no API Product subscription is used, this column writes an empty string (not "null" and not omitted). When an API Product subscription is present, the column contains the API Product ID.

## Elasticsearch Reporter Field

The Elasticsearch reporter conditionally includes an `apiProductId` field in log and metrics documents. The field is present when the request is associated with an API Product subscription and absent for standalone API access.

### Index Template Changes

Elasticsearch index templates for `gravitee-v4.log.*` and `gravitee-v4.metric.*` indices now include an `api-product-id` field with `keyword` type:

The templates are automatically updated when the reporter starts if `extendedRequestTracingEnabled` is enabled.

{% hint style="info" %}
Existing logs and metrics without `api-product-id` will continue to function. The field is optional.
{% endhint %}

{% hint style="warning" %}
Queries filtering by `API_PRODUCT` will return empty results for logs indexed before the migration. Administrators with existing deployments must update index templates and consider rollover for indices created before version 4.12.
{% endhint %}

## Restrictions

* API Product filtering is only supported for v4 APIs. Filtering by API Product on v2 APIs will return no results.
* API Product IDs are not indexed in analytics log records. The `API_PRODUCT` filter always queries the database, not Elasticsearch, even when no search query is provided. This differs from `API`, `APPLICATION`, and `PLAN` filters, which fall back to Elasticsearch when no query is present.
* API Products with null names are excluded from filter value search results and cannot be selected in the UI.
* If an API Product is deleted after a log entry is created, the API Product name cannot be resolved and will remain null in the log detail panel.
* The "Standalone API" label is applied client-side when `apiProductId` is null. If the backend changes this logic, the UI must be updated accordingly.
* API Product support does not extend to streaming APIs. Message logs and message metrics are out of scope.

## Related Changes

* The environment logs table and detail panel now display API Product names.
* The observability filter bar includes a new **API Product** filter.
* The `gravitee-reporter-api` dependency is upgraded to version 2.2.0 to support the `apiProductId` field in reporter models.
