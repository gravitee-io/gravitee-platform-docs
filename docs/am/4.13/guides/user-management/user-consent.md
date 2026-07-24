---
metaLinks:
  alternates:
    - >-
      https://app.gitbook.com/s/H4VhZJXn1S232OEmh8Wv/guides/user-management/user-consent
---
# User Consent

## User consent

As described in [RFC 6819](https://tools.ietf.org/html/rfc6819#section-5.1.3), users should always be in control of authorization processes and have the necessary information to make informed decisions.

If you want users to acknowledge and accept that they are giving an app access to their data, you can configure AM to display a consent page during the OAuth 2.0/OIDC authentication flow.

{% hint style="info" %}
You can change the look and feel of the user consent form. See [custom pages](../branding/README.md#custom-pages) for more information.
{% endhint %}

## Selective Scope Consent and Required Scopes

Gravitee Access Management 4.13.0 introduces two complementary capabilities for the OAuth2 user consent page: **opt-in scope selection mode**, where users must explicitly check the scopes they want to grant rather than having all scopes pre-selected, and **required scopes**, which are scopes that must be consented to for an authorization request to succeed. Together, these features give API platform administrators finer control over how end-users grant application permissions during OAuth2 authorization flows.

### Key Concepts

#### Opt-In Scope Selection Mode

By default, newly created applications use opt-in scope selection (`optInScopeSelection = true`), meaning all requested scope checkboxes start **unchecked** on the consent page and users must actively select the permissions they wish to grant. Existing applications default to the legacy behavior (`optInScopeSelection = false`), where all scopes are pre-checked and users can deselect them. Administrators who want existing applications to use opt-in mode must explicitly enable it via the Management Console or Management API.

The server-side context variable `preselectAllScopes` controls pre-selection behavior on the consent page. Custom consent page templates that do not use this variable will not reflect the opt-in or pre-checked setting.

#### Required Scopes

A required scope is a per-scope, per-application flag (`requiredScope = true`) on an application's scope settings. On the consent page, required scopes are rendered as:

- **Checked and disabled** — users cannot deselect them.
- **Displayed first**, above optional scopes.
- **Labeled with a Required chip.**

The following enforcement rules apply:

- If the user approves the consent form but a required scope is missing or not approved in the submitted form, the authorization server responds with an OAuth2 `access_denied` error and does not persist any consent.
- Outright denial (`user_oauth_approval=false`) bypasses required-scope enforcement; all scopes are recorded as denied.
- A scope flagged as required is only enforced when it is also included in the current authorization request's scope set. If not requested, it is ignored.

#### Selective Consent and Scope Narrowing

When a user selects a subset of the presented scopes and approves, the authorization request's scope set is narrowed to only those scopes the user approved.

- Previously approved scopes from prior sessions are not re-presented or overwritten.
- When `prompt=consent` is present in the authorization request, all requested scopes are re-presented to the user regardless of prior approvals.
- Scopes submitted via the consent form that were not part of the original authorization request are ignored and not recorded.

#### Redesigned Consent Page UI

The OAuth2 user consent page has been redesigned from a static read-only display to an interactive table with checkboxes.

| Change | Previous | New |
|---|---|---|
| Primary action button | **Accept** | **Allow** |
| Secondary action button | **Cancel** | **Deny** |
| Scope display | Static, read-only | Interactive checkbox table |
| Page description | — | `Application "<app name>" requests access to your account` |

The **Allow** button is disabled when no scope checkboxes are selected.

{% hint style="warning" %}
**Migration note:** Custom consent templates or test automation that reference the old button labels (`Accept`, `Cancel`) must be updated to use the new labels. Applications using custom consent page templates must also be updated to use the `preselectAllScopes` context variable and reference the new `oauth.button.allow` and `oauth.button.deny` i18n keys.
{% endhint %}

### Prerequisites

- Gravitee Access Management **4.13.0** or later.
- Newly created applications automatically receive `optInScopeSelection = true`. Existing applications retain `optInScopeSelection = false` (pre-checked behavior) until explicitly updated by an administrator.

### Configure Consent Mode for an Application

Navigate to the application's **Scopes** tab in the Management Console, then scroll to the **Consent** section.

1. Locate the **Preselect Consent for All Scopes** toggle.
2. Enable the toggle to pre-check all requested scopes on the consent page. Users can still change individual selections before approving.
3. Disable the toggle to use opt-in mode, where all scope checkboxes start unchecked.

{% hint style="info" %}
This toggle is the inverse of `optInScopeSelection`. Toggle **ON** sets `optInScopeSelection = false` (pre-check all). Toggle **OFF** sets `optInScopeSelection = true` (opt-in mode).
{% endhint %}

| Field | Description | Default (New Applications) | Default (Existing Applications) |
|---|---|---|---|
| **Preselect Consent for All Scopes** | When enabled, all requested scopes are pre-checked on the consent page. | Off (opt-in mode) | On (pre-checked) |

### Mark a Scope as Required

In the application's **Scopes** tab, the scopes table includes a **Required** column.

1. Locate the scope to mark as required in the scopes table.
2. Check the **Required** checkbox for that scope to prevent users from deselecting it on the consent page.

| Column | Description |
|---|---|
| **Required** | When checked, the scope is shown as locked on the consent page. Users cannot deselect it and must consent to it for the authorization request to succeed. |

**Scopes tab sidebar help text:**

| Option | Description |
|---|---|
| **Default** | Added to the authorization request automatically when the client starts an authorization flow without requesting any specific scopes. |
| **Required** | Mandatory scopes that users cannot deselect on the consent screen when requested. Must be consented to for the authorization request to be allowed. |
| **User Consent** | How long the user's approval of a scope is remembered before consent is requested again. |

### Consent Page Toolbar Controls and Scope Display Rules

The redesigned consent page includes contextual toolbar controls that appear based on the number of requested scopes.

| Control | Shown When | Description |
|---|---|---|
| **Select all** / **Clear all** | More than 1 scope | Selects or clears all optional scope checkboxes. Does not affect required (disabled) scopes. |
| Selection count (`{0} of {1} selected`) | More than 1 scope | Displays how many scopes are currently selected. |
| Search input (`Search permissions...`) | More than 10 scopes | Filters the scope list by text. |
| Filter tabs: **All** / **Selected** / **Unselected** | More than 10 scopes | Filters scope display by selection state. |

**Required scope sectioning:**

- When there is at least one required scope **and** the total number of requested scopes exceeds 10, required scopes are displayed in a separate collapsible section labeled `{0} required permissions (always included)`.
- For 10 or fewer total scopes, required scopes appear inline in the main table with the **Required** chip, without a separate collapsible section.

### Management API Schema Properties

#### `ApplicationOAuthSettings`

| Property | Type | Description |
|---|---|---|
| `optInScopeSelection` | `boolean` | When `true`, scope checkboxes start unchecked on the consent page (opt-in mode). When `false`, all scopes are pre-checked. Patchable via `PatchApplicationOAuthSettings`. |

#### `ApplicationScopeSettings`

| Property | Type | Description |
|---|---|---|
| `scope` | `string` | The scope identifier. |
| `defaultScope` | `boolean` | Whether this scope is added automatically when no specific scopes are requested. |
| `requiredScope` | `boolean` | When `true`, the scope cannot be deselected on the consent page and must be approved for the authorization request to succeed. Default: `false`. |
| `scopeApproval` | `integer` | Duration in seconds that the user's approval is remembered before consent is re-requested. |

## Revoke user consent

You can view a list of applications for which each user has provided consent. To revoke access to an application:

1. Log in to AM Console.
2. Click **Settings > Users**.
3. Select the user and in the **Authorized Apps** tab, revoke the application.

<figure><img src="../../.gitbook/assets/guide-user-management-user-consent-150.png" alt=""><figcaption></figcaption></figure>

{% hint style="info" %}
Revoking consent can also be done via the [AM Management API](../../reference/am-api-reference.md).
{% endhint %}
