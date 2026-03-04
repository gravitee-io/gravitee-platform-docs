### Overview

Protected Resources now support secret management, certificate-based authentication, and membership controls. These enhancements enable Protected Resources to participate in token introspection workflows and OAuth 2.0 token exchange flows with the same security capabilities as Applications.

### Prerequisites

Before using these features, ensure the following requirements are met:

* Access Management 4.11.0 or later
* Domain with OAuth 2.0 enabled
* For certificate-based authentication: valid X.509 certificate uploaded to the domain
* For membership management: user or service account with `PROTECTED_RESOURCE_MEMBER` CREATE permission


### Managing Protected Resource Secrets

Protected Resources can manage multiple client secrets with expiration tracking. Each secret is generated securely and can be renewed or deleted independently. Multiple secrets can share the same cryptographic settings, enabling zero-downtime credential rotation.

{% hint style="warning" %}
Secret values are exposed only once at creation or renewal. Subsequent API calls return metadata without the secret value.
{% endhint %}

#### Creating a Secret

1. Send a POST request to `/organizations/{orgId}/environments/{envId}/domains/{domain}/protected-resources/{resourceId}/secrets` with a JSON body containing the secret name:

    ```json
    {
      "name": "production-secret"
    }
    ```

2. The API generates a secure random secret and returns the full secret object including the plaintext secret value:

    ```json
    {
      "id": "string",
      "name": "string",
      "secret": "string",
      "settingsId": "string",
      "expiresAt": "date",
      "createdAt": "date"
    }
    ```

3. Store the secret value immediately—it can't be retrieved later.

#### Listing Secrets

Send a GET request to `/organizations/{orgId}/environments/{envId}/domains/{domain}/protected-resources/{resourceId}/secrets`. The response returns metadata only, without secret values:

```json
[
  {
    "id": "string",
    "name": "string",
    "settingsId": "string",
    "expiresAt": "date",
    "createdAt": "date"
  }
]
```

#### Renewing a Secret

Send a POST request to `/organizations/{orgId}/environments/{envId}/domains/{domain}/protected-resources/{resourceId}/secrets/{secretId}/_renew`. The API deletes the old secret and generates a new one with the same name. The response includes the new secret value.

#### Deleting a Secret

Send a DELETE request to `/organizations/{orgId}/environments/{envId}/domains/{domain}/protected-resources/{resourceId}/secrets/{secretId}`. The API returns HTTP 204 No Content on success.

### Assigning Certificates to Protected Resources

Include the `certificate` field in the Protected Resource JSON payload when creating or updating the resource via the Management API. Set the value to the certificate ID obtained from the domain's certificate store.

The certificate enables mutual TLS authentication for the Protected Resource when acting as a client in token exchange or introspection flows.

#### Removing a Certificate Assignment

To remove a certificate assignment, set the `certificate` field to `null` or omit it in an update request.

{% hint style="danger" %}
Certificates in use by Protected Resources can't be deleted. Attempting deletion returns HTTP 400 with the message "You can't delete a certificate with existing protected resources."
{% endhint %}

### Managing Protected Resource Membership

Protected Resources support role-based access control through membership management. Members (users or service accounts) are assigned roles that grant specific permissions (LIST, CREATE, UPDATE, DELETE) for secrets, settings, and membership operations. Permissions cascade from resource to domain to environment to organization scope.

{% hint style="info" %}
Only the `USER` member type is supported.
{% endhint %}

#### Adding a Member

Send a POST request to `/organizations/{orgId}/environments/{envId}/domains/{domain}/protected-resources/{resourceId}/members` with the following payload:

```json
{
  "memberId": "user-123",
  "memberType": "USER",
  "role": "OWNER"
}
```

The `role` determines granted permissions (e.g., `OWNER`, `READER`).

#### Updating a Member

Send a POST request to the same endpoint with a different role value:

```json
{
  "memberId": "user-123",
  "memberType": "USER",
  "role": "READER"
}
```

#### Retrieving All Members

Send a GET request to `/organizations/{orgId}/environments/{envId}/domains/{domain}/protected-resources/{resourceId}/members`. The response returns an array of membership objects:

```json
{
  "data": [
    {
      "id": "string",
      "memberId": "string",
      "memberType": "USER",
      "referenceId": "string",
      "referenceType": "PROTECTED_RESOURCE",
      "role": "string"
    }
  ]
}
```

#### Querying User Permissions

Send a GET request to `/organizations/{orgId}/environments/{envId}/domains/{domain}/protected-resources/{resourceId}/permissions`. The API returns a flattened array of permission strings after evaluating role assignments across resource, domain, environment, and organization scopes.

### Searching Protected Resources

Use the `q` query parameter on `GET /organizations/{orgId}/environments/{envId}/domains/{domain}/protected-resources` to search by name or client ID. The search is case-insensitive and supports wildcard matching with `*`.

For example, `?q=client*` matches any Protected Resource whose name or client ID starts with "client". Without wildcards, the query performs exact matching. If the `q` parameter is absent, the endpoint falls back to existing type-based filtering behavior.

### Token Introspection Configuration

Token introspection now resolves audiences against both Applications and Protected Resources. When a JWT contains an audience claim, the introspection service first checks for a matching Application client ID, then falls back to Protected Resource client ID lookup.

For multiple audiences, validation follows RFC 8707 resource identifier rules. Certificate resolution returns the certificate ID from the matched client or an empty string for HMAC-signed tokens.

### Client Configuration for MCP Server Context

When configuring a Protected Resource in MCP Server context, the UI restricts available token endpoint authentication methods to `client_secret_basic`, `client_secret_post`, and `client_secret_jwt`. Methods requiring asymmetric keys or TLS client authentication (`private_key_jwt`, `tls_client_auth`, `self_signed_tls_client_auth`, `none`) are hidden.

The allowed grant types are `client_credentials` and `urn:ietf:params:oauth:grant-type:token-exchange`.

{% hint style="info" %}
This filtering applies only in the UI. The API doesn't enforce context-specific restrictions.
{% endhint %}

### Restrictions

* Protected Resource secrets are generated server-side. Custom secret values can't be provided.
* Secret values are returned only at creation or renewal. They can't be retrieved later.
* Certificates assigned to Protected Resources can't be deleted until the assignment is removed.
* Token introspection with multiple audiences always validates via RFC 8707 resource identifiers, not client ID lookup.
* Protected Resources validated by resource identifier in introspection always return an empty certificate ID, even if a certificate is assigned.
* Membership management supports only `USER` member type.
* Search queries without wildcards perform exact case-insensitive matching. Partial matching requires explicit `*` wildcards.
* Token endpoint authentication method filtering for MCP Server context is UI-only. API requests aren't restricted.
