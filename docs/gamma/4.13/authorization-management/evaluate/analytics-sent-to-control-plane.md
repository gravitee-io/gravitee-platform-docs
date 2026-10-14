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

PDP gateways report authorization decision metrics to the Gravitee control plane. This telemetry powers the Authorization Management dashboard and the KPI tiles on the Quick Start page.

Decisions are reported by the callers of the PDP: the PEP policy, the AuthZEN endpoint, and the AuthZEN policy. The decision log shows which caller asked for each decision.

## Data collected

The Quick Start page surfaces four KPI tiles, suggesting the following data is collected:

| Metric | Source |
|--------|--------|
| **Policies** | Count of policies by status (Draft, Deployed, Disabled) |
| **Entities** | Count of principal and resource entities |
| **Decision count** | Number of permit/deny evaluations per time window |
| **Evaluation latency** | P50/P95/P99 latency of policy evaluation |

For each decision, the decision log records the verdict (**Permit**, **Forbid**, or **Not applicable**), the subject, the action, the resource, the reasons reported, the matched policies, and the evaluation time.

## Quick Start KPI tiles

The Quick Start page displays four KPI tiles populated by the `useQuickStartCounts` hook, which queries the backend for:

| Tile | Backend field |
|------|--------------|
| **MCP Servers** | Count of MCPServer entities |
| **AI Models** | Count of Model entities |
| **APIs** | Count of API entities |
| **Policies** | Count of all policies |

## Dashboard pages

The Dashboard page provides per-category analytics cards:

| Category | Status |
|----------|--------|
| **APIs** | Active |
| **MCP Servers** | Active |
| **AI Models** | Active |
| **Agents** | Coming soon |
| **Users and Groups** | Coming soon |

{% hint style="info" %}
The Agent and Users and Groups dashboard cards are marked "Coming soon" in the current release. Analytics for these categories will be available in a future update.
{% endhint %}

The authorization overview dashboard opens on a relative seven-day range. It charts decisions over time, decision mix, coverage gaps, caller mix, decisions by PDP, and decisions by protected API, alongside a health and latency tile that reports failed decisions, not applicable decisions, and P50 and P95 evaluation times.

## How analytics flow

```
PDP Gateway
    │
    │ Metrics (evaluation decisions, latency, counts)
    ▼
Control Plane
    │
    │ Aggregated analytics
    ▼
Console Dashboard
    │
    │ KPI tiles, charts
    ▼
Authorization Management UI
```

## Next steps

* [Configure the Gravitee Gateway as a runtime](configure-gravitee-gateway-as-runtime.md) — Register PDP gateways
* [Policy syncs](policy-syncs.md) — How policies reach the gateway
* Compare the coverage gaps on the authorization overview dashboard with your deployed policy set to find evaluations that no policy matched.
