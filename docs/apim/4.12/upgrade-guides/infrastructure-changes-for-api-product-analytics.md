# Infrastructure Changes for API Product Analytics

## Related Changes

The `gravitee-reporter-api` dependency is upgraded from version 2.1.0 to 2.2.0 to support API Product ID in reporter models.

Elasticsearch index templates for v4-log and v4-metrics must be updated to include the `api-product-id` keyword field mapping. Administrators should apply the updated templates and roll over existing indices to enable API Product filtering.

The environment logs table now displays a loading spinner while fetching log data. The API Product filter in the observability filter bar is fully integrated with the analytics engine. The logs detail panel includes a new **API Product** row in the **More Details** section.
