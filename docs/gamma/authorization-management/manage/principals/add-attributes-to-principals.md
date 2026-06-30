---
hidden: false
noIndex: false
---

# Add attributes to principals

Attach custom metadata to principal entities so the policy engine can evaluate conditions beyond identity alone — department, role level, device trust, or any domain-specific property.

## How attributes work

Every entity in Authorization Management carries an `attributes` map — a set of key-value pairs stored with the entity and available to the policy engine at evaluation time. Attributes let you write policies like:

```
permit (
  principal == User::"alice",
  action == Action::"invoke",
  resource == MCPTool::"search"
)
when {
  principal.department == "engineering"
};
```

## Attribute types

The Attribute Editor supports four types:

| Type | Input | GAPL reference | Example |
|------|-------|----------------|---------|
| **String** | Free text | `principal.key == "value"` | `department = "engineering"` |
| **Number** | Numeric value | `principal.key < 100` | `clearance_level = 5` |
| **Boolean** | Toggle switch | `principal.key == true` | `mfa_enabled = true` |
| **Set** | Comma-separated values | `principal.key.contains("value")` | `scopes = read,write,admin` |

{% hint style="info" %}
All attribute values are stored as text on the wire. The policy engine coerces them based on the declared type. The editor shows a hint for each type: "Stored as text; reference with `principal.<key>` in policies."
{% endhint %}

## Adding attributes during creation

When creating a new principal via **Add Principal**:

1. Scroll to the **Attributes** section at the bottom of the panel
2. Click **Add attribute**
3. Enter the **Key** (must be unique across the entity's attributes)
4. Select the **Type** from the dropdown
5. Enter the **Value**
6. Repeat for additional attributes

## Adding attributes to existing entities

1. On the Entities page, find the entity in the Principals table
2. Click the **⋮** menu → **Edit**
3. In the Edit panel, scroll to the **Attributes** section
4. Click **Add attribute** or modify existing rows
5. Click **Save**

## Attribute key rules

- Keys must not start with `_` (reserved for system attributes like `_displayName` and `_catalogId`)
- Keys must be unique within the entity
- Keys are case-sensitive

## Reserved attributes

The following attributes are managed by the system and should not be set manually:

| Key | Purpose |
|-----|---------|
| `_displayName` | The entity's display name (set via the Display Name field) |
| `_catalogId` | The AI Catalog item ID (set during catalog import) |
| `_importedAt` | Timestamp of the last catalog import |
| `description` | The entity description (set via the Description field) |

## Attribute persistence across syncs

| Entity source | Behavior |
|--------------|----------|
| **Local** | Attributes are fully editable and persist until manually changed |
| **AM** (synced) | Source-managed attributes are re-asserted on each sync. Custom attributes you add are preserved |
| **Gravitee Catalog** (imported) | Catalog-sourced attributes are re-asserted on reimport. Custom attributes and target gateways are preserved |

## Next steps

* [Build principal relationships](build-principal-relationships.md) — Create group memberships
* [Create your first policy](../../get-started/create-your-first-policy.md) — Reference attributes in policy conditions
