---
description: Configure OAuth 2.0 applications to allow users to grant or deny individual permissions during consent, with optional mandatory scopes.
---

# Configure Selective Scope Approval

## Overview

Selective scope approval allows users to grant or deny individual OAuth 2.0 permissions during the consent flow, rather than accepting or rejecting all requested scopes as a single block. Administrators can configure applications to require explicit opt-in for each scope or to preselect all scopes by default, and can mark critical scopes as mandatory to ensure they are always granted. This feature gives end users fine-grained control over data access while enabling administrators to enforce minimum permission requirements for application functionality.

## Key Concepts

### Opt-In Scope Selection

The **Opt-In Scope Selection** setting controls whether scopes are preselected on the consent page. When disabled (default), all requested scopes are checked by default, and users can deselect individual permissions before approving. When enabled, no scopes are preselected. Users must explicitly check each permission they wish to grant. This setting is configured per application and applies to all authorization requests for that client.

### Required Scopes

**Required Scopes** are permissions that users can't deselect during consent. When a scope is marked as required, it appears as a checked and disabled checkbox on the consent page, and the authorization request fails with an `access_denied` error if you attempt to submit consent without approving it. Required scopes ensure that critical permissions necessary for application functionality are always granted. If you click **Deny** to reject the entire authorization request, required scopes aren't enforced. Your explicit rejection is honored.

### Consent Page Presentation

The consent page displays requested scopes in a table with checkboxes, scope names, and descriptions. When the total scope count exceeds 10 and at least one required scope exists, required scopes are displayed in a separate collapsible section preceding the main table, labeled with a "Required" chip. The main table includes a search input, filter buttons (**All**, **Selected**, **Unselected**), and bulk action buttons (**Select all**, **Clear all**) when more than one scope is presented. A selection counter displays the number of approved scopes. The **Allow** button is disabled until at least one scope is selected.

The following table describes the UI elements and their behavior:

| UI Element | Visibility Condition | Behavior |
|:-----------|:---------------------|:---------|
| Search input | Total scope count > 10 | Filters rows by matching scope key or description (case-insensitive) |
| Filter buttons | Total scope count > 10 | Toggle row visibility based on checkbox state |
| Bulk action buttons | Total scope count > 1 | Check or uncheck all non-disabled checkboxes |
| Selection counter | Always visible | Displays "{0} of {1} selected" |
| Required scopes section | Total scope count > 10 AND required scopes exist | Collapsible section with required scopes; toggle expands or collapses |
| **Allow** button | Always visible | Disabled when no scopes are selected |

## Prerequisites

Before configuring selective scope approval, ensure the following:

* The application must be configured with at least one scope in its OAuth settings.
* For required scopes to be enforced, the application's scope settings must include at least one scope with the **Required** flag enabled.
* Users must authenticate successfully before reaching the consent page.

## Create an Application with Selective Scope Approval

To configure selective scope approval for an application, complete the following steps:

1. Open **Applications**.
2. Click your application.
3. Click **Settings**.
4. Click **OAuth 2.0 / OIDC**.
5. Scroll to the **Scopes** section.
6. Add one or more scopes to the application's allowed scope list by entering the scope key and optional name.
7. For each scope, configure the following options in the table:
    * Toggle **Default** to include the scope automatically in authorization requests that don't specify any scopes.
    * Toggle **Required** to mark the scope as mandatory. Users won't be able to deselect it on the consent page.
    * Set **User Consent** duration to define how long your approval is remembered before consent is requested again.
8. Toggle **Preselect consent for all scopes** to control the default checkbox state on the consent page. When enabled, all requested scopes are checked by default, and users can deselect individual permissions. When disabled, no scopes are preselected, and users must explicitly opt in to each permission.
9. Click **Save**.

The following table describes the scope configuration fields:

| Field | Description | Example |
|:------|:------------|:--------|
| Scopes | Scope key and optional display name | `read`, `write`, `admin` |
| Default | When enabled, the scope is added to authorization requests that don't specify any scopes | Checked for `read` |
| Required | When enabled, the scope is mandatory and users can't deselect it during consent | Checked for `admin` |
| User Consent | Duration (in seconds, minutes, hours, or days) that your approval is remembered | `3600` seconds |
| Preselect consent for all scopes | When enabled, all requested scopes are checked by default on the consent page | Enabled |

{% hint style="info" %}
When **Preselect consent for all scopes** is enabled, all requested scopes are checked by default on the consent page. You can still change individual selections before approving.
{% endhint %}

Add scopes to define which permissions this client is allowed to request. Only the scopes listed here can be granted during authorization. Any scope a client requests outside this list is rejected. Each scope can be refined with the following options:

