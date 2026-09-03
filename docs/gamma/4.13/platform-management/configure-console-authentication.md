---
hidden: false
noIndex: false
description: >-
  Decide whether the Gamma console sign-in page shows the local login form, and
  add, edit, activate, and delete the identity providers that users sign in with.
---

# Configure console authentication

The **Authentication** page decides how people sign in to the Gamma console. It holds a toggle that shows or hides the local username and password form. It also lists the identity providers registered in the organization, with a switch that puts each one on the sign-in page.

An identity provider lets people sign in with an external account, from Gravitee Access Management, an OpenID Connect server, Google, or GitHub, instead of a local Gravitee password. A provider also carries optional group and role mappings, which assign Gravitee groups and roles to a user at sign-in from what the provider returns about them.

Identity providers and the local login setting belong to the organization, so they apply whichever environment is selected.

## Open the Authentication page

The page sits in the **System & Security** group of the **Organization** section, with the other settings that apply across environments.

To open it, complete the following steps:

1. From the Gamma console sidebar, select **Platform Management**.
2. Open the **Organization** section.
3. Under **System & Security**, select **Authentication**.

The page subtitle reads "By creating an identity provider, you are providing capabilities to users to login into the portal / management UI using external user accounts from GitHub, Google, OpenID Connect server or Gravitee.io AM."

<!-- TODO: Screenshot of the Authentication page showing the Show login form toggle and the Identity Providers table -->
<figure><img src="../.gitbook/assets/PLACEHOLDER-gamma-platform-authentication.png" alt=""><figcaption><p>The Authentication page of the <strong>Organization</strong> section</p></figcaption></figure>

The page is listed only for a role that reads organization settings and identity providers. If your role reads providers but doesn't change them, the **Add an identity provider** button and the row actions are hidden, and the provider pages open read-only.

### Read the Identity Providers table

The **Identity Providers** card lists each provider with the following columns:

* **Name**. The provider's display name. Select it to open the provider's edit page.
* **Id**. The identifier generated from the name when the provider was created.
* **Status**. **Activated** when the provider is offered on the console sign-in page, and **Deactivated** otherwise.
* **Type**. **Gravitee.io AM**, **OpenID Connect**, **Google**, or **GitHub**.
* **Description**. The description entered on the provider.
* **Sync**. A check mark when group and role mappings are computed at every sign-in.
* **Available on dev portal**. A check mark when the provider's **Allow portal authentication to use this identity provider** setting is on.
* **Updated at**. When the provider was last saved.

Use the search field to filter by name, ID, type, or description. Typing `activated` or `deactivated` filters on status. Sort by any column from its header. The table paginates 10 rows at a time by default, and offers 25, 50, and 100.

When the organization has no provider yet, the card shows the **No identity providers yet** panel instead of the table, with an **Add an identity provider** button.

## Understand what reaches the sign-in page

The console sign-in page is assembled from this page's settings each time it loads:

* When the local login form is on, the sign-in page shows the **Username** and **Password** fields and the **Sign in** button.
* A provider appears as a **Sign in with** button carrying its name when its status is **Activated** and its **Allow portal authentication to use this identity provider** setting is on. Buttons are listed in alphabetical order of name. When the form and at least one button are shown, an **or** separator sits between them.
* When the form is off and no provider qualifies, the sign-in page reports **Sign-in unavailable** with the message "No login method available. Please contact your administrator."

{% hint style="warning" %}
Turn the local login form back on before you deactivate or delete the last activated provider. Neither action is blocked, and with the form off and no activated provider left, the sign-in page offers no way in.
{% endhint %}

Activation on this page applies to the console. Whether a provider is offered on a Developer Portal is a separate, per-environment activation that this page doesn't manage.

## Show or hide the local login form

The **Show login form on management console** toggle at the top of the page controls the username and password form. It's on by default.

To hide the form, turn the toggle off. To show it again, turn it on. The change is saved as soon as the toggle moves, and the page confirms with **Configuration successfully updated!**

The toggle is disabled in the following cases. When more than one applies, the description under the toggle names the first in this list:

* The identity providers or the settings couldn't be loaded. The description reads **Identity provider settings could not be loaded**.
* The setting is supplied by the Management API configuration file or an environment variable, as `console.authentication.localLogin.enabled`. The description reads **Configuration provided by the system**, and the value from that configuration wins over anything saved for the organization.
* Your role doesn't change organization settings. The description reads **You do not have permission to modify these settings. Contact your administrator for access.**
* No identity provider is activated yet. The description reads **You must create and activate an identity provider to be able to update this setting**, because hiding the form without a provider would leave no way to sign in.

While the organization is in maintenance mode, the save is refused and the page shows the refusal message from the Management API.

## Add an identity provider

Before you start, register the Gamma console as a client with the provider, and keep the client ID and client secret it issued at hand. How you register a client is the provider's own concern.

To add a provider, complete the following steps:

