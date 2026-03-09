# Native API phases

## Supported connector modes

Connectors declare which phases they support. The Entrypoint Connect mode is available only on entrypoint connectors.

| Connector | Supported Modes |
|:----------|:----------------|
| Native Kafka Entrypoint | `ENTRYPOINT_CONNECT`, `INTERACT`, `PUBLISH`, `SUBSCRIBE` |
| Native Kafka Endpoint | `INTERACT`, `PUBLISH`, `SUBSCRIBE` |
| Agent-to-Agent Entrypoint | `ENTRYPOINT_CONNECT`, `SUBSCRIBE`, `PUBLISH` |
| Agent-to-Agent Endpoint | `SUBSCRIBE`, `PUBLISH` |
