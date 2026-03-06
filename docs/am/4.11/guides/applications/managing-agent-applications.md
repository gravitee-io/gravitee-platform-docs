### Constraint Enforcement Rules

The platform enforces the following constraints on agent applications at creation, update, DCR, and token endpoint operations:

| Constraint | Value | Applied When |
|:-----------|:------|:-------------|
| Forbidden grant types | `implicit`, `password`, `refresh_token` | Application create, update, DCR, token endpoint |
| Forbidden response types | `token`, `id_token`, `id_token token` | Application create, update, DCR |
| Default grant type | `authorization_code` | When all grant types are stripped or none provided |
| Default response type | `code` | When all response types are stripped and `authorization_code` is granted |
| Default auth method | `client_secret_basic` | When no auth method is explicitly set |

### AgentCard Fetch Limits

| Property | Value | Description |
|:---------|:------|:------------|
| Maximum response size | 512 KB | Agent card responses exceeding this size are rejected |
| Request timeout | 5000 ms | HTTP requests to agent card URLs time out after 5 seconds |
