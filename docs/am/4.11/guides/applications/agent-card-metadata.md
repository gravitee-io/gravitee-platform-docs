
### Fetching agent card metadata


Retrieve agent card metadata via the proxy endpoint.

1. Send a `GET` request to `/organizations/{orgId}/environments/{envId}/domains/{domain}/applications/{appId}/agent-card` with `APPLICATION[READ]` permission.
2. The platform fetches the JSON document from the configured `agentCardUrl`, enforcing SSRF protections:
   * Rejects localhost targets
   * Rejects private IP addresses (10.x.x.x, 192.168.x.x, 172.16-31.x.x, 169.254.x.x)
   * Rejects non-HTTP(S) schemes
3. The response must be valid JSON under 512 KB and return HTTP 200.
4. On success, the platform returns the agent card JSON.

#### Error Responses

| Status Code | Condition | Description |
|:------------|:----------|:------------|
| `400` | No URL configured | The application does not have an `agentCardUrl` configured |
| `400` | Invalid URL | The configured URL is malformed (error message format: `agent_card_url : {url} is malformed`) |
| `404` | Application not found | The specified application does not exist |
| `500` | Upstream failure | The upstream server returned a non-200 status code |
| `500` | Oversized response | The agent card response exceeds 512 KB |
| `500` | Invalid JSON | The agent card response is not valid JSON |

{% hint style="info" %}
AgentCard URLs must use HTTP or HTTPS schemes only. Other schemes are rejected during validation.
{% endhint %}
