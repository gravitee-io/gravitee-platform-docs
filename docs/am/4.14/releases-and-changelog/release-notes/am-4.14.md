# AM 4.14

## Highlights
* Lightweight JWT lets you issue access, refresh, and ID tokens that contain only their reserved claims and the claims you allowlist.

## Breaking Changes

## Custom plugins

## New Features

#### **Lightweight JWT**

* With Lightweight JWT enabled, issued tokens keep their reserved claims and your allowlisted claims, and all other custom claims and ID token profile claims such as `email` and `given_name` are removed.
* You enable it in the application's **Lightweight JWT** section and keep extra claims by adding them to **Allowed access and refresh token claims** or **Allowed ID token claims**, and the info icon next to the **Lightweight JWT** heading opens the **Lightweight JWT reserved claims** dialog that lists the claims each token always keeps.
* It applies to access tokens, refresh tokens, and ID tokens, and it removes custom claims that aren't allowlisted whatever their source: a static value, a user attribute, roles, groups, or a context attribute set by a policy.
* Custom claims named after a reserved claim, such as `act` or `cnf` in the access token, stay in the token with their custom value, and turning the setting off issues full tokens again with all custom and profile claims.
* A lightweight ID token can still be verified against the domain's JWKS, issuer, and client ID audience, and it works as `id_token_hint` with `prompt=none` for silent re-authentication.
