# CIMD Client Usage and Runtime Behavior

## Using CIMD Clients

A client initiates an OAuth 2.0 authorization flow by providing a URL-shaped `client_id` (for example, `https://client.example.com/metadata`). Gravitee detects the URL format and checks the in-memory cache for the canonical form of the `client_id`. On a cache miss, Gravitee fetches the metadata document from the `client_id` URL, validates it against the template application and SSRF rules, and synthesizes an ephemeral client configuration. The metadata document and logo (if `logo_uri` is present) are cached.

The user authenticates and consents (if required), and Gravitee issues an authorization code. The client exchanges the code for tokens at `/oauth/token`, providing the `client_id` in the request body or Basic auth header (URL-encoded). Gravitee re-resolves the metadata (from cache or remote) to validate client authentication. The access token's `aud` claim is set to the CIMD `client_id` URL. Introspection and revocation endpoints accept the CIMD `client_id`.

## End-User Configuration

{% hint style="info" %}
Pre-registered clients take precedence over dynamic CIMD clients. If an application is created in AM with a `client_id` that matches the URL of a remote CIMD resource, the application's configuration applies instead of the remote metadata when that `client_id` is used to authenticate.
{% endhint %}

JWKS public keys presented in CIMD metadata are stored in the in-memory cache alongside keys for pre-registered clients. This cache is configured using `gravitee.yml` settings.

When **Revoke Tokens And Consents When Client Metadata Changes** is enabled, Gravitee stores hashes of CIMD metadata documents per domain and data plane. This data persists indefinitely while the policy is enabled. If disabled, this data is deleted. The stored data is a lightweight thumbprint, but storage impact may be relevant for environments that manage a large volume of CIMD clients. This policy is not affected by the CIMD cache settings. This mode detects changes in remote CIMD metadata only; changes to settings or restrictions in template applications do not trigger revocation of tokens or consents.

Valid OAuth settings present in CIMD metadata are applied to the synthesized client. When omitted, the values from the template application are used, with the following exceptions:

- `token_endpoint_auth_method`: When omitted in the metadata, defaults to `none` and overrides the template application value.
- `grant_types`: The intersection of metadata (default `authorization_code`) and the template application's grant types.
- `response_types`: The intersection of metadata (default `code`) and the template application's response types.
- `scope`: The intersection of metadata and the template application's scopes when present in metadata; otherwise uses template scopes verbatim.

CIMD metadata can only define OAuth/OIDC client-registration surface. Other application configurations (identity provider, metadata, token validity, certificates, MFA) can only be defined in the template application.
