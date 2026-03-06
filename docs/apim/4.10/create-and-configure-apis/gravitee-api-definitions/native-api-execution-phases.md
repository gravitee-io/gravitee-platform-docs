### Execution phases in Native APIs

Native APIs execute policies across four distinct phases in the following order:

1. **Entrypoint Connect** – Policies execute when the client connects to the entrypoint, after TLS handshake (if configured) but before authentication. Policies can access connection metadata (remote address, local address, TLS session) but not the authenticated principal.
2. **Interact** – Policies execute on all interactions between client and Gateway.
3. **Publish** – Policies execute on messages published by the client.
4. **Subscribe** – Policies execute on messages delivered to the client.

| Phase | Executes When | Has Access To | Use Cases |
|:------|:-------------|:--------------|:----------|
| Entrypoint Connect | Client connects, before authentication | Connection metadata, TLS session | IP allowlisting, TLS validation, connection throttling |
| Interact | All client-Gateway interactions | Authenticated principal, connection metadata | Authorization, rate limiting |
| Publish | Client publishes a message | Message payload, authenticated principal | Content validation, transformation |
| Subscribe | Gateway delivers a message to client | Message payload, authenticated principal | Content filtering, transformation |

### Connection interruption

Policies executing in the Entrypoint Connect phase can reject connections by calling `context.interrupt(reason)`. This throws an `InterruptConnectionException`, which the reactor catches and handles by closing the socket. The connection is terminated before authentication or message processing begins.

### Connector mode support

Connectors declare which phases they support. The `ENTRYPOINT_CONNECT` mode applies only to entrypoint connectors for Native APIs. Endpoint connectors don't support this mode.

| Connector | Supported Modes |
|:----------|:---------------|
| Native Kafka Entrypoint | ENTRYPOINT_CONNECT, INTERACT, PUBLISH, SUBSCRIBE |
| Native Kafka Endpoint | INTERACT, PUBLISH, SUBSCRIBE |
| Agent-to-Agent Entrypoint | ENTRYPOINT_CONNECT, SUBSCRIBE, PUBLISH |
| Agent-to-Agent Endpoint | SUBSCRIBE, PUBLISH |

### Prerequisites

Before configuring the Entrypoint Connect phase, ensure the following:

* Gravitee APIM 4.11.x or later
* Native API (e.g., Native Kafka API)
* Entrypoint connector that supports `ENTRYPOINT_CONNECT` mode (e.g., Native Kafka Entrypoint 6.x, Agent-to-Agent Entrypoint 2.x)

### Gateway configuration

