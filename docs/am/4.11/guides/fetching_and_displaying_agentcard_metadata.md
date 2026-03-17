### Fetching AgentCard Metadata

Administrators with `APPLICATION[READ]` permission can fetch an agent's AgentCard metadata via the Management API endpoint:

```
GET /organizations/{organizationId}/environments/{environmentId}/domains/{domain}/applications/{application}/agent-card
```

#### Request Flow

1. The endpoint retrieves the `agentCardUrl` from the application's advanced settings.
2. Access Management fetches the JSON document from the URL, enforcing SSRF protection (blocking localhost and private IP ranges) and a 512 KB size limit.
3. The response proxies the AgentCard JSON to the client.
4. If the URL is missing, malformed, or returns a non-200 status, the endpoint returns a 400 or 500 error.

#### Error Conditions

| Condition | Error Message |
|:----------|:--------------|
| Missing or malformed URL | `agent_card_url : {url} is malformed` |
| Response exceeds 512 KB | `Agent card response exceeds maximum allowed size` |
| SSRF violation (localhost or private IP) | `SSRF protection: localhost target is not allowed` or `SSRF protection: private IP target is not allowed` |
| Non-200 HTTP status | `Agent card URL returned status {code}` |
| Invalid JSON | `Agent card response is not valid JSON` |

#### UI Display

The UI displays the fetched AgentCard in a dedicated "Agent Metadata" tab within application settings. The tab includes parsed views for Capabilities, Tools, Prompts, and Raw JSON.
