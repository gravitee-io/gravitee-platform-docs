---
description: Configure branded sender rules so that notification emails use a different From address and subject prefix per recipient domain.
---

# Branded Senders

## Overview

Branded sender rules can be configured at two scopes: **Organization** and **Environment**. Environment-level rules override the Organization rules when present. If no Environment-level override is saved, the Environment inherits from the Organization or system configuration.

The `brandedSendersInherited` flag in the Environment settings response is `true` when no Environment-level override exists and no valid system-configured value is in effect. At Organization scope, this flag is always `false`.

If you save an empty list, `[]`, at the Environment scope, the result is an **explicit empty override** that doesn't fall back to the Organization value. To remove the override entirely and restore inheritance, use the **Reset to Org settings** action.

### Domain Match Rules and Message Dispatch

When an email notification is dispatched, the backend extracts the domain from each recipient address. The domain is the part after `@`, and it's compared case-insensitively. The backend matches this domain against the `domains` list of each branded sender rule in list order, and the **first matching rule wins**.

Recipients that share the same resolved `(From, Subject)` pair are grouped together, and one message is sent per group.

The following recipients and scenarios fall outside branded dispatch:

- A recipient string that contains more than one `@`, such as a comma-separated multi-address string, isn't matched. The default sender identity is used instead.
- The `DEFAULT_MAIL_TO` sentinel address used for a publisher broadcast isn't itself matched. It's replaced with the default `EMAIL_FROM` address on the default identity message. The real recipients of a broadcast are in `bcc`, and they're branded like any other recipient.
- If the caller supplies an explicit `From` on the notification, branded sender logic is skipped entirely, and a single unbranded message is sent.
- Copies produced by `copyToSender` always use the default identity, `EMAIL_FROM` and `EMAIL_SUBJECT`, regardless of the recipient's domain.

### Branded Sender Rule Structure

Each rule contains the following three fields:

| Field | Description | Constraints |
|:------|:------------|:------------|
| **`domains`** | List of recipient email domains. The match is case-insensitive on the part after `@`. | Required. At least one domain. Valid domain format. No duplicates across rules. |
| **`from`** | Sender address for matching recipients. | Accepts a bare address such as `noreply@example.com`, or the display-name form `Example Team <noreply@example.com>`. Falls back to the default `EMAIL_FROM` if blank. |
| **`subject`** | Subject line prefix template. | Optional. Maximum 255 characters. `%s` or `%1$s` is replaced with the email's subject at send time. Stray `%` characters, `%n`, and width specifiers are treated as literal text. Falls back to the default `EMAIL_SUBJECT` if blank. |

If the same domain appears in multiple rules, the first rule in the list wins. The APIM Console rejects cross-rule duplicate domains at the form level.

## Prerequisites

Before branded sender rules can be configured or saved, all the following conditions must be met:

- The platform SMTP email service must be **enabled** at the Organization or Environment level.
- To save or reset branded sender settings at the **Environment scope**, you need the `ENVIRONMENT_SETTINGS` permission with `UPDATE` access.
- To save branded sender settings at the **Organization scope**, you need the `organization-settings-u` permission.
- The aggregate serialized size of all branded sender configurations must not exceed **4,000 characters**. Configurations that exceed this limit can't be saved.
- If `email.branded_senders` is set to a valid value in `gravitee.yml` or by an environment variable, the field is **locked read-only** in the APIM Console and you can't modify it.
- If the system value is invalid or oversized, it's logged and ignored. The field remains editable, and no error is surfaced in the APIM Console.


## Create Branded Sender Rules at Environment Scope

In the APIM Console, go to **Settings > Settings** and scroll to the **SMTP** card. The **Branded notification email** subsection follows the **Mail properties** subsection, and it displays the current list of rule configurations and controls for adding, editing, or removing rules.

### Add and Edit Rules

1. In the **Branded notification email** subsection, click **Add configuration** to add a new rule card.

    {% hint style="info" %}
    The **Add configuration** button is disabled when email is disabled, when the field is system-configured and read-only, or when you lack the `environment-settings-u` permission.
    {% endhint %}

2. In the **Recipient domains** tag input field, enter one or more values. The placeholder text is `example.com, eu.example.com`. The domain match is case-insensitive on the part after `@`, and at least one domain is required.

3. In the **From** field, enter a sender address. The placeholder text is `noreply@example.com`. The field accepts a bare address or the display-name form `Name <address>`, and it's required.

4. In the **Subject prefix** field, optionally enter a value. The placeholder text is `[Example] %s`. Use `%s` or `%1$s` as a placeholder for the email's subject, up to a maximum of 255 characters.

5. To remove a rule, click the **Delete** trash icon on the rule card.

6. Repeat these steps for additional rule cards as needed. Rules are matched in list order, and the **first matching domain wins**.

7. Save the form to persist the Environment-level rules.

When the Environment inherits from the Organization, each rule card displays an **Inherited from Org** badge.

---

## Reset Environment Rules to Organization Settings

The **Reset to Org settings** button is available at Environment scope when all the following conditions are true:

- An Environment-level override exists, so `brandedSendersInherited` is `false`.
- Email is enabled.
- The field isn't system-configured and read-only.
- You have the `environment-settings-u` permission.

When you click **Reset to Org settings**, the Environment-level override is removed entirely, and the Environment inherits branded sender rules from the Organization or system configuration. This differs from saving an empty list, which stores an explicit empty Environment override and doesn't fall back to the Organization value.

### Confirmation Dialog for Unsaved Changes

If there are unsaved changes on the page when you click **Reset to Org settings**, a confirmation dialog appears before the reset proceeds. The dialog contains the following text:

| Element | Text |
|:--------|:-----|
| Dialog title | `Reset branded senders` |
| Dialog content | `You have unsaved changes on this page that will be discarded. Do you want to reset the branded senders to the organization configuration?` |
| Confirm button | `Reset` |

### Feedback

The following messages report the outcome of the reset:

| Outcome | Message |
|:--------|:--------|
| Success | `Branded senders reset to the organization configuration.` |
| Error | Server error message, or `An error occurred while resetting the branded senders.` |

---

## Manage Branded Sender Rules at Organization Scope

The same **Branded notification email** subsection is available in the **SMTP** section of **Organization > Settings** in the APIM Console. Behavior at this scope differs from the Environment scope in the following ways:

- The **Reset to Org settings** button is **not present** at this scope.
- The branded senders control is **disabled** when email is disabled, or when `email.branded_senders` is system-configured and read-only.
- The entire form, including branded senders, is **disabled** when you lack the `organization-settings-u` permission.
