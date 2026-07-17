---
description: Configure and manage user consent during OAuth 2.0/OIDC authentication flows in Gravitee Access Management.
---

# User Consent

## User consent

As described in [RFC 6819](https://tools.ietf.org/html/rfc6819#section-5.1.3), users should always be in control of authorization processes and have the necessary information to make informed decisions.

To have users acknowledge and accept that they're giving an app access to their data, you can configure Gravitee Access Management to display a consent page during the OAuth 2.0/OIDC authentication flow.

Users can grant or deny individual scopes during the consent flow rather than accepting or rejecting all requested permissions as a single block. Administrators can mark critical scopes as required to ensure they're always granted. For more information, see [Selective Scope Approval](../applications/configure-selective-scope-approval.md).

During consent, requested scopes are presented as checkboxes. Users can approve individual scopes, search and filter the scope list when the count exceeds 10, and use bulk actions to select or clear all optional scopes. Required scopes appear as checked and disabled checkboxes and can't be deselected. If a user attempts to submit consent without approving all required scopes, the authorization request fails with an `access_denied` error (HTTP 403), displays the message "Consent could not be verified", and redirects the user to the login page.

{% hint style="info" %}
You can change the look and feel of the user consent form. See [custom pages](../branding/README.md#custom-pages) for more information.
{% endhint %}

## Revoke user consent

You can view a list of applications for which each user has provided consent. To revoke access to an application, complete the following steps:

1. In Management Console, click **Settings > Users**.
2. Select the user.
3. In the **Authorized Apps** tab, revoke the application.

<figure><img src="../../.gitbook/assets/guide-user-management-user-consent-150.png" alt="Authorized Apps tab showing user consent revocation"><figcaption><p>Revoke user consent for an application</p></figcaption></figure>

{% hint style="info" %}
You can also revoke consent using the [Management API](../../reference/am-api-reference.md).
{% endhint %}
