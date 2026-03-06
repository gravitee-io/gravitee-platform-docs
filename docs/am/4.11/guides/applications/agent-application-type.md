### Overview

The Agent application type enables secure integration of agentic applications (AI assistants, autonomous agents) with Gravitee Access Management. Agent applications enforce restricted grant types to prevent insecure flows and support the A2A (Agent-to-Agent) specification through optional AgentCard metadata. This feature is designed for API administrators configuring OAuth 2.0 clients for AI-driven systems.

### Key Concepts

#### Agent Application Type

Agent applications are OAuth 2.0 clients restricted to secure grant flows. The platform automatically strips forbidden grant types (`implicit`, `password`, `refresh_token`) and response types (`token`, `id_token`, `id_token token`) during application creation, update, and Dynamic Client Registration. If all grant types are removed, the system defaults to `authorization_code`. Agent applications use `client_secret_basic` authentication by default.

#### AgentCard Metadata

AgentCard is an optional URL pointing to an A2A-compliant JSON document describing the agent's capabilities, tools, and provider information. The platform fetches and validates this metadata on demand, enforcing SSRF protections (blocks localhost, private IPs, non-HTTP(S) schemes) and size limits (512 KB maximum). AgentCard URLs must use HTTP or HTTPS schemes and return valid JSON with a 200 status code.

#### Grant Type Enforcement

The token endpoint validates grant type requests at runtime. Agent applications attempting `password`, `refresh_token`, or `implicit` grants receive a `400 Bad Request` error with message: `Grant type '{grantType}' is not allowed for agent applications`. Allowed flows include `client_credentials` and `authorization_code`. Refresh tokens are never issued to agent applications.

### Prerequisites

Before configuring agent applications, ensure the following requirements are met:

* Gravitee Access Management 4.11.0 or later
* `APPLICATION[CREATE]` or `APPLICATION[UPDATE]` permission to configure agent applications
* `APPLICATION[READ]` permission to fetch agent card metadata
* Valid HTTPS endpoint for AgentCard URL (if using A2A metadata)

### Gateway Configuration

#### Application Type Configuration

Configure the application type during creation or update:

| Property | Description | Example |
|----------|-------------|---------|
| `type` | Application type enum; set to `AGENT` for agentic applications | `"AGENT"` |
| `agentCardUrl` | Optional URL to A2A-compliant agent card JSON | `"https://example.com/.well-known/agent-card.json"` |

#### Grant Type Constraints

The platform enforces these constraints automatically:

| Constraint | Value | Applied When |
|:-----------|:------|:-------------|
| Forbidden grant types | `implicit`, `password`, `refresh_token` | Application create, update, DCR, token endpoint |
| Forbidden response types | `token`, `id_token`, `id_token token` | Application create, update, DCR |
| Default grant type | `authorization_code` | When all grant types are stripped or none provided |
| Default response type | `code` | When all response types are stripped and `authorization_code` is granted |
| Default auth method | `client_secret_basic` | When no auth method is explicitly set |

#### AgentCard Fetch Limits

| Property | Value | Description |
|:---------|:------|:------------|
| Maximum response size | 512 KB | Agent card responses exceeding this size are rejected |
| Request timeout | 5000 ms | HTTP requests to agent card URLs time out after 5 seconds |

### Creating an Agent Application

Create an agent application by setting `type` to `AGENT` in the application payload:

1. Submit a `POST` request to `/organizations/{orgId}/environments/{envId}/domains/{domain}/applications` with `type: "AGENT"` and optional `agentCardUrl`.
2. The platform strips forbidden grant types and response types, defaulting to `authorization_code` and `code` if necessary.
3. If an `agentCardUrl` is provided, the platform validates the URL format (must be HTTP/HTTPS with valid scheme).
4. The application is created with enforced constraints; attempting forbidden grant types at the token endpoint returns `400 Bad Request`.

### Updating Agent Application Settings

Modify agent application settings using the PATCH endpoint:

1. Send a `PATCH` request to `/organizations/{orgId}/environments/{envId}/domains/{domain}/applications/{appId}` with `settings.advanced.agentCardUrl` in the request body.
2. The platform validates the new URL format and applies SSRF protections.
3. Grant type and response type constraints are re-applied if modified.

### Restrictions

Agent applications enforce the following restrictions:

* **Forbidden grant types:** `implicit`, `password`, `refresh_token` are automatically stripped during create, update, and DCR operations
* **Forbidden response types:** `token`, `id_token`, `id_token token` are automatically stripped during create, update, and DCR operations
* **No refresh tokens:** Refresh tokens are never issued to agent applications, even when using allowed grant types
* **AgentCard URL constraints:** URLs must use HTTP or HTTPS schemes; non-HTTP(S) schemes are rejected with error message `agent_card_url : {url} is malformed`
* **SSRF protections:** AgentCard fetch requests block localhost targets (error: `SSRF protection: localhost target is not allowed`) and private IP ranges (10.x.x.x, 192.168.x.x, 172.16-31.x.x, 169.254.x.x; error: `SSRF protection: private IP target is not allowed`)
* **Size limits:** Agent card responses exceeding 512 KB are rejected with error message `Agent card response exceeds maximum allowed size`
* **Timeout limits:** HTTP requests to agent card URLs time out after 5000 ms
* **Token endpoint errors:** Attempting forbidden grant types at the token endpoint returns `400 Bad Request` with error message `Grant type '{grantType}' is not allowed for agent applications`

