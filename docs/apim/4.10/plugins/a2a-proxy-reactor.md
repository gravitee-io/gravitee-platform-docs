### Overview

The A2A Proxy reactor enables agent-to-agent communication through Gravitee API Management. It operates as a standalone protocol type alongside HTTP Proxy, HTTP Message, Native Kafka, MCP Proxy, and LLM Proxy. The reactor uses dedicated entrypoint and endpoint connectors to handle agent-to-agent traffic with `REQUEST_RESPONSE` mode support.

A2A Proxy APIs support `REQUEST` and `RESPONSE` flow phases. Flows use HTTP path extractors for selector validation and routing decisions.

### Prerequisites

Before deploying the A2A Proxy reactor, ensure the following requirements are met:

* Enterprise license with `apim-a2a-proxy-reactor` feature enabled
* Gravitee API Management 4.x gateway and management API
* Compatible policy versions (see Policy Compatibility)

### Gateway Configuration

#### Reactor Plugin

Deploy `gravitee-reactor-a2a-proxy-*.zip` to the gateway plugins directory.

| Property | Description | Example |
|:---------|:------------|:--------|
| `publish-folder-path` | Installation directory for reactor plugin | `graviteeio-ee/apim/plugins/reactors` |

### API Type Identifier

The A2A Proxy API type uses the identifier `a2a-proxy` in API definitions and `A2A_PROXY` in protocol type enumerations. The UI displays this as "A2A Proxy" with the icon `gio-literal:a2a-proxy`.

#### Endpoint Plugin

Deploy `gravitee-endpoint-a2a-proxy-*.zip` to the gateway plugins directory. The `target` property is required and cannot be null or empty.

| Property | Description | Example |
|:---------|:------------|:--------|
| `publish-folder-path` | Installation directory for endpoint plugin | `graviteeio-ee/apim/plugins/endpoints` |
| `target` | Backend URL for proxied requests | `https://agent.example.com` |

#### Policy Compatibility

The following policies support A2A Proxy APIs. Policies must explicitly declare A2A Proxy support in `plugin.properties`.

| Policy | Minimum Version | Phases |
|:-------|:---------------|:-------|
| `gravitee-policy-assign-attributes` | 3.2.0 | REQUEST, RESPONSE |
| `gravitee-policy-callout-http` | 5.4.0 | REQUEST, RESPONSE |
| `gravitee-policy-groovy` | 4.2.0 | REQUEST, RESPONSE |
| `gravitee-policy-interrupt` | 2.1.0 | REQUEST, RESPONSE |
| `gravitee-policy-ipfiltering` | 2.2.0 | REQUEST, RESPONSE |
| `gravitee-policy-javascript` | 2.1.0 | REQUEST, RESPONSE |
| `gravitee-policy-ratelimit` | 4.3.0 | REQUEST, RESPONSE |
| `gravitee-policy-retry` | 4.1.0 | REQUEST, RESPONSE |
| `gravitee-policy-role-based-access-control` | 2.1.0 | REQUEST, RESPONSE |
| `gravitee-policy-transformheaders` | 5.2.0 | REQUEST, RESPONSE |
| `gravitee-policy-ai-prompt-guard-rails` |  | REQUEST |

### Error Mappings

The A2A Proxy endpoint connector maps connection and timeout exceptions to the following error keys:

| Exception Type | Error Key |
|:--------------|:----------|
| Connection failures | `GATEWAY_CLIENT_CONNECTION_ERROR` |
| `ConnectTimeoutException` | `GATEWAY_CLIENT_CONNECTION_ERROR` |
| `ReadTimeoutException` | `REQUEST_TIMEOUT` |
| `TimeoutException` | `REQUEST_TIMEOUT` |
| `NoStackTraceTimeoutException` | `REQUEST_TIMEOUT` |
