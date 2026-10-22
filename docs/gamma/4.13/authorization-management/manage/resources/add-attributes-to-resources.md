---
hidden: false
noIndex: false
description: Attach custom metadata to a resource, such as sensitivity or ownership, so policy conditions can test it. Follow the steps to add attributes.
---

# Add attributes to resources

Attach custom metadata to resource entities so the policy engine can evaluate fine-grained conditions — sensitivity levels, ownership, cost tiers, or any domain-specific property.

## How attributes work with resources

Resource attributes are referenced in policy `when` conditions using the `resource.` prefix:

```
permit (
  principal == User::"alice",
  action == Action::"demo-hr-mcp.search",
  resource == MCPTool::"demo-hr-mcp.search"
)
when {
  resource.sensitivity != "restricted"
};
```

## Attribute types

The Attribute Editor offers twelve types: **String**, **Integer**, **Boolean**, **Set&lt;String&gt;**, **Decimal**, **Timestamp**, **Duration**, **IP**, **CIDR**, **Enum**, **EntityRef**, and **Set&lt;EntityRef&gt;**. For the GAPL value each type becomes and an example condition for each, see [Console attribute types in GAPL](../../gapl-reference/values-and-types.md#console-attribute-types-in-gapl).

## Adding attributes

### During creation

When creating a resource via **Add Resource**, scroll to the **Attributes** section, click **Add attribute**, and fill in the key, type, and value.

### To existing entities

1. Find the entity in the Resources table
2. Click the **⋮** menu → **Edit**
3. Scroll to the **Attributes** section
4. Add, modify, or remove attribute rows
5. Click **Save**

## Attribute persistence

| Source | Behavior on reimport/sync |
|--------|--------------------------|
| **Local** | Fully editable; persists until manually changed |
| **Gravitee Catalog** | Catalog-sourced attributes (`_displayName`, `_catalogId`, `description`) are overwritten on reimport. Custom attributes you add are preserved |
| **APIM** | APIM-sourced attributes are re-asserted. Custom attributes and target gateways are preserved |

## Common resource attributes

| Attribute | Type | Example | Use in policies |
|-----------|------|---------|-----------------|
| `sensitivity` | String | `"high"`, `"low"` | `resource.sensitivity == "high"` |
| `owner` | String | `"team-data"` | `resource.owner == principal.team` |
| `cost_tier` | String | `"premium"` | `resource.cost_tier != "premium"` |
| `max_tokens` | Integer | `50000` | `resource.max_tokens > context.usage.tokens_today` |
| `public` | Boolean | `true` | `resource.public == true` |

## Next steps

* [Build resource relationships](build-resource-relationships.md) — Establish parent-child hierarchies
* [Create, update, and delete policies](../../configure/create-update-delete-policies.md) — Reference resource attributes in conditions
