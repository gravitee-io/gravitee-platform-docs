---
description: Configuration guide for authentication.
metaLinks:
  alternates:
    - ./
---

# Authentication

Gravitee API Management (APIM) natively supports several types of authentication:

* Authentication providers (in-memory, LDAP, and the APIM repository)
* Social providers (GitHub and Google)
* A custom OAuth2 / OpenID authorization server, including Microsoft Entra ID and Gravitee Access Management

You can specify as many identity providers as you want. For in-memory, LDAP, and repository users, APIM API loops through the providers in the order they are declared in the `providers` section of `gravitee.yml` until one of the authentication methods completes successfully.

```yaml
security:
  providers:
    # First authentication source
    - type: ldap
      # ...
    # Second authentication source
    - type: memory
      # ...
    # Third authentication source
    - type: gravitee
      # ...
```

Social and OIDC providers are not part of that loop. They appear as buttons on the Console or Portal login page when they are **activated** for that scope.

## How identity providers are scoped

{% hint style="info" %}
In this section, the **organization** scope is the APIM Console (and Cockpit / Gravitee Cloud open-Console). The **environment** scope is the Developer Portal. Providers are always defined at organization level. You then choose, independently, whether each provider is offered on each login window.
{% endhint %}

All identity providers are created under **Organization → Authentication**. Each provider then has three independent controls:

| Control | Where | What it does |
| --- | --- | --- |
| **Activated / Deactivated** (Status) | Organization → Authentication → identity provider list | Organization activation. Puts the provider on the **Console** login page. This is the Console off-switch. Deactivate to remove Console (and Cockpit) SSO. |
| **Allow portal authentication to use this identity provider** | Edit the provider. Listed as **Available on dev portal**. Stored as `enabled`. | Portal eligibility only. It does **not** hide or show the Console button. Leave it **off** for Console-only SSO. |
| **Activate** on the environment list | Environment → Settings → Authentication | Environment activation. Required, together with the portal-allow flag, for the **Portal** login page. |

A provider appears on a login page only when **both** conditions for that page are true:

* **Console:** organization Status = Activated. The portal-allow flag is ignored.
* **Portal:** environment Activate = on **and** **Allow portal authentication…** = on.

### Console-only SSO

Supported and intended:

1. Create the provider under **Organization → Authentication**.
2. Set Status to **Activated**.
3. Leave **Allow portal authentication to use this identity provider** **off**.
4. Leave the provider **off** under **Settings → Authentication** for every environment.

The Console (and Cockpit open-Console) shows the SSO button. The Portal does not.

{% hint style="warning" %}
**Known issue on 4.9.33, 4.10.29, 4.11.26, and 4.12.18**

Those patches applied the portal-allow flag to Console login as well. An organization with the Console-only configuration above lost its Console SSO button on upgrade. If local login was also disabled, the organization could not sign in through the UI. Fixed in 4.9.34, 4.10.30, 4.11.27, and 4.12.19: the flag is portal-scoped again. After you install the fix, turn **Allow portal authentication…** back **off** if a workaround had turned it on.

If you used that flag as a Console kill switch on those four releases, it no longer blocks Console login. Use **Deactivate** instead.
{% endhint %}

### Example

Three providers are defined: Google, GitHub, and Gravitee AM.

* GitHub and Gravitee AM are **Activated** on the organization list (Console).
* Google and Gravitee AM have **Allow portal authentication…** on.
* On the environment list, only Gravitee AM is activated.

| Provider | Org Activated | Allow portal authentication | Env Activated | Console login | Portal login |
| --- | --- | --- | --- | --- | --- |
| GitHub | Yes | Off | Off | Yes | No |
| Google | No | On | Off | No | No |
| Gravitee AM | Yes | On | Yes | Yes | Yes |

Console shows **GitHub** and **Gravitee AM**. Portal shows only **Gravitee AM**.

## APIs

| Surface | List providers on the login page | Authenticate | Scope | Reads `enabled`? |
| --- | --- | --- | --- | --- |
| Console | `GET /organizations/{org}/social-identities` | `POST /organizations/{org}/auth/oauth2/{identity}` | Organization activation | No |
| Portal | `GET /environments/{env}/configuration/identities` | Portal `POST …/auth/oauth2/{identity}` | Environment activation | Yes |

Deactivating a provider for the Console removes its organization activation (`PUT /organizations/{org}/identities`). Both `findAll` and `findById` then omit it, so the button disappears and a direct auth call is rejected.

## Providers declared in gravitee.yml

If you declare a social or OIDC provider under `security.providers` (or the Helm / environment-variable equivalent), `IdentityProviderInitializer` rewrites that provider on **every** Management API startup:

* The provider record is upserted. **`enabled` is set to `true`**, so the portal-allow flag cannot stay off across a restart.
* Every organization and environment activation is deleted, then only the targets in `activations` are recreated.
* The UI shows *Configuration provided by the system. Every modifications will be overridden at the next startup.*

```yaml
security:
  providers:
    - type: oidc
      id: entra
      # credentials and endpoints...
      activations:
        - "DEFAULT"            # organization → Console
        - "DEFAULT:DEFAULT"    # organization:environment → Portal
```

* `"<ORGANIZATION_ID>"` — Console only.
* `"<ORGANIZATION_ID>:<ENVIRONMENT_ID>"` — that environment’s Portal. YAML-declared providers are also forced `enabled: true`, so the Portal button appears as soon as the environment activation exists.

In-memory, LDAP, and the built-in `gravitee` provider are not rewritten this way. In-Console edits to a YAML-declared social or OIDC provider do not survive a restart.

Provider-specific setup, including the password policy applied to locally managed accounts:

<table data-view="cards"><thead><tr><th data-type="content-ref"></th><th></th><th data-hidden data-card-target data-type="content-ref"></th></tr></thead><tbody><tr><td><a href="authentication-providers.md">authentication-providers.md</a></td><td></td><td><a href="authentication-providers.md">authentication-providers.md</a></td></tr><tr><td><a href="password-policy.md">password-policy.md</a></td><td></td><td><a href="password-policy.md">password-policy.md</a></td></tr><tr><td><a href="gravitee-access-management.md">gravitee-access-management.md</a></td><td></td><td><a href="gravitee-access-management.md">gravitee-access-management.md</a></td></tr><tr><td><a href="social-providers.md">social-providers.md</a></td><td></td><td><a href="social-providers.md">social-providers.md</a></td></tr><tr><td><a href="openid-connect.md">openid-connect.md</a></td><td></td><td><a href="openid-connect.md">openid-connect.md</a></td></tr><tr><td><a href="microsoft-entra-id.md">microsoft-entra-id.md</a></td><td></td><td><a href="https://app.gitbook.com/o/8qli0UVuPJ39JJdq9ebZ/s/Fc1ETPs5seXizrv8ozOs/~/changes/74/getting-started/configuration/authentication/page-1">https://app.gitbook.com/o/8qli0UVuPJ39JJdq9ebZ/s/Fc1ETPs5seXizrv8ozOs/~/changes/74/getting-started/configuration/authentication/page-1</a></td></tr></tbody></table>
