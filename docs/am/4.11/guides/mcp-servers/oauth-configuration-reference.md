### Default OAuth Settings

When creating or updating a Protected Resource without explicit OAuth settings, the system applies these defaults:

| Property | Default Value | Description |
|:---------|:--------------|:------------|
| `grantTypes` | `["client_credentials"]` | Allowed OAuth grant types |
| `responseTypes` | `["code"]` | Allowed OAuth response types |
| `tokenEndpointAuthMethod` | `"client_secret_basic"` | Default authentication method for token endpoint |
| `clientId` | Resource's `clientId` | OAuth client identifier |

The `clientSecret` field is preserved from the existing resource if available.

### MCP Server Token Endpoint Restrictions

For Protected Resources of type MCP Server, only these token endpoint authentication methods are available:

| Method | Description |
|:-------|:------------|
| `client_secret_basic` | HTTP Basic authentication with client credentials |
| `client_secret_post` | Client credentials in POST body |
| `client_secret_jwt` | JWT signed with client secret |

Methods excluded for MCP Servers: `private_key_jwt`, `tls_client_auth`, `self_signed_tls_client_auth`, `none`.

The UI enforces these restrictions by filtering the available options in the Grant Flows component. MCP Server resources are limited to `client_credentials` and `urn:ietf:params:oauth:grant-type:token-exchange` grant types.

