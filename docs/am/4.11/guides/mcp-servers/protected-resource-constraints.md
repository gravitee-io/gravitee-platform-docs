### Restrictions and Validation Rules

#### Grant Type Restrictions

MCP Servers support only the following grant types:

* `client_credentials`
* `urn:ietf:params:oauth:grant-type:token-exchange`

All other grant types (`authorization_code`, `password`, `implicit`, `refresh_token`) are excluded from MCP Server configuration.

#### Authentication Method Restrictions

MCP Servers support the following token endpoint authentication methods:

* `client_secret_basic`
* `client_secret_post`
* `client_secret_jwt`

The following authentication methods are excluded:

* `private_key_jwt`
* `tls_client_auth`
* `self_signed_tls_client_auth`
* `none`

#### Resource Identifier Constraints

The `resourceIdentifiers` field is subject to the following constraints:

* Must not be empty
* All `resourceIdentifiers` within a domain must be unique across Protected Resources

Attempting to create or update a Protected Resource with empty or duplicate resource identifiers results in an `InvalidProtectedResourceException`.

#### Feature Key Uniqueness

All feature keys within a Protected Resource must be unique. Duplicate feature keys result in an `InvalidProtectedResourceException` with the message "Feature keys must be unique within a protected resource."

#### Certificate Deletion Constraint

Certificates referenced by Protected Resources cannot be deleted until the reference is removed. Attempting to delete a referenced certificate results in a `CertificateWithProtectedResourceException` with HTTP status 400 and the message "You can't delete a certificate with existing protected resources."

#### Token Exchange Requirements

Token exchange requires domain-level configuration:

* `tokenExchangeSettings.enabled` must be set to `true`
* If `allowedSubjectTokenTypes` is configured, only the listed token types are accepted in token exchange requests

Requests with disallowed subject token types are rejected with error `invalid_request` and description "subject_token_type not allowed."

#### Secret Value Retrieval

Secret values are returned only during creation or renewal. After creation or renewal, secret values cannot be retrieved and are redacted in API responses.

#### Token Introspection with Multiple Audiences

When a token contains multiple audiences, token introspection always validates via RFC 8707 resource identifiers. Single-audience tokens follow a fallback sequence: client ID lookup, Protected Resource client ID lookup, and finally RFC 8707 resource identifier validation.
