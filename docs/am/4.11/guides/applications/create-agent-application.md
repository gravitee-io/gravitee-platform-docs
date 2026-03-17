### Overview

The Agent application type is a new OAuth client category designed for agentic applications such as AI assistants and autonomous agents. Agent applications enforce stricter grant type constraints than traditional OAuth clients and support optional AgentCard metadata import via the A2A specification. This feature enables administrators to register, manage, and audit agent identities as first-class entities within Access Management.

### Key Concepts

#### Agent Application Type

Agent applications are OAuth clients with restricted grant types to align with agentic use cases. They default to confidential client type and support only `authorization_code` and `client_credentials` flows. The `implicit`, `password`, and `refresh_token` grants are forbidden. 

#### AgentCard Metadata

AgentCard is an optional JSON document hosted at a URL specified in the application's `agentCardUrl` property. The AgentCard follows the A2A specification and describes the agent's capabilities, tools, and prompts. Access Management fetches and proxies this metadata through a dedicated endpoint, enforcing SSRF protection and size limits (512 KB maximum). The UI displays parsed AgentCard data in tabs for Capabilities, Tools, Prompts, and Raw JSON.

#### Grant Type Enforcement

Agent applications are restricted to `authorization_code` and `client_credentials` grant types. The system strips forbidden grant types (`implicit`, `password`, `refresh_token`) during application creation, Dynamic Client Registration (DCR), and token endpoint requests. If all grant types are removed, the system defaults to `authorization_code` with response type `code`.

### Prerequisites

* Access Management domain with OAuth 2.0 enabled
* User with `APPLICATION[CREATE]` and `APPLICATION[READ]` permissions
* (Optional) Publicly accessible AgentCard URL using `http` or `https` scheme

### Gateway Configuration

#### Application Type

| Property | Description | Example |
|:---------|:------------|:--------|
| `type` | Application type enum value | `AGENT` |
| `agentCardUrl` | Optional URL to the agent's AgentCard JSON document. Must use `http` or `https` scheme. | `https://example.com/.well-known/agent-card.json` |

#### Default OAuth Settings

| Property | Description | Default |
|:---------|:------------|:--------|
| `grantTypes` | Allowed OAuth grant types | `["authorization_code"]` |
| `responseTypes` | Allowed OAuth response types | `["code"]` |
| `tokenEndpointAuthMethod` | Token endpoint authentication method | `client_secret_basic` |
| `clientType` | OAuth client type | `CONFIDENTIAL` |

#### AgentCard Fetch Configuration

| Property | Description | Value |
|:---------|:------------|:------|
| Max body size | Maximum allowed AgentCard response size | 512 KB |
| Timeout | HTTP request timeout for fetching AgentCard | 5000 ms |
| SSRF protection | Blocked targets | localhost, 10.x.x.x, 172.16-31.x.x, 192.168.x.x, 169.254.x.x |

### Creating an Agent Application

1. Navigate to the **Applications** section in the Access Management console, and then click the **plus icon**.
2. Choose "Agentic Application" as the application type.
3. Provide a name and optional description.
4. (Optional) Enter an AgentCard URL in the "Advanced Settings" section. The URL must use `http` or `https` scheme and point to a valid JSON document.
5. Configure redirect URIs and other OAuth settings as needed. The system automatically sets the client type to confidential and restricts grant types to `authorization_code` and `client_credentials`.
6. Save the application to generate client credentials.

### Creating an Agent via Dynamic Client Registration

To register an agent application via DCR, send a POST request to the DCR endpoint with `application_type` set to `agent`. The system automatically strips forbidden grant types and response types, defaulting to `authorization_code` and `code` if no valid types remain.

**Example DCR Request:**

```json
{
  "application_type": "agent",
  "grant_types": ["authorization_code", "client_credentials"],
  "response_types": ["code"],
  "redirect_uris": ["https://example.com/callback"]
}
```
