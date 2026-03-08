### Prerequisites

Before configuring the Entrypoint Connect phase, ensure the following components are installed:

* Gravitee API Management 4.11.0 or later
* Native Kafka reactor 6.0.0-alpha.1 or later (for Native Kafka APIs)
* Agent-to-agent connectors 2.0.0-alpha.1 or later (for agent-to-agent APIs)
* UI components 17.6.1 or later (for Policy Studio support)

### API Definition Model

The `entrypointConnect` field in the API definition model defines policies for the Entrypoint Connect phase.

| Property | Type | Description |
|:---------|:-----|:------------|
| `entrypointConnect` | Array of Step objects | Policies executed during the Entrypoint Connect phase |
| `interact` | Array of Step objects | Policies executed on all client-gateway interactions |
| `publish` | Array of Step objects | Policies executed during message publishing |
| `subscribe` | Array of Step objects | Policies executed during message subscription |

{% hint style="info" %}
The `connect` field has been removed from the API definition model. Use `entrypointConnect` instead.
{% endhint %}

### Database Schema Requirements

JDBC-based flow repositories must support the `ENTRYPOINT_CONNECT` enum value in the `flow_step_phase` column. The deprecated `CONNECT` enum value has been removed.

### Phase Execution Order

The gateway executes policies in the following order:

| Order | Phase | Timing |
|:------|:------|:-------|
| 1 | Entrypoint Connect | Before authentication, before message processing |
| 2 | Authentication | Gateway-managed authentication step |
| 3 | Interact | On all client-gateway interactions |
| 4 | Publish / Subscribe | During message flow |

### Context Attribute Propagation

Attributes set during the Entrypoint Connect phase are automatically propagated to the connection context and remain available to all subsequent phases. When the Entrypoint Connect policy chain completes, attributes are copied back to the connection context for use in authentication and message-phase policies.

### Creating Policies for Entrypoint Connect

To add policies to the Entrypoint Connect phase:

1. Open the API in Policy Studio and navigate to the Global tab.
2. Select the Entrypoint Connect phase tile, which displays the helper text "Policies will be applied when client connects to entrypoint before authentication and message processing."
3. Click "Add policy" to open the policy catalog dialog.
4. Select a policy compatible with the Entrypoint Connect phase and configure its parameters.
5. Reorder policies within the phase as needed using drag-and-drop.
6. Save and deploy the API to activate the Entrypoint Connect policy chain.

### Interrupting Connections

Policies can interrupt a connection during the Entrypoint Connect phase by calling the `interrupt()` method on the `EntrypointConnectContext`. When a policy interrupts the connection:

1. The gateway does not attempt any upstream connection.
2. The gateway sends a Kafka-compatible error to the client and terminates the client connection.
3. All downstream message-phase policies are skipped for that connection.

Interrupting errors are logged at DEBUG level. Non-interrupting errors are logged at WARN level and execution continues.
