# Branded Senders

Branded sender rules can be configured at two scopes: **Organization** and **Environment**. Environment-level rules override the Organization rules when present. If no Environment-level override has been saved, the Environment inherits from the Organization or system configuration.

The `brandedSendersInherited` flag in the Environment settings response is `true` when no Environment-level override exists and no valid system-configured value is in effect. At Organization scope, this flag is always `false`.

Saving an empty list (`[]`) at the Environment scope stores an **explicit empty override** and does **not** fall back to the Organization value. To remove the override entirely and restore inheritance, use the **Reset to Org settings** action.

---

## Domain Matching and Message Dispatch

When an email notification is dispatched, the backend extracts the domain from each recipient address — the part after `@`, compared case-insensitively — and matches it against the `domains` list of each branded sender rule in order. The **first matching rule wins**.

Recipients sharing the same resolved `(From, Subject)` pair are grouped together, and one message is sent per group.

The following recipients and scenarios fall outside branded dispatch:

- A recipient string containing more than one `@` (for example, a comma-separated multi-address string) is not matched; the default sender identity is used.
- Recipients in the `DEFAULT_MAIL_TO` sentinel address are not matched for branding.
- If the caller supplies an explicit `From` on the notification, branded sender logic is skipped entirely and a single unbranded message is sent.
- `copyToSender` copies always use the default identity (`EMAIL_FROM` / `EMAIL_SUBJECT`), regardless of the recipient's domain.

---

## Branded Sender Rule Structure

Each rule contains three fields:

| Field | Description | Constraints |
|:------|:------------|:------------|
| **`domains`** | List of recipient email domains (case-insensitive match on the part after `@`) | Required; at least one domain; valid domain format; no duplicates across rules |
| **`from`** | Sender address for matching recipients | Accepts bare address (`noreply@example.com`) or display-name form (`Example Team <noreply@example.com>`); falls back to default `EMAIL_FROM` if blank |
| **`subject`** | Subject line prefix template | Optional; max 255 characters; `%s` or `%1$s` is replaced with the email's title at send time; stray `%` characters, `%n`, and width specifiers are treated as literal text; falls back to default `EMAIL_SUBJECT` if blank |

If the same domain appears in multiple rules, the first rule in the list wins. The console UI rejects cross-rule duplicate domains at the form level.

---

## Prerequisites

Before branded sender rules can be configured or saved, all of the following conditions must be met:

- The platform email (SMTP) service must be **enabled** at the Organization or Environment level.
- Saving or resetting branded sender settings at the **Environment scope** requires the `ENVIRONMENT_SETTINGS` permission with `UPDATE` access.
- Saving branded sender settings at the **Organization scope** requires the `organization-settings-u` permission.
- The aggregate serialized size of all branded sender configurations must not exceed **4,000 characters**. Configurations exceeding this limit cannot be saved.
- If `email.branded_senders` is set in `gravitee.yml` or via environment variable with a valid value, the field is **locked read-only** in the console and cannot be modified through the UI.
- If the system value is invalid or oversized, it is logged and ignored; the field remains editable and no error is surfaced in the console.

---

## Creating Branded Sender Rules (Environment Scope)

Navigate to **Portal Settings** and locate the **Mail properties** section. The **Branded notification email** subsection displays the current list of rule configurations and controls for adding, editing, or removing rules.

### Adding and Editing Rules

1. In the **Branded notification email** subsection, click **Add configuration** to add a new rule card.

   > The **Add configuration** button is disabled when email is disabled, the field is system-configured (read-only), or you lack `environment-settings-u` permission.

2. Enter one or more values in the **Recipient domains** field (tag input; placeholder: `example.com, eu.example.com`). Domain matching is case-insensitive on the part after `@`. At least one domain is required.

3. Enter a sender address in the **From** field (placeholder: `noreply@example.com`). Accepts a bare address or display-name form (`Name <address>`). This field is required.

4. Optionally enter a value in the **Subject prefix** field (placeholder: `[Example] %s`). Use `%s` or `%1$s` as a placeholder for the email's subject. Maximum 255 characters.

5. To remove a rule, click the **Delete** (trash) icon button on the rule card.

6. Repeat for additional rule cards as needed. Rules are matched in list order; the **first matching domain wins**.

7. Save the form to persist the Environment-level rules.

When the Environment is currently inheriting from the Organization, each rule card displays an **Inherited from Org** badge.

---

## Resetting Environment Rules to Organization Settings

The **Reset to Org settings** button is available at Environment scope when all of the following conditions are true:

- An Environment-level override exists (`brandedSendersInherited` is `false`).
- Email is enabled.
- The field is not system-configured (read-only).
- You have `environment-settings-u` permission.

Clicking **Reset to Org settings** removes the Environment-level override entirely, so the Environment inherits branded sender rules from the Organization or system configuration. This is distinct from saving an empty list, which stores an explicit empty Environment override without falling back to the Organization value.

### Confirmation Dialog (Unsaved Changes)

If there are unsaved changes on the page when you click **Reset to Org settings**, a confirmation dialog is shown before proceeding:

- **Dialog title:** `Reset branded senders`
- **Dialog content:** `You have unsaved changes on this page that will be discarded. Do you want to reset the branded senders to the organization configuration?`
- **Confirm button:** `Reset`

### Feedback

| Outcome | Message |
|:--------|:--------|
| Success | `Branded senders reset to the organization configuration.` |
| Error | Server error message, or `An error occurred while resetting the branded senders.` |

---

## Managing Branded Sender Rules at Organization Scope

The same **Branded notification email** subsection is available under **Organization Settings**. Behavior at this scope differs from the Environment scope in the following ways:

- The **Reset to Org settings** button is **not present** at this scope.
- The branded senders control is **disabled** when email is disabled or when `email.branded_senders` is system-configured (read-only).
- The entire form, including branded senders, is **disabled** when the user lacks the `organization-settings-u` permission.
