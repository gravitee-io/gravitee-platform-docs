# Dictionary Management Overview

## Overview

Dictionary Management enables administrators to create, update, and delete dictionaries via the Automation API and Kubernetes CRD. Dictionaries store key-value pairs that can be referenced in API policies and configurations. Manual dictionaries hold static properties, while dynamic dictionaries poll external HTTP providers to refresh values automatically.

## Key Concepts

### Dictionary Types

Dictionaries exist in two types: `MANUAL` and `DYNAMIC`. Manual dictionaries store static key-value pairs defined at creation time. Dynamic dictionaries fetch properties from an external HTTP endpoint at scheduled intervals using a JOLT transformation specification to map the response into key-value pairs. Both types can be deployed to the gateway (manual) or started/stopped (dynamic) to control availability.

| Type | Properties Source | Deployment Behavior |
|:-----|:-----------------|:--------------------|
| `MANUAL` | Static `properties` map | Deploy/undeploy to gateway |
| `DYNAMIC` | HTTP provider with JOLT spec | Start/stop polling provider |

### HRID and Uniqueness

Each dictionary is identified by a human-readable ID (HRID) that must match the pattern `^[a-zA-Z0-9][a-zA-Z0-9_-]+[a-zA-Z0-9]$` with a maximum length of 256 characters. HRIDs are unique within an environment. When creating a dictionary via the Automation API, the HRID is used as the primary key. If not provided, the system derives an ID from the dictionary name.

### Deployment State

A dictionary's deployment state determines whether it is active on the gateway. For manual dictionaries, `deployed: true` means the dictionary is deployed to the gateway (indicated by a non-null `deployedAt` timestamp). For dynamic dictionaries, `deployed: true` starts the polling provider (state becomes `STARTED`). Setting `deployed: false` undeploys manual dictionaries (sets `deployedAt` to null) or stops dynamic dictionaries.
