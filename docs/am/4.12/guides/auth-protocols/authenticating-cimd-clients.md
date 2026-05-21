# Authenticating CIMD Clients

CIMD clients authenticate using the standard OAuth 2.0 authorization code flow. The client initiates authorization by redirecting the user to `/oauth/authorize` with `client_id` set to the metadata document URL (for example, `http://example.com/my-app`). The gateway canonicalizes the `client_id`, checks the in-memory cache, and fetches the metadata document if not cached. The metadata is validated against required fields, forbidden fields, SSRF rules, and intersection with the template application. The gateway synthesizes an ephemeral client configuration from the metadata and template. The user authenticates and consents, and the gateway issues an authorization code. The client exchanges the code for tokens at `/oauth/token` using `grant_type=authorization_code`.

For `token_endpoint_auth_method=none`, no client secret is required. For `private_key_jwt`, the gateway validates the JWT signature using `jwks` or `jwks_uri` from the metadata. The gateway issues an access token and, if `grant_types` includes `refresh_token`, a refresh token.

Refresh token flows follow the same client resolution logic: the gateway resolves the client via cache or metadata fetch, validates the refresh token, and issues a new access token.

{% hint style="info" %}
CIMD clients always require exact redirect_uri matching, even if domain-level `redirectUriStrictMatching` is `false`.
{% endhint %}


{% hint style="info" %}
The metadata cache is in-memory only and lost on gateway restart. The first request after restart fetches metadata remotely.
{% endhint %}
