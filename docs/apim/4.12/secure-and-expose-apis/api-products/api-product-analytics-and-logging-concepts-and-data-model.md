# API Product Analytics and Logging: Concepts and Data Model

## Overview

API Product Analytics and Logging lets you track and filter API requests by API Product across analytics dashboards, environment logs, and reporter outputs. When an API is accessed through an API Product subscription, the request is associated with that product, allowing product-level observability and filtering. This feature applies to v4 request/response APIs only.

## Key Concepts

### API Product Association

When a request is made through an API Product subscription, it is associated with that API Product, and the product name is displayed alongside the API in analytics and logs. For APIs accessed without an API Product subscription, the console displays **Standalone API** as the product name.

### Analytics Filtering

You can filter analytics by one or more API Products. This filtering is available for v4 APIs only.

### Reporter Integration

Reporters capture the API Product ID in their output. The Datadog reporter adds an `ApiProductId:<value>` metric tag when the request is made through an API Product subscription; the tag is absent for standalone API access. For the file and TCP reporters the field name depends on the configured output format: `apiProductId` in JSON output, and `api-product-id` in Elasticsearch output. The Elasticsearch reporter indexes the field as `api-product-id`. In CSV output the value is appended to each record, using an empty string when no API Product subscription is used.
