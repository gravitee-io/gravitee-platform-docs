### MCP Server Context Restrictions

Protected Resources with type `MCP_SERVER` are restricted to `client_credentials` and `urn:ietf:params:oauth:grant-type:token-exchange` grant types. Token endpoint authentication methods are limited to `client_secret_basic`, `client_secret_post`, and `client_secret_jwt`. Methods requiring asymmetric keys (`private_key_jwt`, `tls_client_auth`, `self_signed_tls_client_auth`) and `none` are excluded from the UI and validation logic.

### Prerequisites

Before creating or managing Protected Resources, ensure the following:

* Domain with OAuth 2.0 settings configured
* `PROTECTED_RESOURCE[CREATE]` permission to create resources
* `PROTECTED_RESOURCE[UPDATE]` permission to manage secrets and certificates
* Valid domain certificate uploaded (if using certificate-based authentication)
* User or group memberships defined (if assigning roles to Protected Resources)

### Gateway Configuration

#### Default OAuth Settings

When creating or updating a Protected Resource, the following defaults are applied if `settings.oauth` is null or incomplete:

| Property | Default Value | Description |
|:---------|:--------------|:------------|
| `grantTypes` | `["client_credentials"]` | Default grant types for Protected Resources |
| `responseTypes` | `["code"]` | Default response types |
| `tokenEndpointAuthMethod` | `client_secret_basic` | Default authentication method |
| `clientId` | (copied from resource) | Matches the Protected Resource's client ID |
| `clientSecret` | (preserved if exists) | Existing secret is retained during updates |

#### Event Configuration

Protected Resource secret lifecycle events are published to the event bus:

| Event Type | Action | Description |
|:-----------|:-------|:------------|
| `PROTECTED_RESOURCE_SECRET` | `CREATE` | Secret created |
| `PROTECTED_RESOURCE_SECRET` | `RENEW` | Secret renewed (new value generated) |
| `PROTECTED_RESOURCE_SECRET` | `DELETE` | Secret deleted |

### Creating a Protected Resource

To create a Protected Resource, send a POST request to `/organizations/{orgId}/environments/{envId}/domains/{domain}/protected-resources` with a JSON body containing `name`, `clientId`, `type` (e.g., `MCP_SERVER`), and optional `resourceIdentifiers`.

If `settings.oauth` is omitted, the system applies default grant types (`client_credentials`), response types (`code`), and token endpoint auth method (`client_secret_basic`). If a `certificate` field is provided, the system validates that the certificate exists in the domain. The response includes the full resource configuration, including generated `clientId` if not provided.

### Managing Protected Resource Secrets

Secrets are managed via `/organizations/{orgId}/environments/{envId}/domains/{domain}/protected-resources/{resourceId}/secrets`.

