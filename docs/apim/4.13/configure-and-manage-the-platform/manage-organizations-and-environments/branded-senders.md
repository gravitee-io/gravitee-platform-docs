---
description: Configure branded sender rules so that notification emails use a different From address and subject prefix per recipient domain.
---
# Branded Senders

## Overview

By default, every notification email that APIM sends uses a single sender address and subject prefix, taken from your SMTP configuration. Branded senders let you override that pair for specific recipient domains. The people who receive those notifications then see an address on your own domain instead of the platform default.

For example, a rule that lists the domain `example.com` with the From address `noreply@example.com` means that a subscription approval sent to `alice@example.com` arrives from `noreply@example.com`, while the same notification sent to `bob@partner.org` still arrives from the default address.

{% hint style="warning" %}
Rules are matched on the **recipient's** email domain, not on the API, the application, or the publisher. A rule applies to everyone you send mail to at the listed domains, across every notification type.
{% endhint %}

A rule changes only the sender address and the subject prefix. The body of each notification is unchanged, and is still customized through the Notification Templates page.

Branded senders can be configured at three scopes:

- **Organization scope** — Console settings (organization-wide branding)
- **Environment scope** — Portal settings (environment-level override)
- **System scope** — `gravitee.yml` or environment variable

## Prerequisites

- The SMTP email service must be **enabled** (`email.enabled`) at the Organization or Environment level. Branded sender controls are disabled while email is off.
- The **Default From** and **Default subject prefix** (`email.from`, `email.subject`) must be configured; they are used whenever no rule matches.
- To save or reset branded senders at the **Environment** scope, you need the `ENVIRONMENT_SETTINGS` permission with `UPDATE` access. Without it, the branded-senders control is disabled and **Reset to Org settings** is hidden.
- To save branded senders at the **Organization** scope, you need the `ORGANIZATION_SETTINGS` permission with `UPDATE` access. Without it, the whole settings form is read-only.
- If `email.branded_senders` is provided by system configuration and is valid, the console field remains read-only even after toggling email on.

## Prepare Each Sending Domain

A branded message claims to come from your domain while being sent by your SMTP relay. Two separate things have to be arranged before such a message reaches anyone: the relay has to accept it, and the receiving mail server has to trust it.

### Confirm That Your Relay Accepts the Branded Sender

Many SMTP providers only accept a message whose sender address matches the account used to authenticate. A branded **From** on a different domain doesn't match, so those providers refuse it.

They refuse it in one of two ways, and the difference matters:

- **Rejected at submission.** APIM records the failure, and the SMTP error appears in the Management API log.
- **Accepted and then discarded.** APIM records a successful send, no bounce is produced, and the message never arrives. Nothing in the log indicates a problem.

{% hint style="warning" %}
Because of the second case, a successful send isn't evidence that a branded rule works. Send a branded notification to yourself and confirm that it **arrives** before you apply a rule to real recipients.
{% endhint %}

If your relay restricts senders, ask your email provider what's needed to send as an additional domain. Providers usually require you to prove that you control the domain first.

### Authorize the Relay in Your DNS

Receiving mail servers check whether the sending relay is allowed to use your domain. Publish the following records for every domain you put in the **From** field:

| Record | Purpose |
|:-------|:--------|
| **SPF** | Authorizes the relay to send mail for your domain. Add the relay to your existing SPF record rather than creating a second one, because a domain must publish only one SPF record. |
| **DKIM** | Publishes the public key used to sign outbound mail, so receivers can verify the message wasn't altered and came from an authorized sender. |
| **DMARC** | Tells receivers what to do when a message fails authentication, and where to send reports. Start with a monitoring policy such as `p=none` and review the reports before you tighten it. |

The values to publish depend on which relay you send through, so get them from your email provider. Note that a message needs only one of SPF or DKIM to align with the **From** domain for DMARC to pass.

{% hint style="danger" %}
Without these records, branded notifications are likely to be marked as spam or rejected, especially by strict receivers and by any domain publishing a `p=reject` DMARC policy.
{% endhint %}

The APIM console doesn't verify that you own the domain in the **From** field, and it doesn't check your DNS records before sending. A rule that names a domain you don't control is saved and used, and its messages fail authentication at the receiver.

## How Branded Senders Are Matched

When a notification is sent, the APIM console takes the domain from each recipient address, which is the part after `@`, and compares it against the domains on each rule in order. The **first rule that matches wins**. The comparison ignores case, so `Example.com` and `example.com` are the same domain. Both bare addresses (`user@example.com`) and display-name form (`Name <user@example.com>`) are accepted.

