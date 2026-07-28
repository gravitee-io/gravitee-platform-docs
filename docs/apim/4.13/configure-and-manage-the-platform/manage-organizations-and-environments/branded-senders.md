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

Branded senders can be configured at two scopes, **Organization** and **Environment**, and for self-hosted installations in `gravitee.yml`.

## Prerequisites

- The SMTP email service must be **enabled** at the Organization or Environment level. Branded sender controls are disabled while email is off.
- To save or reset branded senders at the **Environment** scope, you need the `ENVIRONMENT_SETTINGS` permission with `UPDATE` access.
- To save branded senders at the **Organization** scope, you need the `ORGANIZATION_SETTINGS` permission with `UPDATE` access. Without it, the whole settings form is read-only.

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

When a notification is sent, the APIM console takes the domain from each recipient address, which is the part after `@`, and compares it against the domains on each rule in order. The **first rule that matches wins**. The comparison ignores case, so `Example.com` and `example.com` are the same domain.

Recipients that match no rule keep the default sender address and subject prefix. When one notification goes to recipients at several branded domains, each domain receives its own message, sent from its own address.

## Branded Sender Rule Fields

Each rule has three fields:

| Field | Description | Constraints |
|:------|:------------|:------------|
| **Recipient domains** | The recipient email domains the rule applies to. | Required, at least one. Each entry must be a valid domain name, such as `example.com`. |
| **From** | The sender address used for those recipients. | Required. Accepts a bare address such as `noreply@example.com`, or the display-name form `Example Team <noreply@example.com>`. |
| **Subject prefix** | The subject prefix applied to those messages. | Optional, maximum 255 characters. Use `%s` where the notification's own subject should appear. If you leave this blank, the default subject prefix is used. |

A domain can appear in only one rule. The APIM Console rejects duplicates across rules when you save the form.

## Configure Branded Senders in the APIM Console

Go to **Settings > Settings**, scroll to the **SMTP** card, and find the **Branded notification email** subsection, which follows the **Mail properties** subsection. It also shows a read-only **Default notification email** preview, listing the **Default From** and **Default subject prefix** that apply to any recipient no rule matches.

1. Click **Add configuration** to add a rule.

    {% hint style="info" %}
    **Add configuration** is disabled when email is disabled, when the value is set in `gravitee.yml` and therefore read-only, or when you lack the `ENVIRONMENT_SETTINGS` permission with `UPDATE` access.
    {% endhint %}

2. In the **Recipient domains** field, enter one or more domains. The placeholder text is `example.com, eu.example.com`.

3. In the **From** field, enter the sender address to use for those domains. The placeholder text is `noreply@example.com`.

4. In the **Subject prefix** field, optionally enter a prefix such as `[Example] %s`.

5. To remove a rule, click the **Delete** trash icon on its card.

6. Repeat for any further rules. Rules are matched in order, so put your most specific rules first.

7. Save the form.

### Inheritance Between Scopes

An Environment inherits the Organization's rules until you save rules of your own at the Environment scope. While it's inheriting, each rule card shows an **Inherited from Org** badge, and **Reset to Org settings** is unavailable because there's nothing to reset. The badge disappears as soon as you edit a card, before you save.

Saving an **empty** list at the Environment scope isn't the same as inheriting. It stores an explicit "no branded senders" override, and the Organization rules no longer apply. To restore inheritance, use **Reset to Org settings**.

If `email.branded_senders` is set in `gravitee.yml` or by an environment variable, that value takes precedence over both scopes. The Environment doesn't inherit from the Organization, and the field is read-only in both.

## Reset Environment Rules to the Organization Settings

**Reset to Org settings** is available at the Environment scope when all the following are true:

- An Environment-level override exists.
- Email is enabled.
- The value isn't set in `gravitee.yml`.
- You have the `ENVIRONMENT_SETTINGS` permission with `UPDATE` access.

Clicking it removes the Environment override, so the Environment inherits from the Organization again. If you have unsaved changes on the page, the APIM Console asks you to confirm before discarding them.

## Manage Branded Senders at the Organization Scope

The same **Branded notification email** subsection is available in the **SMTP** section of **Organization > Settings**. It behaves as it does at the Environment scope, with these differences:

- There's no **Reset to Org settings** button, because the Organization is the top scope.
- The control is disabled when email is disabled, or when `email.branded_senders` is set in `gravitee.yml`.
- The entire settings form is disabled when you lack the `ORGANIZATION_SETTINGS` permission with `UPDATE` access.

## Configure Branded Senders for a Self-Hosted Installation

Branded senders can be set outside the APIM Console, alongside the rest of your [SMTP configuration](smtp-configuration.md). A value set this way applies to every Organization and Environment on the installation and makes the APIM Console field read-only.

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
If the value is invalid, APIM writes the problem to the Management API log and ignores it. The APIM Console field stays editable and shows no error, so check that log if a self-hosted configuration doesn't take effect.
{% endhint %}
