# CIMD Metadata Document Specification

## CIMD Metadata Document Fields

CIMD clients provide metadata via a JSON document at the `client_id` URL. The gateway fetches and validates this document during OAuth flows.

| Field | Description | Example |
|:------|:------------|:--------|
| `client_id` | Must match the request URL in canonical form. Required. | `"http://example.com/my-app"` |
| `redirect_uris` | Array of redirect URIs. At least one required. | `["https://client.example.com/callback"]` |
| `token_endpoint_auth_method` | Authentication method. Defaults to `none`. Secret-based methods (`client_secret_basic`, `client_secret_post`, `client_secret_jwt`) are forbidden. When omitted in metadata, defaults to `none` and overrides the template application value. | `"none"` or `"private_key_jwt"` |
| `grant_types` | Array of grant types. Defaults to `["authorization_code"]`. Intersected with template application's allowed grant types. | `["authorization_code", "refresh_token"]` |
| `response_types` | Array of response types. Defaults to `["code"]`. Intersected with template application's allowed response types. | `["code"]` |
| `scope` | Space-separated scopes. When present in metadata, intersected with template application's scopes. When omitted, uses template scopes verbatim. | `"openid profile email"` |
| `jwks` | Inline JWKS for `private_key_jwt`. Public keys are stored in the in-memory cache alongside keys for pre-registered clients. | `{"keys": [...]}` |
| `jwks_uri` | URI to fetch JWKS for `private_key_jwt`. Subject to SSRF validation. Must be HTTPS unless `allowUnsecuredHttpUri = true`. | `"https://example.com/jwks"` |
| `logo_uri` | URI to client logo. Subject to SSRF validation. | `"https://example.com/logo.png"` |
| `client_name` | Human-readable client name. | `"My CIMD Client"` |
| `client_uri` | Client homepage URI. | `"https://example.com"` |
| `policy_uri` | Privacy policy URI. | `"https://example.com/privacy"` |
| `tos_uri` | Terms of service URI. | `"https://example.com/terms"` |
| `contacts` | Array of contact email addresses. | `["admin@example.com"]` |
| `software_id` | Software identifier. | `"my-software-id"` |
| `software_version` | Software version. | `"1.0.0"` |
| `software_statement` | Software statement JWT. | `"eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9..."` |
| `application_type` | Application type (`web` or `native`). | `"web"` |
| `subject_type` | Subject identifier type (`public` or `pairwise`). | `"public"` |
| `sector_identifier_uri` | Sector identifier URI for pairwise subjects. | `"https://example.com/sector"` |
| `id_token_signed_response_alg` | ID token signing algorithm. | `"RS256"` |
| `request_object_signing_alg` | Request object signing algorithm. | `"RS256"` |
| `tls_client_auth_subject_dn` | TLS client certificate subject DN. | `"CN=client.example.com"` |
| `tls_client_auth_san_dns` | TLS client certificate SAN DNS. | `"client.example.com"` |
| `tls_client_auth_san_uri` | TLS client certificate SAN URI. | `"https://client.example.com"` |
| `tls_client_auth_san_ip` | TLS client certificate SAN IP. | `"192.0.2.1"` |
| `tls_client_auth_san_email` | TLS client certificate SAN email. | `"admin@example.com"` |
| `tls_client_certificate_bound_access_tokens` | Bind access tokens to TLS client certificate. | `true` |
| `post_logout_redirect_uris` | Array of post-logout redirect URIs. | `["https://client.example.com/logout"]` |
| `request_uris` | Array of request URIs for request objects. | `["https://example.com/request"]` |
| `backchannel_token_delivery_mode` | CIBA token delivery mode (`poll`, `ping`, or `push`). | `"poll"` |
| `backchannel_client_notification_endpoint` | CIBA notification endpoint. | `"https://example.com/notify"` |
| `backchannel_authentication_request_signing_alg` | CIBA request signing algorithm. | `"RS256"` |
| `backchannel_user_code_parameter` | CIBA user code parameter support. | `true` |
| `require_pushed_authorization_requests` | Require PAR for authorization requests. | `true` |

{% hint style="info" %}
CIMD metadata cannot define non-OAuth application settings such as identity providers, MFA, certificates, or token validity. These settings are inherited from the template application.
{% endhint %}
