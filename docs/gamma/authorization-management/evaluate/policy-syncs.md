---
hidden: false
noIndex: true
---

# Policy syncs

Understand how authorization policies are synchronized from the control plane to PDP gateways.

## Sync lifecycle

When you deploy a policy in the console, the following sequence occurs:

1. **Console action**: You click **Deploy to PDP Runtime** or **Create and Deploy policy**
2. **Backend update**: The policy status changes to `DEPLOYED` and the backend records the policy text
3. **Gateway sync**: Within approximately 30 seconds, the gateway's PDP pulls the updated policy from the control plane
4. **Enforcement**: The PDP begins evaluating requests against the new policy

## Sync timing

| Event | Timing |
|-------|--------|
| **Policy deploy** | Immediate in the console |
| **Gateway picks up change** | ~30 seconds |
| **Policy undeploy** | Gateway drops the policy within ~30 seconds |

{% hint style="info" %}
The ~30 second sync window is noted in the UI's setup walkthrough: "A policy stays a Draft until you deploy it to the PDP Runtime — the gateway picks it up within ~30 seconds and starts enforcing. Undeploy or edit any time."
{% endhint %}

## What syncs

The PDP synchronization covers:

| Data type | Sync behavior |
|-----------|--------------|
| **Policies** | Full policy text (GAPL) and metadata (type, target, status) |
| **Entities** | Principal and resource entities referenced by deployed policies |
| **Schema** | The published schema definition |
| **Scope targets** | Gateway-specific scoping from the `scopeTargets` field |

## Scope targeting

Both policies and entities support **scope targets** — an array of PDP gateway identifiers that restrict where the item is enforced:

| Scope targets value | Behavior |
|-------------------|----------|
| `["*"]` | Synced to all gateways |
| `["eu-prod", "us-prod"]` | Synced only to gateways with matching Target PDP IDs |
| `[]` (empty) | Synced to all gateways (same as `*`) |

## Monitoring sync status

### PDP Gateways page

The PDP Gateways table shows the status of each registered gateway:

| Status | Meaning |
|--------|---------|
| **PENDING** | The engine is provisioning or has not connected yet |
| **PUBLISHED** | The engine is active and receiving policy updates |

### Policy list pages

Each policy row shows the status badge (`Draft`, `Deployed`, or `Disabled`), indicating whether it has been synced to the PDP runtime.

## Troubleshooting

| Symptom | Possible cause | Resolution |
|---------|---------------|------------|
| Policy shows `Deployed` but not enforced | Gateway has not synced yet | Wait 30 seconds, then verify PDP gateway status is `PUBLISHED` |
| Gateway stays `PENDING` | Gateway cannot reach the control plane | Check network connectivity between the gateway and the control plane |
| Policy enforced on wrong gateway | Incorrect scope targets | Verify the policy's target gateways match the intended PDP gateway |

## Next steps

* [Configure the Gravitee Gateway as a runtime](configure-gravitee-gateway-as-runtime.md) — Register PDP gateways
* [AuthZEN PDP synchronization](../authz-gateway-sync.md) — Sync protocol reference
