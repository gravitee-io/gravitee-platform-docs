---
hidden: false
noIndex: false
---

# Import your first resource from the AI Catalog

This guide walks you through importing a resource from the AI Catalog into Authorization Management. Imported resources use the same Entity ID as in the Catalog, so every policy refers to one canonical identifier.

## Prerequisites

* At least one item published in the AI Catalog (an MCP server, AI model, or agent)
* The Agent Identity Module (AIM) must be installed. If it is not available, the **Import from Context Catalog** option is disabled with the hint: "The Agent Identity module must be installed to import from the AI Catalog."
* The `ENVIRONMENT_AUTHZ_ENTITY[CREATE]` permission

## Steps

### 1. Open the Entities page

From the Authorization Management sidebar, select **Policy Structure → Entities**. Select the **Resources** tab.

### 2. Open the import dialog

Click the **Import** dropdown and select **Import from Context Catalog**. A slide-out panel titled **Import from AI Catalog** opens.

### 3. Browse catalog entries

The dialog presents three tabs:

| Tab | What it lists | Entity type |
|-----|--------------|-------------|
| **MCP Servers** | MCP servers from the Catalog | `MCPServer` |
| **AI Models** | AI models and providers | `Model` |
| **Agents** | A2A agents | `Agent` |

Each entry shows:
- **Display name** — derived from the catalog item's title, name, or query name
- **Entity type badge** — the canonical type (for example, `MCPServer`)
- **Entity ID** — the bare slug that becomes the Authorization entity identifier
- **Description** — from the catalog item definition
- **Imported badge** — shown if the item has already been imported

### 4. Select items to import

Check the checkbox next to each entry you want to import. Use **Select visible** to select all currently displayed items, or **Clear** to deselect all.

{% hint style="info" %}
Items that have already been imported are shown with a disabled checkbox and an "Imported" badge. You cannot reimport them from this dialog.
{% endhint %}

### 5. Import

Click **Import**. The dialog shows a progress indicator (`Importing 1 / 3…`). For MCP servers, the import also fetches and creates all associated tools as child entities with parent references back to the server.

When the import completes:
- A toast confirms the number of imported entities
- Each imported entity appears in the Resources table with the source label **Gravitee Catalog**
- Catalog-sourced attributes are re-asserted on the next import, while target gateways you set are preserved

## Entity ID mapping

The Authorization entity ID is the Catalog's bare slug — the exact value the runtime MCP resolver registers. For example:

| Catalog item | Kind | Authorization Entity ID |
|-------------|------|------------------------|
| Demo HR Server | `mcp-server` | `demo-hr-mcp` |
| Search tool on Demo HR | `mcp-tool` | `demo-hr-mcp.search` |
| GPT-4o model | `model` | `gpt-4o` |
| Research Agent | `agent` | `research-agent` |

The kind lives in the `entityType` field — it is never duplicated into the Entity ID.

## Alternative import methods

In addition to the Catalog import, you can:

- **Import from file** — Upload a JSON file of entities via the **Import → Import from file…** option
- **Create a local resource** — Manually define a resource via the **Add Resource** button

## Next steps

* [Create a local resource](../manage/resources/create-a-local-resource.md) — Define custom resources not in the Catalog
* [Build resource relationships](../manage/resources/build-resource-relationships.md) — Set up parent-child hierarchies
* [Create your first policy](create-your-first-policy.md) — Write a policy targeting your imported resource
