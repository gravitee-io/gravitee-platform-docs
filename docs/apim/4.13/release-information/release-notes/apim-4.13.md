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
* API Products reach the New Developer Portal: publish an API Product in the portal navigation with its APIs and documentation, and consumers discover it in the catalog, subscribe to it, and manage the subscription that covers every API it includes.
* New Developer Portal navigation pages fetch their content from external sources such as GitHub, GitLab, or an HTTP URL, on demand or on an auto-fetch schedule, and a repository import mirrors a whole documentation tree into a read-only folder.
* Identity provider claims travel into dynamic client registration requests: list the claims to persist on the identity provider, map them to registration request fields on the client registration provider, and the registration provider receives tenant or user context for each application it registers.
* A Kafka Topic Mapping entry that sets only one of `client` and `broker` becomes a rule that applies to any topic, with the `#topic` expression variable bound to the name being resolved, so one entry can prefix or strip a prefix across every topic.
* The FIPS images move to a JDK 25 base, where `jks` and `pkcs12` keystores no longer load, so a FIPS deployment converts the Gateway's listener stores to `pem`, or to `bcfks` where a store is read from a file, before upgrading.
* SAP Business Technology Platform joins the federation providers: an agent ingests the API proxies of SAP API Management with their OpenAPI specification and documentation, turns the subscribable SAP products into plans, and creates approved Gravitee subscriptions in the SAP Developer Hub.
* Native Kafka connection logs record each lifecycle event of a connection as its own entry, can report clean closes as **Disconnected**, and show the client library and credential of each connection.
* The XML Validation policy reads its XSD schema, and the schemas it imports, from a schema registry through the new HTTP Schema Registry resource, and a request that fails validation gets a JSON list of up to 20 violations with their position in the payload.
* Dictionary properties can be encrypted: APIM stores the value encrypted and masks it in the APIM Console and the Management API, and the Gateway decrypts it at deployment so Expression Language resolves the original value.
* Dynamic API properties now support encryption, one property at a time or for every fetched value: APIM stores the value encrypted and masks it in the APIM Console and in the Management API v2, and Expression Language resolves the original value once the API is deployed.

## Breaking Changes and deprecations

#### **The Gateway resolves the request path before it routes**

The `http.pathHandling` Gateway setting now defaults to `NORMALIZE`. In 4.12 and earlier the default was `RAW`. A deployment that upgrades without changing its configuration resolves request paths before it resolves the listener context path, and therefore before it enforces any plan. A request carrying dot segments is routed on the resolved path, so it can reach a different API than it did before. Percent-encoded unreserved characters are decoded, duplicate slashes are merged, and a malformed `%` sequence is answered with `400`. Encoded slashes are never decoded. Set `http.pathHandling: RAW` to restore the previous behavior, which also restores a known authorization bypass, or `http.pathHandling: REJECT` to close the exposure without changing any routing decision. For the upgrade checklist and the limits of each mode, see [Request Path Handling](../../configure-and-manage-the-platform/gravitee-gateway/request-path-handling/README.md). For more information, see [Breaking Changes and Deprecations](../breaking-changes-and-deprecations.md).

#### **Management API v1 plan endpoints reject V4, Federated, and Federated Agent APIs**

The plan endpoints of the legacy Management API v1 no longer accept V4, Federated, and Federated Agent APIs. Every plan operation for one of these APIs returns HTTP `400`. The error message names the API's definition version and points to the Management API v2 plan endpoints. Previously, these endpoints didn't check the API's definition version. Read operations for these APIs could fail with HTTP `500` or behave inconsistently, and write operations, for example creating or deleting a plan, could succeed. For more information, see [Breaking Changes and Deprecations](../breaking-changes-and-deprecations.md).

#### **Kafka Topic Mapping policy: Invalid mapping entries now stop an API from deploying**

The Kafka Topic Mapping policy now checks its mapping entries when the API is deployed, where 4.12 and earlier checked nothing. An API that deploys today can fail to deploy after the upgrade. Four kinds of entry are refused. An entry that sets neither `client` nor `broker`. An entry whose plain name Kafka wouldn't accept as a topic name. An entry that references `#topic` in both fields. And two entries whose plain `broker` values are equal, or whose plain `client` values are equal. The last is the likeliest to appear in a configuration that works today. Review every Kafka Topic Mapping policy against those four cases before upgrading. For more information, see [Breaking Changes and Deprecations](../breaking-changes-and-deprecations.md).

#### **Native Kafka connection logs: One log entry per connection event**

A native Kafka connection now writes one log entry per lifecycle event: one when it opens, one when it fails, and, if the API selects it, one when it closes cleanly. In 4.12, the entries of a connection shared the same request ID, so the Elasticsearch reporter kept only the last one. The request ID is now unique to each entry, and the transaction ID, which is the connection ID, ties the entries of a connection together. Review any dashboard or query that counts connection log entries, or that looks up an entry by request ID. For more information, see [Breaking Changes and Deprecations](../breaking-changes-and-deprecations.md).

#### **Subscription forms apply only to the APIs they're assigned to**

An environment now holds several subscription forms, and each form applies only to the APIs assigned to it. On the first Management API startup after the upgrade, the existing form of each environment is named **Global Default Form**. If it was visible, it's assigned to every API of the environment. If it was hidden, it's assigned to no API. An API created after the upgrade has no subscription form until you assign it to one, where previously the environment's form applied to every API. New environments start with no subscription form. The Management API v2 `GET /subscription-forms` endpoint now returns a list of forms, and `PUT /subscription-forms/{subscriptionFormId}` requires `name`, `gmdContent`, and `apiIds`. For more information, see [Breaking Changes and Deprecations](../breaking-changes-and-deprecations.md).

