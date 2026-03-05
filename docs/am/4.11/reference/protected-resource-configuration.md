### Prerequisites

Before configuring a Protected Resource, ensure the following requirements are met:

* Domain with OAuth 2.0 enabled
* `PROTECTED_RESOURCE[CREATE]` permission to create resources
* `PROTECTED_RESOURCE[UPDATE]` permission to manage secrets and certificates
* Valid certificate uploaded to the domain (if using certificate-based authentication)
* User or group memberships configured (if delegating resource management)

### Default OAuth Settings

When creating or updating a Protected Resource, the system applies default OAuth 2.0 settings if the `settings.oauth` field is null or incomplete:

| Property | Default Value | Description |
|:---------|:--------------|:------------|
| `grantTypes` | `["client_credentials"]` | Default grant types applied to the resource |
| `responseTypes` | `["code"]` | Default response types |
| `tokenEndpointAuthMethod` | `client_secret_basic` | Default authentication method for token endpoint |
| `clientId` | (copied from resource) | Matches the Protected Resource's client ID |
| `clientSecret` | (preserved if exists) | Retained from existing settings during updates |

### Event Configuration

Protected Resource secret lifecycle operations publish events with type `PROTECTED_RESOURCE_SECRET`:

| Action | Event Type | Description |
|:-------|:-----------|:------------|
| `CREATE` | `PROTECTED_RESOURCE_SECRET` | Secret created |
| `RENEW` | `PROTECTED_RESOURCE_SECRET` | Secret renewed (new value generated) |
| `DELETE` | `PROTECTED_RESOURCE_SECRET` | Secret deleted |

### Certificate-Based Authentication

When a JWT's `aud` claim matches a Protected Resource's `clientId`, the introspection service retrieves the associated certificate for signature validation. Certificate deletion is blocked if any Protected Resource references it, returning HTTP 400 with error message `"You can't delete a certificate with existing protected resources."`

### MCP Server Context

Protected Resources with type `MCP_SERVER` have restricted OAuth 2.0 capabilities:

**Allowed Grant Types:**
* `client_credentials`
* `urn:ietf:params:oauth:grant-type:token-exchange`

**Allowed Token Endpoint Authentication Methods:**
* `client_secret_basic`
* `client_secret_post`
* `client_secret_jwt`

**Excluded Methods:**
* `private_key_jwt`
* `tls_client_auth`
* `self_signed_tls_client_auth`
* `none`

The refresh token and PKCE configuration sections are not available for MCP Server resources.
