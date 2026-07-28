# Entrypoint Connect phase

## Overview

The Entrypoint Connect phase runs as soon as a client opens a connection to the entrypoint, before authentication and before any message processing. Use it to apply connection-level controls, such as IP filtering, and to reject a connection before the client authenticates.

The phase applies to native Kafka APIs.

## Prerequisites

Before you configure the Entrypoint Connect phase, check that the following components are installed:

* Gravitee API Management 4.11.0 or later
* Native Kafka reactor 6.0.0 or later

## Phase execution order

The Gateway runs policies in the following order:

| Order | Phase | Timing |
|:------|:------|:-------|
| 1 | Entrypoint Connect | Before authentication and before message processing |
| 2 | Authentication | Gateway-managed authentication step |
| 3 | Interact | On all client-gateway interactions |
| 4 | Publish and subscribe | During message flow |

## Native flow phases in the API definition

A native flow defines the policies that run in each phase:

| Property | Type | Description |
|:---------|:-----|:------------|
| `entrypointConnect` | Array of Step objects | Policies that run during the Entrypoint Connect phase |
| `interact` | Array of Step objects | Policies that run on all client-gateway interactions |
| `publish` | Array of Step objects | Policies that run during message publishing |
| `subscribe` | Array of Step objects | Policies that run during message subscription |

{% hint style="info" %}
The `connect` field was removed from the API definition. Use `entrypointConnect` instead.
{% endhint %}

## Add policies to the phase

1. Open your API in Policy Studio.
2. Click the **Global** tab.
3. Select the **Entrypoint Connect phase** tile. The tile description reads "Policies will be applied when client connects to entrypoint before authentication and message processing".
4. Click **Add policy**.
5. Select a policy that supports the Entrypoint Connect phase, then configure its parameters.
6. Optional: Drag the policies to reorder them within the phase.
7. Save the API, then deploy it to activate the policy chain.

## What's next

* For the Expression Language variables available to policies in this phase, see [Connection interruption in the Entrypoint Connect phase](connection-interruption.md).
* To write your own policy that runs in this phase, see [Policies for the Entrypoint Connect phase](../../../plugins/customization/entrypoint-connect-phase-policies.md).
