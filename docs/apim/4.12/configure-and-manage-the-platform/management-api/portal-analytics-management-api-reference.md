# Portal Analytics Management API Reference

## Management API

The Portal Analytics Management API provides REST endpoints for programmatically accessing and querying analytics dashboards. All endpoints require the `PORTAL_NEXT_ANALYTICS_ENABLED` environment parameter to be enabled. When this parameter is disabled, all analytics endpoints return 403.

### List dashboards

**Endpoint:** `GET /portal/environments/{envId}/analytics/dashboards`

Returns a paginated list of analytics dashboards for the specified environment.

**Query Parameters:**

| Parameter | Type | Default | Description |
|:----------|:-----|:--------|:------------|
| `page` | integer | 1 | Page number for pagination |
| `size` | integer | 20 | Number of dashboards per page |

**Response Schema:**

```json
{
  "data": [
    {
      "id": "string",
      "name": "string",
      "createdBy": "string",
      "createdAt": "2025-10-07T06:50:30Z",
      "lastModified": "2025-12-07T11:35:30Z",
      "labels": { "key": "value" },
      "widgets": []
    }
  ],
  "metadata": {
    "pagination": {
      "current_page": 1,
      "total_pages": 5,
      "total": 100
    }
  },
  "links": { "self": "..." }
}
```

### Compute Measures

**Endpoint:** `POST /portal/environments/{envId}/analytics/computation/measures`

Computes aggregated measures for one or more metrics over a specified time range.

**Request Schema:**

```json
{
  "timeRange": {
    "from": "2025-10-07T06:50:30Z",
    "to": "2025-12-07T11:35:30Z"
  },
  "filters": [],
  "metrics": [
    {
      "name": "HTTP_REQUESTS",
      "measures": ["COUNT", "SUM", "AVG", "MIN", "MAX"],
      "filters": []
    }
  ]
}
```

**Request Fields:**

| Field | Type | Required | Description |
|:------|:-----|:---------|:------------|
| `timeRange` | object | Yes | Time range for the query with `from` and `to` timestamps |
| `filters` | array | No | Global filters applied to all metrics |
| `metrics` | array | Yes | Array of metric definitions to compute |
| `metrics[].name` | string | Yes | Metric name (e.g., `HTTP_REQUESTS`) |
| `metrics[].measures` | array | Yes | Aggregation functions: `COUNT`, `SUM`, `AVG`, `MIN`, `MAX` |
| `metrics[].filters` | array | No | Metric-specific filters |

**Response Schema:**

```json
{
  "metrics": [
    {
      "name": "HTTP_REQUESTS",
      "unit": "COUNT",
      "measures": [
        { "name": "COUNT", "value": 12345 }
      ]
    }
  ]
}
```

**Response Fields:**

| Field | Type | Description |
|:------|:-----|:------------|
| `metrics` | array | Array of computed metric results |
| `metrics[].name` | string | Metric name |
| `metrics[].unit` | string | Unit of measurement: `COUNT`, `BYTES`, or `MILLISECONDS` |
| `metrics[].measures` | array | Computed measure values |
| `metrics[].measures[].name` | string | Measure name (e.g., `COUNT`, `AVG`) |
| `metrics[].measures[].value` | number | Computed value |

### Compute Facets

**Endpoint:** `POST /portal/environments/{envId}/analytics/computation/facets`

Computes faceted measures grouped by one or more dimensions.

**Request Schema:**

Extends the measures request with additional grouping parameters:

```json
{
  "timeRange": {
    "from": "2025-10-07T06:50:30Z",
    "to": "2025-12-07T11:35:30Z"
  },
  "filters": [],
  "metrics": [
    {
      "name": "HTTP_REQUESTS",
      "measures": ["COUNT"],
      "filters": []
    }
  ],
  "by": ["API", "APPLICATION"],
  "limit": 10,
  "ranges": [
    { "from": 100, "to": 199 },
    { "from": 200, "to": 299 }
  ]
}
```

**Additional Request Fields:**

| Field | Type | Required | Description |
|:------|:-----|:---------|:------------|
| `by` | array | Yes | Grouping dimensions: `API`, `APPLICATION`, `HTTP_STATUS_CODE_GROUP`, `HTTP_STATUS` |
| `limit` | integer | No | Maximum number of buckets per dimension |
| `ranges` | array | No | Numeric grouping ranges with `from` and `to` values |

**Response Schema:**

