### Fetching AgentCard Metadata

Administrators with `APPLICATION[READ]` permission can fetch the AgentCard JSON for an agent application by sending a GET request to:

```
/organizations/{organizationId}/environments/{environmentId}/domains/{domain}/applications/{application}/agent-card
```

The endpoint proxies the AgentCard JSON from the application's configured `agentCardUrl`. The system enforces the following constraints:

| Constraint | Value | Error Condition |
|:-----------|:------|:----------------|
| Max body size | 512 KB | `"Agent card response exceeds maximum allowed size"` |
| Timeout | 5000 ms | Upstream timeout error |
| SSRF protection: localhost | Blocked | `"SSRF protection: localhost target is not allowed"` |
| SSRF protection: private IPs | Blocked (10.x.x.x, 172.16-31.x.x, 192.168.x.x, 169.254.x.x) | `"SSRF protection: private IP target is not allowed"` |

The endpoint returns:

- **200**: Agent card JSON successfully fetched
- **400**: No `agentCardUrl` configured or invalid URL
- **404**: Application not found
- **500**: Internal server error or upstream failure

If the upstream URL returns a non-200 status, the system returns an error: `"Agent card URL returned status {code}"`. If the response is not valid JSON, the system returns: `"Agent card response is not valid JSON"`.
