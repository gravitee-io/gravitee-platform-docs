---
hidden: false
noIndex: false
description: Create a local principal in Authorization Management so the policy engine has an identity to evaluate. Follow the steps to add your first one.
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

| Preset | Engine type | Use case |
|--------|-------------|----------|
| **User** | `User` | Individual human identity |
| **Group** | `Group` | Collection of users that share access |
| **Service Account** | `ServiceAccount` | Machine or application identity |
| **Agent Identity** | `AgentIdentity` | AI agent acting on behalf of a user |

If your schema defines additional principal types, those appear in the dropdown instead of the presets. You can also select **Other (custom type)** to create a principal of a type the presets don't cover.

{% hint style="info" %}
When you select **Other (custom type)**, a **Custom type** field appears. The policy engine uses the value as the type exactly as you enter it, for example `Webhook` or `HR::Team`. If you enter a type that the dropdown already offers, the console warns you to select it from the dropdown instead.
{% endhint %}

### 4. Enter a display name and Entity ID

Enter a **Display name** (required). The **Entity ID** fills in from the display name: lowercase, with accents removed and every other character replaced with a dash. Change it to the ID that requests carry for this principal, such as the subject of the user's token. Once you edit it, it no longer follows the display name.

The Entity ID carries no type prefix: the type is stored separately. The hint under the field shows how the policy engine sees the principal, for example `User::"alice"`. An Entity ID holds at most 255 characters, isn't `.` or `..`, and holds no whitespace, control or formatting character, double quote, backslash, `/`, `%`, `;`, `?`, or `#`.

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
| **Entity ID** | The identifier the policy engine uses with the type (for example, `alice` for `User::"alice"`). Click the copy icon to copy it to your clipboard |
| **Name** | The display name |
| **Relationships** | Parent/child counts (for example, "in 1" for a user in one group, or "contains 3 User" for a group) |
| **Policies** | Number of policies targeting this entity |
| **Target gateways** | Gateway scope labels |
| **Source** | Where the principal came from: **Local**, **AM**, or **APIM** |

## Next steps

* [Sync principals from Access Management](../manage/principals/sync-principals-from-access-management.md) — Import users from your identity provider
* [Add attributes to principals](../manage/principals/add-attributes-to-principals.md) — Attach metadata for condition-based policies
* [Create your first policy](create-your-first-policy.md) — Write a permit rule referencing your new principal
