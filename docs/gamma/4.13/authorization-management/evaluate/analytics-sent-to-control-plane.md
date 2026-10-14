---
hidden: false
noIndex: false
description: The observability data that Policy Decision Point gateways send back to the Gravitee control plane. Learn what is collected and where it appears.
---

# Analytics sent to the control plane

Understand the observability data that PDP gateways send back to the Gravitee control plane.

{% hint style="warning" %}
This feature is under active development and may not be available in all environments at this time.
{% endhint %}

## Overview

PDP gateways report each authorization decision to the Gravitee control plane through the gateway's reporters. These decision records power the **Dashboards** and **Decisions** pages in the **Observability** section of Authorization Management.

Decisions are reported by the callers of the PDP: the PEP policy, the AuthZEN endpoint, and the AuthZEN policy. The **Decisions** page shows which caller asked for each decision.

## Data collected

The gateway writes one decision record for each evaluation. For each decision, the record holds the verdict (**Permit**, **Forbid**, or **Not applicable**), the subject, the action, the resource, the reasons reported, the matched policies, and the evaluation time.

## Dashboards

The **Authorization — Overview** dashboard opens on a relative seven-day range. It charts decisions over time, decision mix, coverage gaps, caller mix, decisions by PDP, and decisions by protected API, alongside a health and latency tile that reports failed decisions, not applicable decisions, and P50 and P95 evaluation times.

## Quick Start tiles

The four tiles on the **Quick Start** page don't use decision records. They count what's configured in the environment:

<table>
    <thead>
        <tr>
            <th width="200">Tile</th>
            <th>What it counts</th>
        </tr>
    </thead>
    <tbody>
        <tr>
            <td><strong>MCP</strong></td>
            <td>MCP policies</td>
        </tr>
        <tr>
            <td><strong>Agents</strong></td>
            <td>Agent policies</td>
        </tr>
        <tr>
            <td><strong>AI Models</strong></td>
            <td>AI model policies</td>
        </tr>
        <tr>
            <td><strong>Users and groups</strong></td>
            <td>Principal entities</td>
        </tr>
    </tbody>
</table>

{% hint style="info" %}
The **Users and groups** tile shows **Coming soon** in place of a management link in the current release.
{% endhint %}

## How analytics flow

```
Caller of the PDP (PEP policy, AuthZEN endpoint, or AuthZEN policy)
    │
    │ One decision record for each evaluation
    ▼
Gateway reporters
    │
    │ Decision records
    ▼
Control plane
    │
    │ Queries from the Dashboards and Decisions pages
    ▼
Authorization Management Observability
```

## Next steps

* [Configure the Gravitee Gateway as a runtime](configure-gravitee-gateway-as-runtime.md): Register PDP gateways.
* [Policy syncs](policy-syncs.md): Learn how policies reach the gateway.
* Compare the coverage gaps on the **Authorization — Overview** dashboard with your deployed policy set to find evaluations that no policy matched.
