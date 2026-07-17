---
description: Configure user consent pages, scope selection controls, and required permissions for OAuth 2.0 authorization flows in Gravitee Access Management.
---

# User Consent

## User consent

As described in [RFC 6819](https://tools.ietf.org/html/rfc6819#section-5.1.3), users should always be in control of authorization processes and have the necessary information to make informed decisions.

To have users acknowledge and accept that they're giving an app access to their data, you can configure Access Management to display a consent page during the OAuth 2.0/OIDC authentication flow.

Gravitee Access Management provides fine-grained control over how users grant permissions during OAuth 2.0 authorization flows. Administrators can configure whether scopes are preselected or require explicit opt-in on the consent page, and can mark specific scopes as mandatory, ensuring users can't proceed without granting critical permissions.

{% hint style="info" %}
You can change the look and feel of the user consent form. For more information, see [Custom pages](../branding/README.md#custom-pages).
{% endhint %}

### Opt-in scope selection

By default, all requested scopes are preselected (checked) on the consent page, allowing users to deselect permissions they don't want to grant. When opt-in scope selection is enabled, no scopes are preselected. Users must explicitly check each permission they want to approve. This mode is useful for applications that require explicit user acknowledgment of each requested permission.

| Mode | Consent Page Behavior |
|:-----|:----------------------|
| Preselect (default) | All requested scopes are checked by default. Users can deselect individual scopes before approving. |
| Opt-in | No scopes are checked by default. Users must explicitly select each scope they wish to grant. |

### Required scopes

A required scope is a permission that can't be deselected by the user during consent. Required scopes are always displayed as checked and disabled on the consent page, and a hidden form field ensures they're submitted even though the checkbox is disabled. If a required scope is missing from the submission or submitted as `false`, the authorization server responds with HTTP 403 and the error message "Consent could not be verified". When the user rejects the entire consent request, required scope validation is skipped and all scopes are denied.

### Consent page layout

The consent page adapts its layout based on the number of scopes and the presence of required scopes:

* **10 or fewer total scopes, or no required scopes:** All scopes are displayed in a single table with interactive checkboxes.
* **More than 10 total scopes and at least one required scope:** Scopes are split into two sections:
    * **Required scopes section (collapsible):** Displays only required scopes, always checked and disabled.
    * **Main scopes section:** Displays optional scopes with interactive checkboxes, search, filter, and bulk-select controls.

Search, filter, and bulk action controls operate only on the main scopes section. Required scopes in the collapsible section aren't affected by these controls.

## Configure scope selection controls

To configure opt-in scope selection and required scopes for an OAuth 2.0 application, complete the following steps:

1. In the Management Console, navigate to **Applications → [Your Application] → Settings → OAuth2 / OIDC → Scopes**.
2. Toggle **Preselect consent for all scopes** to control the default selection behavior. When enabled, all requested scopes are checked by default on the consent page. When disabled, users must explicitly select each scope they wish to grant.
3. Add scopes to the table to define the permissions this client is allowed to request. Only the scopes listed here can be granted during authorization. Any scope a client requests outside this list is rejected.
4. Check the **Default** column for a scope to add it to the authorization request automatically when the client starts an authorization flow without requesting any specific scopes. When **Enhance scopes** is enabled, the authenticating user's role scopes are also granted when the request carries no scope, or only `openid`.
5. Check the **Required** column for a scope to mark it as mandatory. Required scopes can't be deselected by the user on the consent screen when they're requested. They must be consented to for the authorization request to be allowed.
6. Select a **User consent** duration from the dropdown to control how long the user's approval of the scope is remembered before consent is requested again.

The following table describes the fields available in the scopes configuration:

| Field | Description | Example |
|:------|:------------|:--------|
| **Preselect consent for all scopes** | When enabled, all requested scopes are checked by default on the consent page. Users can still change individual selections before approving. When disabled, no scopes are preselected and users must explicitly opt in to each permission. | Enabled (default for existing applications), Disabled (default for new applications) |
| **Default** | Adds the scope to the authorization request automatically when the client starts an authorization flow without requesting any specific scopes. | Checked for `profile`, `email` |
| **Required** | Marks the scope as mandatory. The user can't deselect it on the consent screen, and the authorization request fails if the scope isn't granted. | Checked for `openid` |
| **User consent** | Controls how long the user's approval of the scope is remembered before consent is requested again. | `Until revoked`, `30 days`, `1 hour` |

## Consent page interaction

When a user is redirected to the consent page during an OAuth 2.0 authorization flow, they see a list of requested permissions with the following controls:

* **Search input:** Appears when more than 10 scopes are requested. Filters the displayed scopes by matching the search term against scope names and descriptions.
* **Filter buttons:** Appear when more than 10 scopes are requested. Toggle between viewing all scopes, only selected scopes, or only unselected scopes.
* **Bulk action buttons:** Appear when more than 1 scope is requested. **Select all** checks all non-disabled checkboxes in the main scopes section. **Clear all** unchecks all non-disabled checkboxes.
* **Selection count label:** Displays the number of selected scopes out of the total number of optional scopes (for example, "3 of 5 selected").
* **Required scopes section:** Appears when more than 10 total scopes are requested and at least one is required. A collapsible section displaying required scopes, always checked and disabled. Click the section header to expand or collapse.

The **Allow** button is disabled when no scopes are selected. Clicking **Allow** submits the selected scopes and completes the authorization flow. Clicking **Deny** rejects the entire consent request and returns an error to the client application.

### Consent persistence

Only the scopes presented on the current consent page are persisted when the user submits the form. These are the scopes not already approved in a previous session. Previously approved scopes aren't re-submitted or overwritten unless the authorization request includes `prompt=consent`, which forces all requested scopes to be re-presented and re-evaluated.

### Error handling

If a required scope is missing from the consent submission or submitted as `false`, the authorization server responds with the following:

* **HTTP status:** 403 Forbidden
* **Error code:** `access_denied`
* **Error message:** "Consent could not be verified"

This error is returned only when the user approves the consent request (`user_oauth_approval=true`) but fails to grant a required scope. When the user rejects the entire consent request (`user_oauth_approval=false`), required scope validation is skipped and all scopes are denied without error.

## Revoke user consent

You can view a list of applications for which each user has provided consent. To revoke access to an application, complete the following steps:

1. Log in to Access Management Console.
2. Click **Settings > Users**.
3. Select the user.
4. In the **Authorized Apps** tab, revoke the application.

    <figure><img src="../../.gitbook/assets/guide-user-management-user-consent-150.png" alt="Authorized Apps tab showing revoke option"><figcaption><p>Revoke user consent for an application</p></figcaption></figure>

{% hint style="info" %}
Revoking consent can also be done using the [Access Management Management API](../../reference/am-api-reference.md).
{% endhint %}

## Management API

The following schema extensions support programmatic configuration of scope selection controls:

**ApplicationOAuthSettings** schema extension:

| Property | Type | Description |
|:---------|:-----|:------------|
| `optInScopeSelection` | `boolean` | When `true`, users must explicitly select (opt in to) each scope. When `false`, all requested scopes are preselected and users can deselect. |

**ApplicationScopeSettings** schema extension:

| Property | Type | Description |
|:---------|:-----|:------------|
| `requiredScope` | `boolean` | `true` if the scope is required: it can't be deselected by the user during consent and must be granted to allow the authorization request. |

## Migration and backward compatibility

Existing applications without the opt-in scope selection setting configured default to `false`, preserving the legacy "preselect all scopes" behavior. New applications created using the Management Console have opt-in scope selection enabled by default. The **Required** column is added to the scopes table with a default value of `false`, ensuring existing scope settings aren't marked as required during upgrade.
