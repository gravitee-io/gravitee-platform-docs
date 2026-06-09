# Automation API Restrictions and Changes

## Restrictions

- The Automation API is disabled by default and must be explicitly enabled via `gravitee.http.api.automation.enabled` in `gravitee.yml` or Helm values.
- Cookie-based JWT authentication is not supported. The Automation API accepts only bearer tokens (JWT or opaque user service-account access tokens).
- Resources created outside the Automation API (via the Management REST API or Console) are not returned by Automation API list endpoints.
- Each domain can have at most one system identity provider. Attempting to create a second system identity provider is rejected with the error "The domain already has a system identity provider".
- System identity providers are immutable through the Automation API. Re-PUTting a system identity provider is an idempotent no-op.
- The `system` flag is immutable for existing identity providers. Changing it requires deleting and recreating the identity provider.
- The `type` field is immutable for existing certificates, identity providers, and reporters. Changing it requires deleting and recreating the resource.
- Database reporter types (`mongodb`, `reporter-am-jdbc`) can only be created as system reporters (`system: true`). Manual creation is rejected.
- Embedded file content in certificate configurations is normalized to filename-only form before persistence. Raw base64 content is not stored in the configuration field.
- Repository lookups during authentication honor `http.blockingGet.timeoutMillis`. If a lookup exceeds this timeout, the security context is cleared and the request continues unauthenticated (401 returned by Spring Security).
- The Access Management Terraform provider is currently in technical preview.

## Related Changes

- The Automation API introduces a new OpenAPI specification served at the configured entrypoint when the API is enabled. The specification is automatically regenerated during release workflows and enforced by CI checks for staleness and breaking changes.
- Validation error messages now resolve `@JsonProperty` field names instead of internal Java field names (e.g., `defaultIdentityProviderForRegistration` instead of `defaultIdentityProviderForRegistrationKey`).
- The identity provider endpoint path has been renamed from `/identity-providers` to `/identities`, and the path parameter has been renamed from `idpKey` to `identityKey`.
- OpenAPI timestamp fields now use `integer` type (format: `int64`) with the description "Epoch timestamp in milliseconds" instead of `string` type.
- The `type` field is now enforced as immutable for certificates, identity providers, and reporters.
- Certificate PUT responses are normalized to use file names instead of raw base64 content.
- When a system identity provider is created, if the domain's `accountSettings.defaultIdentityProviderForRegistration` holds a stale key-based id, the domain is automatically updated to reference the real system identity provider id.
