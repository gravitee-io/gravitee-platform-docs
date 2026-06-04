# API Product Analytics and Logging: Concepts and Data Model

## Overview

API Product Analytics and Logging lets you track and filter API requests by API Product across analytics dashboards, environment logs, and reporter outputs. When an API is accessed through an API Product subscription, the request is associated with that product, allowing product-level observability and filtering. This feature applies to v4 request/response APIs only.

## Key Concepts

### API Product Association

When a request is made through an API Product subscription, it is associated with that API Product, and the product name is displayed alongside the API in analytics and logs. For APIs accessed without an API Product subscription, the console displays **Standalone API** as the product name.

### Analytics Filtering

You can filter analytics by one or more API Products. This filtering is available for v4 APIs only.

### Reporter Integration

Reporters capture API Product IDs in their output formats. The Datadog reporter emits an `apiproductid` tag when the request is made through an API Product subscription; the tag is absent for standalone API access. The CSV reporter writes an `api-product-id` column for all requests, using an empty string when no API Product subscription is used. Log payloads sent to Elasticsearch, file, or TCP reporters include the `apiProductId` field automatically.
