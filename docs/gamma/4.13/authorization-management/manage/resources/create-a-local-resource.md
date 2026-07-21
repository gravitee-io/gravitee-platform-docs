---
hidden: false
noIndex: false
---

# Create a local resource

Create a resource entity directly in Authorization Management for items not available in the AI Catalog — internal applications, data assets, custom tools, or any domain-specific resource.

## Resource type presets

The **Add Resource** dialog provides these presets:

| Type | Canonical prefix | Policy type | Use case |
|------|-----------------|-------------|----------|
| **MCP Server** | `mcp` | `MCP` | MCP servers not in the Catalog |
| **AI Model** | `model` | `MODEL` | Models from providers not in the Catalog |
| **Agent** | `agent` | `AGENT` | A2A agents not in the Catalog |
| **API** | `api` | `API` | API proxies |
| **Event** | `event` | `EVENT` | Event streams and topics |
| **Generic Resource** | `resource` | — | Any resource without a dedicated category |
| **Other (custom prefix)** | User-defined | `CUSTOM` | Domain-specific resources |

{% hint style="info" %}
If your environment has a published schema, the type dropdown shows the schema-defined resource types instead of the presets. The schema's `appliesTo.resourceTypes` declarations determine which types appear.
{% endhint %}

## Steps

### 1. Navigate to Resources

From the Authorization Management sidebar, select **Policy Structure → Entities**. Select the **Resources** tab.

### 2. Add a resource

Click **Add Resource**. A slide-out panel opens.

### 3. Select a type

Choose from the **Type** dropdown. The canonical prefix determines the `<kind>` portion of the Entity ID and maps the entity to the correct policy category page.

### 4. Enter details

| Field | Required | Notes |
|-------|----------|-------|
| **Display name** | Yes | Human-readable name for the table and policy chip pickers |
| **Slug** | Yes | Auto-derived from display name. Must match `[a-z0-9_-]+` |
| **Description** | No | Stored as an attribute |

**Entity ID preview**: `<prefix>.<slug>` (for example, `api.orders-service`)

### 5. Set parents (optional)

Use the **Parents** combobox to establish containment. For example:
- An `MCPTool` is a child of an `MCPServer`
- A `DataField` is a child of an `API`
- A custom resource can be nested under another custom resource

### 6. Set target gateways (optional)

Scope this resource to specific PDP gateways using the **Target gateways** combobox.

### 7. Add attributes (optional)

Click **Add attribute** to define custom key-value pairs used in policy conditions (for example, `resource.sensitivity == "high"`).

### 8. Create

Click **Create Resource**. The entity appears in the Resources table with source label **Local**.

## Custom prefix rules

When selecting **Other (custom prefix)**:

| Rule | Detail |
|------|--------|
| Must start with a letter | `webhook` ✓, `3proxy` ✗ |
| Lowercase letters, digits, and dashes only | `data-lake` ✓, `Data_Lake` ✗ |
| Must not match a preset canonical name | The console warns: "mcp" is a preset type — pick it from the dropdown instead |

The custom prefix becomes the `entityType` in PascalCase (for example, prefix `webhook` → type `Webhook`).

## Next steps

* [Add attributes to resources](add-attributes-to-resources.md) — Attach metadata for condition-based policies
* [Build resource relationships](build-resource-relationships.md) — Create containment hierarchies
