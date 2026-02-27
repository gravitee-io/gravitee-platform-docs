### Agent applications

Agent applications are confidential clients designed for machine-to-machine integrations such as CI/CD pipelines, monitoring agents, and resource management tools. They enforce stricter security controls than standard service applications by restricting OAuth 2.0 flows to secure grant types only.

Agent applications cannot use the following grant types:
- `implicit`
- `password`
- `refresh_token`

They also cannot use these response types:
- `token`
- `id_token`
- `id_token token`

When you create an agent application via the Management API or Dynamic Client Registration (DCR), the system automatically strips forbidden grant types from the request. If no valid grant types remain after stripping, the application defaults to `authorization_code` with response type `code`. The token endpoint authentication method defaults to `client_secret_basic` if not specified.

At runtime, the token endpoint rejects requests from agent applications attempting to use forbidden grant types. The endpoint returns a 400 error with `UnauthorizedClientException`.

### Protected resource secrets

Protected resources can have multiple secrets with independent lifecycles. Each secret follows the same expiration rules as application secrets. This enables zero-downtime secret rotation for agent applications accessing protected resources.

Manage protected resource secrets through dedicated endpoints:
- Create: `POST /protected-resources/{protected-resource}/secrets`
- Rotate: `POST /protected-resources/{protected-resource}/secrets/{secretId}/_renew`
- Delete: `DELETE /protected-resources/{protected-resource}/secrets/{secretId}`
- List: `GET /protected-resources/{protected-resource}/secrets`

### Agent cards

Agent cards are JSON manifests that describe agent capabilities, configuration, and metadata. The agent card endpoint fetches these manifests from a configured URL with SSRF protection.

Configure the agent card URL in `settings.advanced.agentCardUrl` when creating or updating an application. The URL must use HTTP or HTTPS schemes and cannot target localhost or private IP ranges (10.x, 172.16-31.x, 192.168.x, 169.254.x).

Fetch the agent card by calling `GET /domains/{domain}/applications/{application}/agent-card`. The endpoint returns the raw JSON response from the configured URL.

SSRF protection enforces these constraints:
- Blocks localhost and private IP ranges (10.x, 172.16-31.x, 192.168.x, 169.254.x)
- Requires HTTP or HTTPS schemes
- Limits response size to 512 KB
- Validates JSON structure
- Enforces 5-second timeout

If the URL is missing or invalid, the endpoint returns a 400 error. If the upstream service returns a non-200 status, exceeds 512 KB, or returns invalid JSON, the endpoint returns a 500 error.

### Create an agent application

Create an agent application using the Management API or DCR.

**Management API:**
Set `type=AGENT` in your request.

**DCR:**
Set `application_type=agent` in your request.

The system enforces these security constraints automatically:
1. Strips forbidden grant types (`implicit`, `password`, `refresh_token`)
2. Defaults to `authorization_code` with response type `code` if no valid grant types remain
3. Sets token endpoint authentication method to `client_secret_basic` if not specified
4. Marks the application as `CONFIDENTIAL`

Optionally configure `settings.advanced.agentCardUrl` to enable agent card discovery.

### Three-layer enforcement

Agent application constraints are enforced at three architectural layers:

**Token endpoint:**
Rejects forbidden grant types at runtime with `UnauthorizedClientException`.

**DCR flow:**
Strips forbidden grants and response types during registration. Defaults to `authorization_code` if all grants are removed.

**Application template:**
Enforces agent type classification and removes forbidden grants when applying the agent template to existing applications.

This defense-in-depth approach ensures agent applications cannot bypass restrictions through any registration or token request path.

<!-- ASSETS USED (copy/rename exactly):
None
-->

### Agent Card Service

Configuration for the agent card fetch mechanism.

