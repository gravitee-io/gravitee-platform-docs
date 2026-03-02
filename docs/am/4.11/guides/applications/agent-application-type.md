### Overview

The Agent application type enables secure integration of agentic applications (AI assistants, autonomous agents) with Gravitee Access Management. Agent applications enforce stricter OAuth grant type restrictions and support the A2A AgentCard specification for machine-readable metadata discovery.

### Key Concepts

#### Agent Application Type

Agent applications are a specialized OAuth client type designed for autonomous systems. They default to the authorization code flow with confidential client credentials and prohibit implicit and password-based grants. When creating an agent application, the system automatically strips forbidden grant types and applies secure defaults if no valid grants remain.

#### AgentCard Metadata

AgentCard is a JSON metadata format from the A2A specification that describes an agent's capabilities, endpoints, and configuration. Administrators configure an `agentCardUrl` pointing to the agent's hosted AgentCard JSON. The gateway proxies this metadata through a secure endpoint with SSRF protection, size limits (512 KB), and JSON validation.

#### Grant Type Restrictions

Agent applications cannot use `implicit`, `password`, or `refresh_token` grant types. Attempts to request tokens with these grants are rejected at the token endpoint with an `UnauthorizedClientException`. During application creation or Dynamic Client Registration (DCR), the system automatically removes forbidden grants and defaults to `authorization_code` with response type `code` if no valid grants remain.

### Prerequisites

Before creating or configuring an agent application, ensure the following:

* Gravitee Access Management 4.11.0 or later
* Domain with OAuth 2.0 enabled
* `APPLICATION[CREATE]` permission to create agent applications
* `APPLICATION[READ]` permission to fetch agent card metadata
* Valid AgentCard JSON hosted at an accessible http or https URL (if using AgentCard feature)

### Gateway Configuration

#### Application Advanced Settings

| Property | Description | Example |
|:---------|:------------|:--------|
| `settings.advanced.agentCardUrl` | Optional URL to the agent's AgentCard JSON. Must use http or https scheme. | `https://agent.example.com/.well-known/agent-card.json` |

#### Default OAuth Settings for Agent Applications

| Property | Description | Default Value |
|:---------|:------------|:--------------|
| `grantTypes` | Allowed OAuth grant types | `["authorization_code"]` |
| `responseTypes` | Allowed OAuth response types | `["code"]` |
| `tokenEndpointAuthMethod` | Client authentication method | `client_secret_basic` |
| `clientType` | OAuth client confidentiality | `CONFIDENTIAL` |
| `applicationType` | OAuth application type | `agent` |

### Creating an Agent Application

Create an agent application through the Management API by setting `type: "AGENT"` in the application payload.

1. Submit a POST request to `/organizations/{orgId}/environments/{envId}/domains/{domain}/applications` with the agent type specified.
2. The system validates the request and strips any forbidden grant types (`implicit`, `password`, `refresh_token`) from the configuration.
3. If no valid grants remain after filtering, the system defaults to `authorization_code` grant with `code` response type.
4. Optionally include `settings.advanced.agentCardUrl` pointing to your hosted AgentCard JSON.
5. The system validates the URL scheme (must be http or https) and returns the created application with sanitized OAuth settings.

### Registering an Agent via Dynamic Client Registration

Register an agent application through the DCR endpoint by setting `application_type: "agent"` in the registration payload.

1. Submit a POST request to the DCR endpoint with `application_type: "agent"` and desired OAuth settings.
2. The system validates the request through the standard DCR chain, then applies agent-specific constraints.
3. Forbidden grant types and response types are automatically removed.
4. If `token_endpoint_auth_method` is not specified, the system defaults to `client_secret_basic`.
5. If no valid grants remain, the system assigns `authorization_code` grant and `code` response type.
6. The validated client credentials are returned with sanitized settings.

### Fetching Agent Card Metadata

Retrieve an agent's AgentCard JSON through the gateway proxy endpoint at `/organizations/{orgId}/environments/{envId}/domains/{domain}/applications/{appId}/agent-card`.

1. Ensure the application has `agentCardUrl` configured in advanced settings.
2. Send a GET request to the agent-card endpoint with `APPLICATION[READ]` permission.
3. The gateway fetches the JSON from the configured URL with a 5-second timeout and 512 KB size limit.
4. SSRF protection blocks requests to localhost, private IP ranges (10.0.0.0/8, 172.16.0.0/12, 192.168.0.0/16, 169.254.0.0/16), and non-http(s) schemes.
5. The response is validated as JSON and proxied to the client with a 200 status, or an error is returned if validation fails.

### Restrictions

* Agent applications cannot use `implicit`, `password`, or `refresh_token` grant types
* Agent applications cannot use response types `token`, `id_token`, or `id_token token`
* AgentCard URLs must use http or https schemes only
* AgentCard responses are limited to 512 KB maximum size
* AgentCard fetch timeout is 5 seconds
* SSRF protection blocks localhost and private IP ranges (10.0.0.0/8, 172.16.0.0/12, 192.168.0.0/16, 169.254.0.0/16)
* AgentCard responses must return HTTP 200 status and valid JSON
* Token endpoint authentication method `none` is disabled for agent applications in the UI
* Agent application type requires Gravitee Access Management 4.11.0 or later
