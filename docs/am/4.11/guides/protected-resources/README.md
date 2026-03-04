### Managing Protected Resource Credentials

Protected Resources support multiple client secrets with expiration policies. Each secret is generated securely and can be renewed or deleted independently. Secrets follow domain-level expiration settings and trigger notifications before expiry.

#### Prerequisites

* Domain with OAuth 2.0 enabled
* For certificate-based authentication: Valid X.509 certificate uploaded to the domain

#### Creating a Secret

1. Send a POST request to `/organizations/{organizationId}/environments/{environmentId}/domains/{domain}/protected-resources/{protected-resource}/secrets` with a `name` field in the request body.
2. Store the plaintext `secret` value from the response securely. Subsequent GET requests return only metadata without the secret value.

#### Renewing a Secret

1. Send a POST request to `/secrets/{secretId}/_renew`.
2. The system deletes the old secret value and generates a new one with the same settings. This operation cannot be reversed.

#### Deleting a Secret

1. Send a DELETE request to `/secrets/{secretId}`.
2. The system removes the secret. If no other secrets reference the same `settingsId`, the associated settings entry is also removed.

#### Configuring Secret Expiration

Configure domain-level settings to apply expiration policies to Protected Resource secrets.

| Property | Description | Example |
|:---------|:------------|:--------|
| `enabled` | Enable automatic secret expiration | `true` |
| `expiryDuration` | Duration before secrets expire | `90d` |

## Overview

Protected Resources now support secret management, certificate-based authentication, and membership controls. These enhancements enable secure server-to-server communication patterns and allow Protected Resources to act as OAuth clients in token introspection and token exchange flows.

Key capabilities include:

* **Secret management**: Full lifecycle management for client credentials
* **Certificate-based authentication**: Support for mutual TLS (mTLS) authentication
* **Membership controls**: Granular permissions for Protected Resource access

#### Secret Settings Schema

Each secret references a settings entry with algorithm metadata.

| Property | Description | Example |
|:---------|:------------|:--------|
| `id` | Settings identifier | `"settings-uuid"` |
| `algorithm` | Hashing algorithm | `"SHA-256"` |

#### Assigning Certificates for JWT Authentication

1. Upload a valid X.509 certificate to the domain.
2. Include the `certificate` field with the certificate ID when creating or updating a Protected Resource via POST or PATCH to `/organizations/{organizationId}/environments/{environmentId}/domains/{domain}/protected-resources`.
3. The system validates the certificate ID before assignment. Certificate deletion is blocked if any Protected Resource references it, returning HTTP 400 with the error `"You can't delete a certificate with existing protected resources."`

---

### Token Introspection with Protected Resources

When introspecting a token, the system validates the `aud` (audience) claim against both Application client IDs and Protected Resource client IDs.

#### Single-Audience Validation

1. The system checks if the audience matches an Application client ID.
2. If no match is found, the system checks if the audience matches a Protected Resource client ID.
3. If no match is found, the system falls back to resource identifier validation per RFC 8707.

#### Multi-Audience Validation

The system always validates via resource identifiers (RFC 8707), not client ID matching.

#### Certificate-Based Signature Verification

* If the Protected Resource has a certificate assigned, the system uses it for JWT signature verification.
* If the certificate is `null`, the system assumes HMAC signing.

#### Introspection Response

The introspection response includes `client_id` and `aud` matching the Protected Resource's `clientId`.

---

### Protected Resource OAuth Settings Reference

Protected Resources automatically receive default OAuth settings on creation and update.

| Property | Description | Default |
|:---------|:------------|:--------|
| `grantTypes` | Allowed grant types | `["client_credentials"]` |
| `responseTypes` | Allowed response types | `["code"]` |
| `tokenEndpointAuthMethod` | Client authentication method | `"client_secret_basic"` |
| `clientId` | OAuth client identifier | Copied from `clientId` field |
| `clientSecret` | OAuth client secret | Preserved from existing resource on update |

---

### Managing Protected Resource Membership and Permissions

Administrators can grant and revoke administrative permissions on Protected Resources by managing member assignments.

#### Prerequisites

* User or group identities in the domain

#### Adding a Member

1. Send a POST request to `/organizations/{organizationId}/environments/{environmentId}/domains/{domain}/protected-resources/{protected-resource}/members` with `memberId`, `memberType` (e.g., `"USER"`), and `role` in the request body.

#### Listing Members

1. Send a GET request to `/members`.
2. The response includes an array of membership objects with `memberId`, `memberType`, `referenceId`, `referenceType`, and `role` fields.

#### Checking Permissions

1. Send a GET request to `/permissions`.
2. The response includes a flattened array of permission strings for the authenticated user.

#### Removing a Member

1. Send a DELETE request to `/members/{member}`.
2. The system returns HTTP 204 on success.

---

### Token Exchange with Protected Resources

Protected Resources can participate in OAuth 2.0 Token Exchange flows (RFC 8693) as clients, exchanging subject tokens for new access tokens scoped to their identity.

#### Prerequisites

* Domain-level token exchange settings configured with allowed subject token types

#### Configuring Token Exchange Settings

Configure domain-level settings to restrict allowed subject token types.

| Property | Description | Example |
|:---------|:------------|:--------|
| `allowedSubjectTokenTypes` | Array of permitted token type URNs | `["urn:ietf:params:oauth:token-type:id_token"]` |

Default allowed types if not restricted: `access_token`, `refresh_token`, `id_token`, `jwt`.

#### Exchanging a Token

1. Obtain a subject token from an Application using a standard grant (e.g., `password` grant).
2. Authenticate as the Protected Resource using `client_secret_basic`, `client_secret_post`, or `client_secret_jwt`.
3. Send a POST request to `/oauth/token` with `grant_type=urn:ietf:params:oauth:grant-type:token-exchange`, `subject_token=<TOKEN>`, and `subject_token_type=<TYPE_URN>`.
4. The response includes an `access_token` with `client_id` and `aud` set to the Protected Resource's `clientId`, `expires_in` capped at the subject token's remaining lifetime, and the `gis` claim preserved from the subject token.

#### Restrictions

* Exchanged tokens never include `refresh_token` or `id_token`.
* Exchanged token `expires_in` cannot exceed the subject token's remaining lifetime.
* If `allowedSubjectTokenTypes` is restricted and the subject token type is not allowed, the request returns HTTP 400 with `invalid_request`.
* Protected Resources in MCP Server context are limited to `client_credentials` and token exchange grant types.
* Token endpoint authentication methods for MCP Server context are restricted to `client_secret_basic`, `client_secret_post`, and `client_secret_jwt`.

---

### Searching Protected Resources

Administrators can search for Protected Resources by name or client ID using wildcard queries.

#### Searching by Name or Client ID

1. Send a GET request to `/organizations/{organizationId}/environments/{environmentId}/domains/{domain}/protected-resources` with the `q` query parameter.
2. Use `*` to match zero or more characters (e.g., `client*` matches `clientId123` and `client-test`).
3. Searches are case-insensitive and return paginated results with total count metadata.
4. If `q` is omitted, the endpoint falls back to type-based filtering.

#### Example Queries

* `q=client*` matches Protected Resources with names or client IDs starting with "client"
* `q=*test` matches Protected Resources with names or client IDs ending with "test"
* `q=*server*` matches Protected Resources with names or client IDs containing "server"

