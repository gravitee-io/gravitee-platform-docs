# API Product Analytics: Prerequisites and Restrictions

## Prerequisites

- Gravitee API Management 4.12 or later
- v4 APIs (API Product tracking is not supported for v2 APIs)
- Elasticsearch index templates updated to include `api-product-id` keyword mapping

## Filtering and Viewing API Product Data

### Filtering Analytics by API Product

Navigate to the analytics dashboard and open the filter bar. Select **API Product** from the filter dropdown and choose one or more API Products. The dashboard displays aggregated metrics for the selected API Products.

### Viewing API Product Information in Environment Logs

The environment logs table displays the API Product name below the API name in the **API** column. When a log entry is associated with an API Product, the product name appears in a lighter font beneath the API name. Logs from standalone APIs display **Standalone API** as the product name. When a request was made through an API Product subscription, open the log detail panel to view the **API Product** field in the **More details** section; this field is not shown for standalone API logs.

### Filtering Environment Logs by API Product

Open the filter panel and select **API Product** to filter environment logs by one or more API Products. This filter applies to v4 request/response APIs only.

## Restrictions

- API Product tracking is only supported for v4 request/response APIs. v2 APIs and streaming APIs (message logs, message metrics) do not track API Product associations.
- If an API Product has been deleted or is inaccessible, its name might not display in logs and analytics.
- Elasticsearch index templates must be updated to include the `api-product-id` keyword mapping. Existing indices without this field will not break, but filtering by API Product will not work until the mapping is updated and indices are rolled over.
