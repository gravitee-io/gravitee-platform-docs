# V2 API Analytics Continuity After Migration

## Overview

Starting with this release, migrating an HTTP Proxy API (v2) to v4 no longer causes a loss of historical analytics data. The v4 analytics dashboard now queries both v4 and v2 analytics indices, allowing administrators to view complete analytics history for migrated APIs. This capability is enabled through Elasticsearch field aliases that map v4 field names to their v2 equivalents.

## Key Concepts

### Analytics Query Unification

The v4 analytics dashboard executes queries against both `gravitee-v4-metrics-*` (v4 data) and `gravitee-request-*` (v2 data) indices. Queries use v4 canonical field names (e.g., `api-id`, `gateway-response-time-ms`), which Elasticsearch resolves to v2 field names (e.g., `api`, `response-time`) via field aliases. This allows a single query to retrieve analytics data from both API definition versions without requiring separate query logic.

### Field Alias Mapping

Field aliases are Elasticsearch mapping constructs that create alternate names for existing fields. The following aliases map v4 field names to their v2 equivalents in the `gravitee-request` index:

| V4 Field Name | V2 Field Name |
|:--------------|:--------------|
| `api-id` | `api` |
| `application-id` | `application` |
| `plan-id` | `plan` |
| `gateway-response-time-ms` | `response-time` |
| `http-method` | `method` |
| `transaction-id` | `transaction` |
| `subscription-id` | `subscription` |
| `gateway-latency-ms` | `proxy-latency` |
| `endpoint-response-time-ms` | `api-response-time` |

### Supported API Types

Analytics queries are supported for APIs with definition version V2 or V4. Federated APIs and TCP proxy APIs are not supported and will result in query errors.

## Prerequisites

Before creating field aliases for existing indices, ensure the following:

* Elasticsearch 7.x, 8.x, 9.x, or OpenSearch cluster
* Existing `gravitee-request-*` indices containing v2 analytics data
* Access to execute mapping update requests against the Elasticsearch or OpenSearch cluster (via Kibana Dev Tools, `curl`, or any HTTP client)

## Creating Field Aliases for Existing Indices

Index templates only apply to newly created indices. If your Gravitee installation has been running prior to this release, existing `gravitee-request-*` indices do not include the field aliases required for v4 analytics queries to match v2 documents. The APIM gateway updates the template automatically on startup, but does not retroactively modify existing indices. Without the aliases on existing indices, queries from the v4 analytics dashboard will fail to match v2 documents, resulting in incomplete or missing analytics for migrated APIs.

Execute the following request against your Elasticsearch or OpenSearch cluster to add the aliases to all existing `gravitee-request-*` indices. You can execute this via Kibana Dev Tools, `curl`, or any HTTP client:

```json
PUT /gravitee-request-*/_mapping
{
  "properties": {
    "api-id": {
      "type": "alias",
      "path": "api"
    },
    "application-id": {
      "type": "alias",
      "path": "application"
    },
    "plan-id": {
      "type": "alias",
      "path": "plan"
    },
    "gateway-response-time-ms": {
      "type": "alias",
      "path": "response-time"
    },
    "http-method": {
      "type": "alias",
      "path": "method"
    },
    "transaction-id": {
      "type": "alias",
      "path": "transaction"
    },
    "subscription-id": {
      "type": "alias",
      "path": "subscription"
    },
    "gateway-latency-ms": {
      "type": "alias",
      "path": "proxy-latency"
    },
    "endpoint-response-time-ms": {
      "type": "alias",
      "path": "api-response-time"
    }
  }
}
```

Example using `curl`:

```bash
curl -X PUT "https://<your-es-host>:9200/gravitee-request-*/_mapping" \
  -H "Content-Type: application/json" \
  -d '{
  "properties": {
    "api-id": { "type": "alias", "path": "api" },
    "application-id": { "type": "alias", "path": "application" },
    "plan-id": { "type": "alias", "path": "plan" },
    "gateway-response-time-ms": { "type": "alias", "path": "response-time" },
    "http-method": { "type": "alias", "path": "method" },
    "transaction-id": { "type": "alias", "path": "transaction" },
    "subscription-id": { "type": "alias", "path": "subscription" },
    "gateway-latency-ms": { "type": "alias", "path": "proxy-latency" },
    "endpoint-response-time-ms": { "type": "alias", "path": "api-response-time" }
  }
}'
```

{% hint style="info" %}
If your indices use a custom prefix (configured via `reporters.elasticsearch.index` in `gravitee.yml`), replace `gravitee-request-*` with `<your-prefix>-request-*`.
{% endhint %}

A successful response returns:

```json
{
  "acknowledged": true
}
```

The operation is idempotent. If an alias already exists on an index (from a previous run or because the index was created after the template update), the call succeeds without error.

### Verification

Confirm the aliases are in place by inspecting the mapping of any `request` index:

```json
GET /gravitee-request-*/_mapping
```

Each index should list the nine alias fields alongside the original v2 fields. For example:

```json
"api-id": {
  "type": "alias",
  "path": "api"
}
```

## Migrating V2 APIs to V4

The v2 to v4 API migration dialog no longer displays a warning banner stating "Analytics history will not be preserved" or requires confirmation that analytics history will be lost. The **Start Migration** button is enabled immediately when the migration dialog opens. After migration completes, the v4 analytics dashboard displays both pre-migration (v2) and post-migration (v4) analytics data.

### Known Limitations

* **Entrypoint-id field absence in V2 indices**: The `entrypoint-id` field exists only in v4 metrics indices. Queries using an `exists` filter on `entrypoint-id` will not match v2 documents. Terms aggregations on `entrypoint-id` will exclude v2 data.
* **TCP proxy APIs**: Analytics queries for TCP proxy APIs (regardless of definition version) are not supported.
* **Federated APIs**: Analytics queries for federated APIs are not supported (only V2 and V4 definition versions are supported).
