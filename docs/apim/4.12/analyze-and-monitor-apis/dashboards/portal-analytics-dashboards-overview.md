# Portal Analytics Dashboards Overview

## Overview

Portal Analytics Dashboards provide API consumers and administrators with pre-configured visualizations of API traffic, performance, and usage metrics. Dashboards aggregate data from HTTP requests, response times, and status codes, enabling users to monitor trends, identify issues, and analyze API consumption patterns. This feature is available to authenticated users with access to APIs or applications in the portal, and to administrators managing environment-wide analytics.

## Key Concepts

### Dashboard

A dashboard is a collection of widgets organized in a grid layout. Each dashboard belongs to a single environment and includes metadata such as name, labels, and creation date. Users can pin up to 4 dashboards for quick access. Dashboards are isolated by environment—attempting to access a dashboard from a different environment returns a 404 error.

### Widget

A widget visualizes a single analytics query. Widget types include:

* **stats**: Displays a single metric value
* **doughnut/pie/polar area**: Shows proportional breakdowns
* **time-series line/bar**: Illustrates trends over time
* **vertical/horizontal bar**: Compares values across categories

Each widget defines a request specifying:

* **Metrics**: The data source (e.g., `HTTP_REQUESTS`)
* **Measures**: Aggregation functions (`COUNT`, `SUM`, `AVG`, `MIN`, `MAX`)
* **Time range**: Start and end timestamps for the query
* **Filters**: Constraints applied to the query (see Analytics Filter)
* **Grouping dimensions**: Optional facets (`API`, `APPLICATION`, `HTTP_STATUS_CODE_GROUP`, `HTTP_STATUS`)

### Analytics Filter

Filters scope analytics queries to specific APIs, applications, or HTTP status codes. Filter types include:

| Filter Name | Type | Operators | Values/Range |
|:------------|:-----|:----------|:-------------|
| `API` | KEYWORD | `EQ`, `IN` | Dynamic (user's authorized APIs) |
| `APPLICATION` | KEYWORD | `EQ`, `IN` | Dynamic (user's applications) |
| `HTTP_STATUS_CODE_GROUP` | ENUM | `EQ`, `IN` | `1XX`, `2XX`, `3XX`, `4XX`, `5XX` |
| `HTTP_STATUS` | NUMBER | `EQ`, `LTE`, `GTE` | 100–599 |

Filters are applied at the widget level or globally across a dashboard. Users can only filter by APIs they are authorized to view and applications they own.

### Access Control

Analytics access is determined by user role and API/application visibility:

| User Role | Authorized APIs | Authorized Applications |
|:----------|:----------------|:------------------------|
| Environment Admin | All APIs in environment | None (empty map) |
| Organization Admin | All APIs in environment | None (empty map) |
| Authenticated User | APIs visible in portal navigation + subscribed APIs | User's applications |
| Anonymous User | Public APIs visible in portal navigation | None (empty map) |

The feature is gated by the `PORTAL_NEXT_ANALYTICS_ENABLED` environment parameter. When disabled, all analytics endpoints return 403.
