---
hidden: false
noIndex: false
---

# Import resources from the Catalog

Import resource entities from the AI Catalog into Authorization Management. Imported resources use the same Entity ID as in the Catalog, ensuring every policy refers to one canonical identifier.

## How catalog import works

The **Import from AI Catalog** dialog connects to the AI Catalog service and lists all published items across three categories:

| Category | Entity type | Policy type |
|----------|------------|-------------|
| **MCP Servers** | `MCPServer` | `MCP` |
| **AI Models** | `Model` | `MODEL` |
| **Agents** | `Agent` | `AGENT` |

For MCP servers, the import also fetches associated tools from the Catalog and creates them as child `MCPTool` entities with parent references back to the server. Tool imports run with a concurrency limit of 4 to avoid overloading the backend.

## Prerequisites

* The Agent Identity Module (AIM) must be installed
* At least one item published in the AI Catalog
* The `ENVIRONMENT_AUTHZ_ENTITY[CREATE]` permission

## Steps

### 1. Navigate to Resources

From the Authorization Management sidebar, select **Policy Structure → Entities**. Select the **Resources** tab.

### 2. Open the import dialog

Click the **Import** dropdown → **Import from Context Catalog**.

### 3. Browse and select

The dialog opens with three tabs: **MCP Servers**, **AI Models**, and **Agents**. Each tab shows:

- **Display name** — derived from the catalog item definition
- **Entity type badge** — the canonical type
- **Entity ID** — the bare slug used as the Authorization identifier
- **Description** — from the catalog item
- **Imported badge** — if already imported, the checkbox is disabled

Use the search field to filter by name or Entity ID. Use **Select visible** to bulk-select and **Clear** to deselect.

### 4. Import

Click **Import**. The footer shows progress: `Importing 1 / 5…`

Each imported entity receives these system attributes:

| Attribute | Value |
|-----------|-------|
| `_displayName` | Display name derived from the catalog item |
| `_catalogId` | The catalog item's unique ID |
| `_importedAt` | ISO 8601 timestamp of the import |
| `description` | From the catalog item definition (if present) |

### 5. Verify

Imported resources appear in the Resources table with source label **Gravitee Catalog**. MCP server tools appear as child entities with the source badge showing their parent relationship.

## Entity ID derivation

The Authorization Entity ID uses the Catalog's bare slug — the exact value the runtime MCP resolver registers. The derivation order is:

1. **`slug` field** — preferred (available in AIM ≥ PR #468)
2. **De-qualified `entityId`** — strips the `<kind>.` prefix from older AIM formats
3. **Name-based fallback** — slugified from the item's name, title, or query name

{% hint style="info" %}
The `entityType` field carries the kind (for example, `MCPServer`), and the `entityId` carries only the bare slug (for example, `demo-hr-mcp`). The kind is never duplicated into the Entity ID.
{% endhint %}

## Re-import behavior

Reimporting an item that already exists performs an upsert:
- Catalog-sourced attributes (`_displayName`, `_catalogId`, `description`) are overwritten
- Custom attributes you added are preserved
- Target gateways you set are preserved

## Alternative import methods

| Method | When to use |
|--------|-------------|
| **Import from file** | Upload a JSON file of entities (available via **Import → Import from file…**) |
| **Create a local resource** | Manually define resources not in the Catalog |
| **APIM sync** | Resources sourced from API Management appear with the `APIM` source label |

## Next steps

* [Create a local resource](create-a-local-resource.md) — Define custom resources
* [Add attributes to resources](add-attributes-to-resources.md) — Attach custom metadata
* [Build resource relationships](build-resource-relationships.md) — Set up parent-child hierarchies
