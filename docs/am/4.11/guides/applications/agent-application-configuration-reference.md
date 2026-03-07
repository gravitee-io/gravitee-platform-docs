### Application Type Property

Agent applications use the `AGENT` application type enum value. This type enforces grant type restrictions and enables AgentCard metadata discovery.

| Property | Description | Example |
|:---------|:------------|:--------|
| `type` | Application type enum; set to `AGENT` for agentic applications | `"AGENT"` |

### AgentCard Configuration

The `agentCardUrl` property points to a JSON document describing the agent's capabilities per the A2A specification. The URL must use the HTTP or HTTPS scheme.

| Property | Description | Example |
|:---------|:------------|:--------|
| `agentCardUrl` | Optional URL to the agent's AgentCard JSON document; must use HTTP or HTTPS scheme | `"https://example.com/.well-known/agent-card.json"` |

### Grant Type Constraints

Agent applications automatically strip forbidden grant types and response types during creation, update, and Dynamic Client Registration.

| Constant | Value | Description |
|:---------|:------|:------------|
| `FORBIDDEN_GRANT_TYPES` | `["implicit", "password", "refresh_token"]` | Grant types automatically stripped from agent applications |
| `FORBIDDEN_RESPONSE_TYPES` | `["token", "id_token", "id_token token"]` | Response types automatically stripped from agent applications |

Allowed grant types include `authorization_code` and `client_credentials`. If all grant types are stripped or none are provided, the system defaults to `authorization_code`.

### AgentCard Fetch Limits

The platform enforces size and timeout limits when fetching AgentCard documents.

| Property | Value | Description |
|:---------|:------|:------------|
| `MAX_BODY_SIZE` | `524288` (512 KB) | Maximum allowed size for AgentCard response body |
| `TIMEOUT_MS` | `5000` | HTTP request timeout in milliseconds |

### URL Validation Rules

The platform validates the `agentCardUrl` format at application creation and update time. The URL must use the HTTP or HTTPS scheme.

| Validation | Error Message |
|:-----------|:--------------|
| Malformed URI | `agent_card_url : {url} is malformed` |
| Non-HTTP(S) scheme | `agent_card_url : {url} is malformed` |
| Missing scheme | `agent_card_url : {url} is malformed` |

### SSRF Protection Rules

The platform applies SSRF protection when fetching AgentCard documents. The following targets are blocked:

| Rule | Error Message |
|:-----|:--------------|
| Localhost target | `SSRF protection: localhost target is not allowed` |
| Private IP ranges (10.x.x.x, 192.168.x.x, 172.16-31.x.x, 169.254.x.x) | `SSRF protection: private IP target is not allowed` |
| Non-HTTP(S) scheme | `Only http/https schemes are allowed for agentCardUrl` |

### AgentCard Fetch Validation

The platform validates the AgentCard response when the `/agent-card` endpoint is called.

| Validation | Error Message |
|:-----------|:--------------|
| Response exceeds 512 KB | `Agent card response exceeds maximum allowed size` |
| Invalid JSON | `Agent card response is not valid JSON` |
| Non-200 HTTP status | `Agent card URL returned status {code}` |

### Token Endpoint Behavior

The token endpoint rejects forbidden grant types for agent applications at runtime.

| Grant Type | Behavior |
|:-----------|:---------|
| `authorization_code` | Allowed |
| `client_credentials` | Allowed |
| `implicit` | Rejected with `UnauthorizedClientException` |
| `password` | Rejected with `UnauthorizedClientException` |
| `refresh_token` | Rejected with `UnauthorizedClientException` |

**Error Message:**
```
Grant type '{grantType}' is not allowed for agent applications
```

### Default Authentication Method

Agent applications default to `client_secret_basic` authentication unless explicitly overridden during creation or update.

