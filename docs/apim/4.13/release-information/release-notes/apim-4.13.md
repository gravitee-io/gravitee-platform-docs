---
description: Release notes for Gravitee API Management 4.13.
---

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

* Branded senders apply a different **From** address and subject prefix to notification emails for each recipient domain, configurable per Organization and Environment.
* The new `#jsonEscape` Expression Language function escapes a value so it can be safely inserted into a JSON document or JSON string literal, for example in a response template body.
* The Generate JWT policy adds optional `x5t` and `x5t#S256` certificate thumbprint headers to generated JWTs, for downstream systems that select the validation certificate by thumbprint.

## Breaking Changes and deprecations

#### **Generate JWT policy: Changes to `x5c` with the `INLINE` and `PEM` key resolvers**

Starting with APIM 4.13.0, the Generate JWT policy resolves the `x5c` certificate chain from the certificates included in the key material when the key resolver is `INLINE` or `PEM`. Generated JWTs now carry an `x5c` header when a matching certificate is present, and the policy rejects requests with HTTP `500` when `x509CertificateChain` is set to `X5C` but no usable certificate is available. In earlier versions, this option had no effect with these key resolvers. For more information, see [Breaking Changes and Deprecations](../breaking-changes-and-deprecations.md).

## New Features

#### **Branded Senders for Notification Emails**

* Override the sender address and subject prefix that APIM uses for notification emails, per recipient email domain. Recipients then see an address on your own domain instead of the platform default. The body of each notification is unchanged and is still customized through Notification Templates.
* Each rule takes one or more recipient domains, a **From** address, and an optional subject prefix. The **From** field accepts a bare address such as `noreply@example.com` or the display-name form `Example Team <noreply@example.com>`. The subject prefix can be up to 255 characters and uses `%s` for the notification's own subject.
* Rules are matched on the recipient's email domain. Matching ignores case, and the first matching rule wins. Recipients that match no rule keep the default sender address and subject prefix.
* In the APIM Console, configure rules under the **Branded notification email** subsection of the **SMTP** card, at both the Organization and Environment scope. An Environment inherits the Organization's rules until it saves its own, and **Reset to Org settings** restores inheritance. Branded senders require the SMTP email service to be enabled, plus `ORGANIZATION_SETTINGS[UPDATE]` or `ENVIRONMENT_SETTINGS[UPDATE]` permission for the corresponding scope.
* For a self-hosted installation, set `email.branded_senders` in the Management API `gravitee.yml`, as a JSON array in an environment variable, or under the Helm chart's `smtp:` section. A value set this way applies to every Organization and Environment. It also makes the APIM Console field read-only.
* APIM doesn't verify domain ownership and doesn't check DNS before sending. Publish SPF, DKIM, and DMARC records authorizing your relay for every domain you use in a **From** address. Confirm that your SMTP relay accepts a sender address outside its authenticated domain. Some relays accept such a message and then discard it, which APIM records as a successful send.

#### **JSON Escape Function for Expression Language**

* `#jsonEscape` converts `"` and `\` to their escaped forms (`\"` and `\\`) and escapes control characters, which prevents a value taken from the current API transaction from breaking the JSON document you insert it into.
* Call the function from any field that supports Expression Language, for example `{#jsonEscape(#error.message)}` in a response template body.
* The function accepts exactly one argument, and collections and arrays are joined into a single space-separated string before escaping, so you can pass a multi-valued header or query parameter directly.

#### **X.509 certificate thumbprint headers in the Generate JWT policy**

* The Generate JWT policy now injects the `x5t` (SHA-1) and `x5t#S256` (SHA-256) certificate thumbprint headers defined by RFC 7515 into the protected header of generated JWTs. Downstream systems use these thumbprints to identify the certificate to validate the token against.
* Enable each header independently with the `x509CertSha1Thumbprint` and `x509CertSha256Thumbprint` options of the policy configuration. Both options default to off, so existing configurations are unchanged.
* The thumbprints are computed from the DER-encoded signing certificate resolved by the configured key resolver (`INLINE`, `PEM`, `JKS`, or `PKCS12`). The options apply to RS256 signatures only, and the Console disables them when an HMAC signature is selected.
* If a thumbprint option is enabled and no certificate matching the signing key is available, the policy rejects requests with HTTP `500` instead of issuing a token without the header.
* For more information, see [Generate JWT](../../create-and-configure-apis/apply-policies/policy-reference/generate-jwt.md).

## Improvements

#### **Generate JWT policy: Support for `x5c` with the `INLINE` and `PEM` key resolvers**

* The `x509CertificateChain` option now works with the `INLINE` and `PEM` key resolvers. The policy builds the `x5c` header from the certificates included in the key material, ordered from the signing certificate outward, and drops certificates that don't link into the chain.
* The policy now parses key material that bundles certificates together with the private key.
* This change affects existing `INLINE` and `PEM` configurations that already set `x509CertificateChain` to `X5C`. For more information, see [Breaking Changes and Deprecations](../breaking-changes-and-deprecations.md).
