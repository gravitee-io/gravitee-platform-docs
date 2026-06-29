---
hidden: false
noIndex: false
---

# Configure a sidecar as runtime

Deploy the Policy Decision Point (PDP) as a sidecar alongside your application for latency-sensitive or air-gapped environments.

{% hint style="warning" %}
Sidecar deployment is an advanced pattern. For most environments, the Gravitee Gateway PDP is the recommended runtime. See [Configure the Gravitee Gateway as a runtime](configure-gravitee-gateway-as-runtime.md).
{% endhint %}

## Overview

A sidecar PDP runs as a co-located process alongside your application. Instead of evaluating policies at the gateway, the sidecar evaluates them locally with sub-millisecond latency and no network hop.

## Architecture

```
┌────────────────────────────────┐
│        Application Pod         │
│  ┌──────────┐  ┌────────────┐  │
│  │  Your    │  │  PDP       │  │
│  │  App     │──│  Sidecar   │  │
│  │          │  │            │  │
│  └──────────┘  └─────┬──────┘  │
│                      │         │
└──────────────────────┼─────────┘
                       │ Sync
              ┌────────┴──────────┐
              │  Gravitee Control │
              │  Plane            │
              └───────────────────┘
```

## Prerequisites

* The PDP sidecar image deployed in your cluster
* Network connectivity from the sidecar to the Gravitee control plane for policy sync
* A registered PDP gateway in Authorization Management

## Steps

### 1. Register a PDP gateway

In the Gravitee console, navigate to **Authorization Management → PDP Gateways** and click **Register PDP gateway**. Set the **Target PDP ID** to an identifier for this sidecar (for example, `sidecar-checkout`).

### 2. Create an AuthZEN endpoint

In the registration dialog, check **Create AuthZEN endpoint** and set the path (for example, `/sidecar-checkout/`).

### 3. Deploy the sidecar

Deploy the PDP sidecar container alongside your application. Configure it with:

| Configuration | Value |
|--------------|-------|
| **Control plane URL** | Your Gravitee control plane address |
| **Environment ID** | The environment the policies are published to |
| **Target PDP ID** | The identifier from step 1 (for example, `sidecar-checkout`) |

### 4. Verify policy sync

Once deployed, the sidecar polls the control plane for policy updates. The PDP gateway status in the console transitions from `PENDING` to `PUBLISHED` when the sidecar connects.

### 5. Integrate with your application

Point your application's authorization checks to the sidecar's local endpoint (typically `http://localhost:<port>/access/v1/evaluation`).

## When to use sidecar vs. gateway

| Factor | Gateway PDP | Sidecar PDP |
|--------|------------|-------------|
| **Latency** | Network hop to gateway | Sub-millisecond (local) |
| **Deployment** | Centralized | Per-application |
| **Maintenance** | Single upgrade point | Each sidecar must be upgraded |
| **Network dependency** | Inline | Control plane only |
| **Best for** | Most environments | Latency-critical or air-gapped |

## Next steps

* [Policy syncs](policy-syncs.md) — How the sidecar receives policy updates
* [AuthZEN PDP synchronization](../authz-gateway-sync.md) — Sync protocol details
