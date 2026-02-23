## Multi-tenant endpoint selection

Multi-tenant endpoint selection enables a single Native Kafka API definition to serve multiple backend Kafka clusters. The gateway automatically selects the appropriate endpoint based on its configured tenant identifier. This eliminates the need to maintain separate API definitions for different environments (e.g., internal vs. external, production vs. staging).

### Prerequisites

Before configuring multi-tenant endpoints, ensure you have:

- A Native Kafka API definition with at least one endpoint group
- Gateway version that supports the `tenant` configuration property
- Understanding of your deployment topology (which gateways connect to which Kafka clusters)

### Tenant-based endpoint filtering

Each endpoint in a Native Kafka API can be tagged with one or more tenant identifiers. When a gateway is configured with a tenant, it filters endpoints to match that tenant. If no tenant is configured on the gateway, all endpoints remain eligible for selection. This allows the same API definition to be deployed across multiple gateways that connect to different Kafka clusters.

### Endpoint matching rules

The gateway applies a permissive matching algorithm. An endpoint matches if:

1. The gateway has no tenant configured, or
2. The endpoint has no tenants assigned, or
3. The gateway's tenant appears in the endpoint's tenant list

Within an endpoint group, the first matching endpoint is selected—there is no load balancing across tenant-matched endpoints.

### Optional tenant configuration

Tenant filtering is entirely optional. Existing API definitions without tenant assignments continue to work unchanged. Tenants are assigned at the endpoint level, not the endpoint group level, allowing fine-grained control over which backends serve which gateways.

### Configure the gateway tenant property

The `tenant` property is a gateway-level identifier used to filter endpoints in Native Kafka APIs. When configured, the gateway selects only endpoints tagged with a matching tenant identifier. If the property is unset, all endpoints remain eligible for selection.

| Property | Description | Example | Configuration file (`gravitee.yml`) | Environment variable |
|:---------|:------------|:--------|:-------------------------------------|:---------------------|
| `tenant` | Gateway-level tenant identifier used to filter endpoints. If unset, all endpoints are eligible. | `tenant-a` | `tenant: tenant-a` | `GRAVITEE_TENANT=tenant-a` |

**Configuration file** (`gravitee.yml`):

```yaml
tenant: tenant-a
```

**Environment variable**:

```bash
GRAVITEE_TENANT=tenant-a
```

**Behavior**:

- **Endpoint Matching**: The gateway evaluates each endpoint's `tenants` array. An endpoint matches if the gateway's tenant appears in the array, or if the endpoint has no tenants assigned.
- **No Tenant Configured**: If the gateway has no tenant configured, all endpoints are eligible for selection.
- **Case Sensitivity**: Tenant identifiers are case-sensitive and must match exactly between the gateway configuration and the endpoint definition.
- **Native Kafka APIs Only**: Tenant filtering applies exclusively to Native Kafka APIs. <!-- GAP: Confirm whether this applies to other native protocols (e.g., MQTT, AMQP) -->

### Assign tenants to endpoints

Add tenant identifiers to endpoint definitions in your API configuration:

1. Open the API definition in the console or export it as JSON
2. Locate the `endpointGroups` array and find the endpoint to configure
3. Add a `tenants` field containing an array of tenant identifiers (e.g., `["internal", "external"]`)
4. Save and redeploy the API

Endpoints without a `tenants` field or with an empty array match all gateways.

**Example endpoint configuration**:

```json
{
  "endpointGroups": [
    {
      "endpoints": [
        {
          "name": "internal-endpoint",
          "tenants": ["internal"],
          "configuration": "{ \"bootstrapServers\": \"localhost:9093\" }"
        },
        {
          "name": "external-endpoint",
          "tenants": ["external"],
          "configuration": "{ \"bootstrapServers\": \"localhost:9094\" }"
        }
      ]
    }
  ]
}
```

### View tenant assignments

The endpoint groups table in the API console displays a **Tenants** column when at least one endpoint in the group has tenants configured. The column shows tenant names as a comma-separated list (e.g., "internal, external"). If no endpoints in the group have tenants, the column is hidden.

### Error handling

When no endpoint matches the gateway's tenant, the `KafkaEndpointManager` throws a `KafkaNoApiEndpointFoundException`. The exception message format depends on the gateway's tenant configuration:

- **Gateway with tenant configured**: `No endpoint found for tenant: <tenant-id>`
- **Gateway without tenant configured**: `No endpoint found for api`

The error is logged at **WARN** level rather than ERROR. This reduces log noise in multi-tenant environments where endpoint mismatches may occur during configuration changes or planned maintenance windows.

**Example log output** (gateway with tenant `tenant-a`):
```
WARN  i.g.a.k.KafkaEndpointManager - No endpoint found for tenant: tenant-a
```

**Example log output** (gateway without tenant):
```
WARN  i.g.a.k.KafkaEndpointManager - No endpoint found for api
```

The custom exception type (`KafkaNoApiEndpointFoundException`) improves error diagnostics compared to the generic `IllegalStateException` used in earlier versions. This allows monitoring systems and error handlers to distinguish tenant-related endpoint selection failures from other configuration issues.

### Restrictions

- Tenant filtering applies only to Native Kafka APIs <!-- GAP: Confirm whether this applies to other native protocols (e.g., MQTT, AMQP) -->
- Only the first matching endpoint in an endpoint group is selected
- Tenant identifiers are case-sensitive and must match exactly between the gateway configuration and endpoint definition
- The `tenant` property must be set in `gravitee.yml` or as an environment variable; it can't be configured via the console UI <!-- GAP: Confirm whether dynamic tenant configuration via API or console is planned -->
- If an endpoint group contains no matching endpoints, the API invocation fails immediately with a `KafkaNoApiEndpointFoundException`