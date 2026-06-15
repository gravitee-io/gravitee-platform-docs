# Portal analytics API reference

The portal analytics REST endpoints let API consumers and administrators retrieve dashboard definitions and run analytics queries from the New Developer Portal. These endpoints belong to the **Portal API**, not the Management API. They are scoped to a single environment, require authentication, and require the `portal.next.analytics.enabled` environment parameter. When it's disabled, every analytics endpoint returns `403`. Results are scoped to the APIs and applications the authenticated user is allowed to see.

## Portal API

Base path: `/portal/environments/{envId}/analytics`

All paths below are relative to this base path. For enablement and UI behavior, see [Portal analytics configuration reference](../../developer-portal/new-developer-portal/portal-analytics-configuration-reference.md).

## List dashboards

**Endpoint:** `GET /analytics/dashboards`

Returns a paginated list of analytics dashboards for the specified environment.

**Query parameters:**

| Parameter | Type | Default | Description |
|:----------|:-----|:--------|:------------|
| `page` | integer | 1 | Page number for pagination |
| `size` | integer | 10 | Number of dashboards per page |

**Response schema:**

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

## Get a dashboard

**Endpoint:** `GET /analytics/dashboards/{dashboardId}`

Returns the full definition of a single dashboard, including all widget configurations. If the dashboard's environment doesn't match the request's environment, the endpoint returns `404` rather than `403`, so it doesn't disclose that the dashboard exists in another environment.

## Compute measures

**Endpoint:** `POST /analytics/measures`

Computes aggregated measures for one or more metrics over a specified time range.

