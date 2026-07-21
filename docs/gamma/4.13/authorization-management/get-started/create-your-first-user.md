---
hidden: false
noIndex: false
---

# Create your first user

This guide walks you through creating a local principal in Authorization Management. A principal is an identity — a user, group, service account, or agent identity — that the policy engine evaluates in `permit` and `forbid` statements.

## Prerequisites

* Access to Authorization Management in the Gamma console
* The `ENVIRONMENT_AUTHZ_ENTITY[CREATE]` permission

## Steps

### 1. Open the Entities page

From the Authorization Management sidebar, select **Policy Structure → Entities**. The Entities page shows two tabs: **Principals** and **Resources**. Select the **Principals** tab.

### 2. Add a principal

Click **Add Principal**. A slide-out panel opens with the title **Add Principal**.

### 3. Choose a type

Select a principal type from the **Type** dropdown. The presets are:

| Preset | Canonical prefix | Use case |
|--------|----------------|----------|
| **User** | `user` | Individual human identity |
| **Group** | `group` | Collection of users that share access |
| **Service Account** | `serviceaccount` | Machine or application identity |
| **Agent Identity** | `agent-identity` | AI agent acting on behalf of a user |

If your schema defines additional principal types, those appear in the dropdown instead of the presets. You can also select **Other (custom prefix)** to create a principal with a custom type prefix.

{% hint style="info" %}
When you select **Other (custom prefix)**, a prefix field appears. The prefix must start with a letter and contain only lowercase letters, digits, or dashes. If you enter a prefix that matches a preset type, the console warns you to select it from the dropdown instead.
{% endhint %}

### 4. Enter a display name and slug

Enter a **Display name** (required). The **Slug** auto-derives from the display name using NFD normalization: lowercase, non-alphanumeric characters replaced with dashes. You can override the slug manually; once edited, it no longer follows the display name.

The **Entity ID** preview shows the composed identifier: `<prefix>.<slug>`. This is the canonical identifier the policy engine uses in GAPL statements (for example, `user.alice`).

{% hint style="warning" %}
The Entity ID is immutable after creation. If an entity with the same ID already exists, the console rejects the creation with an error: `An entity with ID "<id>" already exists.`
{% endhint %}

### 5. Add optional fields

| Field | Description |
|-------|-------------|
| **Description** | A short note about what this principal represents |
| **Parents** | Link this principal to one or more parent entities of the same kind. For example, add a User to a Group. The parent picker searches existing entities by name |
| **Target gateways** | Scope this principal to specific PDP gateways. Select individual gateways or `*` to target all. If no targets are selected, the principal is available to every gateway |
| **Attributes** | Key-value pairs the policy engine can reference in conditions. Each attribute has a key, a type (String, Number, Boolean, or Set), and a value |

### 6. Create the principal

Click **Create Principal**. The principal appears in the Principals table with the source label **Local** (editable).

## What you see in the table

After creation, the Principals table displays:

| Column | Description |
|--------|-------------|
| **Type** | The entity type badge (for example, `User`) |
| **Entity ID** | The canonical identifier (for example, `user.alice`). Click the copy icon to copy it to your clipboard |
| **Name** | The display name |
| **Relationships** | Parent/child counts (for example, "in 1" for a user in one group, or "contains 3 User" for a group) |
| **Policies** | Number of policies targeting this entity |
| **Target gateways** | Gateway scope labels |
| **Source** | Where the principal came from: **Local**, **AM**, or **APIM** |

## Next steps

* [Sync principals from Access Management](../manage/principals/sync-principals-from-access-management.md) — Import users from your identity provider
* [Add attributes to principals](../manage/principals/add-attributes-to-principals.md) — Attach metadata for condition-based policies
* [Create your first policy](create-your-first-policy.md) — Write a permit rule referencing your new principal