**Fallback conditions** — the default `email.from` and `email.subject` are used when:

- No configuration matches the recipient's domain
- The recipient value contains more than one `@` (a multi-address list, in either form)
- The domain cannot be parsed from the recipient address
- The recipient value is blank or malformed
- The matched configuration has no recipient domains declared
- Two configurations list the same domain — the first one wins (the console rejects duplicates, but a manually edited stored value may still contain them)

### Message Grouping

Recipients are grouped by the resolved `(From, Subject)` pair. One message is sent per group, so recipients on different branded domains never appear in the same message. When no configuration is set, or when all recipients resolve to the same sender, a single message is sent exactly as before.

| Condition | Result |
|:---|:---|
| Matched configuration has a blank **From** | Default `email.from` used; branded subject kept |
| Matched configuration has a blank **Subject prefix** | Default `email.subject` used; branded From kept |
| Caller supplies an explicit From | Branding skipped: one unbranded message with the default subject template |
| Self-send notifications (platform mailing its own default address) | Not branded; sent with the default identity |
| Publisher broadcast to subscribers (delivered via Bcc) | Bcc recipients are branded by domain; no spurious default-identity message is emitted when every recipient matches a brand |
| Copy to sender | The sender's own copy uses the default identity and merges into the default group when one exists |
| Reply-To | Preserved on all messages, including branded ones |
| Branded From with a display name (`Example Team <noreply@example.com>`) | Honoured as-is |
| Branded bare From plus a notification sender name | The sender name is stamped onto the branded address |

Bcc-only groups are sent without a `To` header, matching existing notification behaviour. Sending is fail-fast: if one group fails, the notification fails with `Error while sending email notification`.

## Branded Sender Rule Fields

Each rule has three fields:

| Field | Description | Constraints |
|:------|:------------|:------------|
| **Recipient domains** | The recipient email domains the rule applies to. | Required, at least one. Each entry must be a valid domain name, such as `example.com`. Alphabetic or ACE/punycode IDN TLDs such as `xn--p1ai` are accepted. |
| **From** | The sender address used for those recipients. | Required. Accepts a bare address such as `noreply@example.com`, or the display-name form `Example Team <noreply@example.com>`. |
| **Subject prefix** | The subject prefix applied to those messages. | Optional, maximum 255 characters. Use `%s` where the notification's own subject should appear. If you leave this blank, the default subject prefix is used. |

A domain can appear in only one rule. The APIM Console rejects duplicates across rules when you save the form. The combined size of all configurations must stay within the save limit (approximately 4,000 characters).

### Subject Prefix Templates

Subject templates are substituted as follows:

- `%s` and `%1$s` are both replaced with the email's title
- Every other `%` sequence is emitted as typed
- A stray `%` is kept literal — for example, `100% off %s` → `100% off Approved`
- `%n` is **not** expanded into a newline — for example, `[Example]%n %s` → `[Example]%n Approved`

Existing templates using `%s` or `%1$s` continue to work unchanged.

### Field Validation Reference

| Field | Rule | Message |
|:---|:---|:---|
| **Recipient domains** | At least one domain required | `At least one domain is required.` |
| **Recipient domains** | Each entry must be a valid dot-separated host name (case-insensitive); alphabetic or ACE/punycode IDN TLDs accepted | `Invalid domain(s): <list>` |
| **Recipient domains** | A domain may appear in only one configuration (case- and whitespace-insensitive) | `Each domain may only be used in one configuration. Used more than once: <list>.` |
| **From** | Required | `From is required.` |
| **From** | Bare address or `Name <user@example.com>` form | `Enter a valid email address, optionally with a display name.` |
| **Subject prefix** | Maximum 255 characters | `Must be at most 255 characters.` |
| All configurations | Combined size must stay within the save limit (approximately 4,000 characters) | `These configurations are too large to save. Remove some domains or configurations and try again.` |

Console format checks are intentionally lenient usability aids; the server remains the authority on what can be saved and rejects invalid, oversized, or empty-entry payloads.

## Configure Branded Senders in the APIM Console

Go to **Settings > Settings**, scroll to the **SMTP** card, and find the **Branded notification email** subsection, which follows the **Mail properties** subsection. It also shows a read-only **Default notification email** preview — *Used when no branded rule matches the recipient's email domain* — listing the **Default From** and **Default subject prefix** that apply to any recipient no rule matches. The **Default subject prefix** hint reminds you that `%s` is replaced with the email's subject.

