---
hidden: false
noIndex: false
---

# Monitor AI Gateway usage from employee systems
<!-- GAP-STRUCTURAL: Missing procedural content source -->
<!-- GAP: 72 · Confirmable · Confirm the full set of metrics available and the time range/granularity options. Needs: Demo session, Engineering input -->

The Edge Management dashboard provides centralized visibility into AI traffic originating from employee devices where the Edge Daemon is installed. This dashboard is the control plane complement to the Edge Daemon's local enforcement — it shows what's happening across your entire device fleet.

## Dashboard overview

The Edge Management dashboard provides four main views:

### Fleet overview

| Column                  | Description                                                              |
| ----------------------- | ------------------------------------------------------------------------ |
| **Device name**         | The enrolled device's hostname or MDM-assigned name.                     |
| **Status**              | Online, offline, or degraded. Based on the Edge Daemon's last heartbeat. |
| **OS**                  | Operating system and version.                                            |
| **Edge Daemon version** | The version of the Edge Daemon installed on this device.                 |
| **Last heartbeat**      | Timestamp of the most recent check-in from the Edge Daemon.              |

### Metrics

AI usage metrics filterable by **device**, **team**, and **model**:

| Metric              | Description                                                                                      |
| ------------------- | ------------------------------------------------------------------------------------------------ |
| **Tokens consumed** | Total input and output tokens across all models, with cost based on the model's configured rate. |
| **Requests**        | Total API requests to AI providers.                                                              |
| **Cost**            | Aggregated cost across all models and providers.                                                 |

### Shadow AI panel

Shadow AI detection surfaces AI traffic that bypasses the governance layer — traffic going directly to AI providers instead of through the Edge Daemon and AI Gateway.

| Metric                      | Description                                                                                       |
| --------------------------- | ------------------------------------------------------------------------------------------------- |
| **Managed traffic**         | Requests routed through the Edge Daemon → AI Gateway. Fully governed.                             |
| **Unmanaged traffic**       | Requests detected by the Edge Daemon going directly to known AI provider endpoints. Not governed. |
| **Managed/unmanaged ratio** | The percentage of AI traffic under governance vs. shadow traffic.                                 |
| **Shadow AI detail**        | Per-device breakdown of which tools and providers are being used outside of governance.           |

The shadow AI panel is the starting point for the MDM feedback loop: identify unmanaged traffic → push an MDM configuration to route that traffic through the Edge Daemon → verify the traffic shifts to managed. See [Configure Kandji to deploy the Edge Daemon](../edge-daemon/configure-kandji-daemon.md) for the full loop.

### System health

| Metric                  | Description                                                                                                        |
| ----------------------- | ------------------------------------------------------------------------------------------------------------------ |
| **MDM connectivity**    | Status of the connection between the Gamma control plane and your MDM provider (Kandji, Jamf, Intune).             |
| **Edge Daemon status**  | Aggregate fleet status — how many devices are online, offline, or running outdated Edge Daemon versions.           |
| **Deployment tracking** | Configuration rollout status — how many devices have received the latest model allowlist and policy configuration. |

## Access the dashboard

1. From the Gamma console sidebar, select **Agent Management**.
2. Navigate to **Observe** → **Edge Management**.
3. The dashboard displays the fleet overview, with tabs for metrics, shadow AI, and system health.

## Next steps

* [Configure Kandji to deploy the Edge Daemon](../edge-daemon/configure-kandji-daemon.md) — Set up Edge Management and deploy the Edge Daemon to your fleet.
* [Connect Claude Code to the Edge Daemon](../edge-daemon/connect-claude-code-to-daemon.md) — Route AI tool traffic through the Edge Daemon.
* [Inspect your agent log](inspect-your-agent-log.md) — Trace individual invocations at the AI Gateway level.
