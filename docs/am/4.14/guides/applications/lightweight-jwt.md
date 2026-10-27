# Lightweight Jwt

With Lightweight JWT enabled, issued tokens contain the following claims:

- **Access token.** It keeps its reserved claims and the claims in **Allowed access and refresh token claims**.
- **Refresh token.** It keeps its reserved claims, which include `orig_resources`, and the claims in the same **Allowed access and refresh token claims** allowlist.
- **ID token.** It keeps its reserved claims and the claims in **Allowed ID token claims**. `at_hash`, `c_hash`, and `s_hash` are always present when the flow produces them.
- **Custom claims named after a reserved claim.** These stay in the token with their custom value. Examples are `act` or `cnf` in the access token, and `sub` or `acr` in the ID token.
- **Other custom claims.** These are removed unless they're allowlisted. This applies whatever the claim's source: a static value, a user attribute, roles, groups, or a context attribute set by a policy.
- **Profile claims in the ID token.** Claims such as `email` and `given_name` are removed unless they're allowlisted.
- **Turning the setting off.** Full tokens are issued again, with all custom and profile claims.

A lightweight ID token can be verified against the domain's JWKS, issuer, and client ID audience. It also works as `id_token_hint` with `prompt=none` for silent re-authentication.

### Verify the token contents

To check which claims each token contains, follow these steps:

1. Request tokens with a password grant and scope `openid email profile`.
2. Decode the tokens.

If the flow sets no optional claims and no allowlists are configured, each token contains exactly these claim names:

```
Access token:  aud, client_id, domain, exp, gis, iat, iss, jti, scope, sub
Refresh token: aud, domain, exp, gis, iat, iss, jti, scope, sub
ID token:      aud, auth_time, exp, gis, iat, iss, sub
```

In the access token, both `client_id` and `aud` equal the client ID.

## View the Lightweight JWT reserved claims

The reserved claims dialog shows which claims each lightweight token always keeps.

1. In the **Lightweight JWT** section, click the info icon next to the **Lightweight JWT** heading. Its accessible label is **Lightweight JWT claims**.
2. Review the **Lightweight JWT reserved claims** dialog. Hover over a claim to see its description, for example **Issuer** or **Original resources**.

    <!-- TODO: Screenshot of the Lightweight JWT reserved claims dialog -->
    <figure><img src="../../.gitbook/assets/PLACEHOLDER-lightweight-jwt-reserved-claims.png" alt="Lightweight JWT reserved claims dialog"><figcaption><p>Lightweight JWT reserved claims</p></figcaption></figure>

3. Click **Close**.

The dialog states: "A lightweight token always keeps its reserved claims. To keep other claims, including your custom claims, add them to the allowlists. All other claims are removed."

| Token | Always reserved | Reserved when the flow sets them | Internal |
|:---|:---|:---|:---|
| Access token | `iss`, `sub`, `aud`, `exp`, `iat`, `jti`, `scope`, `client_id` | `cnf`, `act`, `client_profile`, `permissions`, `authorization_details` | `gis`, `domain`, `claims_request_parameter` |
| ID token | `iss`, `sub`, `aud`, `exp`, `iat`, `auth_time` | `nonce`, `acr`, `client_profile`, `at_hash`, `c_hash`, `s_hash` | `gis` |
| Refresh token | `iss`, `sub`, `aud`, `exp`, `iat`, `jti`, `scope` | `cnf`, `act`, `client_profile`, `permissions`, `authorization_details`, `orig_resources` | `gis`, `domain` |

## Next steps

- Use the **Userinfo claims** section to expose user-profile claims from the OIDC `/userinfo` endpoint instead of embedding them in tokens.
- Review your application's **Custom claims** and allowlist any that downstream services must read directly from the token.
