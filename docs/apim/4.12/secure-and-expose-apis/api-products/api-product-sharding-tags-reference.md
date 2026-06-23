# API Product Sharding Tags Reference

## Management API

The Management API v2 exposes sharding tags on API Product entities and supports tag assignment through create, update, and plan update operations.

### API Product Entity Schema

The `tags` field contains the list of sharding tags associated with the API Product:

```json
{
  "tags": ["string"]
}
```

### Create API Product Request Schema

```json
{
  "tags": ["string"]
}
```

### Update API Product Request Schema

```json
{
  "tags": ["string"]
}
```

### Update API Product Plan Request Schema

The `tags` field contains the list of sharding tags associated with the plan:

```json
{
  "tags": ["string"]
}
```

Plan tags must be a subset of the API Product's tags. If plan tags include values not present in the parent product's tag set, the API returns a validation error:

**Error message:** `"Plan tags mismatch the tags defined by the API Product"`

**Error details structure:**

| Field | Type | Description |
|:------|:-----|:------------|
| `planTags` | string | Comma-separated plan tag keys |
| `apiProductTags` | string | Comma-separated API Product tag keys |

### Gateway Runtime Behavior

The following table describes how the Gateway indexes API Products, plans, and APIs based on sharding tag configuration:

| Gateway Configuration | Behavior |
|:----------------------|:---------|
| No sharding tags configured | Gateway retrieves all API Products, plans, and APIs. |
| One or more sharding tags configured | Gateway only indexes entities whose tags intersect with its configured tags. Within an eligible product, only published or deprecated plans whose plan tags match the gateway are indexed. Tagless plans match any gateway that already matched the product. |

#### Member API Eligibility

A member API is shard-eligible on a gateway if either:

* Its own sharding tags match the gateway, **or**
* It has at least one published or deprecated API Product plan indexed on that gateway, where:
  * The product's tags match the gateway (tagless product matches all gateways), **and**
  * The plan's tags are empty (inherits product placement) or match the gateway (subset of product tags)

Standalone APIs (not relying on product eligibility) deploy only when their own tags match the gateway.

#### Undeployment and Resync

When an API Product is undeployed or its tags or plans change such that member APIs are no longer eligible, affected APIs are undeployed on that gateway. Product deploy and update events trigger ordered resync and re-evaluation of member APIs.

## Organization Tag Deletion

When an organization-level tag is deleted via **Organization → Entrypoints & Sharding Tags**, the system removes the tag from all API Products and their plans in all environments. This operation is idempotent and safe to retry after partial failure (e.g., product updated but plan cleanup interrupted). All tag changes on API Products and plans produce audit log entries on the affected resource.