#### **Kafka Topic Mapping policy: A blank mapping field now defines a rule**

A Kafka Topic Mapping entry that sets only one of `client` and `broker` is now a rule that applies to any topic. A field set to a blank string counts as absent. In 4.12 and earlier such an entry matched nothing and never applied. An entry left with a blank field therefore changes from inert to claiming every topic the client names. The configuration schema required both fields before 4.13.0, so an affected entry is one whose field was set to an empty string. Review every Kafka Topic Mapping policy for a blank `client` or `broker` before upgrading. For more information, see [Breaking Changes and Deprecations](../breaking-changes-and-deprecations.md).

#### **FIPS images: JKS and PKCS12 keystores no longer load**

The 4.13 FIPS images run on JDK 25, where `jks` and `pkcs12` stores don't load. Convert them before upgrading. For more information, see [Breaking Changes and Deprecations](../breaking-changes-and-deprecations.md).

#### **Inline Authentication Provider resource 3.0.0: Usernames and passwords are read as Expression Language**

Version 3.0.0 of the Inline Authentication Provider resource evaluates the username and password of each user as Gravitee Expression Language when the API is deployed. A literal value that contains `{#`, `{T`, or `{(` followed by `}` is now read as an expression, not as the text it holds. Spaces after the `{` don't change this, and a `{#` with no closing `}` makes the evaluation fail. Before you deploy version 3.0.0, check every Inline Authentication Provider resource for usernames and passwords that contain a `{`. For more information, see [Breaking Changes and Deprecations](../breaking-changes-and-deprecations.md).

#### **Latency policy: The response phase now adds latency**

The Latency policy now runs in the response phase of v2 APIs, v4 HTTP proxy APIs, and v4 message APIs. In 4.12.21 and earlier, a Latency policy in a response phase had no effect. The **Policy Studio** of a v2 API and the **Platform flows** on the organization's **Policies** page already let you add it there. After the upgrade, such a policy delays the responses that its flow handles by its configured time. Before you upgrade, check the response phase of every flow in the **Policy Studio** of your v2 APIs and in the **Platform flows**. For more information, see [Breaking Changes and Deprecations](../breaking-changes-and-deprecations.md).

#### **LLM proxy: Sent tokens include the prompt cache for Anthropic and Bedrock**

On an LLM proxy API, three values now count the whole prompt for models served by the Anthropic and Bedrock providers: the `long_llm-proxy_tokens-sent` metric, the `llmproxy.usage.sent.token` context attribute, and the `X-LLM-Proxy-Tokens-Sent` response header. The whole prompt includes the tokens read from or written to the provider's prompt cache. In 4.12, they used the input count that these two providers report, which leaves those tokens out. A Token Rate Limit policy therefore counts more tokens for the same cached traffic. The sent cost also prices the cache reads and cache writes, at the model's cache prices when they're set and at the input price otherwise. Before you upgrade, review the Token Rate Limit policies on LLM proxy APIs that serve Anthropic or Bedrock models. For more information, see [Breaking Changes and Deprecations](../breaking-changes-and-deprecations.md).

#### **XML Validation policy: Failed validations return a list of violations**

APIM 4.13 bundles version 2.x of the XML Validation policy, which changes the response to a request that fails validation. On v4 HTTP proxy APIs and on v2 APIs in emulation mode, the response body is a JSON object with a `message` field and a `violations` array. The error key is `XML_VALIDATION_FAILED`. `message` holds **Http error message**, or `XML validation failed` when that field is empty. In 4.12, the message was `Bad Request` when the field was empty, and a request that accepted JSON got a body with `message` and `http_status_code` fields. Other requests got the message alone, and now get the JSON object, still with the `text/plain` content type. On v2 APIs with emulation mode disabled, an empty **Http error message** now returns a text summary of the violations instead of `Bad Request`, and the error key is `XML_INVALID_PAYLOAD`. When the request's `Accept` header includes `application/json` or `*/*`, the body is a JSON object with the message in `message` and the status code in `http_status_code`, and the content type is `application/json`. Otherwise, the body is the message alone, and the content type is `text/plain`. Before you upgrade, check the API consumers that read these responses. For more information, see [Breaking Changes and Deprecations](../breaking-changes-and-deprecations.md).

#### **XML Validation policy: Requests that declare a `DOCTYPE` and schema downloads are blocked**

The XML Validation policy that APIM 4.13 bundles rejects a request body that declares a `DOCTYPE`, with the same `400` response as a body that doesn't match the schema. It also no longer downloads a schema that an `xs:import` or `xs:include` names with an `http`, `https`, or `file` URL, so an inline schema that does this doesn't compile, and the policy isn't applied. When **Schema source** is **Schema registry**, a schema that names such a URL fails to compile. Requests fail with `500` and the error key `XML_VALIDATION_SCHEMA_COMPILE_FAILED`, and don't reach the backend. In 4.12, the policy accepted a `DOCTYPE` and downloaded those schemas. Before you upgrade, check for API consumers that send a `DOCTYPE`, and for inline schemas that import or include a schema by URL. For more information, see [Breaking Changes and Deprecations](../breaking-changes-and-deprecations.md).

#### **Encrypted API properties: The Management API v2 masks values and checks encryption**

The Management API v2 now returns `••••••••••••` in place of the value of an encrypted API property when it returns an API, for v2 and v4 APIs. In 4.12, it returned the encrypted value. When you update an API, send `••••••••••••` back to keep the stored value. Saving an API refuses `••••••••••••` for a property without an encrypted value. Saving a v4 API also refuses an encrypted property sent back as plain text, and a new value for an encrypted property that the installation's secret can't decrypt. These checks return HTTP `400`. When the secret can't encrypt a value, saving an encrypted property of a v4 API fails with HTTP `500` instead of storing its plain text value. For more information, see [Breaking Changes and Deprecations](../breaking-changes-and-deprecations.md).

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

