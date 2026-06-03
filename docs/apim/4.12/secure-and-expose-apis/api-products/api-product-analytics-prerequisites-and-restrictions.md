# API Product Analytics: Prerequisites and Restrictions

## Prerequisites

- Gravitee API Management 4.12 or later
- v4 APIs (API Product tracking is not supported for v2 APIs)
- Elasticsearch index templates updated to include `api-product-id` keyword mapping

## Filtering and Viewing API Product Data

### Filtering Analytics by API Product

Navigate to the analytics dashboard and open the filter bar. Select **API Product** from the filter dropdown and choose one or more API Products using the `EQ` or `IN` operator. The analytics engine queries the database for matching API Product IDs and returns aggregated metrics.

### Viewing API Product Information in Environment Logs

The environment logs table displays the API Product name below the API name in the **API** column. When a log entry is associated with an API Product, the product name appears in a lighter font beneath the API name. Logs from standalone APIs display **Standalone API** as the product name. Open the log detail panel to view the **API Product** field in the **More Details** section; this field shows the resolved product name or a dash (`—`) when no product is associated.

### Filtering Environment Logs by API Product

Use the `apiProductIds` query parameter in the logs API to filter logs by API Product ID. This parameter accepts an array of API Product IDs and is only supported for v4 APIs. The filter returns logs where the `apiProductId` field matches one of the provided IDs.

## Restrictions

- API Product tracking is only supported for v4 request/response APIs. v2 APIs and streaming APIs (message logs, message metrics) do not track API Product associations.
- The `API_PRODUCT` filter and facet are only available for v4 APIs.
- API Product IDs are not indexed in analytics log records. Filter queries always query the database, not Elasticsearch.
- Displaying API Product names in logs requires a batch query to the API Product service. If the product is deleted or inaccessible, the name will be `null`.
- Elasticsearch index templates must be updated to include the `api-product-id` keyword mapping. Existing indices without this field will not break, but filtering by API Product will not work until the mapping is updated and indices are rolled over.
