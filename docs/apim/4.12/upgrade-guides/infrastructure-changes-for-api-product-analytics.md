# Infrastructure Changes for API Product Analytics

To enable filtering by API Product, you must update the Elasticsearch index templates for the v4-log and v4-metrics indices to include the `api-product-id` keyword field mapping. Apply the updated templates and roll over existing indices.

Existing indices without this field continue to work, but filtering by API Product is not available until the mapping is added and the indices are rolled over.
