# MDC Keys Reference

## MDC Keys Reference

### Node Information (Management API and Gateway)

| MDC Key | Description |
|:--------|:------------|
| `nodeId` | Unique node identifier |
| `nodeHostname` | Node hostname |
| `nodeApplication` | Application name (e.g., `gio_apim_gateway`) |

### API Information (Gateway Only)

| MDC Key | Description |
|:--------|:------------|
| `apiId` | API identifier |
| `apiName` | API name |
| `apiType` | API type (v2, v4, etc.) |
| `envId` | Environment identifier |
| `orgId` | Organization identifier |
| `appId` | Application identifier |
| `planId` | Plan identifier |
| `user` | User identifier |

{% hint style="info" %}
MDC keys were renamed to shorter forms (`envId`, `orgId`, `appId`, `planId`) in PR #328.
{% endhint %}

### HTTP, MESSAGE, A2A, LLM, MCP APIs (Gateway Only)

| MDC Key | Description |
|:--------|:------------|
| `serverId` | Server identifier |
| `contextPath` | Request context path |
| `requestMethod` |  |

### TCP APIs (Gateway Only)

| MDC Key | Description |
|:--------|:------------|
| `serverId` | Server identifier |
| `sni` | Server Name Indication |

### Kafka Native APIs (Gateway Only)

| MDC Key | Description |
|:--------|:------------|
| `connectionId` |  |
| `principal` |  |