| Property | Value | Description |
|:---------|:------|:------------|
| `MAX_BODY_SIZE` | 524288 bytes (512 KB) | Maximum allowed agent card response size |
| `TIMEOUT_MS` | 5000 ms (5 seconds) | HTTP request timeout for agent card fetch |
| `PRIVATE_IP_PATTERN` | RFC 1918 ranges | Regex blocking 10.x, 172.16-31.x, 192.168.x, 169.254.x |

### Creating an Agent Application

Create an agent application by setting `type=AGENT` in the Management API or `application_type=agent` in a DCR request. The system automatically enforces security constraints:

1. Forbidden grant types (`implicit`, `password`, `refresh_token`) are stripped from the request
2. If no grant types remain, the application defaults to `authorization_code` with response type `code`
3. The token endpoint authentication method defaults to `client_secret_basic` if not specified
4. The application is marked as `CONFIDENTIAL`

Optionally configure `settings.advanced.agentCardUrl` to enable agent card discovery. The application will reject token requests using forbidden grant types at runtime with a 400 error.

### Creating Protected Resource Secrets

Manage protected resource secrets through dedicated endpoints:

- **Create a secret**: Send a `POST` request to `/protected-resources/{protected-resource}/secrets` with a `NewClientSecret` payload (requires `PROTECTED_RESOURCE[CREATE]` permission)
- **Rotate a secret**: Call `POST /protected-resources/{protected-resource}/secrets/{secretId}/_renew` (requires `PROTECTED_RESOURCE[UPDATE]`)
- **Delete a secret**: Use `DELETE /protected-resources/{protected-resource}/secrets/{secretId}` (requires `PROTECTED_RESOURCE[DELETE]`)
- **List all secrets**: Call `GET /protected-resources/{protected-resource}/secrets` (requires `PROTECTED_RESOURCE[LIST]`)

Secrets follow the same expiration rules as application secrets.

### Configuring Agent Cards

Set the `agentCardUrl` field in `settings.advanced` when creating or updating an application. The URL must use HTTP or HTTPS schemes and cannot target localhost or private IP ranges (10.x, 172.16-31.x, 192.168.x, 169.254.x).

Fetch the agent card by calling `GET /domains/{domain}/applications/{application}/agent-card` with `APPLICATION[READ]` permission. The endpoint returns the raw JSON response from the configured URL.

**Error responses:**
- **400**: URL is missing or invalid
- **500**: Upstream service returns a non-200 status, exceeds 512 KB, or returns invalid JSON

### Architecture Notes

#### Three-Layer Enforcement

See [Three-Layer Enforcement](#three-layer-enforcement) above for details.
#### SSRF Protection

The agent card fetch mechanism includes comprehensive SSRF mitigations:

- Validates the URL scheme (HTTP/HTTPS only)
- Blocks localhost targets
- Rejects private IP ranges using a compiled regex pattern matching RFC 1918 addresses (10.x, 172.16-31.x, 192.168.x, 169.254.x)
- Requests timeout after 5 seconds
- Response bodies are limited to 512 KB
- Validates JSON structure before returning the payload

These controls prevent agent card URLs from being used to probe internal infrastructure or exfiltrate data.

#### Protected Resource Secret Lifecycle

Protected resources now support multiple secrets with independent lifecycles, enabling zero-downtime rotation. Each secret is managed through dedicated CRUD endpoints with granular permissions (`PROTECTED_RESOURCE_MEMBER[CREATE]`, `[DELETE]`, `[LIST]`, `[UPDATE]`). Secrets inherit expiration behavior from application secret settings. The renewal endpoint (`/_renew`) generates a new secret value while preserving the secret ID, allowing clients to update credentials without changing configuration references.

### Restrictions

- Agent applications can't use `implicit`, `password`, or `refresh_token` grant types
- Agent applications can't use `token`, `id_token`, or `id_token token` response types
- Agent card URLs must use HTTP or HTTPS schemes (no FTP, file://, etc.)
- Agent card URLs can't target localhost or private IP ranges
- Agent card responses must be valid JSON and can't exceed 512 KB
