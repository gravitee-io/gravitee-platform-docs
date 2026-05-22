# CIMD Authentication Flow and Restrictions

## Restrictions

- CIMD clients can't use secret-based authentication methods (`client_secret_basic`, `client_secret_post`, `client_secret_jwt`).
- CIMD clients always require exact `redirect_uri` matching. Prefix matching isn't supported.
- Logo fetch is limited to 256 KB.
- Metadata fetch retries up to 3 times with 100 ms delay between attempts.
- CIMD clients inherit the template application's identity providers, multi-factor authentication policies, token validity, certificates, and other settings not overridable via metadata.
- `grant_types`, `response_types`, and `scope` are intersected with the template application's allowed values. Requesting values not in the template results in an empty set.
- CIMD metadata cache is in-memory only and isn't shared across gateway instances.
- CIMD client state (for revoke-on-change) is stored in the database but isn't replicated to the management API.
- Pre-registered clients take precedence over CIMD clients. If an application is created in Access Management with a `client_id` that is the URL of a remote CIMD resource, the pre-registered application's configuration applies.
- Changes to template application settings or restrictions don't trigger revocation of tokens and consents for CIMD clients, even when **Revoke Tokens and Consents When Client Metadata Changes** is enabled.
- The `client_secret` and `client_secret_expires_at` fields are forbidden in CIMD metadata documents.
- When **Revoke Tokens and Consents When Client Metadata Changes** is enabled, metadata document hashes persist indefinitely in the `cimd_client_state` table until the policy is disabled.

## Related Changes

The OIDC discovery document now advertises `client_id_metadata_document_supported` when CIMD is enabled. A new CIMD settings page is available under **Settings → OAuth 2.0 → CIMD** with permission `domain_openid_read`. Applications marked as CIMD templates display a badge in the UI and can't be deleted or have their template flag unset while referenced in domain CIMD settings. Attempting to do so raises an `ApplicationTemplateInUseException` with the message "Application is referenced as a CIMD template and cannot be modified." Audit events for CIMD clients include `metadataDocumentHash` in actor attributes, and actor links are disabled for CIMD clients (no application detail page). The configuration property `softwareId` has been renamed to `templateId`. Existing `softwareId` values are automatically mapped to `templateId` in API responses. JWKS public keys presented in CIMD metadata are stored in the in-memory cache alongside keys for pre-registered clients, using the cache configured in `gravitee.yml`.
