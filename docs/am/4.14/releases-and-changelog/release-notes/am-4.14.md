---
description: The Access Management 4.14 release notes cover Lightweight JWT and a breaking change to the Helm chart, which no longer deploys MongoDB. Browse the changes.
---

# AM 4.14

## Breaking Changes

Check these changes before you upgrade to AM 4.14.

### The Helm chart no longer deploys MongoDB

* The AM Helm chart drops its `mongodb-replicaset` dependency, so it no longer deploys MongoDB. Before you upgrade an installation whose values set `mongodb-replicaset.enabled` to `true`, move your data to a MongoDB that runs outside the chart, and point the chart at it. See [Breaking Changes for Access Management](../../getting-started/install-and-upgrade-guides/breaking-changes-for-access-management.md#the-helm-chart-no-longer-deploys-mongodb).

## New Features

### Lightweight JWT

* An application can receive lightweight access, refresh, and ID tokens that carry only the reserved protocol claims and the claims you allowlist per token type. The new **Enable Lightweight JWT** setting sits on the **Tokens & User Profile** tab of the application's **OAuth 2.0 / OIDC** settings. It comes with the **Allowed access and refresh token claims** and **Allowed ID token claims** lists, and it's off by default.
* The introspection endpoint returns the full claim set of a lightweight access token or refresh token. The UserInfo endpoint returns the user claims for the granted scopes, as it does for a full token. As a result, resource servers and API gateways see the same claims as before.
* During a token exchange, a custom claim expression reads only the claims that a lightweight subject token or actor token carries. See [Configure Lightweight JWT](../../guides/auth-protocols/oauth-2.0/lightweight-jwt.md).
