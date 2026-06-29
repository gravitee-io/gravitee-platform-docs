---
hidden: false
noIndex: true
---

# Build resource relationships

Establish parent-child hierarchies between resource entities. Relationships enable the `in` operator in GAPL: `resource in MCPServer::"weather"` matches the server and all its child tools.

## Relationship patterns

The resource hierarchy mirrors the Gamma service architecture:

| Parent type | Child type | Example |
|------------|-----------|---------|
| **MCPServer** | MCPTool | Tools on a server (`resource in MCPServer::"weather"` matches all tools) |
| **MCPServer** | MCPPrompt | Prompts exposed by a server |
| **MCPServer** | MCPResource | Resources exposed by a server |
| **API** | Endpoint | Endpoints on an API proxy |
| **API** | DataField | Data fields on an API response |
| **Agent** | AgentSkill | Skills an agent can perform |
| **Agent** | AgentTool | Tools an agent can invoke |
| **Agent** | AgentKnowledge | Knowledge bases an agent accesses |

{% hint style="info" %}
When you import an MCP server from the Catalog, its tools are automatically created as child entities with the server as their parent. You do not need to set these relationships manually.
{% endhint %}

## Setting parents

### During creation

In the **Add Resource** dialog, use the **Parents** combobox to search and select existing entities. The picker shows entities of the same kind (`RESOURCE`).

### On existing entities

1. On the Entities page, click the **⋮** menu on a resource row → **Edit**
2. Modify the **Parents** combobox
3. Click **Save**

## Viewing relationships

The Entities table **Relationships** column displays:

| Badge | Meaning |
|-------|---------|
| `in 1` | Child of 1 parent |
| `contains 3 MCPTool` | Parent of 3 MCPTool entities |
| `contains 2 Endpoint` | Parent of 2 Endpoint entities |

Click an entity name to open the **Entity Detail** panel, which includes a **Relationships** tab showing all parents and children grouped by type.

## Relationship semantics in policies

| GAPL syntax | What it matches |
|------------|----------------|
| `resource == MCPTool::"weather.get-forecast"` | Only this specific tool |
| `resource in MCPServer::"weather"` | The server and all its child entities (tools, prompts, resources) |
| `resource in API::"orders-service"` | The API and all its child endpoints and data fields |

## Entity categories

Resources are classified into categories for the schema outline and UI color coding:

| Category | Entity types | Color |
|----------|-------------|-------|
| **MCP** | MCPServer, MCPTool, MCPPrompt, MCPResource | chart-2 |
| **APIs** | API, Endpoint, DataField | chart-8 |
| **Agents** | Agent, AgentSkill, AgentTool, AgentMemory, AgentKnowledge | chart-7 |
| **AI Models** | Model | chart-5 |
| **Events** | EventStream, Topic, SchemaField | chart-10 |
| **Resources** | Resource (generic) | chart-3 |
| **Custom** | Application, Asset, and user-defined types | muted |

## Next steps

* [Schema generation](../schemas/schema-generation.md) — See how relationships are reflected in the schema
* [Create, update, and delete policies](../../configure/create-update-delete-policies.md) — Write policies using containment