1. From the Authentication page, select **Add an identity provider**.
2. Under **Provider type**, select **Gravitee.io AM**, **OpenID Connect**, **Google**, or **GitHub**. Changing the type later clears the **Configuration** and **User profile mapping** fields.

    <!-- TODO: Screenshot of the Create a new identity provider page showing the Provider type cards -->
    <figure><img src="../.gitbook/assets/PLACEHOLDER-gamma-platform-authentication-create.png" alt=""><figcaption><p>The <strong>Provider type</strong> cards of the Create a new identity provider page</p></figcaption></figure>

3. Under **General**, enter the settings described in the following table:

    | Field                                                            | Description                                                                                                                                                                                  | Required |
    | ---------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | -------- |
    | **Name**                                                         | The provider's display name, 2 to 50 characters. It generates the provider's ID and labels the provider's button on the sign-in page.                                                       | Yes      |
    | **Description**                                                  | A description of the provider, shown in the table.                                                                                                                                           | No       |
    | **Allow portal authentication to use this identity provider**    | Whether the provider is offered on sign-in pages. On by default. Together with the provider's activation, it decides whether the provider appears on the console sign-in page.              | -        |
    | **A public email is required to be able to authenticate**        | When on, a sign-in whose profile carries no email address is refused. On by default.                                                                                                         | -        |
    | **Group and role mappings**                                      | **Computed only during first user authentication**, the default, or **Computed during each user authentication**. See [Map groups and roles](#map-groups-and-roles).                        | -        |

4. Under **Configuration**, enter the settings for the selected type. **Client Id** and **Client Secret** are required for every type. Google and GitHub take nothing else. The following table lists the other fields of Gravitee.io AM and OpenID Connect:

    | Field                             | Type            | Description                                                                                                                                                                      | Required                |
    | --------------------------------- | --------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ----------------------- |
    | **Server URL**                    | Gravitee.io AM  | The URL of the Access Management instance.                                                                                                                                       | Yes                     |
    | **Security domain**               | Gravitee.io AM  | The security domain that holds the client.                                                                                                                                       | Yes                     |
    | **Token Endpoint**                | OpenID Connect  | The provider's token endpoint.                                                                                                                                                   | Yes                     |
    | **Token Introspection Endpoint**  | OpenID Connect  | The provider's token introspection endpoint.                                                                                                                                     | No                      |
    | **Authorize Endpoint**            | OpenID Connect  | The provider's authorization endpoint.                                                                                                                                           | Yes                     |
    | **UserInfo Endpoint**             | OpenID Connect  | The provider's user info endpoint.                                                                                                                                               | Yes                     |
    | **UserInfo Logout Endpoint**      | OpenID Connect  | The provider's logout endpoint.                                                                                                                                                  | No                      |
    | **Scopes**                        | Both            | The scopes requested at sign-in. Type a scope and press Enter to add it. OpenID Connect starts with `openid`, `profile`, and `email`, and keeps at least one scope.              | Yes, for OpenID Connect |
    | **Authentication button color**   | Both            | The background color of the provider's button on the sign-in page, as a six-digit hex value such as `#1E90FF`. Pick it from the color picker or type it. Any other value is discarded. | No                 |

5. For Gravitee.io AM and OpenID Connect, under **User profile mapping**, map the provider's user info response to the Gravitee profile. Each value names the attribute of the response that fills the field. A value that contains an Expression Language expression is evaluated instead. The following table lists the fields:

    | Field          | Default       | Required |
    | -------------- | ------------- | -------- |
    | **ID**         | `sub`         | Yes      |
    | **First name** | `given_name`  | No       |
    | **Last name**  | `family_name` | No       |
    | **Email**      | `email`       | No       |
    | **Picture**    | `picture`     | No       |

    **ID** identifies the user across sign-ins. The first name, last name, picture, and email are refreshed from the provider at each sign-in. For Google and GitHub, the card doesn't appear.

6. Select **Create**.

The page confirms with **Identity provider successfully saved!** and opens the provider's edit page. The provider's ID is generated from its name. Accents are removed and letters are converted to lowercase. Characters other than letters, digits, spaces, and hyphens are dropped, and each run of spaces or hyphens becomes one hyphen. A name that generates an ID already in use is refused with "An identity provider with name [name] already exists."

A new provider is activated for the console as soon as it's created, so it reaches the sign-in page immediately when its portal setting is on.

{% hint style="info" %}
**OpenID Connect** requires an enterprise license that includes the OpenID Connect SSO feature. Without it, the card carries a lock icon. Selecting the card then opens the **OpenID Connect SSO** dialog, with a **Start a free trial** link, instead of switching the type. The Management API refuses to create an OpenID Connect provider without the license too.
{% endhint %}

## Edit an identity provider

To open a provider, select its name in the **Identity Providers** table. The heading reads **Update [type] identity provider**, and the page carries the **General**, **Configuration**, and **User profile mapping** cards from the create page, followed by the **Groups Mapping** and **Roles Mapping** cards. The provider type is fixed once the provider exists.

Change the fields, then select **Update**. The page confirms with **Identity provider successfully saved!** **Discard** returns every field to the saved values. Both buttons stay disabled until something has changed. Leaving the page with unsaved changes opens the **Unsaved changes** dialog, and the browser warns before the tab closes.

If your role reads providers but doesn't update them, the fields are disabled and the buttons are hidden.

## Map groups and roles

Mappings assign Gravitee groups and roles to a user at sign-in, based on what the provider returns about them. They're set on the provider's edit page, in the **Groups Mapping** and **Roles Mapping** cards, and saved with **Update**.

<!-- TODO: Screenshot of the Groups Mapping and Roles Mapping cards on the edit page -->
<figure><img src="../.gitbook/assets/PLACEHOLDER-gamma-platform-authentication-mappings.png" alt=""><figcaption><p>The <strong>Groups Mapping</strong> and <strong>Roles Mapping</strong> cards of a provider's edit page</p></figcaption></figure>

### Write a condition

Each mapping starts with a **Condition**: a Gravitee Expression Language expression that evaluates to `true` or `false`. It runs against three values from the sign-in:

* `#profile`. The provider's user info response, as a JSON string.
* `#accessToken`. The payload of the access token, when the token is a JWT.
* `#idToken`. The payload of the ID token, when the provider returned one.

The following condition matches users whose user info carries a `job_id` of `API_BREAKER`:

```text
{#jsonPath(#profile, '$.job_id') == 'API_BREAKER'}
```

A condition that fails to evaluate counts as not matched. Two mappings in the same card can't share a condition.

### Map groups

To add a group mapping, select **Add group mapping**, enter the **Condition**, and select at least one group under **Group**. The list holds every group of the organization, sorted by name. Select **Delete** in a mapping to remove it.

A membership granted this way carries the group's default API role and default application role, or the organization's default role for each of those scopes when the group sets none.

### Map roles

To add a role mapping, select **Add role mapping**, enter the **Condition**, and select at least one role under **Organization roles**. The table under it lists each environment of the organization, with its **Name**, **Description**, and **Roles selected**. Select roles in an environment's row to grant environment roles there. Environment roles are optional. Select **Delete** in a mapping to remove it.

### Understand when mappings apply

What happens at sign-in depends on the **Group and role mappings** setting in the **General** card:

* With **Computed only during first user authentication**, the mappings run when the user's account is created at their first sign-in. Later sign-ins leave the memberships alone, so roles and groups assigned by hand afterwards persist.
* With **Computed during each user authentication**, the mappings run at every sign-in. For each kind of membership, groups, organization roles, and environment roles, when the provider carries at least one mapping of that kind, the user's existing memberships of that kind are replaced by the mapping result, including memberships assigned by hand. When the provider carries no mapping of a kind, the user's existing memberships of that kind are kept.

When no role mapping matches, the user receives the organization's default organization role, and the default environment roles in the environment of the sign-in, or in the default environment when the sign-in isn't tied to one. A group named in a matched mapping that no longer exists is skipped.

## Activate or deactivate a provider for the console

Activation decides whether a provider is offered on the console sign-in page. The **Status** column shows **Activated** or **Deactivated** for each provider.

To change it, complete the following steps:

1. In the provider's row, open the actions menu.
2. Select **Activate** or **Deactivate**.
3. In the **Activate an Identity Provider** or **Deactivate an Identity Provider** dialog, select **Ok**.

The page confirms with **Identity Provider [name] successfully activated!** or **Identity Provider [name] successfully deactivated!**. A deactivated provider keeps its configuration and mappings. It only leaves the sign-in page.

## Delete an identity provider

Deleting a provider removes it from the organization and deactivates it wherever it was activated, on the console and on every Developer Portal.

To delete a provider, complete the following steps:

1. In the provider's row, open the actions menu.
2. Select **Delete**.
3. In the **Delete an Identity Provider** dialog, select **Delete**.

The page confirms with **Identity Provider [name] successfully deleted!**

## Verification

To verify that console authentication is working as expected, follow these steps:

1. From the Gamma console sidebar, select **Platform Management**.
2. Open the **Organization** section.
3. Under **System & Security**, select **Authentication**.
4. Select **Add an identity provider**.
5. Select a provider type, enter a name and the settings for that type, and select **Create**.
6. Confirm that the page reports **Identity provider successfully saved!** and opens the provider's edit page.
7. Select **Back to Authentication**.
8. Confirm that the provider appears in the **Identity Providers** table with the status **Activated**.
9. Open the console sign-in page in a private browser window, and confirm that it shows a **Sign in with** button carrying the provider's name.

<!-- TODO: Screenshot of the Identity Providers table showing the new provider with the Activated status -->
<figure><img src="../.gitbook/assets/PLACEHOLDER-gamma-platform-authentication-activated.png" alt=""><figcaption><p>The new provider listed with the <strong>Activated</strong> status</p></figcaption></figure>

## Next steps

* [Manage users](manage-users.md). Review the users who sign in through these providers, and the roles and group memberships they hold.
* [Configure console management and schedulers](configure-console-management-and-schedulers.md). Set the other organization-wide console settings.
