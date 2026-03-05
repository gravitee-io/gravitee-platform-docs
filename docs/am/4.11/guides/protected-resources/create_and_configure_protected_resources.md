### Creating a Protected Resource

Create a Protected Resource by submitting a `NewProtectedResource` payload to the domain's protected resources endpoint:

Include `settings` in the request body to configure OAuth parameters. The system applies default OAuth settings during creation:

| Field | Default Value |
|:------|:--------------|
| `grantTypes` | `["client_credentials"]` |
| `responseTypes` | `["code"]` |
| `tokenEndpointAuthMethod` | `"client_secret_basic"` |

The system generates a default client secret and returns it in the response. The response includes a `ClientSecret` object with the following fields:

### Managing Secrets

#### Creating Additional Secrets

Create additional secrets for a Protected Resource:

**Request body:**

The system generates a secure random secret value and returns a `ClientSecret` object.

#### Renewing Secrets

Renew an existing secret to generate a new value and update the expiration date:

The system preserves the `settingsId` and returns the updated `ClientSecret` object with the new secret value.

#### Deleting Secrets

Delete a secret:

At least one secret must exist. Attempting to delete the last secret returns the error `"Cannot delete the last client secret"`.

### Binding a Certificate

Protected Resources support certificate-based authentication for mutual TLS scenarios.

1. Upload a certificate to the domain using the certificate management API.

    Reference the certificate ID in the Protected Resource's `certificate` field during creation or update.

The system validates certificate availability. Attempting to delete a certificate referenced by any Protected Resource returns the error `"You can't delete a certificate with existing protected resources."`

Certificate binding is stored in the `protected_resources.certificate` column (nullable, nvarchar(64)).
