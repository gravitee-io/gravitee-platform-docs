# Configuring API Product Analytics: Gateway and Elasticsearch Setup

## Prerequisites

Before configuring API Product analytics, ensure the following requirements are met:

* Gravitee API Management 4.12 or later
* v4 APIs (API Product filtering is not supported for v2 APIs)
* Elasticsearch index templates updated to include the `api-product-id` keyword field (see Gateway Configuration)

## Gateway Configuration

### Elasticsearch Index Templates

Administrators must update Elasticsearch index templates for `gravitee-v4.log.*` and `gravitee-v4.metric.*` indices to include the `api-product-id` field. The reporter applies these templates automatically on startup, but existing indices require manual rollover or reindexing.

The following table describes the `api-product-id` field:

| Property | Type | Description |
|:---------|:-----|:------------|
| `api-product-id` | keyword | Stores the API Product ID associated with the log or metric entry |

**Template Update (Elasticsearch 7.x, 8.x, 9.x, OpenSearch):**

```json
{
  "mappings": {
    "properties": {
      "api-id": { "type": "keyword" },
      "api-name": { "type": "keyword" },
      "api-product-id": { "type": "keyword" }
    }
  }
}
```


### Reporter Configuration

No configuration changes are required. The `gravitee-reporter-api` dependency (version 2.2.0) automatically includes `apiProductId` in log and metrics payloads when the field is populated by the gateway. Custom reporter implementations must be recompiled against `gravitee-reporter-api` version 2.2.0 to support the `apiProductId` field.
