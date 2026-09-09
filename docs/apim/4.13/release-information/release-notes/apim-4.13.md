---
description: >-
  Release notes for Gravitee API Management 4.13, covering new features,
  improvements, breaking changes, and deprecations. Browse the full list of
  changes.
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

* The Gateway resolves the request path before it routes: `http.pathHandling` now defaults to `NORMALIZE`, so a request carrying dot segments reaches the API its resolved path designates, and is enforced by that API's plan.
* Branded senders apply a different **From** address and subject prefix to notification emails for each recipient domain, configurable per Organization and Environment.
* The new `#jsonEscape` Expression Language function escapes a value so it's safe to insert into a JSON document or JSON string literal, for example in a response template body.
* The Generate JWT policy adds optional `x5t` and `x5t#S256` certificate thumbprint headers to generated JWTs, for downstream systems that select the validation certificate by thumbprint.
* The schema registry provider contract now exposes the serialization format of each schema and answers subject membership and version-list lookups, and the bundled Confluent Schema Registry resource implements all three.
* The plan endpoints of the legacy Management API v1 now reject V4, Federated, and Federated Agent APIs with an HTTP `400` error that points to Management API v2.
* The New Developer Portal catalog gains categories, so you group APIs in the APIM Console and consumers filter the catalog to one category and share that view by URL.
* New Developer Portal navigation pages fetch their content from external sources such as GitHub, GitLab, or an HTTP URL, on demand or on an auto-fetch schedule, and a repository import mirrors a whole documentation tree into a read-only folder.

## Breaking Changes and deprecations

#### **The Gateway resolves the request path before it routes**

The `http.pathHandling` Gateway setting now defaults to `NORMALIZE`. In 4.12 and earlier the default was `RAW`. A deployment that upgrades without changing its configuration resolves request paths before it resolves the listener context path, and therefore before it enforces any plan. A request carrying dot segments is routed on the resolved path, so it can reach a different API than it did before. Percent-encoded unreserved characters are decoded, duplicate slashes are merged, and a malformed percent sequence is answered with `400`. Encoded slashes are never decoded. Set `http.pathHandling: RAW` to restore the previous behavior, which also restores a known authorization bypass, or `http.pathHandling: REJECT` to close the exposure without changing any routing decision. For the upgrade checklist and the limits of each mode, see [Request Path Handling](../../configure-and-manage-the-platform/gravitee-gateway/request-path-handling/README.md). For more information, see [Breaking Changes and Deprecations](../breaking-changes-and-deprecations.md).

#### **Management API v1 plan endpoints reject V4, Federated, and Federated Agent APIs**

The plan endpoints of the legacy Management API v1 no longer accept V4, Federated, and Federated Agent APIs. Every plan operation for one of these APIs returns HTTP `400`. The error message names the API's definition version and points to the Management API v2 plan endpoints. Previously, these endpoints didn't check the API's definition version. Read operations for these APIs could fail with HTTP `500` or behave inconsistently, and write operations, for example creating or deleting a plan, could succeed. For more information, see [Breaking Changes and Deprecations](../breaking-changes-and-deprecations.md).

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

#### **Categories in the New Developer Portal catalog**

* Group the APIs of your New Developer Portal catalog into categories, and let consumers filter the catalog to one category at a time. An API belongs to as many categories as you assign it to.
* Create and manage categories in the APIM Console, under **Catalog** in the Portal Settings menu. A category carries a title, an optional description, and a **Visible** toggle that decides whether consumers see it. Titles are unique per environment, compared without case, and each environment keeps its own set of categories.
* Assign APIs to a category from the same screen, with **Add API to Category**. Only APIs published in the portal navigation are offered, so an API that consumers can't reach in the portal can't be added to a category.
* In the portal, the catalog header carries a **Category** dropdown that filters to a single visible category, and list view gains a **Category** column. The selection travels in the catalog URL's `category` query parameter, so consumers share or bookmark a filtered view by its address. API Products are excluded while a category filter is applied.
* On the first Management API startup after the upgrade, Gravitee copies the existing Classic Developer Portal categories and their API assignments into New Developer Portal categories, once per environment. The two sets are independent from then on.
* These categories are stored and managed apart from the categories under **Categories** in the environment **Settings**, so a change on one screen doesn't affect the other.
* For more information, see [Manage New Developer Portal categories](../../developer-portal/new-developer-portal/manage-new-developer-portal-categories.md).

#### **Schema types and subject membership in the schema registry provider contract**