#### **Multiple subscription forms in the New Developer Portal**

* Create several subscription forms per environment, and assign each form to the APIs it applies to. An API is assigned to one form at most. Consumers see the form assigned to the API they subscribe to, and an API without an assigned form has no subscription form.
* Manage forms from **Subscription Form** in the portal settings. The **Subscription Forms** list shows every form with a **Visible** toggle, and **Add** creates a form from a starter template. Each form carries a name that's unique in the environment.
* Choose a form's APIs with **Assign APIs**. An API already assigned to another form can't be selected.
* A new form is hidden until you turn on its **Visible** toggle. Deleting a form leaves its APIs without a subscription form, and deleting an API removes it from its form.
* The Management API v2 adds endpoints to create, retrieve, and delete a form, and to retrieve the starter template.
* For more information, see [Creating and managing subscription forms](../../secure-and-expose-apis/subscriptions/creating-and-managing-subscription-forms.md).

#### **Categories in the New Developer Portal catalog**

* Group the APIs of your New Developer Portal catalog into categories, and let consumers filter the catalog to one category at a time. An API belongs to as many categories as you assign it to.
* Create and manage categories in the APIM Console, under **Catalog** in the Portal Settings menu. A category carries a title, an optional description, and a **Visible** toggle that decides whether consumers see it. Titles are unique per environment, compared without case, and each environment keeps its own set of categories.
* Assign APIs to a category from the same screen, with **Add API to Category**. Only APIs published in the portal navigation are offered, so an API that consumers can't reach in the portal can't be added to a category.
* In the portal, the catalog header carries a **Category** dropdown that filters to a single visible category, and list view gains a **Category** column. The selection travels in the catalog URL's `category` query parameter, so consumers share or bookmark a filtered view by its address.
* On the first Management API startup after the upgrade, Gravitee copies the existing Classic Developer Portal categories and their API assignments into New Developer Portal categories, once per environment. The two sets are independent from then on.
* These categories are stored and managed apart from the categories under **Categories** in the environment **Settings**, so a change on one screen doesn't affect the other.
* For more information, see [Manage New Developer Portal categories](../../developer-portal/new-developer-portal/manage-new-developer-portal-categories.md).

#### **API Products in the New Developer Portal**