```json
{
  "metrics": [
    {
      "name": "HTTP_REQUESTS",
      "unit": "COUNT",
      "buckets": [
        {
          "type": "LEAF",
          "key": "api-1",
          "name": "My API",
          "measures": [ { "name": "COUNT", "value": 500 } ]
        },
        {
          "type": "GROUP",
          "key": "api-2",
          "name": "Other API",
          "buckets": []
        }
      ]
    }
  ]
}
```

**Response Fields:**

| Field | Type | Description |
|:------|:-----|:------------|
| `metrics[].buckets` | array | Hierarchical bucket structure |
| `metrics[].buckets[].type` | string | Bucket type: `LEAF` (single value) or `GROUP` (nested buckets) |
| `metrics[].buckets[].key` | string | Bucket identifier |
| `metrics[].buckets[].name` | string | Human-readable bucket name |
| `metrics[].buckets[].measures` | array | Computed measures for this bucket |
| `metrics[].buckets[].buckets` | array | Nested buckets (for `GROUP` type only) |

### Compute Time-Series

**Endpoint:** `POST /portal/environments/{envId}/analytics/computation/time-series`

Computes time-series data with optional faceting.

**Request Schema:**

Extends the facets request with an interval parameter:

```json
{
  "timeRange": {
    "from": "2025-10-07T06:50:30Z",
    "to": "2025-12-07T11:35:30Z"
  },
  "filters": [],
  "metrics": [
    {
      "name": "HTTP_REQUESTS",
      "measures": ["COUNT"],
      "filters": []
    }
  ],
  "interval": 60000,
  "by": ["API"],
  "limit": 10
}
```

**Additional Request Fields:**

| Field | Type | Required | Description |
|:------|:-----|:---------|:------------|
| `interval` | number or string | Yes | Time interval in milliseconds (e.g., `60000`) or duration shorthand (e.g., `5m`, `1h`, `1d`) |

**Interval Format:**

The `interval` field accepts:
- Milliseconds as a number (e.g., `60000`)
- Duration shorthand strings: `5m`, `1h`, `1d`

{% hint style="info" %}
ISO 8601 duration format (e.g., `PT5M`) is not directly supported by the shorthand parser.
{% endhint %}

**Response Schema:**

```json
{
  "metrics": [
    {
      "name": "HTTP_REQUESTS",
      "unit": "COUNT",
      "buckets": [
        {
          "type": "LEAF",
          "key": "2025-10-07T06:50:00Z",
          "timestamp": 1728285000000,
          "measures": [ { "name": "COUNT", "value": 42 } ]
        }
      ]
    }
  ]
}
```

**Response Fields:**

| Field | Type | Description |
|:------|:-----|:------------|
| `metrics[].buckets[].key` | string | ISO 8601 timestamp for the interval |
| `metrics[].buckets[].timestamp` | number | Unix timestamp in milliseconds |
| `metrics[].buckets[].measures` | array | Computed measures for this time interval |

Time-series can be combined with faceting to produce multi-dimensional time-series (e.g., requests per API over time).

**Filter Schema:**

All computation endpoints support the following filter types:

**String Filter:**

```json
{
  "name": "API",
  "operator": "EQ",
  "value": "api-id-123"
}
```

**Array Filter:**

```json
{
  "name": "APPLICATION",
  "operator": "IN",
  "value": ["app-1", "app-2"]
}
```

**Number Filter:**

```json
{
  "name": "HTTP_STATUS",
  "operator": "GTE",
  "value": 200
}
```

**Supported Filter Operators:**

| Operator | Description | Applicable Types |
|:---------|:------------|:-----------------|
| `EQ` | Equals | String, Number |
| `IN` | In array | String, Array |
| `LTE` | Less than or equal | Number |
| `GTE` | Greater than or equal | Number |

{% hint style="warning" %}
Other operators (e.g., `NEQ`, `NOT_IN`) are not exposed in the API.
{% endhint %}

**Filter Dimensions:**

| Dimension | Type | Operators | Values |
|:----------|:-----|:----------|:-------|
| `API` | KEYWORD | `EQ`, `IN` | Dynamic (user's authorized APIs) |
| `APPLICATION` | KEYWORD | `EQ`, `IN` | Dynamic (user's applications) |
| `HTTP_STATUS_CODE_GROUP` | ENUM | `EQ`, `IN` | `1XX`, `2XX`, `3XX`, `4XX`, `5XX` |
| `HTTP_STATUS` | NUMBER | `EQ`, `LTE`, `GTE` | 100–599 |

{% hint style="info" %}
ENUM filter values for `HTTP_STATUS_CODE_GROUP` are hardcoded. Dynamic value loading is not supported.
{% endhint %}
