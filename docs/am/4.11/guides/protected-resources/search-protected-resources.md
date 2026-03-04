### Searching Protected Resources

Search for Protected Resources by client ID or name using the following endpoint:

```
GET /organizations/{orgId}/environments/{envId}/domains/{domain}/protected-resources?q={query}
```

The `q` parameter supports exact matches and wildcard prefixes. For example:

* `clientId` — Case-insensitive exact match
* `clientId*` — Case-insensitive prefix match

Searches match against both `client_id` and `name` fields. Multiple consecutive wildcards are compacted to a single wildcard (e.g., `client**Id` becomes `client*Id`).

{% hint style="warning" %}
Only prefix wildcards are supported. Infix or suffix wildcards (e.g., `*clientId` or `client*Id*`) are not supported.
{% endhint %}

#### Pagination

Control result pagination with the following query parameters:

| Parameter | Type | Description |
|:----------|:-----|:------------|
| `page` | Integer | Page number (zero-indexed) |
| `size` | Integer | Number of results per page |

The response returns `Page<ProtectedResourcePrimaryData>` with a `totalCount` field indicating the total number of matching resources.

#### Implementation Details

* **SQL**: Uses `LIKE` with `%` wildcards for pattern matching
* **MongoDB**: Uses regex with case-insensitive matching (`/^pattern.*/i`)

## Token Introspection Configuration

Token introspection validates the `aud` (audience) claim against Applications and Protected Resources. The validation process follows a specific sequence and applies different rules depending on the token type.

### Validation Process

The system validates audience claims using the following logic:

1. **Single-audience tokens**: The system checks for matching clients in this order:
   * `ClientSyncService` for Application clients
   * `ProtectedResourceSyncService` for Protected Resource clients
   * `ProtectedResourceManager` for RFC 8707 resource identifiers

2. **Multi-audience tokens**: All audiences are validated using RFC 8707 standards.

3. **Certificate verification**: The certificate ID from the matched client or resource is used for JWT signature verification.

4. **Verification modes**:
   * **Offline verification**: Decodes the JWT and validates the audience claim
   * **Online verification**: Performs offline verification plus additional checks for token existence and expiration in the repository

### Error Handling

Token introspection returns the following errors when validation fails:

* **Missing audience claim**: `Token has no audience claim`
* **Unmatched audience**: `Client or resource not found: {aud}`

{% hint style="info" %}
Tokens must include a valid `aud` claim that matches a registered Application or Protected Resource for introspection to succeed.
{% endhint %}

## Configuring Certificate-Based Authentication

To assign a certificate to a Protected Resource, set the `certificate` field to a valid certificate ID during creation or update.

### Certificate Validation Process

1. The system validates that the certificate exists in the domain via `CertificateService`.
2. If the certificate is not found, the request fails with `CertificateNotFoundException`.
3. During token introspection, the certificate ID is extracted from the Protected Resource and used to verify JWT signatures.

### Certificate Deletion Restrictions

Certificates in use by Protected Resources cannot be deleted. Deletion attempts return `CertificateWithProtectedResourceException` with the message:

```
You can't delete a certificate with existing protected resources.
```

{% hint style="warning" %}
Ensure the certificate is no longer assigned to any Protected Resources before attempting deletion.
{% endhint %}