**Request schema:**

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
      "measures": ["COUNT", "AVG"],
      "filters": []
    }
  ]
}
```

**Request fields:**

| Field | Type | Required | Description |
|:------|:-----|:---------|:------------|
| `timeRange` | object | Yes | Time range for the query, with `from` and `to` timestamps |
| `filters` | array | No | Top-level filters applied to every metric |
| `metrics` | array | Yes | Array of metric definitions to compute |
| `metrics[].name` | string | Yes | Metric name, for example `HTTP_REQUESTS` |
| `metrics[].measures` | array | No | Aggregation functions: `COUNT`, `AVG`, `MIN`, `MAX`, `P50`, `P90`, `P95`, `P99`, `PERCENTAGE` |
| `metrics[].filters` | array | No | Metric-specific filters |

**Response schema:**

```json
{
  "metrics": [
    {
      "name": "HTTP_REQUESTS",
      "unit": "NUMBER",
      "measures": [
        { "name": "COUNT", "value": 12345 }
      ]
    }
  ]
}
```

**Response fields:**

| Field | Type | Description |
|:------|:-----|:------------|
| `metrics` | array | Array of computed metric results |
| `metrics[].name` | string | Metric name |
| `metrics[].unit` | string | Unit of measurement: `NUMBER`, `BYTES`, `MILLISECONDS`, or `PERCENT` |
| `metrics[].measures` | array | Computed measure values |
| `metrics[].measures[].name` | string | Measure name, for example `COUNT` or `AVG` |
| `metrics[].measures[].value` | number | Computed value |

## Compute facets

**Endpoint:** `POST /analytics/facets`

Computes faceted measures grouped by one or more dimensions.

**Request schema:**

Extends the measures request with grouping parameters:

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

**Additional request fields:**

| Field | Type | Required | Description |
|:------|:-----|:---------|:------------|
| `by` | array | Yes | Grouping dimensions. Accepts any analytics facet name, for example `API`, `APPLICATION`, `HTTP_STATUS_CODE_GROUP`, or `HTTP_STATUS`. Maximum of three dimensions. |
| `limit` | integer | No | Maximum number of buckets to return |
| `ranges` | array | No | Numeric ranges to bucket values into, with `from` and `to` values, applied to the last facet |

Each metric can also carry a `sorts` array (a `measure` and an `order` of `ASC` or `DESC`) to sort the buckets of the last facet.

**Response schema:**

```json
{
  "metrics": [
    {
      "name": "HTTP_REQUESTS",
      "unit": "NUMBER",
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

**Response fields:**

| Field | Type | Description |
|:------|:-----|:------------|
| `metrics[].buckets` | array | Hierarchical bucket structure |
| `metrics[].buckets[].type` | string | Bucket type: `LEAF` (single value) or `GROUP` (nested buckets) |
| `metrics[].buckets[].key` | string | Bucket identifier |
| `metrics[].buckets[].name` | string | Human-readable bucket name |
| `metrics[].buckets[].measures` | array | Computed measures for this bucket (`LEAF` only) |
| `metrics[].buckets[].buckets` | array | Nested buckets (`GROUP` only) |

## Compute time-series

**Endpoint:** `POST /analytics/time-series`

Computes time-series data with optional faceting.

**Request schema:**

Extends the facets request with an `interval`. Time-series queries accept a maximum of two facet dimensions in `by`.

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

**Additional request fields:**

| Field | Type | Required | Description |
|:------|:-----|:---------|:------------|
| `interval` | number or string | Yes | Time interval in milliseconds, for example `60000`, or a duration shorthand, for example `30s`, `5m`, `1h`, or `1d` |

**Interval format:**

The `interval` field accepts:

* Milliseconds as a number, for example `60000`
* Duration shorthand strings that match `<number><unit>`, where the unit is `s`, `m`, `h`, or `d`, for example `30s`, `5m`, `1h`, or `1d`

{% hint style="info" %}
The ISO 8601 duration format, for example `PT5M`, isn't supported by the shorthand parser.
{% endhint %}

**Response schema:**

```json
{
  "metrics": [
    {
      "name": "HTTP_REQUESTS",
      "unit": "NUMBER",
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

**Response fields:**

| Field | Type | Description |
|:------|:-----|:------------|
| `metrics[].buckets[].key` | string | ISO 8601 timestamp for the interval |
| `metrics[].buckets[].timestamp` | number | Unix timestamp in milliseconds |
| `metrics[].buckets[].measures` | array | Computed measures for this time interval |

Time-series queries can be combined with faceting to produce multi-dimensional time-series, for example requests per API over time.

## Filters

All computation endpoints accept the following filter types.

**String filter:**

```json
{
  "name": "API",
  "operator": "EQ",
  "value": "api-id-123"
}
```

**Array filter:**

```json
{
  "name": "APPLICATION",
  "operator": "IN",
  "value": ["app-1", "app-2"]
}
```

**Number filter:**

```json
{
  "name": "HTTP_STATUS",
  "operator": "GTE",
  "value": 200
}
```

**Supported filter operators:**

The operator determines the value shape of the filter.

| Operator | Description | Value |
|:---------|:------------|:------|
| `EQ` | Equals | String |
| `IN` | In a list | Array of strings |
| `LTE` | Less than or equal | Number |
| `GTE` | Greater than or equal | Number |

{% hint style="warning" %}
No other operators are exposed. The API accepts only `EQ`, `IN`, `LTE`, and `GTE`.
{% endhint %}

**Filter dimensions:**

The portal UI exposes the following filter dimensions. The Portal API itself accepts any analytics filter name.

| Dimension | Type | Operators | Values |
|:----------|:-----|:----------|:-------|
| `API` | KEYWORD | `EQ`, `IN` | Dynamic (the user's authorized APIs) |
| `APPLICATION` | KEYWORD | `EQ`, `IN` | Dynamic (the user's applications) |
| `HTTP_STATUS_CODE_GROUP` | ENUM | `EQ`, `IN` | `1XX`, `2XX`, `3XX`, `4XX`, `5XX` |
| `HTTP_STATUS` | NUMBER | `EQ`, `LTE`, `GTE` | 100 to 599 |

{% hint style="info" %}
The `HTTP_STATUS_CODE_GROUP` values are a fixed set. Dynamic value loading isn't supported for this dimension.
{% endhint %}

### Selecting time ranges

Time ranges define the temporal scope of dashboard data. Users can select from predefined relative periods or specify a custom absolute range.

**To select a time range:**

1. Select a relative period from the dropdown (e.g., **Last 5 minutes**, **Last 1 hour**, **Last 1 day**).
2. For a custom absolute range, select **Custom** from the dropdown, then choose start and end dates from the date pickers.
3. Click **Apply** to confirm the custom range.
4. Click **Refresh** to reload dashboard data with the current time range.

**Valid relative periods:**

`1m`, `5m`, `1h`, `1d`, `1w`, `1M`

The default period is `5m`. The selected time range is encoded in the URL and persists across page reloads.

### URL encoding for filters and time ranges

Dashboard filters and time ranges are encoded in the URL as a `q` query parameter with version marker `v=1`. This allows users to share dashboard views and return to saved configurations.

**Filter condition encoding:**

Each filter condition is encoded as `{ field, operator, value }`. Multiple values for the same field are merged into array-based operators (`IN`, `NOT_IN`) when compatible.

**Time range encoding:**

Relative periods are stored as `{ type: 'relative', period: '5m' }`. Absolute ranges are stored as `{ type: 'absolute', from: <timestamp>, to: <timestamp> }`. The default period (`5m`) is omitted from the URL.

**Valid relative periods:**

`1m`, `5m`, `1h`, `1d`, `1w`, `1M`

Invalid periods are ignored during encoding and default to `5m` during decoding.

**Decoding validation rules:**

- URL decoding returns default state if the version parameter `v` is not `1`.
- Filters missing `field` or `operator` are silently discarded.
- Filter labels and value labels are never persisted in URL encoding. On decode, `label` defaults to `field` value.

## Resolve filter labels

**Endpoint:** `POST /environments/{envId}/observability/filters/resolve`

Resolves filter value identifiers (API, APPLICATION, PLAN UUIDs) into display labels for the dashboard UI.

**Request schema:**

```json
{
  "entries": [
    {
      "filterName": "API",
      "ids": ["67e246cb-ab02-4da4-8f47-f9fa3e061d6b"]
    }
  ]
}
```

**Request fields:**

| Field | Type | Required | Description |
|:------|:-----|:---------|:------------|
| `entries` | array | Yes | Array of filter entries to resolve |
| `entries[].filterName` | string | Yes | Filter name: `API`, `APPLICATION`, or `PLAN` |
| `entries[].ids` | array | Yes | Array of identifiers to resolve (maximum 100 per entry) |

**Response schema:**

```json
{
  "entries": [
    {
      "filterName": "API",
      "labels": {
        "67e246cb-ab02-4da4-8f47-f9fa3e061d6b": "Public API"
      }
    }
  ]
}
```

**Response fields:**

| Field | Type | Description |
|:------|:-----|:------------|
| `entries` | array | Array of resolved filter entries |
| `entries[].filterName` | string | Filter name |
| `entries[].labels` | object | Map of identifier to display label |

**Validation limits:**

- Maximum 10 entries per request
- Maximum 100 identifiers per entry

Requests exceeding these limits return a 400 error with message `"Too many filter entries to resolve"` or `"Too many filter ids to resolve"`.

**Permissions:**

User must have `ENVIRONMENT_DASHBOARD` read permission. Requests without this permission return a 403 error.
