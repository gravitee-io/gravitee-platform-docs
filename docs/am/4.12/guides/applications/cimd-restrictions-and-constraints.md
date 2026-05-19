# CIMD Restrictions and Constraints

## Restrictions

CIMD clients are subject to the following restrictions:

- **Authentication methods**: CIMD clients cannot use secret-based authentication methods (`client_secret_basic`, `client_secret_post`, `client_secret_jwt`).
- **Redirect URI matching**: CIMD clients require exact `redirect_uri` matching (no prefix matching), regardless of the domain `redirectUriStrictMatching` setting.
- **Default authentication method**: CIMD clients default to `token_endpoint_auth_method=none`. This value overrides the template application's setting.
- **Metadata caching**: CIMD metadata documents are cached. Changes to remote metadata may not be reflected immediately until the cache TTL expires.
- **Logo fetch size limit**: Logo fetch is limited to 256 KB.
- **Wildcard domain matching**: Wildcard domain matching supports only first-level subdomains. For example, `*.example.com` matches `app.example.com` but not `api.app.example.com`.
- **Template inheritance**: CIMD clients inherit the template's `authorizedGrantTypes`, `responseTypes`, and `scopeSettings` via intersection. Metadata cannot expand beyond the template's allowed values.
- **Template deletion**: Deleting or un-templating the CIMD template application is blocked while it is referenced in domain CIMD settings.
- **Pre-registered client precedence**: Pre-registered clients take precedence over CIMD clients. If an application is created in Access Management with a `client_id` that is the URL of a remote CIMD resource, the pre-registered application's configuration applies instead of the remote metadata.
- **Prohibited metadata fields**: Metadata documents must not include `client_secret` or `client_secret_expires_at` fields.
- **Private key JWT requirements**: `token_endpoint_auth_method=private_key_jwt` requires `jwks` or `jwks_uri` in the metadata document.
- **Client ID validation**: `client_id` in the metadata document must match the requested URL (canonical form).
- **Redirect URIs validation**: `redirect_uris` is required and must be a non-empty array.
- **Fetch timeout validation**: Fetch timeout must be greater than 0.
- **Max response size validation**: Max response size must be greater than 0.
- **Cache TTL validation**: Cache TTL must be greater than 0.
- **Cache max entries validation**: Cache max entries must be greater than 0.
- **Template ID validation**: Template ID must be a valid application ID configured as a template.

## Related Changes

- The OIDC discovery document now advertises `client_id_metadata_document_supported` when CIMD is enabled.
- The CIMD settings page is accessible under OAuth 2.0 configuration with a new "CIMD" menu item.
- Applications marked as CIMD templates display a "CIMD Template" badge in the UI and cannot be deleted or un-templated while referenced in domain CIMD settings.
- Audit logs for CIMD clients include a `metadataDocumentHash` attribute in actor attributes. These actors are not linked to application detail pages.
- The configuration property `oidc.cimdSettings.softwareId` has been renamed to `oidc.cimdSettings.templateId`. Existing configurations must update this property name.
- CIMD clients now support introspection, revocation, and refresh token flows.
- The application template setting has been moved to improve UX consistency with DCR settings.
