---
hidden: false
noIndex: true
---

# Create a local principal

Create a principal entity directly in Authorization Management when the identity is not synced from Access Management or imported from an external source.

## When to use local principals

Use local principals for:
- Test users during policy development
- Service accounts for machine-to-machine access
- Agent identities for AI agents acting on behalf of users
- Groups that organize principals for shared access patterns

## Steps

### 1. Open the Entities page

From the Authorization Management sidebar, select **Policy Structure → Entities**. Select the **Principals** tab.

### 2. Add a principal

Click **Add Principal**. A slide-out panel opens.

### 3. Select a type

Choose from the **Type** dropdown:

| Type | Canonical prefix | Description |
|------|-----------------|-------------|
| **User** | `user` | Individual human identity |
| **Group** | `group` | Collection of users sharing access |
| **Service Account** | `serviceaccount` | Machine or application identity |
| **Agent Identity** | `agent-identity` | AI agent identity (mapped to `AGENT` policy type) |
| **Other (custom prefix)** | User-defined | Custom principal type for your domain |

{% hint style="info" %}
If your environment has a published schema, the type dropdown shows the schema-defined principal types instead of the presets. The schema's `appliesTo.principalTypes` declarations determine which types appear.
{% endhint %}

### 4. Enter identity details

| Field | Required | Notes |
|-------|----------|-------|
| **Display name** | Yes | Human-readable name shown in the table and policy editor chip pickers |
| **Slug** | Yes | Auto-derived from the display name (NFD normalization → lowercase → dashes). Must match `[a-z0-9_-]+` |
| **Description** | No | Stored as an attribute; visible in the entity detail view |

The **Entity ID** preview shows: `<prefix>.<slug>` (for example, `user.alice`). The maximum Entity ID length is 255 characters.

### 5. Set parents (optional)

Use the **Parents** combobox to link this principal to existing entities of the same kind. For example:
- Add a `User` to a `Group`
- Add a `Group` to another `Group` for nested membership

Parent references are used in `in` clauses in GAPL policies. When a policy says `principal in Group::"engineering"`, it matches all users whose parents include that group.

### 6. Set target gateways (optional)

Use the **Target gateways** combobox to scope this principal to specific PDP gateways. Options are populated from registered PDP gateways. Select `*` to target all gateways, or leave empty for universal availability.

### 7. Add attributes (optional)

Click **Add attribute** to define custom key-value pairs. Each attribute has:

| Field | Description |
|-------|-------------|
| **Key** | Attribute name (must not conflict with reserved keys like `_displayName`) |
| **Type** | `String`, `Number`, `Boolean`, or `Set` |
| **Value** | The attribute value. For Set type, enter comma-separated values |

Attributes are referenced in policy conditions. For example, `principal.department == "engineering"`.

### 8. Create

Click **Create Principal**. The entity appears in the Principals table with source label **Local**.

## Editing and deleting

- **Edit**: Click the **⋮** menu on any entity row → **Edit**. All entities are editable, including synced and imported ones. For synced principals, source-managed attributes are re-asserted on the next sync.
- **Remove**: Click the **⋮** menu → **Remove**. A confirmation dialog shows the Entity ID and warns about the impact.

## Next steps

* [Add attributes to principals](add-attributes-to-principals.md) — Attach metadata for condition-based policies
* [Build principal relationships](build-principal-relationships.md) — Create group memberships and hierarchies
