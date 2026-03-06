### Template Variables in Entrypoint Connect Phase

Policies executing in the Entrypoint Connect phase have access to the following template variables:

| Variable | Description | Example |
|:---------|:------------|:--------|
| `{#connection.id}` | Unique connection identifier | `conn-12345` |
| `{#connection.remoteAddress}` | Client IP address and port | `192.168.1.100:54321` |
| `{#connection.localAddress}` | Gateway IP address and port | `10.0.0.5:9092` |
| `{#ssl.*}` | TLS session details (if SSL configured) | `{#ssl.clientCertificate}` |
| `{#context.*}` | Entrypoint connect context attributes | `{#context.attributes['custom-key']}` |

{% hint style="warning" %}
`{#principal.*}` variables are NOT available in the Entrypoint Connect phase. Authentication has not occurred yet.
{% endhint %}

### Restrictions

- The Entrypoint Connect phase is supported only for Native APIs. It is not available for HTTP Proxy, Message, or LLM Proxy APIs.
- Only entrypoint connectors support the `ENTRYPOINT_CONNECT` mode. Endpoint connectors do not support this mode.
- Policies in this phase cannot access the authenticated principal, as authentication occurs after the Entrypoint Connect phase.
- The legacy `CONNECT` connector mode has been removed and replaced by `ENTRYPOINT_CONNECT`.
- Native Kafka Reactor 6.x requires APIM 4.11.x and Java 21.
- Agent-to-Agent connectors 2.x require APIM 4.11.x.

### Related Changes

The UI policy studio now displays the Entrypoint Connect phase before the Interact phase, reflecting the actual execution order. The phase is labeled "Entrypoint Connect phase" in the policy catalog and flow designer. Backend APIs and database schemas have been updated to store `entrypointConnect` flow steps alongside `interact`, `publish`, and `subscribe` steps. The OpenAPI schema for Native APIs includes the `entrypointConnect` array field. UI libraries (`@gravitee/ui-policy-studio-angular`, `@gravitee/ui-particles-angular`) have been updated to version 17.6.1 to support the new phase.