1. Click **Add configuration** to add a rule. This creates a card titled **Configuration {N}**.

    {% hint style="info" %}
    **Add configuration** is disabled when email is disabled, when the value is set in `gravitee.yml` and therefore read-only, or when you lack the `ENVIRONMENT_SETTINGS` permission with `UPDATE` access.
    {% endhint %}

2. In the **Recipient domains** field, enter one or more domains. The placeholder text is `example.com, eu.example.com`. Matching is case-insensitive on the part after `@` in the recipient address. Domains are trimmed and lower-cased before saving.

3. In the **From** field, enter the sender address to use for those domains. The placeholder text is `noreply@example.com`. A display name is allowed — for example, `Example Team <noreply@example.com>`. The **From** value is trimmed before saving.

4. In the **Subject prefix** field, optionally enter a prefix such as `[Example] %s`. The subject is stored exactly as typed.

5. To remove a rule, click the **Delete** trash icon on its card.

6. Repeat for any further rules. Rules are matched in order, so put your most specific rules first.

7. Save the form.
   - **Portal settings** success: `Settings successfully updated!`
   - **Organization general settings** success: `Configuration successfully saved!`
   - On failure, the server message is shown, falling back to `An error occurred while saving the settings.` or `An error occurred while saving the configuration.`

### Inheritance Between Scopes

The effective value is resolved in the following order:

1. **System configuration** (`gravitee.yml` or environment variable)
2. **Environment override** (Portal settings)
3. **Organization value** (Console settings)

An Environment inherits the Organization's rules until you save rules of your own at the Environment scope. While it's inheriting, each rule card shows an **Inherited from Org** badge, and **Reset to Org settings** is unavailable because there's nothing to reset. The badge disappears as soon as you edit a card, before you save. A freshly loaded server value — after save, discard, or reset — restores the badge.

Saving an **empty** list at the Environment scope isn't the same as inheriting. It stores an explicit "no branded senders" override, and the Organization rules no longer apply. To restore inheritance, use **Reset to Org settings**.

If `email.branded_senders` is set in `gravitee.yml` or by an environment variable, that value takes precedence over both scopes. The Environment doesn't inherit from the Organization, and the field is read-only in both. When a valid system value is in effect, console saves do not persist an organization or environment value.

## Reset Environment Rules to the Organization Settings

**Reset to Org settings** is available at the Environment scope when all the following are true:

- An Environment-level override exists.
- Email is enabled.
- The value isn't set in `gravitee.yml`.
- You have the `ENVIRONMENT_SETTINGS` permission with `UPDATE` access.

**Reset procedure:**

1. Navigate to **Environment → Portal settings** and open the **Email** card.
2. Click **Reset to Org settings**.
3. If the form has unsaved changes, a **Reset branded senders** dialog opens with the message:
   *You have unsaved changes on this page that will be discarded. Do you want to reset the branded senders to the organization configuration?*
   Click **Reset** to continue. If the form is clean, the reset is applied immediately.
4. On success, the snackbar `Branded senders reset to the organization configuration.` is shown, the settings reload, the inherited configuration appears with the **Inherited from Org** badge, and the **Reset to Org settings** button disappears. On failure the server message is shown, falling back to `An error occurred while resetting the branded senders.`

Clicking **Reset to Org settings** removes the Environment override, so the Environment inherits from the Organization again. If you have unsaved changes on the page, the APIM Console asks you to confirm before discarding them.

## Manage Branded Senders at the Organization Scope

The same **Branded notification email** subsection is available in the **SMTP** section of **Organization > Settings**. It behaves as it does at the Environment scope, with these differences:

- There's no **Reset to Org settings** button, because the Organization is the top scope. `brandedSendersInherited` is always `false` at organization scope.
- The control is disabled when email is disabled, or when `email.branded_senders` is set in `gravitee.yml`.
- The entire settings form is disabled when you lack the `ORGANIZATION_SETTINGS` permission with `UPDATE` access.

## Configure Branded Senders for a Self-Hosted Installation

Branded senders can be set outside the APIM Console, alongside the rest of your [SMTP configuration](smtp-configuration.md). A value set this way applies to every Organization and Environment on the installation and makes the APIM Console field read-only.

### Gateway Configuration Properties

