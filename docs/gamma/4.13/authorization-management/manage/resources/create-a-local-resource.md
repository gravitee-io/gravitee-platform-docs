---
hidden: false
noIndex: false
description: Create a resource entity for the internal applications, data assets, and custom tools the AI Catalog does not hold. Follow the steps to add one.
---

# Create a local resource

Create a resource entity directly in Authorization Management for items not available in the AI Catalog — internal applications, data assets, custom tools, or any domain-specific resource.

## Resource type presets

The **Add Resource** dialog provides these presets:

| Type | Engine type | Policy type | Use case |
|------|-------------|-------------|----------|
| **MCP Server** | `MCPServer` | `MCP` | MCP servers not in the Catalog |
| **AI Model** | `Model` | `MODEL` | Models from providers not in the Catalog |
| **Agent** | `Agent` | `AGENT` | A2A agents not in the Catalog |
| **API** | `API` | `API` | API proxies |
| **Event** | `Event` | `EVENT` | Event streams and topics |
| **Generic Resource** | `Resource` | — | Any resource without a dedicated category |
| **Other (custom type)** | As entered | `CUSTOM` | Domain-specific resources |

{% hint style="info" %}
If your environment has a published schema, the type dropdown shows the schema-defined resource types instead of the presets. The schema's `appliesTo.resourceTypes` declarations determine which types appear.
{% endhint %}

## Steps

### 1. Navigate to Resources

From the Authorization Management sidebar, select **Policy Structure → Entities**. Select the **Resources** tab.

### 2. Add a resource

Click **Add Resource**. A slide-out panel opens.

### 3. Select a type

Choose from the **Type** dropdown. The type maps the entity to the correct policy category page.

### 4. Enter details

| Field | Required | Notes |
|-------|----------|-------|
| **Display name** | Yes | Human-readable name for the table and policy chip pickers |
| **Entity ID** | Yes | Fills in from the display name (accents removed, lowercase, other characters replaced with dashes). Change it to the ID that requests carry for this resource |
| **Description** | No | Stored as an attribute |

The Entity ID carries no type prefix: the type is stored separately. The hint under the field shows how the policy engine sees the resource, for example `API::"orders-service"`. An Entity ID holds at most 255 characters, isn't `.` or `..`, and holds no whitespace, control or formatting character, double quote, backslash, `/`, `%`, `;`, `?`, or `#`.

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

## Custom types

When you select **Other (custom type)**, a **Custom type** field appears. The policy engine uses the value as the type exactly as you enter it, for example `Webhook` or `HR::Team`. If you enter a type that the dropdown already offers, the console warns you to select it from the dropdown instead, for example: "mcp" is a preset type — pick it from the dropdown instead.

## Next steps

* [Add attributes to resources](add-attributes-to-resources.md) — Attach metadata for condition-based policies
* [Build resource relationships](build-resource-relationships.md) — Create containment hierarchies
