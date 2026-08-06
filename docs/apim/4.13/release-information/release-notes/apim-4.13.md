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
* Management API v1 plan read operations now reject V4 and Federated APIs with `400 Bad Request`, directing those requests to the Management API v2 plan endpoints.

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

#### **Datadog Reporter: Consumer and error tags on the request count metric**

* `gravitee.apim.api_request_count` now carries `applicationid`, `applicationname`, and `errorkey` tags, so you can filter, group, and alert on failed requests by consumer and by error cause without pivoting to logs. These tags need Datadog Reporter 8.1.1 or later.
* An optional `message` tag carries the error message. It's off by default because each distinct message creates a separate metric series in Datadog. Enable it by setting `reporters.datadog.tags.includeErrorMessage` to `true`.
* The Datadog Reporter adds these tags for v4 APIs only. For a v2 API, `api_request_count` keeps the node, API, and status tags.
* `applicationname` needs APIM 4.13 or later. On an earlier APIM version the Datadog Reporter omits that tag, and the other tags are unaffected.
* For more information, see [Datadog Reporter](../../analyze-and-monitor-apis/reporters/datadog-reporter.md#tags-on-the-request-count-metric).

#### **Generate JWT policy: Support for `x5c` with the `INLINE` and `PEM` key resolvers**

* The `x509CertificateChain` option now works with the `INLINE` and `PEM` key resolvers. The policy builds the `x5c` header from the certificates included in the key material, ordered from the signing certificate outward, and drops certificates that don't link into the chain.
* The policy now parses key material that bundles certificates together with the private key.
* For the `INLINE` and `PEM` key resolvers, if no certificate in the key material matches the signing key, the policy omits the `x5c` header and signs the token anyway, logging a warning when the key material is loaded.

#### **Management API v1 Plan Read Operations Restricted to V1 and V2 APIs**

* Management API v1 plan read operations don't support V4 or Federated APIs and now return `400 Bad Request` for those requests instead of an incomplete plan representation.
* Use the Management API v2 plan endpoints to read plans for V4 and Federated APIs.
* Plan reads for V1 and V2 APIs are unaffected and continue to work through the Management API v1 endpoints.
