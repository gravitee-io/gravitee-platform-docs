# Portal analytics dashboards overview

## Overview

Portal analytics dashboards provide API consumers and administrators with pre-configured visualizations of API traffic, performance, and usage metrics. Dashboards aggregate data from HTTP requests, response times, and status codes, so users can monitor trends, identify issues, and analyze API consumption patterns. This feature is available to authenticated users with access to APIs or applications in the portal, and to administrators managing environment-wide analytics.

## Key concepts

Portal analytics dashboards build on a few core concepts.

### Dashboard

A dashboard is a collection of widgets organized in a grid layout. Each dashboard belongs to a single environment and includes metadata such as name, labels, and creation date. Users can pin up to 4 dashboards for quick access. Dashboards are isolated by environment. Attempting to access a dashboard from a different environment returns a `404` error.

### Widget

A widget visualizes a single analytics query. Widget types include:

* **stats**: Displays a single metric value
* **doughnut, pie, and polar area**: Show proportional breakdowns
* **time-series line and bar**: Illustrate trends over time
* **vertical and horizontal bar**: Compare values across categories

Each widget defines a request that specifies:

* **Metrics**: The data source, for example `HTTP_REQUESTS`
* **Measures**: Aggregation functions, such as `COUNT`, `AVG`, `MIN`, `MAX`, `P50`, `P90`, `P95`, `P99`, and `PERCENTAGE`
* **Time range**: Start and end timestamps for the query
* **Filters**: Constraints applied to the query (see Analytics filter)
* **Grouping dimensions**: Optional facets, such as `API`, `APPLICATION`, `HTTP_STATUS_CODE_GROUP`, and `HTTP_STATUS`

### Analytics filter

Filters scope analytics queries to specific APIs, applications, or HTTP status codes. The portal exposes the following filter dimensions:

| Filter name | Type | Operators | Values or range |
|:------------|:-----|:----------|:----------------|
| `API` | KEYWORD | `EQ`, `IN` | Dynamic (the user's authorized APIs) |
| `APPLICATION` | KEYWORD | `EQ`, `IN` | Dynamic (the user's applications) |
| `HTTP_STATUS_CODE_GROUP` | ENUM | `EQ`, `IN` | `1XX`, `2XX`, `3XX`, `4XX`, `5XX` |
| `HTTP_STATUS` | NUMBER | `EQ`, `LTE`, `GTE` | 100 to 599 |

Filters apply at the widget level or globally across a dashboard. Users can only filter by APIs they're authorized to view and applications they own.

### Access control

Analytics access is determined by user role and API or application visibility:

| User role | Authorized APIs | Authorized applications |
|:----------|:----------------|:------------------------|
| Environment admin | All APIs in the environment | None |
| Organization admin | All APIs in the environment | None |
| Authenticated user | APIs visible in portal navigation, plus APIs the user is a member of or subscribed to | The user's applications |
| Anonymous user | Public APIs visible in portal navigation | None |

The feature is gated by the `portal.next.analytics.enabled` environment parameter, which defaults to `false`. When it's disabled, all analytics endpoints return `403`.
