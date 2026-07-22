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

## Select scopes to consent

The consent page lists each scope of the authorization request on its own row, with the scope key, the scope description when one is defined, and a checkbox. Users adjust the selection to the scopes they agree to grant, then click **Allow**. Clicking **Deny** rejects the entire authorization request.

AM continues the flow with the approved scopes only. The authorization response and the issued tokens contain only the scopes the user approved, and the stored consent records the other presented scopes as denied. The `USER_CONSENT_CONSENTED` event in the [audit trail](../audit-trail.md) records every presented scope with its approved or denied status.

The consent page adapts to the number of scopes in the request:

* **Allow** is disabled until at least one scope is selected.
* When more than one scope is listed, the page displays **Select all** and **Clear all** buttons and a selection counter.
* When more than 10 scopes are listed, the page also displays a search field and **All**, **Selected**, and **Unselected** filters.

### Consent reuse

AM remembers each approved scope for the user consent duration configured on the application or on the scope. When the user starts a new authorization request, AM prompts only for the requested scopes that aren't approved yet. To present the full list of requested scopes again, add `prompt=consent` to the authorization request.

## Configure scope consent for an application

Two application settings control how the consent page behaves: the **Preselect consent for all scopes** toggle and the per-scope **Required** checkbox.

### Preselect consent for all scopes

The **Preselect consent for all scopes** toggle controls the initial state of the checkboxes on the consent page:

* When the toggle is on, all requested scopes are checked by default and users clear the checkboxes of the scopes they don't want to grant. This matches the consent behavior of AM versions earlier than 4.13.0.
* When the toggle is off, no scopes are checked by default and users check each scope they agree to grant.

For applications that existed before AM 4.13.0, the toggle is on, so the consent page behaves like previous versions until you change the setting. For new applications created in the AM Console, the toggle is off.

Recommended: Turn the toggle off for clients that request many scopes, such as MCP clients and AI agents, and on for traditional web applications where full approval is expected.

### Required scopes

Mark a scope as required when the application depends on it to function. Required scopes are always granted when the user allows the request:

* Required scopes are listed first, with a **Required** label, and their checkbox is checked and disabled.
* Required scopes count as a selection, so **Allow** is available even when no other scope is checked.
* When more than 10 scopes are presented and some of them are required, the required scopes are grouped in a separate **_n_ required permissions (always included)** table above the other scopes, where _n_ is the number of required scopes. This table is expanded by default, and clicking its header collapses or expands it. The search field, the filters, the selection counter, and the **Select all** and **Clear all** buttons then apply to the non-required scopes only.
* When the user clicks **Allow**, every required scope is granted along with the checked optional scopes. When the user clicks **Deny**, the whole request is rejected, including the required scopes.

{% hint style="warning" %}
AM validates the submitted consent form against the original authorization request. Submitted scopes that aren't part of the request are ignored, and a consent submission that doesn't grant a presented required scope is rejected with an `access_denied` error.
{% endhint %}

### Configure the settings in the AM Console

1. Log in to AM Console.
2. Click **Applications**.
3. Select your application.
4. Click **Settings**.
5. Click **OAuth 2.0 / OIDC**.
6. Click the **Scopes** tab.
7. In the **Consent** section, turn the **Preselect consent for all scopes** toggle on or off.

    <!-- TODO: Screenshot of the Consent section with the Preselect consent for all scopes toggle -->
    <figure><img src="../../.gitbook/assets/PLACEHOLDER-application-scopes-preselect-consent.png" alt=""><figcaption><p>Preselect consent for all scopes toggle</p></figcaption></figure>

8. Optional: To add a scope to the scopes table, click **ADD SCOPES**.
9. Optional: In the scopes table, select the **Required** checkbox for each scope the application depends on.

    <!-- TODO: Screenshot of the scopes table with the Required column -->
    <figure><img src="../../.gitbook/assets/PLACEHOLDER-application-scopes-required-column.png" alt=""><figcaption><p>Required column in the scopes table</p></figcaption></figure>

10. Click **SAVE**.

{% hint style="info" %}
Both settings are also available through the [AM Management API](../../reference/am-api-reference.md) application operations: `optInScopeSelection` on the application's OAuth settings, and `requiredScope` on each entry of the `scopeSettings` list.
{% endhint %}

## Custom consent templates

Customized consent page templates keep working after an upgrade to AM 4.13.0. AM derives each scope's outcome from its own form field:

* The consent form posts one field per scope, named `scope.<scope key>`, for example `scope.read:orders`. A value of `true`, or a value that starts with `approve`, grants the scope. Any other value, or a missing field, denies it.
* The **Deny** button posts `user_oauth_approval=false`, which denies every presented scope.
* Templates that post a fixed hidden `scope.<scope key>` input with value `true` for every scope behave like the previous all-or-nothing consent: clicking the approve button grants all requested scopes.
* For a required scope, pair the disabled checkbox with a hidden input that posts `scope.<scope key>=true`, like the default template does. Browsers don't submit disabled form controls, and AM rejects a consent submission that doesn't grant a presented required scope.

The consent template receives the following variables:

<table>
    <thead>
        <tr>
            <th width="200">Variable</th>
            <th>Description</th>
        </tr>
    </thead>
    <tbody>
        <tr>
            <td><code>scopes</code></td>
            <td>The scopes to present, with required scopes first. Each scope exposes its <code>key</code>, <code>name</code>, and <code>description</code>.</td>
        </tr>
        <tr>
            <td><code>requiredScopes</code></td>
            <td>The presented scopes that are marked as required on the application.</td>
        </tr>
        <tr>
            <td><code>optionalScopes</code></td>
            <td>The presented scopes that aren't marked as required.</td>
        </tr>
        <tr>
            <td><code>preselectAllScopes</code></td>
            <td>Boolean that is <code>true</code> when the application preselects all scopes on the consent page.</td>
        </tr>
    </tbody>
</table>

{% hint style="info" %}
See [custom pages](../branding/README.md#custom-pages) for how to edit page templates and for the other variables available in the execution context.
{% endhint %}

## Verification

To verify scope consent is working as expected, follow these steps:

1. Start an authorization request for your application that includes several scopes, with at least one scope marked as required.
2. Log in as a test user. The consent page lists each requested scope with a checkbox, and required scopes are checked, disabled, and labeled **Required**.

    <!-- TODO: Screenshot of the consent page showing required and optional scopes with checkboxes -->
    <figure><img src="../../.gitbook/assets/PLACEHOLDER-consent-page-select-scopes.png" alt=""><figcaption><p>Consent page with selective scope consent</p></figcaption></figure>

3. Check a subset of the optional scopes and click **Allow**.
4. Inspect the token response: the `scope` value contains the scopes you checked and the required scopes, and none of the scopes you left unchecked.
5. Start the same authorization request again. AM doesn't prompt again for the scopes that are already approved. Add `prompt=consent` to the request to display the full list again.

## Revoke user consent

You can view a list of applications for which each user has provided consent. To revoke access to an application:

1. Log in to AM Console.
2. Click **Settings > Users**.
3. Select the user and in the **Authorized Apps** tab, revoke the application.

<figure><img src="../../.gitbook/assets/guide-user-management-user-consent-150.png" alt=""><figcaption></figcaption></figure>

{% hint style="info" %}
Revoking consent can also be done via the [AM Management API](../../reference/am-api-reference.md).
{% endhint %}