* **Default**—added to the authorization request automatically when the client starts an authorization flow without requesting any specific scopes. When **Enhance scopes** is enabled, the authenticating user's role scopes are also granted when the request carries no scope, or only `openid`.
* **Required**—mandatory scopes that you can't deselect on the consent screen when they are requested. They must be consented to for the authorization request to be allowed.
* **User Consent**—how long your approval of the scope is remembered before consent is requested again.

## Approve Scopes During Authorization

When you initiate an OAuth 2.0 authorization flow, the gateway checks for prior consent. If no prior consent exists for the requested scopes, or if the authorization request includes `prompt=consent`, you are presented with a consent page. The consent page displays all requested scopes (or only new scopes if some were previously approved) in a table with checkboxes. If the application has **Opt-In Scope Selection** disabled, all scopes are preselected. If enabled, no scopes are preselected, and you must explicitly check each permission.

Required scopes are displayed as checked and disabled checkboxes. When the total scope count exceeds 10 and at least one required scope exists, required scopes appear in a separate collapsible section preceding the main table, labeled "{0} required permissions (always included)". You can expand or collapse this section by clicking the header. A "Required" chip is displayed next to each required scope's name.

You can search for scopes using the search input (visible when total scope count > 10), filter scopes by selection state using the filter buttons (**All**, **Selected**, **Unselected**), or use the bulk action buttons (**Select all**, **Clear all**) to check or uncheck all non-disabled checkboxes. The selection counter displays the number of approved scopes in the format "{0} of {1} selected". The **Allow** button is disabled until at least one scope is selected.

When you click **Allow**, the gateway validates that all required scopes are approved. If any required scope is missing or set to false in the submitted form, the server responds with HTTP 403 and OAuth error `access_denied`, displaying the message "Consent could not be verified". You are redirected back to the login page with the error. If all required scopes are approved, the gateway narrows the authorization request's scope set to only the approved scopes and persists the consent with `APPROVED` status for each granted scope.

If you click **Deny**, all scopes are denied, and the authorization request is rejected. No `access_denied` error is raised. Your explicit rejection is honored. The gateway persists `DENIED` status for all presented scopes, including required scopes.

The following table summarizes the consent flow outcomes:

| User Action | Required Scopes Approved | Outcome |
|:------------|:-------------------------|:--------|
| Clicks **Allow** | Yes | Authorization proceeds with approved scopes; consent is persisted |
| Clicks **Allow** | No (missing or false) | HTTP 403 `access_denied`; consent isn't persisted; you are redirected to the login page |
| Clicks **Deny** | N/A | All scopes are denied; authorization is rejected; consent is persisted with `DENIED` status |

**Incremental consent:** If some scopes were previously approved, only the new scopes not yet approved are presented on the consent page (unless `prompt=consent` is used to force re-presentation of all scopes). Required-scope validation applies only to presented scopes. If a required scope was previously approved and isn't re-presented, the server doesn't re-validate its approval during the current authorization request.

**Behavioral changes from prior versions:**

* **Before selective scope approval:** The consent page displayed all requested scopes as static text with hidden inputs. You could only approve or deny the entire request by clicking **Accept** or **Cancel**.
* **After selective scope approval:** The consent page displays scopes as checkboxes. You can selectively approve individual scopes. The default behavior is preserved. **Opt-In Scope Selection** defaults to disabled (all scopes preselected), matching the legacy "Accept all" behavior. Newly created applications have **Opt-In Scope Selection** enabled by default.
* **Before required scopes:** No concept of required scopes existed. You could deselect any scope.
* **After required scopes:** Scopes flagged as required are rendered as checked and disabled. The server enforces approval of required scopes. Missing approval triggers `access_denied`. The **Required** flag defaults to disabled for all existing scope settings.

**Known limitations:**

* **Scope ordering:** Required scopes are always displayed first in the consent page's ordered scope list. This ordering can't be customized.
* **Collapsible required section threshold:** The separate collapsible section for required scopes is only rendered when the total scope count exceeds 10 and at least one required scope exists. Below this threshold, required scopes are displayed inline with optional scopes in the main table.
* **Bulk actions skip disabled checkboxes:** The **Select all** and **Clear all** buttons don't affect required scopes (which are rendered as disabled checkboxes).
* **Search and filter scope:** The search input and filter buttons operate only on the main scope table. Required scopes in the separate collapsible section aren't affected by these controls.
* **Consent persistence on rejection:** When you click **Deny**, the server persists `DENIED` status for all presented scopes, including required scopes. No `access_denied` error is raised in this case.
