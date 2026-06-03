# API Product Analytics and Logging: Concepts and Data Model

## Overview

API Product Analytics and Logging Integration enables administrators to track and filter API requests by API Product association across analytics dashboards, environment logs, and reporter outputs. When an API is accessed through an API Product subscription, the product ID and name are captured in logs, metrics, and analytics facets, allowing product-level observability and filtering. This feature applies to v4 request/response APIs only.

## Key Concepts

### API Product Association

When a request is routed through an API Product subscription, the gateway captures the API Product ID in logs and metrics. The API Product name is resolved at query time and displayed in the console. For APIs accessed without an API Product subscription, the console displays **Standalone API** as the product name. This label is computed at display time and not stored in the database.

### Analytics Filtering and Faceting

The `API_PRODUCT` filter and facet are available in the analytics engine for v4 APIs. Administrators can filter analytics queries by one or more API Product IDs using the `apiProductIds` query parameter. The filter supports `EQ` (equals) and `IN` (set membership) operators. API Product IDs are indexed in Elasticsearch v4-log and v4-metrics indices as keyword fields. API Product IDs are not indexed in analytics log records; filter queries always hit the database.

### Reporter Integration

Reporters capture API Product IDs in their output formats. The Datadog reporter emits an `apiproductid` tag when the request is made through an API Product subscription; the tag is absent for standalone API access. The CSV reporter writes an `api-product-id` column for all requests, using an empty string when no API Product subscription is used. Log payloads sent to Elasticsearch, file, or TCP reporters include the `apiProductId` field automatically.
