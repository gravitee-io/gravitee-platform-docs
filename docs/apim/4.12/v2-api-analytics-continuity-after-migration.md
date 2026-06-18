# Maintain analytics continuity after migrating v2 APIs to v4

## Overview

When you migrate an HTTP proxy API from v2 to v4, historical analytics data is no longer lost. After migration, the API's pre-migration (v2) and post-migration (v4) data appear together, so you keep visibility into traffic from before the migration.

Analytics continuity currently applies to the per-API analytics dashboard and the API's connection logs. It doesn't extend to environment-level analytics.

## Update existing indices

The gateway updates the Elasticsearch or OpenSearch index template automatically on startup, but index templates only apply to newly created indices. If your installation was running before this release, your existing `gravitee-request-*` indices don't include the field aliases that let v4 analytics queries match v2 documents. Until you add those aliases, the per-API analytics dashboard and connection logs show incomplete data for migrated APIs.

Run the following one-time mapping update against your Elasticsearch or OpenSearch cluster to add the aliases to all existing `gravitee-request-*` indices. You can run it from Kibana Dev Tools, `curl`, or any HTTP client:

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
If your indices use a custom prefix (configured with `reporters.elasticsearch.index` in `gravitee.yml`), replace `gravitee-request-*` with `<your-prefix>-request-*`.
{% endhint %}

A successful response returns:

```json
{
  "acknowledged": true
}
```

The operation is idempotent. If an alias already exists on an index, the call succeeds without error.

## Verification

To confirm the aliases are in place, inspect the mapping of any request index:

```json
GET /gravitee-request-*/_mapping
```

Each index lists the nine alias fields alongside the original v2 fields. For example:

```json
"api-id": {
  "type": "alias",
  "path": "api"
}
```

## Limitations

Analytics continuity doesn't extend to environment-level analytics. Environment-level dashboards don't include a migrated API's pre-migration v2 data.