| Property | Description | Example |
|:---|:---|:---|
| `email.branded_senders` | Branded-sender configurations, as a native YAML list or a JSON string. When set at system scope and valid, it is applied and the console field is read-only. | See below |
| `email.branded_senders[N].domains` | Recipient domains this configuration applies to (list of strings; a bare scalar is also accepted). | `[example.com]` |
| `email.branded_senders[N].from` | From address used for matching recipients. | `noreply@example.com` |
| `email.branded_senders[N].subject` | Subject prefix template used for matching recipients. | `[Example] %s` |
| `gravitee_email_branded_senders` | Flat environment-variable form: a JSON array of `{domains, from, subject}`. Normalised identically to the YAML list. | `[{"domains":["example.com"],"from":"noreply@example.com","subject":"[Example] %s"}]` |
| `email.from` | Default From used when no branded configuration matches. | `default@gravitee.io` |
| `email.subject` | Default subject template used when no branded configuration matches. | `[Gravitee.io] %s` |
| `email.enabled` | When `false`, the branded-senders console control is disabled. | `true` |

{% tabs %}
{% tab title="gravitee.yaml" %}
Add a `branded_senders:` list to the `email:` section of the Management API `gravitee.yml` file:

```yaml
email:
  host: smtp.my.domain
  port: 465
  from: noreply@my.domain
  subject: "[Gravitee.io] %s"
  branded_senders:
    - domains:
        - example.com
        - eu.example.com
      from: noreply@example.com
      subject: "[Example] %s"
    - domains:
        - partner.example.org
      from: Partner Team <partners@example.org>
      subject: "[Partner] %s"
```
{% endtab %}

{% tab title=".env" %}
A list can't be expressed as a single environment variable, so supply the value as a JSON array instead:

```bash
gravitee_email_branded_senders=[{"domains":["example.com","eu.example.com"],"from":"noreply@example.com","subject":"[Example] %s"}]
```

Docker Compose example:

```yaml
- gravitee_email_branded_senders=[{"domains":["example.com"],"from":"noreply@example.com","subject":"[Example] %s"}]
```
{% endtab %}

{% tab title="Helm values.yaml" %}
Add `branded_senders` to the top-level `smtp:` section of your `values.yaml`. The APIM Helm chart renders the `smtp:` values into the Management API `gravitee.yml` `email:` block at install time:

```yaml
smtp:
  enabled: true
  host: smtp.my.domain
  port: 465
  from: noreply@my.domain
  subject: "[Gravitee.io] %s"
  branded_senders:
    - domains:
        - example.com
        - eu.example.com
      from: noreply@example.com
      subject: "[Example] %s"
```
{% endtab %}
{% endtabs %}

{% hint style="info" %}
If the value is invalid or oversized, APIM writes the problem to the Management API log and ignores it. The effective value falls through to the environment, organization, or default value, and the APIM Console field stays editable and shows no error. Check that log if a self-hosted configuration doesn't take effect.
{% endhint %}

An entry declared without `domains` is reported as:
`Branding entry '{}[{}]' has no 'domains'; it will never match a recipient`

## Management API Reference

### Email Settings Payload

The `email` object appears in both Console settings (organization scope) and Portal settings (environment scope):

```json
{
  "email": {
    "enabled": true,
    "host": "...",
    "port": 1025,
    "subject": "[Gravitee.io] %s",
    "from": "default@gravitee.io",
    "brandedSenders": [
      {
        "domains": ["example.com", "eu.example.com"],
        "from": "noreply@example.com",
        "subject": "[Example] %s"
      }
    ],
    "brandedSendersInherited": false
  }
}
```

| Field | Type | Scope | Description |
|:---|:---|:---|:---|
| `email.brandedSenders` | Array of `{domains: string[], from: string, subject: string}` | Organization + Environment | Branded-sender configurations. |
| `email.brandedSendersInherited` | Boolean (default `false`) | Environment responses only | `true` only when no environment override exists **and** no valid system value is in effect. Does **not** imply the organization has a non-empty configuration. Always `false` at organization scope. |

### Reset Endpoint

| Method | Path (environment-scoped) | Permission | Responses |
|:---|:---|:---|:---|
| `POST` | `/settings/email/branded-senders/reset` | `ENVIRONMENT_SETTINGS` + `UPDATE` | `200` refreshed portal settings, `403` missing update permission, `404` environment does not exist, `500` internal server error |

The request body is empty. The endpoint deletes the environment override so the value falls back through the cascade (organization, or system configuration if set) and returns the refreshed portal settings.
