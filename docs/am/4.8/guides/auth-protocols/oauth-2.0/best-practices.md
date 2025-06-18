# Best Practices

The [OAuth 2.0 Security Best Current Practice](https://tools.ietf.org/html/draft-ietf-oauth-security-topics) describes security requirements and other recommendations for clients and servers implementing OAuth 2.0.

We recommend you note the following points:

* **Use HTTPs**: communicate with AM server over HTTPs all the way.
* **Token expiration**: use short-lived access tokens (a couple of minutes) to limit the risk of leaked access tokens.
* **Force PKCE**: PKCE must be used for SPA and mobile/native applications.
* **Restrict data payload**: tokens can be easily decoded and propagated to multiple layers, so add the minimum information to the payload.
* **Set up callbacks**: configure application callbacks to avoid open redirection attacks.
* **Privilege restriction**: limit the use of OAuth 2.0 scopes to strictly match application actions.
