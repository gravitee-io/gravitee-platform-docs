# APIM 4.13

<!--
TEMPLATE NOTES (delete before publishing)

Structure follows the APIM 4.11 and 4.12 release notes:

- Highlights: one bullet per notable change, written as a single sentence that names
  the feature and what it lets a user do. Order roughly by impact.
- Breaking Changes and deprecations: add this section only if the release has any.
  Use `#### **Title**` followed by prose paragraphs (not bullets), and link to the
  Breaking changes and deprecations page for details.
- New Features: one `#### **Feature name**` per feature, followed by 3-5 bullets
  covering what it does, how it is configured (property names, permissions, UI
  location), what it applies to, and any limits or prerequisites.
- Improvements: same shape as New Features, for enhancements to existing behavior.
  Add the section when the release has its first entry.

Use bold in the `####` headings. Reference configuration keys, permissions, and
property names in backticks. Use relative links for in-space pages and absolute
documentation.gravitee.io links for other versions.
-->

## Highlights

* Branded senders let notification emails go out from a different From address and subject prefix for each recipient domain, configurable per Organization and Environment.

## New Features

#### **Branded Senders for Notification Emails**

* Override the sender address and subject prefix that APIM uses for notification emails, per recipient email domain, so recipients see an address on your own domain instead of the platform default. The body of each notification is unchanged and is still customized through Notification Templates.
* Each rule takes one or more recipient domains, a **From** address (a bare address such as `noreply@example.com` or the display-name form `Example Team <noreply@example.com>`), and an optional subject prefix of up to 255 characters that uses `%s` for the notification's own subject.
* Rules are matched on the recipient's email domain, ignoring case, and the first matching rule wins. Recipients that match no rule keep the default sender address and subject prefix.
* Configure rules in the APIM Console under the **Branded notification email** subsection of the **SMTP** card, at both the Organization and Environment scope. An Environment inherits the Organization's rules until it saves its own, and **Reset to Org settings** restores inheritance. Requires the SMTP email service to be enabled, plus `ORGANIZATION_SETTINGS[UPDATE]` or `ENVIRONMENT_SETTINGS[UPDATE]` permission for the corresponding scope.
* Self-hosted installations can set `email.branded_senders` in the Management API `gravitee.yml`, as a JSON array in an environment variable, or under the Helm chart's `smtp:` section. A value set this way applies to every Organization and Environment and makes the APIM Console field read-only.
* APIM does not verify domain ownership or check DNS before sending. Publish SPF, DKIM, and DMARC records authorizing your relay for every domain you use in a **From** address, and confirm your SMTP relay accepts a sender address outside its authenticated domain — some relays accept such a message and then discard it, which APIM records as a successful send.
