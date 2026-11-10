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

### Configurable client ID length for Dynamic Client Registration

* By default, Dynamic Client Registration generates a 43-character URL-safe base64 client ID. You can now have it generate an alphanumeric client ID of a fixed length that uses only the characters `A-Z`, `a-z`, and `0-9`.
* To use it, set `handlers.oidc.dcr.clientIdLength` in the AM Gateway configuration to an integer from `8` to `255`, inclusive.
* The setting applies to the whole installation and affects both standard registration and template-based registration. Template-based registration is used when Dynamic Client Registration templates are enabled on the domain and the request contains `software_id`. Clients that are already registered keep their client ID. See [Dynamic Client Registration client ID length](../../getting-started/configuration/configure-am-gateway/README.md#dynamic-client-registration-client-id-length).
