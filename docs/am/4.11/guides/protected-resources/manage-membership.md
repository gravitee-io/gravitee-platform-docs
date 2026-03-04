### Managing Protected Resource Membership

Control access to Protected Resources by managing membership via the `/organizations/{orgId}/environments/{envId}/domains/{domain}/protected-resources/{resourceId}/members` endpoint.

#### Listing members

Retrieve all members with access to a Protected Resource:

```
GET /organizations/{orgId}/environments/{envId}/domains/{domain}/protected-resources/{resourceId}/members
```

Required permission: `PROTECTED_RESOURCE_MEMBER.LIST`

#### Adding or updating a member

Add a new member or update an existing member's role:

```
POST /organizations/{orgId}/environments/{envId}/domains/{domain}/protected-resources/{resourceId}/members
```

**Request body:**

```json
{
  "memberId": "user-id",
  "memberType": "USER",
  "role": "OWNER"
}
```

| Field | Type | Description |
|:------|:-----|:------------|
| `memberId` | String | User or group ID |
| `memberType` | String | Member type (`USER` or `GROUP`) |
| `role` | String | Role to assign (e.g., `OWNER`) |

Required permission: `PROTECTED_RESOURCE_MEMBER.CREATE`

{% hint style="info" %}
Users or groups must exist in the organization before they can be added as members.
{% endhint %}

#### Removing a member

Remove a member's access to a Protected Resource:

```
DELETE /organizations/{orgId}/environments/{envId}/domains/{domain}/protected-resources/{resourceId}/members/{memberId}
```

Required permission: `PROTECTED_RESOURCE_MEMBER.DELETE`

#### Permission hierarchy

Permissions are checked hierarchically in the following order:

1. Protected Resource level
2. Domain level
3. Environment level
4. Organization level

If a permission is not granted at the Protected Resource level, the system checks the domain, then the environment, and finally the organization.

## Client Configuration

Clients using Protected Resources must configure OAuth 2.0 settings and token exchange parameters.

| Property | Type | Example | Description |
|:---------|:-----|:--------|:------------|
| `grantTypes` | Array | `["client_credentials", "urn:ietf:params:oauth:grant-type:token-exchange"]` | Allowed grant types. MCP Servers are limited to these two grant types. |
| `tokenEndpointAuthMethod` | String | `"client_secret_basic"` | Authentication method. MCP Servers support `client_secret_basic`, `client_secret_post`, and `client_secret_jwt` only. |
| `resourceIdentifiers` | Array | `["https://mcp-server` |   |

{% hint style="info" %}
MCP Servers must use one of the following token endpoint authentication methods: `client_secret_basic`, `client_secret_post`, or `client_secret_jwt`.
{% endhint %}

## Token Introspection Configuration

Token introspection validates the `aud` (audience) claim against Applications and Protected Resources. The validation process follows a specific sequence and applies different rules depending on the token type.

### Validation Process

The system validates audience claims using the following logic:

1. **Single-audience tokens**: The system checks for matching clients in this order:
   * `ClientSyncService` for Application clients
   * `ProtectedResourceSyncService` for Protected Resource clients
   * `ProtectedResourceManager` for RFC 8707 resource identifiers

2. **Multi-audience tokens**: All audiences are validated via RFC 8707.

3. **Certificate verification**: The certificate ID from the matched client or resource is used for JWT signature verification.

4. **Verification modes**:
   * **Offline verification**: Decodes the JWT and validates the audience claim
   * **Online verification**: Decodes the JWT, validates the audience claim, and checks token existence and expiration in the repository

### Error Handling

Token introspection returns the following errors when validation fails:

| Condition | Error Message |
|-----------|---------------|
| Token has no `aud` claim | `Token has no audience claim` |
| Audience does not match any client or resource | `Client or resource not found: {aud}` |

## Configuring Certificate-Based Authentication

To enable certificate-based authentication for a Protected Resource, assign a certificate by setting the `certificate` field to a valid certificate ID during resource creation or update.

### Configuration workflow

1. **Certificate validation**: The system validates that the specified certificate exists in the domain using `CertificateService`.
2. **Error handling**: If the certificate is not found, the request fails with `CertificateNotFoundException`.
3. **Token introspection**: During token introspection, the certificate ID is extracted from the Protected Resource and used to verify JWT signatures.

### Certificate deletion restrictions

Certificates assigned to Protected Resources cannot be deleted. Deletion attempts return `CertificateWithProtectedResourceException` with the following message:

```
You can't delete a certificate with existing protected resources.
```

{% hint style="warning" %}
Ensure the certificate is removed from all Protected Resources before attempting deletion.
{% endhint %}

