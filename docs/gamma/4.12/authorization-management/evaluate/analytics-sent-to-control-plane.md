---
hidden: false
noIndex: false
---

# Analytics sent to the control plane

Understand the observability data that PDP gateways send back to the Gravitee control plane.

{% hint style="warning" %}
This feature is under active development and may not be available in all environments at this time.
<!-- GAP: Analytics reporting from PDP gateways to the control plane is referenced in the QuickStart page KPI tiles and the DashboardPage infrastructure, but the specific metrics payload, collection interval, and dashboard visualizations need engineering confirmation. -->
{% endhint %}

## Overview

PDP gateways report authorization decision metrics to the Gravitee control plane. This telemetry powers the Authorization Management dashboard and the KPI tiles on the Quick Start page.

## Data collected

The Quick Start page surfaces four KPI tiles, suggesting the following data is collected:

| Metric | Source |
|--------|--------|
| **Policies** | Count of policies by status (Draft, Deployed, Disabled) |
| **Entities** | Count of principal and resource entities |
| **Decision count** | Number of permit/deny evaluations per time window |
| **Evaluation latency** | P50/P95/P99 latency of policy evaluation |

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
