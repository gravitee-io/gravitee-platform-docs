---
description: The Access Management 4.14 release notes cover Lightweight JWT, which trims tokens to their reserved and allowlisted claims. Browse the new features.
---

# AM 4.14

## New Features

### Lightweight JWT

* An application can receive lightweight access, refresh, and ID tokens that carry only the reserved protocol claims and the claims you allowlist per token type. The new **Enable Lightweight JWT** setting sits on the **Tokens & User Profile** tab of the application's **OAuth 2.0 / OIDC** settings. It comes with the **Allowed access and refresh token claims** and **Allowed ID token claims** lists, and it's off by default.
* The introspection endpoint returns the full claim set of a lightweight access token or refresh token. The UserInfo endpoint returns the user claims for the granted scopes, as it does for a full token. As a result, resource servers and API gateways see the same claims as before.
* During a token exchange, a custom claim expression reads only the claims that a lightweight subject token or actor token carries. See [Configure Lightweight JWT](../../guides/auth-protocols/oauth-2.0/lightweight-jwt.md).

#### **OpenShift Support in the Helm Chart**

* You can use the Gravitee Access Management Helm Chart to deploy Access Management on OpenShift versions later than 3.10.
* The chart exposes Access Management through standard Ingress objects.
* The chart doesn't support OpenShift Routes, so you need to use standard Ingress objects to expose Access Management on OpenShift.
