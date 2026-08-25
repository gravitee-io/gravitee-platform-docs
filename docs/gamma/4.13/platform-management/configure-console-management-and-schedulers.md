---
hidden: false
noIndex: false
description: >-
  Name the console, set the URL Gravitee puts in the emails it sends, control
  who can register, and set how often the console polls.
---

# Configure console management and schedulers

The **Management & Schedulers** page holds console settings that apply to the whole organization. It's split into two cards. **Management** names the console, sets the URL used in outbound email links, and controls support and self-registration. **Schedulers** sets the polling intervals the console uses for tasks and for notifications.

These settings are stored at organization scope, so they apply to every environment in the organization.

## Open the Management & Schedulers page

The page sits in the **Organization** section, which is where the settings that apply across environments live.

To open it, complete the following steps:

1. From the Gamma console sidebar, select **Platform Management**.
2. Open the **Organization** section.
3. Navigate to **Management & Schedulers**.

The page subtitle reads "Name this organization console, decide who can register, and how often background tasks and notifications run."

<!-- TODO: Screenshot of the Management & Schedulers page showing the Management and Schedulers cards -->
<figure><img src="../.gitbook/assets/PLACEHOLDER-gamma-platform-management-and-schedulers.png" alt=""><figcaption><p>The Management &#x26; Schedulers page of the <strong>Organization</strong> section</p></figcaption></figure>

Every page in this group opens with a note that the configuration may be overridden by a local configuration file. The next section explains what that means for an individual field.

## Understand which fields you can edit

Two separate things decide whether a field accepts input: your own access, and where the value comes from.

If your role can read these settings but not change them, the page opens with the message "You do not have permission to modify these settings. Contact your administrator for access." and every control is inert.

If a setting is supplied by the Management API configuration file or by an environment variable, that file wins over anything stored for the organization. The field is disabled and carries the tooltip **Configuration provided by the system**. Removing the setting from the configuration file and restarting the Management API is what returns the field to the console.

The following table maps each field on this page to the configuration setting that locks it:

<table><thead><tr><th width="330">Field</th><th>Configuration key</th></tr></thead><tbody>
<tr><td><strong>Title</strong></td><td><code>management.title</code></td></tr>
<tr><td><strong>Management URL</strong></td><td><code>management.url</code></td></tr>
<tr><td><strong>Activate Support</strong></td><td><code>console.support.enabled</code></td></tr>
<tr><td><strong>Allow User Registration</strong></td><td><code>console.userCreation.enabled</code></td></tr>
<tr><td><strong>Enable automatic validation of registration requests</strong></td><td><code>console.userCreation.automaticValidation.enabled</code></td></tr>
<tr><td><strong>Tasks (in seconds)</strong></td><td><code>console.scheduler.tasks</code></td></tr>
<tr><td><strong>Notifications (in seconds)</strong></td><td><code>console.scheduler.notifications</code></td></tr>
</tbody></table>

**Management URL** locks for a second reason as well. When the installation configuration sets a console URL for the organization, the page shows that URL and the field is read-only, whatever is stored for the organization.

## Configure the management settings

The **Management** card carries two text fields and up to three toggles.

### Title

**Title** names the APIM Console. The value becomes the browser tab title of the APIM Console, and it defaults to `Gravitee.io Management`. When your installation carries a console customization that supplies its own title, that title is used instead.

The Gamma console doesn't read this value, so changing it doesn't rename the Gamma console.

### Management URL

**Management URL** is the base URL of the APIM Console. Gravitee builds the links it puts into its outbound mail from this value, such as the registration and password-reset links in user emails. It also builds the redirect that returns a user to the console after an external login.

Enter the address your users reach the console at, including the scheme. When no console URL is configured anywhere, Gravitee falls back to `http://localhost:4000` and records a warning in the Management API log. The links in your emails then point nowhere useful.

### Activate Support

**Activate Support** controls whether support tickets can be opened for this organization. It's on by default.

When it's on, the APIM Console offers a **Support** entry and the platform accepts the ticket. When it's off, the entry is hidden and the platform refuses the ticket.

### Allow User Registration

**Allow User Registration** controls whether people can register a console account themselves. It's on by default.

When it's off, a self-registration attempt is refused. It doesn't affect accounts an administrator creates from the **Users** page, which are created as Active whatever this toggle says. For those, see [Manage users](manage-users.md).

### Enable automatic validation of registration requests

**Enable automatic validation of registration requests** only appears while **Allow User Registration** is on, and it's on by default. It decides what happens to an account that someone registers themselves.

When it's on, the new account is created Active, and the person receives the email that lets them finish setting up their account.

When it's off, the new account is created Pending and the person receives no email. A registration-request notification is sent instead, so that an administrator can review the request and accept or reject it from the **Users** page.

## Set the scheduler intervals

The **Schedulers** card sets how often the console asks the Management API for new items, in seconds. Both fields default to `10`.

A shorter interval surfaces new items faster, at the cost of more requests to the Management API.

### Tasks (in seconds)

**Tasks (in seconds)** sets how often the console refreshes the tasks it shows you, such as subscriptions waiting on your approval.

Both the Gamma console and the APIM Console use this value. The Gamma console reads it once when the tasks view first loads, so a new interval takes effect the next time the console is loaded rather than immediately.

A value of `0` doesn't stop the polling. Both consoles treat it as unset and fall back to 10 seconds.

### Notifications (in seconds)

**Notifications (in seconds)** sets how often the APIM Console refreshes the notifications shown in its notification list.

The Gamma console has no notification poller of its own, so this value changes the APIM Console only.

A value of `0` is treated the same way as it is for tasks: the APIM Console falls back to 10 seconds.

## Save or discard your changes

Nothing is written until you save. As soon as a value differs from what's stored, a bar appears at the bottom of the page with **Discard** and **Save changes**.

To keep your changes, click **Save changes**. The button stays disabled while either scheduler field holds something other than a whole number of zero or more. A toast reading "Configuration successfully saved!" confirms the write, and a toast reading "An error occurred while saving the configuration." reports a failure.

To abandon your changes, click **Discard**. The form returns to the values last read from the Management API and the bar disappears.

{% hint style="info" %}
Saving is refused while the platform is in maintenance mode. The Management API answers with `503` and the message "The server is currently in maintenance mode. Please retry later or contact your administrator."
{% endhint %}

Each of the three organization settings pages sends the whole configuration back to the Management API, with only its own section changed. It works from the copy it read when it loaded, so reload the page before saving if someone else may have changed the organization's settings in the meantime.
