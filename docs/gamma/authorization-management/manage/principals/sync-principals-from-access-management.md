---
hidden: false
noIndex: true
---

# Sync principals from Access Management

Synchronize users and groups from Gravitee Access Management (AM) into Authorization Management so the policy engine can reference your organization's identity directory.

## Prerequisites

* An Access Management connection configured in **Platform → Access Management**
* The `ENVIRONMENT_AUTHZ_ENTITY[CREATE]` permission

{% hint style="info" %}
If no AM connection is configured, the **Sync from AM** button is disabled with the hint: "Connect Access Management first — configure the AM connection in Platform → Access Management."
{% endhint %}

## How sync works

When you trigger a sync, the console calls the backend's AM sync endpoint. The backend:

1. Walks the AM user directory in batches
2. Upserts each user as a `PRINCIPAL` entity with source `gravitee_am`
3. Reports progress via an async job (status transitions: `PENDING → SUCCESS` or `PENDING → ERROR`)

During the sync, the console:
- Polls the Principals list every 2.5 seconds, so synced users appear progressively in the table without a manual refresh
- Shows a toast: "Syncing entities from Gravitee Access Management…"
- On completion, shows a toast: "Sync finished, synced N entities"

{% hint style="warning" %}
If a sync is already running, a new sync request returns a `409 Conflict`. The console suppresses the error and reflects the in-flight job status.
{% endhint %}

## Steps

### 1. Open the Entities page

From the Authorization Management sidebar, select **Policy Structure → Entities**. Select the **Principals** tab.

### 2. Start the sync

Click the **Import** dropdown on the Principals toolbar. Select the **Sync from AM** option.

### 3. Monitor progress

The Principals table refreshes automatically while the sync is in progress. Synced users appear with the source label **AM**.

### 4. Verify synced principals

Once complete, the synced principals appear in the Principals table. Each synced principal:

| Property | Value |
|----------|-------|
| **Source** | `AM` |
| **Editability** | Source-managed attributes are re-asserted on the next sync. Target gateways you set are preserved |
| **Entity type** | Determined by AM (typically `User` or `Group`) |

## Sync behavior

| Aspect | Behavior |
|--------|----------|
| **Direction** | AM → Authorization Management (one-way) |
| **Conflict resolution** | Upsert — existing entities are updated, not duplicated |
| **Attribute precedence** | Source-managed attributes from AM overwrite local changes on each sync |
| **Target gateways** | Preserved across syncs; AM does not manage gateway scope |
| **Deletion** | Removing a user from AM does not delete them from Authorization Management. Use the entity table's **Remove** action to delete manually |

## Next steps

* [Create a local principal](create-a-local-principal.md) — Add principals not in your AM directory
* [Add attributes to principals](add-attributes-to-principals.md) — Attach custom metadata for policy conditions
