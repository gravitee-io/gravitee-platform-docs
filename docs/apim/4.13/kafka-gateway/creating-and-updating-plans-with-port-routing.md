---
description: Create and update plans with port routing for Native Kafka APIs, including bootstrap port and broker range configuration.
---

# Create and Update Plans with Port Routing

## Create a Plan with Port Routing

Navigate to the plan configuration screen for a Native Kafka API. When port routing is enabled at the environment level, the plan general step displays three port configuration fields.

1. Enter a value in the **Bootstrap port** field (range: 1024–65535). This is the port clients use to connect to the API.

2. Enter a value in the **Broker range start** field (range: 1024–65535). This defines the beginning of the port range allocated for backend brokers.

3. Enter a value in the **Broker range end** field (range: 1024–65535). This defines the end of the port range allocated for backend brokers.

When you set a bootstrap port and leave the broker range fields empty, the Management Console auto-fills the broker range start to `bootstrapPort + 1` and the broker range end to `bootstrapPort + 3`, allocating three broker slots by default. User-edited ranges are never overwritten by auto-fill logic.

The Management Console validates that the broker range start is less than or equal to the broker range end and that the bootstrap port doesn't fall within the broker range. It also validates that all ports are within the 1024–65535 range. The gateway checks for port conflicts with other plans in the same environment before saving.

The following table describes the port configuration fields and their validation rules:

| Field | Description | Validation |
|:------|:------------|:-----------|
| **Bootstrap port** | Entry point for client connections | 1024–65535; must not overlap with broker range or other plans' bootstrap ports |
| **Broker range start** | Start of broker port range | 1024–65535; must be ≤ broker range end |
| **Broker range end** | End of broker port range | 1024–65535; must be ≥ broker range start |

## Update Port Allocations

When editing a plan for a deployed API, changing the broker range displays a warning banner:

> "Changing the broker port range will cause a brief reconnection for active consumers. Clients will automatically reconnect on their next metadata refresh — no configuration change required on the client side."

If you change the bootstrap port, a confirmation dialog appears before saving. The dialog resolves to `true` to proceed with the save or `false` to abort. The confirmation is not triggered when setting a bootstrap port for the first time or when the bootstrap port is unchanged.
