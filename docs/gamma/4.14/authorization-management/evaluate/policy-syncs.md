---
hidden: false
noIndex: false
description: How authorization policies travel from the control plane to your runtime gateways, and how long it takes. Learn to read and monitor sync status.
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
| **Entities** | Every principal and resource entity, whether or not a policy names it, routed by its target gateways like a policy |
| **Schema** | Each schema document assigned to a PDP gateway or to the **Bootstrap PDP** syncs to the gateways that host it. An unassigned document doesn't sync. |
| **Scope targets** | Gateway-specific scoping from the `scopeTargets` field |

## Scope targeting

Both policies and entities support **scope targets** — an array of PDP gateway identifiers that restrict where the item is enforced:

| Scope targets value | Behavior |
|-------------------|----------|
| `["*"]` | Every registered PDP, and the default engine of every gateway |
| `["eu-prod", "us-prod"]` | Only the PDPs with matching Target PDP IDs |
| `[]` (empty) | The default engine of every gateway only. A named PDP doesn't get the item: target it, or use `*` |

## Monitoring sync status

### PDP Gateways page

Each registered PDP gateway shows the status `PUBLISHED` as soon as it's registered. The status records the registration only. It doesn't show whether a gateway runs the engine: a PDP gateway whose sharding tag no gateway carries is `PUBLISHED` too. To check that a policy is enforced, ask for a decision, for example through the PDP gateway's [AuthZEN endpoint](ask-for-a-decision/authzen-endpoint.md), or read the **Decisions** page.

### Policy list pages

Each policy row shows the status badge (`Draft`, `Deployed`, or `Disabled`), indicating whether it has been synced to the PDP runtime.

## Troubleshooting

| Symptom | Possible cause | Resolution |
|---------|---------------|------------|
| Policy shows `Deployed` but not enforced | Gateway has not synced yet, or no running gateway carries the PDP gateway's sharding tag | Wait 30 seconds. Check that a gateway with the matching sharding tag is running and can reach the control plane |
| Policy enforced on wrong gateway | Incorrect scope targets | Verify the policy's target gateways match the intended PDP gateway |

## Next steps

* [Configure the Gravitee Gateway as a runtime](configure-gravitee-gateway-as-runtime.md) — Register PDP gateways
* [Authorization policy synchronization](../authz-gateway-sync.md) — Sync protocol reference
