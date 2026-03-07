### Prerequisites

Before configuring Entrypoint Connect flows, ensure the following:

* Gravitee APIM 4.11.x or later
* Native API definition (Kafka or Agent-to-Agent)
* Policies that declare `ENTRYPOINT_CONNECT` phase support in their plugin manifest
* Java 21 runtime (for Native Kafka reactor 6.x)

### Connector Mode Support

Native API connectors must declare `ENTRYPOINT_CONNECT` in their supported modes. The legacy `CONNECT` mode is no longer valid.

| Connector | Supported Modes |
|:----------|:----------------|
| `AgentToAgentEntrypointConnector` | `ENTRYPOINT_CONNECT`, `SUBSCRIBE`, `PUBLISH` |
| `AgentToAgentEndpointConnector` | `SUBSCRIBE`, `PUBLISH` |
| `NativeKafkaEntrypointConnector` | `ENTRYPOINT_CONNECT`, `INTERACT`, `PUBLISH`, `SUBSCRIBE` |
| `NativeKafkaEndpointConnector` | `INTERACT`, `PUBLISH`, `SUBSCRIBE` |
