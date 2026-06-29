---
hidden: false
noIndex: true
---

# Schema generation

The schema is the contract your policies are written against — it declares the entity types, their relationships, and the actions the policy engine can reason about.

## What the schema defines

The schema is a GAPL document (`schema.gapl`) that declares:

1. **Entity types** — The kinds of principals and resources in your authorization world (for example, `User`, `MCPServer`, `MCPTool`)
2. **Attributes** — Typed properties on each entity type (for example, `department: String`)
3. **Relationships** — Parent-child hierarchies via `memberOfTypes` (for example, `MCPTool` is a member of `MCPServer`)
4. **Actions** — The verbs policies can grant or forbid, with `appliesTo` declarations that specify which principal types and resource types each action governs

## The Schema page

From the Authorization Management sidebar, select **Policy Structure → Schema**. The Schema page has two views:

### Code tab (`schema.gapl`)

Shows the raw GAPL schema text in a Monaco editor. In read-only mode, you can inspect the full schema definition. Click **Edit** to modify.

### Entities tab

Shows a visual breakdown of all entity types defined in the schema, organized by category:

| Category | Icon | Entity types |
|----------|------|-------------|
| **Principals** | Users | User, Group, ServiceAccount, AgentIdentity |
| **MCP** | Server | MCPServer, MCPTool, MCPPrompt, MCPResource |
| **APIs** | Globe | API, Endpoint, DataField |
| **Agents** | Bot | Agent, AgentSkill, AgentTool, AgentMemory, AgentKnowledge |
| **AI Models** | Brain | Model |
| **Events** | Radio | EventStream, Topic, SchemaField |
| **Resources** | Shield | Resource (generic) |
| **Custom** | Boxes | Application, Asset, and user-defined types |

Each entity card shows:
- The entity type name
- Parent membership badges (for example, `in [MCPServer]`)
- Attribute badges with name and type (for example, `department: String`)

## KPI tiles

The Schema page displays four summary tiles:

| Tile | Description |
|------|-------------|
| **Entities** | Total number of entity types defined in the schema |
| **Actions** | Total number of actions defined |
| **Principal kinds** | Number of entity types classified as principals |
| **Resource kinds** | Number of entity types classified as resources |

## Outline panel

A sidebar outline groups entity types by category. Click any entity name to jump to its card in the Entities tab. Categories can be collapsed or expanded.

## Schema and entity creation

When a schema is published, it affects entity creation:

- The **Type** dropdown in the Add Principal and Add Resource dialogs shows schema-defined types instead of the default presets
- The schema's `appliesTo.principalTypes` and `appliesTo.resourceTypes` declarations determine which types appear in each dialog

{% hint style="info" %}
If no schema is defined, the console shows an empty state: "No schema defined yet. Once a `schema.gapl` is published for this environment, its entity types and actions will appear here."
{% endhint %}

## Creating a schema

1. On the Schema page, click **Create schema**
2. Write your GAPL schema in the Monaco editor
3. The editor validates the schema in real time using the backend's validation endpoint
4. Click **Save** to publish

## Next steps

* [Edit your schema](edit-your-schema.md) — Modify an existing schema
* [Validate schema changes](validate-schema-changes.md) — Understand the validation pipeline
