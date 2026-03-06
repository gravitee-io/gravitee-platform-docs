### Overview

Protected Resources now support secret management, certificate binding, membership control, and search capabilities. These enhancements enable Protected Resources to participate in token introspection workflows and token exchange scenarios, particularly for MCP Server integrations. Administrators can manage multiple secrets per resource, assign certificates for mTLS authentication, and control access through role-based memberships.

### Key Concepts

#### Protected Resource Secrets

Protected Resources maintain a list of client secrets for authentication. Each secret has a unique ID, optional name, expiration date, and associated settings. At least one secret must exist at all times. Secrets can be created, renewed (generating a new value while preserving metadata), or deleted. The system automatically generates secure random values and tracks expiration for notification purposes.

#### Certificate Binding

Protected Resources can reference a certificate for mTLS authentication scenarios. The certificate field stores a certificate ID that must exist in the domain's certificate store. Certificate deletion is blocked if any Protected Resource references it, preventing broken authentication configurations.

#### Membership and Permissions

Protected Resources support role-based access control through memberships. Members can be users or groups assigned specific roles. Permissions cascade from organization → environment → domain → resource levels. Four permission types control access: LIST (view members), CREATE (add/update members), DELETE (remove members), and READ (view permissions).

### Prerequisites for Secret Management

* Domain with OAuth 2.0 enabled
* User or group identities configured in the domain

### Prerequisites for Certificate Binding

* Valid certificate uploaded to the domain certificate store

### Prerequisites for Membership Management

See [Prerequisites for Membership Management](#prerequisites-for-membership-management) above for details.
### Prerequisites for Token Introspection

* Applications or Protected Resources configured as token issuers

### Gateway Configuration

No gateway-level configuration is required for these features.

### Creating Protected Resource Secrets

To create a secret, send a POST request to `/organizations/{orgId}/environments/{envId}/domains/{domainId}/protected-resources/{resourceId}/secrets` with a JSON body containing the secret name:

```json
{
  "name": "production-secret"
}
```

The system generates a secure random secret value, creates associated settings, and returns a `ClientSecret` object containing the ID, name, plaintext secret (visible only on creation), settings ID, expiration date, and creation timestamp. The secret is immediately available for authentication.

To renew an existing secret, POST to `/secrets/{secretId}/_renew`. This generates a new secret value and updates the expiration date while preserving the settings ID.

To delete a secret, send DELETE to `/secrets/{secretId}`. Note that at least one secret must exist at all times. Attempting to delete the last secret returns an error.
