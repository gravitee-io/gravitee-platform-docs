---
hidden: false
noIndex: false
description: Define the verbs your policies grant or forbid by creating an action entity that statements reference. Follow the steps on the Actions page.
---

# Create an action

Define the verbs your policies grant or forbid. Actions are the vocabulary the policy engine evaluates — every `permit` and `forbid` statement references an action.

## How actions work

An action is an entity of type `Action`. Its Entity ID is the action name exactly as a request carries it, with no prefix, for example `invoke` or `GET`. In GAPL, actions appear in the `action` clause as `Action::"<Entity ID>"`:

```
permit (
  principal == User::"alice",
  action == Action::"invoke",
  resource == MCPTool::"search"
);
```

## Steps

### 1. Navigate to the Actions page

From the Authorization Management sidebar, select **Policy Structure → Actions**. The Actions page shows a data table of all defined actions with a KPI tile for the total count.

### 2. Add an action

Click **Add action**. A dialog opens with the following fields:

| Field | Required | Description |
|-------|----------|-------------|
| **Display name** | Yes | Human-readable label shown in policy chip pickers |
| **Entity ID** | Yes | The action name a request carries. It fills in from the display name, for example `Approve Refund` → `approve-refund`, and a policy matches it as `Action::"approve-refund"` |
| **Description** | No | Explains what this action represents |

### 3. Create

Click **Create action**. The action appears in the Actions table.

## Actions table columns

| Column | Description |
|--------|-------------|
| **Action** | Display name |
| **Entity ID** | The action name a request carries (for example, `invoke`). Click the copy icon to copy |
| **Description** | Optional description text |
| **Source** | Where the action came from: **Local**, **APIM**, or **Gravitee Catalog** |

## Searching and filtering

Use the search field to filter actions by name, Entity ID, or description. The table supports sorting by Action name, Entity ID, and Source.

## Deleting an action

1. Click the delete icon (trash) on the action row
2. Confirm in the dialog: "Remove action from Authorization?"
3. The dialog warns: "Policies that reference this action will no longer match it."

{% hint style="warning" %}
Deleting an action does not automatically update policies that reference it. Those policies will simply no longer match on that action until you update them.
{% endhint %}

## Next steps

* [Action naming and scope](action-naming-and-scope.md) — Entity ID conventions and policy type scoping
* [Create, update, and delete policies](../../configure/create-update-delete-policies.md) — Use actions in permit and forbid statements
