# Enable the Automation API

## Gateway configuration

### Enabling the Automation API

The Automation API is disabled by default. Enable it by setting the following properties in `gravitee.yml`:

| Property | Description | Example |
|:---------|:------------|:--------|
| `gravitee.http.api.automation.enabled` | Enables the Automation API HTTP endpoint | `true` |
| `gravitee.http.api.automation.entrypoint` | Base path for Automation API endpoints | `/management/automation` |

When the Automation API is enabled, the OpenAPI specification is served at the configured entrypoint.

### Helm Chart Configuration

For Helm deployments, add the following to your `values.yaml`:

```yaml
api:
  http:
    api:
      automation:
        enabled: true
        entrypoint: /management/automation  # optional, defaults to /management/automation
```

### Authentication Timeout

Configure the timeout for repository lookups during bearer token authentication:

| Property | Description | Example |
|:---------|:------------|:--------|
| `http.blockingGet.timeoutMillis` | Timeout in milliseconds for blocking repository lookups during authentication; set to `0` to disable | `120000` |

If a lookup exceeds this timeout, the security context is cleared and the request continues unauthenticated. Spring Security returns 401.
