### What is the Entrypoint Connect phase?

The Entrypoint Connect phase is a policy execution point for Native APIs that runs when a client first connects to the entrypoint. It executes after the transport-layer handshake (e.g., TLS) but before authentication and message processing. Policies in this phase can inspect connection metadata and reject connections early.

### When does the Entrypoint Connect phase execute?

The Entrypoint Connect phase executes in the following sequence:

1. Client connects to entrypoint (TLS handshake if SSL enabled)
2. Entrypoint Connect phase executes
3. Authentication occurs
4. Interact phase executes
5. Message processing begins (Publish/Subscribe phases)

### Phase execution order

Native APIs execute policies in this order:

| Phase | Execution Order | Description |
|:------|:----------------|:------------|
| Entrypoint Connect | 1st | Policies applied when client connects to entrypoint before authentication |
| Interact | 2nd | Policies applied on all interactions between client and Gateway |
| Publish / Subscribe | 3rd | Message-level policies |

HTTP Proxy, Message, LLM Proxy, and MCP Proxy APIs don't support the Entrypoint Connect phase. These API types use Request/Response phases.

### Available context

Policies in the Entrypoint Connect phase can access:

* `connection.id` - Connection identifier
* `connection.remoteAddress` - Client IP address
* `connection.localAddress` - Gateway IP address
* `ssl.*` - TLS session details (if SSL enabled)
* `context.attributes` - API-level attributes

The following context is not available in the Entrypoint Connect phase:

* `principal` - Authentication data (not yet authenticated)
* `request` - Request details (no request processed yet)
* `message` - Message content (no messages yet)

### Connection interruption

Policies can reject connections during the Entrypoint Connect phase by calling `ctx.interrupt(reason)`. This throws an `InterruptConnectionException`, which the reactor catches to close the socket immediately. Use this mechanism to enforce IP allowlists, validate TLS certificates, or apply rate limits before authentication overhead.

### Applicable API types

The Entrypoint Connect phase is available for Native APIs only:

* Native Kafka APIs
* Agent-to-Agent APIs

### Difference from deprecated CONNECT mode

The Entrypoint Connect phase replaces the deprecated `CONNECT` mode. The legacy `CONNECT` mode has been removed from the API definition model and connector implementations.

### Use cases

Use the Entrypoint Connect phase to:

* Enforce IP allowlists before authentication
* Validate TLS certificates
* Apply pre-authentication rate limiting
* Inspect connection properties and reject connections based on criteria
