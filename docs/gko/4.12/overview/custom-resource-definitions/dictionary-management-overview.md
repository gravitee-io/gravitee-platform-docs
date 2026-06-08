# Dictionary management overview

Dictionary management lets administrators create, update, and delete dictionaries through the Automation API and the Kubernetes CRD. Dictionaries store key-value pairs that can be referenced in API policies and configurations using Gravitee Expression Language. Manual dictionaries hold static properties, while dynamic dictionaries poll an external HTTP provider to refresh values automatically.

## Key concepts

The sections below describe the dictionary types, how dictionaries are identified, and how their deployment state works.

### Dictionary types

Dictionaries come in two types: `MANUAL` and `DYNAMIC`. Manual dictionaries store static key-value pairs defined at creation time. Dynamic dictionaries fetch properties from an external HTTP endpoint at scheduled intervals, using a JOLT transformation specification to map the response into key-value pairs.

| Type | Properties source | Deployment behavior |
|:-----|:-----------------|:--------------------|
| `MANUAL` | Static `properties` map | Deployed or undeployed on the gateway |
| `DYNAMIC` | HTTP provider with a JOLT specification | Polling provider started or stopped |

### HRID and uniqueness

Each dictionary is identified by a human-readable ID (HRID) that matches the pattern `^[a-zA-Z0-9][a-zA-Z0-9_-]+[a-zA-Z0-9]$` with a maximum length of 256 characters. The HRID is used as the dictionary key, and HRIDs are unique within an environment. The same HRID can be used in different environments without conflict.

### Deployment state

A dictionary's deployment state controls whether it's active on the gateway. For a manual dictionary, `deployed: true` deploys the dictionary to the gateway, and `deployed: false` undeploys it. For a dynamic dictionary, `deployed: true` starts the polling provider (its state becomes `STARTED`), and `deployed: false` stops it.