* Version `1.1.0` of the schema registry provider contract (`io.gravitee.resource:gravitee-resource-schema-registry-provider-api`) adds a `SchemaType` value (`AVRO`, `JSON`, `PROTOBUF`, or `UNKNOWN`) and a `Schema.getType()` accessor, so a schema-aware plugin detects the payload format from the registry instead of guessing it.
* `lookupUnderSubject(subject, schemaContent)` checks whether a schema definition is registered under a subject, independently of which version is `latest`. It returns the registered schema with its id, version, and type in one round-trip, or empty when the content isn't registered.
* `getVersions(subject)` lists the version identifiers registered under a subject.
* Every addition carries a default implementation (`UNKNOWN` type, empty results), so an existing provider compiled against contract version `1.0.1` compiles and runs unchanged, and a registry that doesn't support these lookups returns the defaults.
* The Confluent Schema Registry resource implements the new surface from plugin version `5.1.0`, bundled with APIM 4.13. For more information, see [Implement a schema registry provider](../../plugins/customization/schema-registry-provider.md).

#### **Kafka Gateway: broker addressing for Virtual Clusters**

* A Virtual Cluster rewrites broker IDs so they stay unique across its backends, which means the hostnames clients resolve are not the ones a single-backend deployment used. `gateway.kafka.routingHostMode.virtualClusterBrokerDomainPattern` sets the broker domain pattern for Kafka APIs backed by a Virtual Cluster only, so adopting one no longer moves the DNS records and certificate SANs of every other Kafka API on the same Gateway. It is optional: left unset, Virtual Clusters keep following `brokerDomainPattern`, and both defaults are unchanged.
* Two placeholders come with it, usable in either pattern: `{realBrokerId}`, the broker ID as configured on the backend, and `{clusterIndex}`, the backend's zero-based position in the Virtual Cluster. Together they let a hostname keep your own broker numbering instead of the rewritten IDs. A Virtual Cluster pattern must still tell the backends apart — through `{brokerId}`, which encodes the backend, or through `{clusterIndex}` alongside `{realBrokerId}` — and the Gateway now refuses to deploy a pattern that cannot, rather than routing to the wrong backend silently.
* A client connecting on a broker hostname the Virtual Cluster never advertised — a DNS record left over from a single-backend deployment, most often — is now served as a bootstrap connection, so it receives the merged metadata and re-targets itself at the correct broker. Previously the connection was closed without a response and the client waited out its own timeout, which typically surfaced as producing failing while bootstrap and topic listing worked. The Gateway logs a warning naming what it could not place, so the stale DNS record stays visible rather than being papered over.
* For more information, see [Virtual Cluster Broker Addressing](../../kafka-gateway/virtual-cluster-broker-addressing.md).

#### **External sources for New Developer Portal pages**

* Link a New Developer Portal navigation page to an external source, so its content is fetched from that source instead of being written in the editor. The source types are the fetcher plugins deployed with the Management API, and APIM bundles the GitHub, GitLab, Git, Bitbucket, and HTTP fetchers. A sourced page is read-only in the Console, and removing its source makes the content editable again.
* Re-fetch content on demand with the **Fetch now** button on a sourced page, or with **Fetch All** on a folder or API to fetch every sourced page below it. A page that fails to fetch doesn't block the others, and it records its error on the page.
* Enable auto-fetch on a source with its own cron expression to re-fetch the content on a schedule. A dedicated Management API job paces all schedules, configured with `services.portal_navigation_auto_fetch.enabled` and `services.portal_navigation_auto_fetch.cron` in `gravitee.yml`, with a default pace of every 5 minutes. It's a different job from the `services.auto_fetch` job that serves Classic Developer Portal and API documentation pages, and each job has its own flag and cron expression.
* Import a whole documentation tree from a remote repository with the **Import** button of the **Navigation items** screen. The import creates an unpublished folder whose subtree mirrors the repository and stays read-only, follows a `.gravitee.json` descriptor when the repository carries one, and re-running the fetch on the folder synchronizes it, including removing pages deleted remotely once a run completes without failures. The import requires a fetcher that lists repository directories, which the bundled GitHub and GitLab fetchers do.
* Import the content of a single page from a local `.md`, `.yaml`, `.yml`, or `.json` file of up to 10 MB, when creating the page or with the **Import file** button on an existing page. This is a one-time import with no link to a source.
* The fetch and import operations are exposed by Management API v2 as `POST /portal-navigation-items/{navId}/_fetch` and `POST /portal-navigation-items/_import`, and both require the `ENVIRONMENT_DOCUMENTATION[UPDATE]` permission.
* For more information, see [Import content from external sources](../../developer-portal/new-developer-portal/customize-the-navigation/import-content-from-external-sources.md).

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