* Add an API Product to the New Developer Portal navigation from the **Add API Product** entry of a folder's context menu on the **Navigation items** screen. Gravitee creates an API item under the API Product for every API it includes and an unpublished **Overview** page under the API Product and under each of those APIs, so the API Product ships with its documentation tree. An API Product can't be at the top level of the navigation, can't sit inside an API or another API Product, and can be added once.
* Assign a published API Product to a New Developer Portal category with **Add API Product to Category** on the category screen. The catalog's **Category** filter then lists the API Products assigned to the category alongside the APIs.
* In the catalog, an API Product card carries the **API PRODUCT** badge and the names of the APIs it includes. The catalog search matches API Product names, with typo-tolerant search when the environment enables it. An API nested under an API Product doesn't get a catalog entry of its own.
* Consumers subscribe from the **Subscribe** button on the API Product's pages, choosing a published plan of the API Product and an application. General conditions and the subscription form don't apply to API Product plans. The **Subscriptions** page of the portal lists API and API Product subscriptions together, with a **Type** filter.
* The subscription details page of an API Product subscription shows the credentials once and one card per included API, with its base URL, a cURL example, and a link to its documentation. Consumers pause, resume, or close the subscription, and renew the API key of an API Key plan, from the same page.
* For more information, see [Manage Portal Navigation and APIs](../../developer-portal/new-developer-portal/customize-the-navigation.md#api-product) and [Manage Subscriptions](../../developer-portal/new-developer-portal/manage-subscriptions.md#subscribe-to-an-api-product).

#### **Schema types and subject membership in the schema registry provider contract**

* Version `1.1.0` of the schema registry provider contract (`io.gravitee.resource:gravitee-resource-schema-registry-provider-api`) adds a `SchemaType` value (`AVRO`, `JSON`, `PROTOBUF`, or `UNKNOWN`) and a `Schema.getType()` accessor, so a schema-aware plugin detects the payload format from the registry instead of guessing it.
* `lookupUnderSubject(subject, schemaContent)` checks whether a schema definition is registered under a subject, independently of which version is `latest`. It returns the registered schema with its id, version, and type in one round-trip, or empty when the content isn't registered.
* `getVersions(subject)` lists the version identifiers registered under a subject.
* Every addition carries a default implementation (`UNKNOWN` type, empty results), so an existing provider compiled against contract version `1.0.1` compiles and runs unchanged, and a registry that doesn't support these lookups returns the defaults.
* The Confluent Schema Registry resource implements the new surface from plugin version `5.1.0`, bundled with APIM 4.13. For more information, see [Implement a schema registry provider](../../plugins/customization/schema-registry-provider.md).

#### **Gamma modules on a JDBC management repository**

* A Gamma module that stores data now runs on the same JDBC management repository as APIM, so an installation standardized on PostgreSQL, MariaDB, MySQL, or Microsoft SQL Server no longer keeps MongoDB alongside it for Gamma's own persistence. The module reads `management.type` and loads its MongoDB or its JDBC persistence accordingly, with `repositories.management.type` accepted as a fallback spelling.
* Each module keeps its migration history in its own tracking tables, `{prefix}<id>_databasechangelog` and `{prefix}<id>_databasechangeloglock`, so a module's migration never touches APIM's own, and isn't touched by it.
* Event Stream Management stores the saved Kafka Explorer connections in one table, `{prefix}kafka_explorer_connections`, created at startup on JDBC.
* An installation that sets `management.jdbc.liquibase` to `false` applies each module's migrations itself. They ship in one archive published with the release, alongside APIM's own. A module whose migration was skipped still starts. In Event Stream Management, the Kafka Explorer pages then report the missing table and the setting that skipped it rather than a bare error.
* For more information, see [Apply schema migrations manually](../../prepare-a-production-environment/repositories/apply-schema-migrations-manually.md).

#### **Kafka Gateway: Broker addressing for Virtual Clusters**

* This feature is also available since APIM 4.12.19.
* A Virtual Cluster rewrites broker IDs so they stay unique across its backends, which means the hostnames clients resolve are not the ones a single-backend deployment used. `kafka.routingHostMode.virtualClusterBrokerDomainPattern` in `gravitee.yml` (`gateway.kafka.routingHostMode.virtualClusterBrokerDomainPattern` in the Helm chart) sets the broker domain pattern for Kafka APIs backed by a Virtual Cluster only, so adopting one no longer moves the DNS records and certificate SANs of every other Kafka API on the same Gateway. It is optional: left unset, Virtual Clusters keep following `brokerDomainPattern`, and both defaults are unchanged.
* Two placeholders come with it, usable in either pattern: `{realBrokerId}`, the broker ID as configured on the backend, and `{clusterIndex}`, the backend's zero-based position in the Virtual Cluster. Together they let a hostname keep your own broker numbering instead of the rewritten IDs. A Virtual Cluster pattern must still tell the backends apart — through `{brokerId}`, which encodes the backend, or through `{clusterIndex}` alongside `{realBrokerId}` — and the Gateway now refuses to deploy a pattern that cannot, rather than routing to the wrong backend silently.
* A client connecting on a broker hostname the Virtual Cluster never advertised — a DNS record left over from a single-backend deployment, most often — is now served as a bootstrap connection, so it receives the merged metadata and re-targets itself at the correct broker. Previously the connection was closed without a response and the client waited out its own timeout, which typically surfaced as producing failing while bootstrap and topic listing worked. The Gateway logs a warning naming what it could not place, so the stale DNS record stays visible rather than being papered over.
* For more information, see [Virtual Cluster Broker Addressing](../../kafka-gateway/virtual-cluster-broker-addressing.md).

#### **Kafka Gateway: Connection events in native Kafka connection logs**

* A connection that closes cleanly can now be reported with the new **Disconnected** status. The entry carries the connection duration and never an error.
* The `analytics.connectionEvents` field of a native Kafka API selects the reported events among `CONNECTED`, `DISCONNECTED`, and `ERROR`. When the field is absent or empty, the Gateway reports `CONNECTED` and `ERROR`, as before. `DISCONNECTED` is opt-in for every API. The APIM Console has no setting for this field: set it through the Management API.
* Each lifecycle event is its own log entry. Entries of one connection share the transaction ID, and each entry has its own request ID.
* Disconnected and error entries carry the number of Kafka requests the connection served, in total (`long_native-kafka_request-count`) and per Kafka request type (`long_native-kafka_requests_<REQUEST_TYPE>`). The APIM Console doesn't display them.
* In the APIM Console, the `SESSION_ERROR` status is now labeled **Interrupted**, and **Disconnected** now stands for the new `DISCONNECTED` status. The **Logs** page shows five summary cards: Connected, Disconnected, Interrupted, Failed, and Unknown.
* The connection log detail page shows the **Client library** and **Client library version** that the client advertises, the **Security type** of the plan, and the **Security token**, which is the client ID for OAuth2 and JWT plans.
* For more information, see [Configure and View Native Kafka API Connection Logs](../../analyze-and-monitor-apis/logging/configuring-and-viewing-native-api-connection-logs.md).

#### **Kafka Gateway: Error metrics and metric dimension cap**

* New Prometheus counters, labeled with the Kafka error name: `kafka_upstream_produce_topic_records_failed_total` and `kafka_upstream_produce_topic_record_bytes_failed_total` count the produced records and bytes the broker rejected, and `kafka_<direction>_fetch_errors_total` and `kafka_<direction>_fetch_partition_errors_total` count failed fetch responses and partition-level fetch errors. `kafka_upstream_produce_topic_records_total` still counts every record sent to the broker.
* `kafka.metrics.dimensions.max` caps the number of metric dimension combinations the Gateway keeps in memory. The default is `100000`. Above the cap, the least recently used combinations are evicted and the Gateway logs a warning.
* The `kafka_active_connections` gauge reports the active client connections per plan, application, and client identity. It's disabled by default. This gauge is also available since APIM 4.12.19.
* For more information, see [Expose Metrics to Prometheus](../../kafka-gateway/expose-metrics-to-prometheus.md).

#### **External sources for New Developer Portal pages**

* Link a New Developer Portal navigation page to an external source, so its content is fetched from that source instead of being written in the editor. The source types are the fetcher plugins deployed with the Management API, and APIM bundles the GitHub, GitLab, Git, Bitbucket, and HTTP fetchers. A sourced page is read-only in the Console, and removing its source makes the content editable again.
* Re-fetch content on demand with the **Fetch now** button on a sourced page, or with **Fetch All** on a folder or API to fetch every sourced page below it. A page that fails to fetch doesn't block the others, and it records its error on the page.
* Enable auto-fetch on a source with its own cron expression to re-fetch the content on a schedule. A dedicated Management API job paces all schedules, configured with `services.portal_navigation_auto_fetch.enabled` and `services.portal_navigation_auto_fetch.cron` in `gravitee.yml`, with a default pace of every 5 minutes. It's a different job from the `services.auto_fetch` job that serves Classic Developer Portal and API documentation pages, and each job has its own flag and cron expression.
* Import a whole documentation tree from a remote repository with the **Import** button of the **Navigation items** screen. The import creates an unpublished folder whose subtree mirrors the repository and stays read-only, follows a `.gravitee.json` descriptor when the repository carries one, and re-running the fetch on the folder synchronizes it, including removing pages deleted remotely once a run completes without failures. The import requires a fetcher that lists repository directories, which the bundled GitHub and GitLab fetchers do.
* Import the content of a single page from a local `.md`, `.yaml`, `.yml`, or `.json` file of up to 10 MB, when creating the page or with the **Import file** button on an existing page. This is a one-time import with no link to a source.
* The fetch and import operations are exposed by Management API v2 as `POST /portal-navigation-items/{navId}/_fetch` and `POST /portal-navigation-items/_import`, and both require the `ENVIRONMENT_DOCUMENTATION[UPDATE]` permission.
* For more information, see [Import content from external sources](../../developer-portal/new-developer-portal/customize-the-navigation/import-content-from-external-sources.md).

#### **Identity provider claims in dynamic client registration requests**

* Propagate tenant or user context from an identity provider to a client registration provider. At each login through a Gravitee AM, OpenID Connect, Google, or GitHub identity provider, APIM stores the claims listed in the provider's new **Persisted Claims** section on the user, reading each claim from the ID token first, then the access token, then the user info response.
* Map the stored claims to fields of the registration request in the new **Claim Mappings** section of the client registration provider. When a user creates an application that registers through the provider, APIM writes each mapped claim into the request body at the mapped field, creating nested objects for dot-separated paths such as `metadata.organization`. A claim the user doesn't carry is skipped. On an application update, the claims of the application's primary owner are sent.
* Only extension fields can be targeted. A mapping that targets a standard registration field, `client_name` or `redirect_uris` for example, is rejected with HTTP `400`.
* Each login replaces the stored claims. Removing a claim from the list, or emptying it, removes the corresponding stored values at the user's next login. The stored claims aren't exposed by the Management API or the Portal API.
* Both settings are also available through the Management API, as the `persistedClaimsWhitelist` array of the identity provider and the `claim_mappings` object of the client registration provider. An update that omits the field keeps the stored value.
* For more information, see [Inject identity provider claims into DCR requests](../../configure-and-manage-the-platform/manage-organizations-and-environments/inject-identity-provider-claims-into-dcr-requests.md).

#### **Kafka Topic Mapping: Dynamic rules with the `#topic` variable**

* A mapping entry that sets only one of `client` and `broker` becomes a rule that applies to any topic, instead of the exact pair the policy has always required. The `#topic` expression variable carries the name the rule is resolving, so one entry can prefix, strip, or rewrite every topic without listing them.
* Setting only `broker` makes a client-to-broker rule, with `#topic` bound to the client-side name. `{"broker": "dev-{#topic}"}` sends a client asking for `orders` to `dev-orders`.
* Setting only `client` makes a broker-to-client rule, with `#topic` bound to the broker-side name, applied to broker topics in an all-topics listing. A rule whose expression returns null or a blank string opts out of that topic.
* Exact pairs still win over rules, and among rules the declaration order decides. A topic resolves once per connection and keeps that result for the connection's lifetime.
* Rules resolve the same way in `ALIAS` mode. A topic a broker-to-client rule renames is listed under both names, each with its own topic ID.
* An entry that sets neither field, or references `#topic` in both, is rejected when the policy is created, and the message names the entry by its position in the list.
* For more information, see [Kafka Topic Mapping](../../create-and-configure-apis/apply-policies/policy-reference/kafka-topic-mapping.md).

#### **SAP Business Technology Platform federation**

* Federate the APIs of SAP API Management on SAP Business Technology Platform. Create an integration with the **SAP Business Technology Platform** provider in the APIM Console, and run its agent with a service key for the SAP API portal and one for the SAP Developer Hub.
* Each API proxy of the API portal becomes a federated API, with its OpenAPI specification and a page of its SAP documentation. Each version of an SAP API is a federated API of its own.
* Each product that the Developer Hub marks as subscribable becomes a plan on every API it contains: an OAuth2 plan for a product of External OAuth APIs, and an API Key plan for the others.
* An approved subscription to an API Key plan creates an SAP application for the Gravitee application in the Developer Hub, and the consumer receives the SAP application key as the API key. Closing a subscription removes only its own access in SAP.
* The agent requires the Developer Hub to approve subscriptions automatically. When SAP waits for its own approval, the agent rejects the Gravitee subscription.
* For more information, see [SAP Business Technology Platform](../../govern-apis/federation/3rd-party-providers/sap-api-management.md).

#### **OAuth 2.0 Token Exchange policy**

* The OAuth 2.0 Token Exchange policy implements RFC 8693. It exchanges the incoming token, usually the consumer's access token, for a token that a trusted authorization server issues, and writes that token to the `Authorization` header before the request reaches the backend.
* The policy reaches the authorization server through an OAuth2 resource of the API, or through a token endpoint and client credentials set on the policy. The Gravitee.io AM Authorization Server resource and the OAuth2 / OpenID Connect Provider resource support the exchange. The OAuth2 / OpenID Connect Provider resource gains a `tokenExchangeEndpoint` option for it.
* The policy applies to the request phase of v4 HTTP proxy APIs, v4 message APIs, and MCP proxies, and requires an Enterprise Edition license.
* For more information, see [OAuth 2.0 Token Exchange](../../create-and-configure-apis/apply-policies/policy-reference/oauth2-token-exchange.md).

#### **XML Validation policy: XSD schemas from a schema registry**

* The XML Validation policy reads its XSD schema from the policy configuration or from a schema registry. Set **Schema source** to **Schema registry**, then set the HTTP Schema Registry resource, the **Group ID**, the **Artifact ID**, and the **Version** of the root schema.
* The new HTTP Schema Registry resource fetches the root schema and the schemas it references over the registry's REST API, and caches them. It connects without authentication, with basic authentication, or with an OIDC client credentials flow.
* With **Byte cache TTL (ms)** set on the resource, a **Version** such as `branch=latest` picks up new registry content when the cached entry expires, without redeploying the API. If the registry becomes unavailable, the policy keeps validating against the last schema it compiled.
* The schema registry source applies to v4 HTTP proxy APIs.
* A request that fails validation gets a JSON response with up to 20 violations, each with its line, column, and element. For more information, see [XML Validation](../../create-and-configure-apis/apply-policies/policy-reference/xml-validation.md) and [HTTP Schema Registry](../../create-and-configure-apis/apply-policies/resources.md#http-schema-registry).

#### **Encrypted dictionary properties**

* Encrypt the value of a dictionary property. APIM stores the value encrypted, and the APIM Console and the Management API show `••••••••••••` in its place. A dictionary can hold encrypted and unencrypted properties side by side.
* In the APIM Console, turn on **Encrypt** when you add a property, or click the lock icon of an existing property. A dynamic dictionary can also encrypt every value it fetches, with **Encrypt fetched values** in its **Encryption** section.
* The Gateway decrypts the values when the dictionary is deployed, so `{#dictionaries['<dictionary-id>']['<property-key>']}` resolves to the original value. Dictionary properties use the same secret as encrypted API properties, `api.properties.encryption.secret`, which must match on the Management API and the Gateway.
* Encryption can't be undone. An encrypted property of a dynamic dictionary stays encrypted when a refresh fetches a new value, and audit entries don't record encrypted values.
* In an Automation API manifest, declare encrypted properties of a manual dictionary under `encryptedProperties`, and set `encryptOnFetch` for a dynamic dictionary. For more information, see [Dictionaries](../../configure-and-manage-the-platform/gravitee-gateway/dictionaries.md#encrypt-dictionary-properties).

#### **Encrypted dynamic API properties**

* Encrypt the value of a dynamic API property. APIM stores the value encrypted, and the APIM Console shows `••••••••••••` in its place, as does the Management API v2 when it returns the API. Encrypted and unencrypted properties sit side by side in the same API.
* In the APIM Console, click the lock icon of a dynamic property in the **Properties** tab, or turn on **Encrypt on fetch** in the **Encryption** section of the dynamic properties settings to encrypt every fetched value. In an API definition, the setting is `encryptOnFetch` under `encryption` in the configuration of the HTTP dynamic properties service.
* The Gateway decrypts the values when the API is deployed, so `{#api.properties['<key>']}` resolves to the original value. Encrypted properties use the existing secret, `api.properties.encryption.secret`. Set the same value on the Management API and the Gateway.
* An encrypted property can't be made plain again. An encrypted dynamic property stays encrypted when a fetch returns a new value. A property whose key is missing from a fetch is removed, and comes back as plain text unless **Encrypt on fetch** is on.
* Audit entries show a `<sha256:…>` value in place of encrypted values. Deploying an API that holds an encrypted property records an `API_ENCRYPTED_PROPERTIES_ACCESSED` entry, and the automatic redeployment after a fetch records `API_ENCRYPTED_PROPERTIES_REFRESHED`. For more information, see [Encrypt dynamic properties](../../create-and-configure-apis/apply-policies/v4-api-policy-studio.md#encrypt-dynamic-properties).

## Improvements

#### **Datadog Reporter: Consumer and error tags on the request count metric**

* `gravitee.apim.api_request_count` now carries `applicationid`, `applicationname`, and `errorkey` tags, so you can filter, group, and alert on failed requests by consumer and by error cause without pivoting to logs. These tags need Datadog Reporter 8.1.1 or later.
* An optional `message` tag carries the error message. It's off by default because each distinct message creates a separate metric series in Datadog. Enable it by setting `reporters.datadog.tags.includeErrorMessage` to `true`.
* The Datadog Reporter adds these tags for v4 APIs only. For a v2 API, `api_request_count` keeps the node, API, and status tags.
* `applicationname` needs APIM 4.13 or later. On an earlier APIM version the Datadog Reporter omits that tag, and the other tags are unaffected.
* For more information, see [Datadog Reporter](../../analyze-and-monitor-apis/reporters/datadog-reporter.md#tags-on-the-request-count-metric).

#### **Consuming application on OpenTelemetry spans and log records**

* The root HTTP server span and the OpenTelemetry log records that the Gateway exports for a request now carry `gravitee.application.id` and `gravitee.application.name`, so a telemetry backend can group and filter them by consuming application.
* A request that the Gateway matches to a subscription carries the subscribing application's identifier and its name. A request on a keyless plan carries `gravitee.application.id` with the value `1` and no `gravitee.application.name`.
* Both attributes sit on the root span alone, and child spans don't repeat them. The log records that carry the individual messages of a Message API don't include them either.
* For more information, see [Attribute placement](../../analyze-and-monitor-apis/opentelemetry.md#attribute-placement) and [OpenTelemetry Logs Integration Overview](../../analyze-and-monitor-apis/opentelemetry-logs-integration-overview.md).

#### **Generate JWT policy: Support for `x5c` with the `INLINE` and `PEM` key resolvers**

* The `x509CertificateChain` option now works with the `INLINE` and `PEM` key resolvers. The policy builds the `x5c` header from the certificates included in the key material, ordered from the signing certificate outward, and drops certificates that don't link into the chain.
* The policy now parses key material that bundles certificates together with the private key.
* For the `INLINE` and `PEM` key resolvers, if no certificate in the key material matches the signing key, the policy omits the `x5c` header and signs the token anyway, logging a warning when the key material is loaded.

#### **Client authentication method for OpenID Connect and Gravitee AM identity providers**

* The new **Client Authentication Method** setting of an OpenID Connect or Gravitee AM identity provider decides how APIM sends its client ID and client secret to the provider's token endpoint during a login and to its token introspection endpoint during a token exchange: in an `Authorization: Basic` header (`client_secret_basic`) or in the request body (`client_secret_post`). Previously, the token endpoint always received them in the request body and the introspection endpoint always received them in a Basic header, with no way to align the two calls.
* **Provider default**, the value of every existing provider, keeps the previous behavior of each call.
* When the provider rejects the credentials, the login or the token exchange now answers HTTP `401` with a JSON body that carries the provider's error code and, for `invalid_client`, a hint naming the setting. Previously, the login answered an empty HTTP `401` and the token exchange an HTTP `500`, neither of them saying what had gone wrong.
* Only the provider's error code is passed on. The token exchange no longer relays the provider's raw response body to the caller.
* Through the Management API, the setting is the `tokenEndpointAuthMethod` key of the provider's `configuration` object. It can't be declared under `security.providers` in `gravitee.yml`.
* For more information, see [Choose how APIM authenticates to the identity provider](../../configure-and-manage-the-platform/manage-organizations-and-environments/authentication/README.md#choose-how-apim-authenticates-to-the-identity-provider).

#### **Settings that keep identity provider tokens out of the browser**

* Four new settings decide whether the identity provider's access token and ID token reach the browser when a user signs in. The APIM Console and the Gamma console share one setting per token, and the Developer Portal (classic and new) has its own. The settings apply to the whole installation.
* By default, neither token is hidden, so sign-in and browser storage stay as they were.
* Roles and groups mapping still reads a hidden token. With the access token hidden, the APIM Console, the Gamma console, and the Developer Portal (classic and new) keep no access token in browser storage.
* For API consumers: a hidden token stays in the sign-in response of `/auth/oauth2/{idp}`, with an empty string (`""`) as its value. The response keeps its shape, so a custom portal that reads it keeps working.
* With the ID token hidden, the sign-out request that the APIM Console or the Developer Portal (classic and new) sends to the identity provider's logout endpoint carries the provider's **Client Id** and no ID token.
* Known limitation in APIM 4.13: hiding the ID token from the consoles stops users from signing in to the APIM Console and the Gamma console through a provider whose **Scopes** include `openid`. Both consoles show their sign-in page again after the provider sends the user back. Keep the ID token visible to the consoles while users sign in through such a provider.
* For more information, see [Keep identity provider tokens out of the browser](../../configure-and-manage-the-platform/manage-organizations-and-environments/authentication/README.md#keep-identity-provider-tokens-out-of-the-browser).

#### **AI Model Text Embedding resource: Expression Language and secrets in the API key and header values**

* The `apiKey` of the OpenAI provider and the value of each HTTP provider header now take Gravitee Expression Language, including `{#secrets.get('...')}` secret references, so a credential no longer sits in the API definition as plain text.
* The Gateway resolves these expressions when it starts the resource, which it does when the API is deployed. An expression reads an API property or a dictionary entry of the environment. The deployment context holds nothing from a request, and a new value in a property or a dictionary reaches the resource at the next deployment of the API.
* Only the value of a header takes an expression. The header name is sent as entered.
* The change ships in AI Model Text Embedding 2.0.0, which APIM bundles from 4.11.26, 4.12.18, and 4.13.0 onward. The configuration format is unchanged, so an existing resource keeps working as it is.
* For more information, see [AI Resources](../../ai-agent-management/AI-resources/README.md).

#### **Inline Authentication Provider resource: Expression Language and secrets in usernames and passwords**

* From version 3.0.0, the username and password of each user take Gravitee Expression Language, so they read, for example, an API property, a dictionary entry, or, in v4 APIs, a `{#secrets.get('...')}` secret reference. The resource no longer has to hold the credential as plain text.
* Both fields are evaluated once, when the API starts on a Gateway. An expression can't read the request. After you change a property, a dictionary entry, or a secret, deploy the API again.
* If an expression fails, or returns no value or an empty value, the resource rejects every user until every expression resolves and the API is deployed again.
* The plugin isn't included in the default APIM distribution. Download and deploy version 3.0.0 to use these expressions. From that version, some literal values that contain a `{` are read as expressions. For more information, see [Breaking Changes and Deprecations](../breaking-changes-and-deprecations.md).
* For more information, see [Resources](../../create-and-configure-apis/apply-policies/resources.md#inline-authentication-provider).

#### **Documentation from private Git repositories**

* Documentation pages that import from **Git** now have **Username** and **Password or access token** fields, so Classic Developer Portal documentation can come from a private repository. Leave both empty for a public repository.
* After you save, the password or token is masked, and auto-fetch keeps using it.
* The change ships in Git fetcher 3.1.0, which APIM bundles from 4.9.36, 4.10.32, 4.11.29, 4.12.21, and 4.13.0 onward.
* For more information, see [API Documentation](../../developer-portal/classic-developer-portal/api-documentation.md).

#### **New Developer Portal: A Settings page in the Portal Settings**

* The Portal Settings gain a **Settings** page, so you configure the New Developer Portal from the Portal Settings. It holds the API key header, the permitted Kafka SASL mechanisms, the Portal URL, the registration settings, and the default OpenAPI viewer. With an Enterprise license, it also holds the **Portal capabilities** and **Application membership** sections.
* **Enable mTLS Certificate Management**, **Enable Analytics**, **Approximate spelling for API search**, and the three application membership toggles move from the **New Developer Portal** section of the Console **Settings** page to the new page. That section keeps **Enable the New Developer Portal**, **Open Website**, and **Open Settings**, and **Open Settings** now opens the new page.
* The API key header, the Portal URL, the registration settings, and the default OpenAPI viewer stay on the Console **Settings** page too. Both pages change the same values, and the values you set before the upgrade don't change.
* The **API** entry of the Portal Settings is removed. Its API key header and Kafka SASL mechanisms settings are on the new page, and its **API Details** list stays under **API Portal Information** in the Console **Settings**.
* For more information, see [Configure New Developer Portal settings](../../developer-portal/new-developer-portal/configure-new-developer-portal-settings.md).

#### **New Developer Portal: An Authentication page in the Portal Settings**

* The Portal Settings gain an **Authentication** page. It holds **Force authentication to access portal**, **Show login form on portal**, and the list of identity providers to activate for the portal.
* The **Authentication** page in the **Portal** section of the Console **Settings** stays. Both pages change the same settings.
* For more information, see [Enforce User Authentication](../../developer-portal/new-developer-portal/configure-authentication/enforce-user-authentication.md) and [Configure authentication with SSO](../../developer-portal/new-developer-portal/configure-authentication/configure-authentication-with-sso.md).

#### **New Developer Portal: The navigation tree starts collapsed**

* The navigation tree of the portal now starts with its folders, APIs, and API Products collapsed, except the ones that lead to the page it opens. Previously, every branch started expanded.
* When a consumer opens an API or API Product from the catalog, the tree expands that API or API Product and keeps the other branches collapsed.
* For more information, see [Manage Portal Navigation and APIs](../../developer-portal/new-developer-portal/customize-the-navigation.md#developer-portal-view).

#### **Kafka endpoint: Producer idempotence and acknowledgements**

* The producer settings of the Kafka endpoint gain **Enable idempotence (enable.idempotence)**, on by default. Turn it off to publish to a Kafka-compatible broker that doesn't support idempotent producers. With it off, a retry can write a record twice or out of order.
* **Acknowledgements (acks)** appears once idempotence is off, and sets how many replicas acknowledge a record before the send succeeds: `all`, `1`, or `0`.
* Existing APIs keep their behavior. The defaults, idempotence on and `acks` set to `all`, give the same producer configuration as the Kafka client's own defaults.
* The change ships in Kafka endpoint 6.2.0, which APIM bundles from 4.13.0.
* For more information, see [Kafka](../../create-and-configure-apis/configure-v4-apis/endpoints/kafka.md#producer-and-consumer-settings).

#### **Secondary endpoints for v4 HTTP proxy APIs in the Console**

* The **General** tab of an endpoint of a v4 HTTP proxy API gains a **Secondary endpoint** checkbox. A secondary endpoint stays out of load balancing until health checks mark every primary endpoint of its group as down. Requests then go to the secondary endpoints.
* The **Options** column of the endpoint list shows **Secondary** for each secondary endpoint.
* For more information, see [Secondary endpoints](../../create-and-configure-apis/configure-v4-apis/load-balancing-and-failover.md#secondary-endpoints).

#### **Latency policy: Response phase and Expression Language**

* The Latency policy now runs in the response phase of v2 APIs, v4 HTTP proxy APIs, and v4 message APIs, where it delays the response.
* The new `dynamicTime` option takes a Gravitee Expression Language expression that returns the time to wait, in the unit set by `timeUnit`, for example `{#request.headers['X-Latency'][0]}`. When it's set, the policy ignores `time`. In the publish and subscribe phases of a message API, the expression is evaluated for each message.
* If the expression fails, returns no value, or returns a number lower than 0, the policy raises the `LATENCY_INVALID_TIME` error key. In the request and response phases, the request fails with HTTP `500`. In the publish and subscribe phases, the error interrupts the message flow instead.
* The policy doesn't cap the time that the expression returns. If the expression reads a value that the client sends, make sure the value is controlled and bounded.
* The change ships in Latency policy 3.1.0, which APIM bundles from 4.12.22 and 4.13.0 onward.
* For more information, see [Latency](../../create-and-configure-apis/apply-policies/policy-reference/latency.md) and [Breaking Changes and Deprecations](../breaking-changes-and-deprecations.md).

#### **LLM proxy: Prompt cache token counts and prices**

* Each model of an LLM proxy endpoint takes two optional prices, **Price per million tokens (input) served from the provider's prompt cache ($)** and **Price per million tokens (input) written into the provider's prompt cache ($)**. A price of `0` means free. An unset cache price bills the cache reads or cache writes at the input price, and the request carries a `COST_CACHE_RATE_NOT_FOUND` warning when the provider reports them.
* The Gateway reports `long_llm-proxy_tokens-cached`, `long_llm-proxy_tokens-cache-write`, `double_llm-proxy_cached-cost`, and `double_llm-proxy_cache-write-cost` when the provider reports the counts, and sets the matching `llmproxy.usage.*` context attributes for policies such as Assign Metrics. They're part of `tokens-sent` and `sent-cost`, not additions to them.
* The GenAI span of a request carries the `gen_ai.usage.cache_read.input_tokens` and `gen_ai.usage.cache_creation.input_tokens` OpenTelemetry attributes when the provider reports the counts.
* For more information, see [Reporters](../../analyze-and-monitor-apis/reporters/README.md) and [Assign Metrics](../../create-and-configure-apis/apply-policies/policy-reference/assign-metrics.md#metrics-on-llm-proxy-apis).
