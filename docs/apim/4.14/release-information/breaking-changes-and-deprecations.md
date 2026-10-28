---
description: Information about breaking changes and deprecations.
metaLinks:
  alternates:
    - breaking-changes-and-deprecations.md
---

# Breaking Changes and Deprecations

## Breaking changes

Here are the breaking changes for versions 4.X of Gravitee and versions 3.X of Gravitee

### Breaking changes from 4.X

Here are the breaking changes from versions 4.X of Gravitee.

#### 4.13.0

**Subscription forms apply only to the APIs they're assigned to**

From 4.13.0, an environment holds several subscription forms, and each form applies only to the APIs assigned to it. In 4.12 and earlier, each environment had one form, and it applied to every API of the environment.

On the first Management API startup after the upgrade, the existing form of each environment is named **Global Default Form** and assigned as follows:

* If the form was visible, it's assigned to every API of the environment.
* If the form was hidden, it's assigned to no API. Showing it later doesn't bring it back to any API until you assign APIs to it.

An API created after the upgrade has no subscription form until you assign it to one. New environments start with no subscription form, where 4.12 created a hidden one for each new environment.

The Management API v2 endpoints change as follows:

* `GET /subscription-forms` returns a list of forms instead of a single form.
* `PUT /subscription-forms/{subscriptionFormId}` requires `name`, `gmdContent`, and `apiIds`. `apiIds` replaces the APIs assigned to the form, so an empty list removes every API from it.
* A subscription form object carries `name` and `apiIds`.

Before you upgrade, update any script that reads the environment's form from `GET /subscription-forms` or updates it with `PUT`. After the upgrade, assign each new API to a form. For more information, see [Creating and managing subscription forms](../secure-and-expose-apis/subscriptions/creating-and-managing-subscription-forms.md).

**Kafka Topic Mapping policy: invalid mapping entries now stop an API from deploying**

From 4.13.0, the Kafka Topic Mapping policy checks its mapping entries when the API is deployed. In 4.12 and earlier it checked nothing, so a configuration the policy can't act on deployed and then behaved unpredictably at runtime. An API that deploys today can therefore fail to deploy after the upgrade.

Four kinds of entry are now refused:

* An entry that sets neither `client` nor `broker`.
* An entry that writes a plain name Kafka wouldn't accept as a topic name.
* An entry that references `#topic` in both fields.
* Two entries whose plain `broker` values are equal, or whose plain `client` values are equal.

The last one is the likeliest to appear in a configuration that works today, because both fields are set and nothing previously objected to the duplicate.

Each message names the entry by its position in the list, counting from zero. Before you upgrade, review every Kafka Topic Mapping policy against the four cases above. For the full set of checks and the messages they produce, see [Kafka Topic Mapping](../create-and-configure-apis/apply-policies/policy-reference/kafka-topic-mapping.md).

At runtime, an exact pair whose expression resolves either side to nothing, or to a name Kafka wouldn't accept, now fails the connection with `INVALID_CONFIG`. Previously the resolved value was sent to the broker as it was.

**Kafka Topic Mapping policy: A blank mapping field now defines a rule**

From 4.13.0, a Kafka Topic Mapping entry that sets only one of `client` and `broker` is a rule that applies to any topic. A field set to a blank string counts as absent. In 4.12 and earlier, the policy resolved a topic by comparing the name the client used with the entry's `client` value. An entry whose `client` was blank therefore matched nothing and never applied.

An entry left with a blank `client` therefore changes from inert to a client-to-broker rule that claims every topic the client names and sends each one to the value in `broker`. An entry left with a blank `broker` becomes a broker-to-client rule that relabels broker topics in an all-topics listing.

The policy's configuration schema required both fields before 4.13.0. An affected entry is therefore one whose field was set to an empty string rather than omitted. Before you upgrade, review every Kafka Topic Mapping policy for an entry with a blank `client` or `broker`. Remove the entry, or set both fields, to keep the behavior you have today. For what a single-field entry now does, see [Kafka Topic Mapping](../create-and-configure-apis/apply-policies/policy-reference/kafka-topic-mapping.md).

**Native Kafka connection logs: One log entry per connection event**

From 4.13.0, a native Kafka connection writes one log entry per lifecycle event: one when it opens, one when it fails, and, if the API selects the Disconnected event, one when it closes cleanly. In 4.12 and earlier, every entry of a connection carried the connection ID as its request ID, and the Elasticsearch reporter uses the request ID as the document ID, so a later entry replaced the earlier one and each connection kept a single entry.

The request ID is now unique to each entry, in the form `<connection-id>:<sequence>:<status>`. The transaction ID is the connection ID and ties the entries of a connection together. Before you upgrade, review any dashboard or query that counts connection log entries as connections, or that looks up an entry by connection ID through the request ID. For more information, see [Native Kafka API Connection Logs: Concepts and Architecture](../analyze-and-monitor-apis/logging/native-api-connection-logs-concepts-and-architecture.md).

The events an API logs are set by `analytics.connectionEvents` in the API definition, through the Management API v2 or the Automation API. It takes `CONNECTED`, `DISCONNECTED`, and `ERROR`. When it's missing or empty, the API logs `CONNECTED` and `ERROR`, so the Disconnected event is opt-in.

The entry that closes a connection, a Disconnected or error entry, now carries the number of Kafka requests the connection served. `long_native-kafka_request-count` holds the total, and `long_native-kafka_requests_<API_KEY>` holds the count for each Kafka API the connection used, for example `long_native-kafka_requests_PRODUCE`. The fields are left out when the connection served no requests. Before you upgrade, review any reporter pipeline that applies a strict schema to these entries.

The native API logs endpoint of the Management API v2, `GET /environments/{envId}/apis/{apiId}/logs/native`, no longer caps the total count at 10,000. A page that reaches beyond the Elasticsearch result window, set by `analytics.elasticsearch.index.max_result_window` and `10000` by default, returns `400`. Ask for a smaller page, or narrow the time range or the filters. When the total exceeds what can be paged, the API's native logs in the Console show `Showing the first <n> of <total> connections` and page only through the first `<n>`.

**The Gateway resolves the request path before it routes**

From 4.13.0, the `http.pathHandling` Gateway setting defaults to `NORMALIZE`. In 4.12 and earlier the default was `RAW`. A deployment that upgrades without changing its configuration resolves request paths before it resolves the listener context path, and therefore before it enforces any plan.

A request carrying dot segments is now routed on the resolved path, so it can reach a different API than it did before, and it's enforced by that API's plan. `/alpha/api/../../beta/api/echo` is read as a call to `beta` and answers `401` without a credential, where it previously matched `alpha` and reached beta's backend unauthenticated. Percent-encoded unreserved characters are also decoded, so `%41` reaches the backend as `A`, duplicate slashes are merged, and a malformed `%` sequence is answered with `400`. Encoded slashes are never decoded.

Set `http.pathHandling: RAW` to restore the previous behavior, which also restores a known authorization bypass. Set `http.pathHandling: REJECT` to close the exposure without changing any routing decision: a non-canonical path is answered with `400` and nothing is rewritten. For the upgrade checklist and the limits of each mode, see [Request Path Handling](../configure-and-manage-the-platform/gravitee-gateway/request-path-handling/README.md).

**The Gateway no longer advertises its truststore during the TLS handshake**

From 4.13.0, the Gateway sends an empty list of acceptable certificate authorities in the TLS `CertificateRequest` it issues when `ssl.clientAuth` is `request` or `required`. Previously, it sent every certificate in its truststore.

This closes an information disclosure. With an mTLS plan, the Gateway loads each subscribed application's client certificate into an in-memory truststore. Those certificates are end-entity leaves, not certificate authorities, and the Gateway advertised them to every client of the listener, including callers of the listener's other APIs who present no certificate at all. Anyone opening a TLS connection could read the distinguished names of the client identities the Gateway accepts.

Client certificate validation is unchanged. The full truststore still validates incoming certificates, so mTLS plan matching and subscription behavior are unaffected. An empty list means "no constraint," so clients continue to present their certificate.

The change affects only clients that relied on the advertised list to choose which certificate to present. A client holding several client certificates, typically a Java client with more than one key entry in its keystore, may now present the wrong one and be rejected. If that applies to you, set `ssl.sendClientCertificateAuthorities` to `true` on the affected listener to send the configured truststore again:

```yaml
http:
  ssl:
    sendClientCertificateAuthorities: true
```

Don't enable it on a listener that serves mTLS plans. A non-empty list is a constraint, not a hint: a client whose certificate issuer is absent from it withholds its certificate entirely. Subscription certificates are self-signed leaves that are never issued by an authority of the configured truststore, so enabling this cuts off every mTLS subscription on that listener. Certificates registered by subscriptions are never advertised, whatever the setting.

For the full option reference, see [Control which certificate authorities the Gateway advertises](../prepare-a-production-environment/configure-your-http-server.md#control-which-certificate-authorities-the-gateway-advertises).

**Management API v1 plan endpoints reject V4, Federated, and Federated Agent APIs**

From 4.13.0, the plan endpoints of the legacy Management API v1 (`/management/organizations/{orgId}/environments/{envId}/apis/{apiId}/plans`) reject V4, Federated, and Federated Agent APIs. Every plan operation for one of these APIs returns HTTP `400`. The error message names the API's definition version, for example: `API definition version 4.0.0 is not supported by Management API v1. Use Management API v2 instead (/management/v2/environments/{envId}/apis/{apiId}/...).`

This applies to listing, reading, creating, updating, and deleting plans, and to closing, publishing, and deprecating a plan. Previously, these endpoints didn't check the API's definition version. Read operations for these APIs could fail with HTTP `500` or behave inconsistently, and write operations, for example creating or deleting a plan, could succeed. Update any scripts or integrations that manage the plans of these APIs to use the Management API v2 plan endpoints (`/management/v2/environments/{envId}/apis/{apiId}/plans`).

**LLM Proxy removes images, audio, video, and files from requests by default**

From 4.13.0, an LLM Proxy reads images, audio, video, and files in requests sent in the OpenAI Chat Completions, OpenAI Responses, Anthropic Messages, and Gemini formats. Four entrypoint options of the LLM Proxy decide what happens to them: **Images sent by the client**, **Audio sent by the client**, **Video sent by the client**, and **Files sent by the client**. Each defaults to `STRIP`, which removes that content before the request reaches the provider. An LLM Proxy created in 4.12 or earlier has none of these options set, so it removes this content after the upgrade.

To forward a content type, set its option to `ALLOW` in the entrypoint configuration of the LLM Proxy, and redeploy the API. `REJECT` refuses a request that carries the content, with an HTTP `400` error and the code `modality_blocked`.

**A plan added to an existing LLM Proxy starts in staging**

From 4.13.0, a plan that you add on the **Plans** page of an LLM Proxy starts in staging, like the plans of MCP Proxies and A2A Proxies. Consumers can't subscribe to it until you publish it from the actions menu of the plan, and it takes effect once you deploy the proxy. In 4.12, a plan added to an existing LLM Proxy was published right away. The plans that the LLM Proxy creation wizard creates are still published.

**FIPS images: JKS and PKCS12 keystores no longer load**

From 4.13.0, the FIPS image variants are built on a JDK 25 FIPS base image. The 4.12 FIPS images used JDK 21. On the JDK 25 base, BouncyCastle FIPS in approved-only mode provides no PKCS12 keystore and answers JKS read-only, so neither format loads. A FIPS deployment that upgrades from 4.12 while keeping a `jks` or `pkcs12` keystore or truststore on the Gateway fails to start its TLS listeners.

Before you upgrade, convert the Gateway's listener keystores and truststores to `pem`, or to `bcfks` where a store is read from a file. Both formats load on the FIPS images of 4.12.19 and later and of 4.13. Some stores don't accept `bcfks`, so on the 4.13 FIPS images:

* The Management API can't serve HTTPS. Its own HTTPS listener reads only a `jks` or `pkcs12` keystore, and neither loads. Terminate TLS in front of it instead.
* A Gateway keystore read from a Kubernetes configmap can't load, because a configmap location takes only `jks` and `pkcs12`. Put it in a Kubernetes TLS secret as `pem` instead, or read it from a file path.
* The Redis stores for rate limiting and distributed sync load `pem` only.

The ordinary images aren't affected. For the full list of formats and how each behaves, see [FIPS images](../self-hosted-installation-guides/docker/fips-images.md).

**Inline Authentication Provider resource 3.0.0: Usernames and passwords are read as Expression Language**

Version 3.0.0 of the Inline Authentication Provider resource evaluates the username and password of each user as Gravitee Expression Language when the API is deployed. Earlier versions didn't evaluate either value. The plugin isn't included in the default APIM distribution, so the change applies when you deploy version 3.0.0.

A literal value that contains `{#`, `{T`, or `{(` followed by a closing `}` is therefore read as an expression, not as the text it holds. Spaces after the `{` don't change this. A `{#` with no closing `}` makes the evaluation fail. If the evaluation fails, or returns no value or an empty value, the resource rejects every user, not only the user that holds the value. When the evaluation fails, the value appears in the Gateway logs as typed.

Before you deploy version 3.0.0, check every Inline Authentication Provider resource for a username or password that contains a `{`, and change it. For more information, see [Inline Authentication Provider](../create-and-configure-apis/apply-policies/resources.md#inline-authentication-provider).

**Latency policy: The response phase now adds latency**

From 4.12.22 and 4.13.0, the Latency policy runs in the response phase of v2 APIs, v4 HTTP proxy APIs, and v4 message APIs. In 4.12.21 and earlier, a Latency policy in a response phase had no effect. The **Policy Studio** of a v2 API and the **Platform flows** on the organization's **Policies** page already let you add it there.

After the upgrade, such a policy delays the responses that its flow handles by its configured time. Before you upgrade, check the response phase of every flow in the **Policy Studio** of your v2 APIs and in the **Platform flows**. Remove any Latency policy that you don't want to take effect. For more information, see [Latency](../create-and-configure-apis/apply-policies/policy-reference/latency.md).

**LLM proxy: Sent tokens include the prompt cache for Anthropic and Bedrock**

On an LLM proxy API, three values now count the whole prompt for models served by the Anthropic and Bedrock providers: the `long_llm-proxy_tokens-sent` metric, the `llmproxy.usage.sent.token` context attribute, and the `X-LLM-Proxy-Tokens-Sent` response header. The whole prompt includes the tokens read from or written to the provider's prompt cache. In 4.12, they used the input count that these two providers report, which leaves those tokens out. For the same traffic, a prompt that uses the provider's cache therefore counts more sent tokens than before, and a Token Rate Limit policy counts more tokens against its limit.

The `double_llm-proxy_sent-cost` metric and the `llmproxy.usage.sent.cost` context attribute now price the cache reads and cache writes at the model's cache prices, and at the input price when the model has no cache price. For the Anthropic and Bedrock providers, the sent cost therefore includes the cache reads and cache writes that 4.12 left out, and a Cost Rate Limit policy counts that cost too.

Before you upgrade, review the Token Rate Limit policies and the dashboards that read sent tokens on LLM proxy APIs that serve Anthropic or Bedrock models. To price cached tokens at the provider's rates, set the cache prices of each model. For more information, see [Assign Metrics](../create-and-configure-apis/apply-policies/policy-reference/assign-metrics.md#metrics-on-llm-proxy-apis) and [Reporters](../analyze-and-monitor-apis/reporters/README.md).

**XML Validation policy: Failed validations return a list of violations**

APIM 4.13 bundles version 2.x of the XML Validation policy, which changes the response to a request that fails validation.

On v4 HTTP proxy APIs and on v2 APIs in emulation mode, the response body is a JSON object with a `message` field and a `violations` array that lists each problem. The error key is `XML_VALIDATION_FAILED`. `message` holds **Http error message**, or `XML validation failed` when that field is empty. In 4.12, the message was `Bad Request` when the field was empty, and a request that accepted JSON got a body with `message` and `http_status_code` fields. Other requests got the message alone, and now get the JSON object, still with the `text/plain` content type.

On v2 APIs with emulation mode disabled, an empty **Http error message** now returns a text summary of the violations instead of `Bad Request`, and the error key is `XML_INVALID_PAYLOAD`. When the request's `Accept` header includes `application/json` or `*/*`, the body is a JSON object with the message in `message` and the status code in `http_status_code`, and the content type is `application/json`. Otherwise, the body is the message alone, and the content type is `text/plain`.

Before you upgrade, check the API consumers that read these responses. For more information, see [XML Validation](../create-and-configure-apis/apply-policies/policy-reference/xml-validation.md#errors).

**XML Validation policy: Requests that declare a `DOCTYPE` and schema downloads are blocked**

The XML Validation policy that APIM 4.13 bundles rejects a request body that declares a `DOCTYPE`, with the same `400` response as a body that doesn't match the schema. It also no longer downloads a schema that an `xs:import` or `xs:include` names with an `http`, `https`, or `file` URL in its `schemaLocation`, so a schema that does this doesn't compile. In 4.12, the policy accepted a `DOCTYPE` and downloaded the schemas at those URLs.

**XML Validation policy: A schema that doesn't compile now fails requests**

When the policy's schema doesn't compile, requests fail with `500`, the error key `XML_VALIDATION_SCHEMA_COMPILE_FAILED`, and the message `Unable to compile the XSD schema`, and don't reach the backend. This applies whatever the **Schema source**. In 4.12, an inline schema that didn't compile left the policy unapplied, so requests reached the backend without validation.

Before you upgrade, check for API consumers that send a `DOCTYPE`, and for schemas that don't compile, including inline schemas that import or include a schema by URL. For more information, see [XML Validation](../create-and-configure-apis/apply-policies/policy-reference/xml-validation.md#errors).

**Encrypted API properties: The Management API v2 masks values and checks encryption**

From 4.13.0, the Management API v2 returns `••••••••••••` in place of the value of an encrypted API property when it returns an API, for v2 and v4 APIs. In 4.12, it returned the encrypted value. When you update an API, send `••••••••••••` back to keep the stored value, or send a new plain text value with `encryptable` set to `true` to replace it. Responses that return the stored API definition, such as `GET /apis/{apiId}/deployments/current` and the API events, still hold the encrypted value, as does the API export.

When you save an API, APIM refuses `••••••••••••` sent as the value of a property that has no encrypted value stored. The response is HTTP `400` with the error key `api.property.maskedValue`. When you save a v4 API, APIM also refuses the following with HTTP `400`:

* An encrypted property sent back as plain text, with `encrypted` and `encryptable` set to `false`. The error key is `api.property.encryptedToPlain`.
* A new value for an encrypted property, marked as encrypted, that the installation's secret can't decrypt, for example an encrypted value exported from an installation that uses another secret. The error key is `api.property.notCiphertext`. In 4.12, the value was accepted.

APIM doesn't check whether it can decrypt a new value for a property that has no encrypted value stored yet, so make sure encrypted values you import were encrypted with this installation's secret.

When the secret can't encrypt a value, saving an encrypted property of a v4 API fails with HTTP `500`. In 4.12, the property was saved with its plain text value.

Before you upgrade, review the scripts that read API properties from the Management API v2, and the scripts that update APIs with encrypted values from another installation. For more information, see [Encrypt dynamic properties](../create-and-configure-apis/apply-policies/v4-api-policy-studio.md#encrypt-dynamic-properties) and [Property Encryption](../prepare-a-production-environment/production-best-practices/general-recommendations/property-encryption.md).

**Gateways connected to Gravitee Cloud: Tracing of v2 APIs is off by default, and deprecated tracing settings are overridden**

From 4.13.0, `services.opentelemetry.tracing.v2.enabled` defaults to `false` on a Gateway that connects to Gravitee Cloud with a Cloud Token. On other Gateways, it still defaults to `true`. In 4.12, a Gateway with OpenTelemetry turned on traced its v2 APIs by default.

A Hybrid Gateway that uses its own OpenTelemetry configuration without this setting therefore stops tracing its v2 APIs after the upgrade. A Gravitee Hosted Gateway linked to an OpenTelemetry reporter in Gravitee Cloud isn't affected, because the reporter's **Include v2 APIs** switch sets the value.

A Gateway that connects to Gravitee Cloud with a Cloud Token now sends its traces and payload logs to Gravitee Cloud unless it has a `services.opentelemetry` setting. The deprecated `services.tracing` settings don't count. A Hybrid Gateway that still uses them sends its traces to Gravitee Cloud after the upgrade, instead of to its own collector.

Before you upgrade a Hybrid Gateway that traces v2 APIs, set `services.opentelemetry.tracing.v2.enabled` to `true` on it. Setting `services.opentelemetry.tracing.v2.enabled` is itself a `services.opentelemetry` setting: on a Gateway without its own OpenTelemetry configuration, it stops the Gateway from sending to Gravitee Cloud and doesn't turn OpenTelemetry on. Set it only on a Gateway that already exports to your own collector. Move any `services.tracing` settings to `services.opentelemetry`. For more information, see [Tracing for v2 APIs](../analyze-and-monitor-apis/opentelemetry.md#tracing-for-v2-apis).

**Helm: `gateway.kafka.secured` is renamed to `gateway.kafka.probe.secured`**

From 4.13.0, the Helm value that sets whether the Gateway's TCP health probe connects to the Kafka port over TLS is `gateway.kafka.probe.secured`. `gateway.kafka.secured` is deprecated. The chart still reads it when `gateway.kafka.probe.secured` isn't set, and `gateway.kafka.probe.secured` wins when both are set. The value affects only the health probe, not the Kafka server.

Before you upgrade, rename `gateway.kafka.secured` to `gateway.kafka.probe.secured` in your values file.

**Management API: Stricter permission and ownership checks**

From 4.13.0, the Management API checks permissions and ownership on more endpoints. A script or integration that relied on a missing check now gets `403`, `404`, or an empty result. Requests made with the right permissions, on resources of the same environment, are unaffected.

* **Subscriptions.** Subscribing an application to an API plan with `POST /applications/{application}/subscriptions` returns `404` unless you're an organization administrator, a member of the API, or the API is published in a portal. `POST /apis/{api}/subscriptions` returns `404` for a plan of another API or environment, and requires the `APPLICATION_SUBSCRIPTION[CREATE]` permission on the application. Listing subscriptions with `GET /subscriptions?application=` requires `APPLICATION_SUBSCRIPTION[READ]` on the application, and otherwise returns `403`. Pausing, resuming, or changing the status of a subscription of another API or environment returns `404`.
* **API search.** `POST /apis/_search` returns an empty result to a user who can access no API.
* **Plans.** Plan endpoints under `/apis/{api}/plans/{plan}` reject a plan that doesn't belong to the API: Management API v1 returns `400`, and Management API v2 returns `404`.
* **Promotions.** Processing a promotion of a V4 API requires `ENVIRONMENT_API[CREATE]`, or `ENVIRONMENT_API[UPDATE]` for an existing API, on the target environment, and otherwise returns `403`. A promotion of another organization returns `404`, and a promotion that isn't awaiting validation returns `400`. Searching promotions requires `API_DEFINITION[READ]` on the API.
* **User search.** `GET /organizations/{orgId}/search/users` returns `403` unless you manage members somewhere, for example with `ORGANIZATION_USERS[READ]`, or with `MEMBER[CREATE]` or `MEMBER[UPDATE]` on an API, application, or group.
* **Roles.** Granting or revoking a role with `PUT /organizations/{orgId}/users/{userId}/roles` requires you to be an organization administrator, or to hold every permission of that role. Otherwise, it returns `403`.
* **Groups, alerts, documentation, and notifications.** Group invitations and group members of another environment, alert events of an alert that doesn't belong to the API, and API pages that don't belong to the API return `404`. Creating a notification setting requires `ENVIRONMENT_NOTIFICATION[CREATE]` for the current environment, and otherwise returns `403`. Deleting a notification setting that doesn't exist returns `404` instead of `204`.
* **API import, API Score, and Newt AI.** Importing an API from a URL with `PUT /apis/import` requires `ENVIRONMENT_API[UPDATE]`. API Score and Newt AI require `ENVIRONMENT_API[READ]`, and Newt AI generation returns `429` above 30 calls a minute for each user.

Before you upgrade, review the scripts and integrations that call these endpoints, and the permissions of the accounts they use.

**Users without specific permissions no longer see request logs, other groups' memberships, or shared policy group steps**

From 4.13.0, the Management API checks a specific permission before it returns the following data. The check applies to every role, including the default USER role, so a user who saw this data in 4.12 can lose access to it after the upgrade:

* **Request logs and analytics.** The environment's request logs show only the APIs on which you hold `API_LOG[READ]`. Analytics aggregates require `API_ANALYTICS[READ]` on each API, or `ENVIRONMENT_PLATFORM[READ]` for the whole environment. `ENVIRONMENT_API[READ]` alone no longer gives access to either. A user who can read no data gets an empty result, not `403`.
* **Group memberships.** `GET /configuration/groups/{group}/memberships` of the Management API v1 returns `403` unless you manage the group: an organization administrator, a group administrator, or a user with `ENVIRONMENT_GROUP[CREATE]`, `ENVIRONMENT_GROUP[UPDATE]`, or `ENVIRONMENT_GROUP[DELETE]`. A member of an API or application can still see the groups attached to it.
* **Shared policy group steps.** Without `SHARED_POLICY_GROUP[UPDATE]`, the Management API v2 and the Automation API return a shared policy group without its `steps`.

Before you upgrade, review the roles of the users and service accounts that read this data, and grant the permissions they need.

**WS-Security Authentication policy 4.0.0: Requests are checked against OASIS WSS 1.1**

APIM 4.13 bundles version 4.0.0 of the WS-Security Authentication policy, which checks the `wsse:Security` header against OASIS WSS 1.1 SOAP Message Security and the UsernameToken Profile. Requests that version 2.x accepted can now be rejected:

* The policy reads only a `wsse:Security` header in the OASIS 2004 or 2003 namespace that targets the ultimate receiver: with no `actor` in SOAP 1.1, and with no `role` or the `ultimateReceiver` role in SOAP 1.2. The request must carry exactly one such header.
* The header must hold exactly one `UsernameToken`, with one `Username` and one `Password`. The password must be `PasswordText`. Any other type, such as `PasswordDigest`, is rejected.
* A `wsu:Timestamp` whose `wsu:Expires` has passed, or whose `wsu:Created` is in the future, is rejected beyond the new **Clock skew (seconds)** option, which defaults to `60`. Times must carry a UTC offset.
* The new **Require a timestamp** option, off by default, rejects a header with no `wsu:Timestamp` or with no `wsu:Expires`.
* A request body that declares a `DOCTYPE` is rejected.

Every rejection still returns HTTP `401`, but the error keys and messages change. In 2.x, every failure used `WSSECURITY_AUTH_UNAUTHORIZED` with the message `Unauthorized`. In 4.0.0, the message is the WS-Security fault string:

<table><thead><tr><th>Error key</th><th>Message</th></tr></thead><tbody><tr><td><code>WSSECURITY_AUTH_INVALID</code></td><td><code>An error was discovered processing the wsse:Security header</code> or <code>An invalid security token was provided</code></td></tr><tr><td><code>WSSECURITY_AUTH_UNSUPPORTED</code></td><td><code>An unsupported token was provided</code></td></tr><tr><td><code>WSSECURITY_AUTH_EXPIRED</code></td><td><code>The message has expired</code></td></tr><tr><td><code>WSSECURITY_AUTH_UNAUTHORIZED</code></td><td><code>The security token could not be authenticated or authorized</code></td></tr></tbody></table>

The policy doesn't return a SOAP Fault. To return one, use a response template. Version 4.0.0 also fixes the HTTP authentication provider, which rejected every request with `401` in earlier versions because the policy didn't wait for its answer.

Before you upgrade, review the response templates keyed on `WSSECURITY_AUTH_UNAUTHORIZED`, because malformed requests now use `WSSECURITY_AUTH_INVALID`. For more information, see [WS-Security Authentication](../create-and-configure-apis/apply-policies/policy-reference/ws-security-authentication.md).

**Generate HTTP Signature policy: No empty first line when the payload isn't signed**

From 4.12.21 and 4.13.0, the Generate HTTP Signature policy signs only the configured headers on a request when payload signing is off, as it did in 4.11. From 4.12.0 to 4.12.20, the signed string started with an empty line in place of the payload. A verifier adjusted for the 4.12 signatures now sees a mismatch. When payload signing is on, an empty payload still adds an empty first line.

Before you upgrade, check the verifiers of APIs that use this policy without payload signing. For more information, see [Generate HTTP Signature](../create-and-configure-apis/apply-policies/policy-reference/generate-http-signature.md).

**Timing metrics: The endpoint response time includes the response body**

For v4 APIs whose endpoint is the HTTP proxy, `endpoint-response-time-ms` now runs until the response body is fully proxied, where it previously stopped at the first byte. Two new fields complete it: `endpoint-response-ttfb-ms`, the time to the first byte, and `endpoint-connect-time-ms`, the time to get a connection to the endpoint. The Gateway latency is still the Gateway response time minus the endpoint response time, so the body transfer moves out of `gateway-latency-ms`. The Gateway response time and latency also now include the time the Gateway takes to dispatch the request to the API.

The File and TCP reporters write the new fields as `endpointResponseTtfbMs` and `endpointConnectTimeMs`. The CSV format doesn't carry them. These changes also ship in 4.12.15 and later, and the dispatch time in 4.12.21 and later.

Before you upgrade, review the dashboards and alert thresholds that read endpoint response time or Gateway latency. For more information, see [Reporters](../analyze-and-monitor-apis/reporters/README.md).

**Flows: A path with the `**` wildcard is rejected when you save an API**

Saving or importing a v4 API whose flow has an HTTP selector with the **Equals** operator and a path that contains `**` fails with `400` and the message `The flow [<name>] contains an HTTP selector with an invalid wildcard path`. The **Starts with** operator is checked the same way. This applies to the Console, the Management API v2, the Automation API, the Gravitee Kubernetes Operator, and the Terraform provider. It also applies from 4.12.0.

Before you upgrade, remove `**` from the flow paths of your v4 APIs and from the API definitions your pipelines push.

**Environment logs: The request URI filter matches by prefix**

From 4.13.0, the environment logs search of the Management API v2, `POST /environments/{envId}/logs/search`, filters `URI` with `STARTS_WITH`, which matches the start of the request URI and accepts the `*`, `?`, and `\` wildcards. `EQ` on `URI` is a deprecated alias of `STARTS_WITH`, so a search for an exact URI also returns the requests whose URI starts with it. A saved Console link that filters the URI with equals opens without that filter.

Before you upgrade, check the scripts that search logs with an exact URI, and recreate the saved links that filter on it.

**Rate Limit, Quota, and Spike Arrest policies: A policy without a limit rejects every request**

A Rate Limit, Quota, or Spike Arrest policy needs a limit. When a policy sets neither a static limit nor a dynamic limit, its limit is now `0`, so it rejects every request with `429` and the error key `RATE_LIMIT_TOO_MANY_REQUESTS`, `QUOTA_TOO_MANY_REQUESTS`, or `SPIKE_ARREST_TOO_MANY_REQUESTS`. Previously, such a policy failed every request with `500`. This also applies from 4.12.17.

Before you upgrade, check that every Rate Limit, Quota, and Spike Arrest policy sets a limit, including the policies that the Gravitee Kubernetes Operator, the Terraform provider, and your import pipelines push.

**MCP entrypoint: A `GET` that asks for a Server-Sent Events stream returns `405`**

An MCP Proxy answers a `GET` request whose `Accept` header contains `text/event-stream` with `405`, the error key `MCP_PROXY_METHOD_NOT_ALLOWED`, and a JSON-RPC error that asks the client to send its requests with `POST`. Previously, the request reached the upstream server, and a keyless plan could answer it with a misleading `401`. Paths that start with `/.well-known` or `/.auth/` aren't affected. This also applies from 4.12.13.

{% hint style="info" %}
**New Developer Portal upgrade notes**

The following changes to the New Developer Portal aren't breaking changes, but they can change what you see or how your automation behaves after the upgrade.

**An "APIs" folder is added to the top navigation bar**

On the first Management API startup after the upgrade, every environment gets a published, public folder named `APIs` at the end of the New Developer Portal's top navigation bar. It isn't added when a top-level folder named `APIs` already exists. The folder is added once, so if you delete it, it doesn't come back.

**Automation API: A hand-made folder blocks an apply at the same path**

From 4.13.0, a folder created for an API in the Console or the portal editor belongs to the API. When an Automation API apply declares a `portalNavigation` path that such a folder already occupies, the apply, and its dry run, fails with `400` and the message `Navigation path [<path>] is already occupied by content not managed by the Automation API`.

Before you upgrade, compare the `portalNavigation` paths of your Automation API configurations, Kubernetes resources, and Terraform configurations with the folders of each API. Rename or remove a conflicting folder to let the apply succeed. For more information, see [API documentation](../developer-portal/new-developer-portal/customize-the-navigation/portal-automation/api-documentation.md).

**Portal capability and application membership settings move to Portal Settings**

From 4.13.0, the **Portal capabilities** and **Application membership** settings of the New Developer Portal are in **Settings** under **Portal Settings**, and no longer in the Console's **Settings**. **Portal Settings** appears in the Console menu when the New Developer Portal is enabled. **Enable the New Developer Portal** stays in the Console's **Settings**. For more information, see [Configure New Developer Portal settings](../developer-portal/new-developer-portal/configure-new-developer-portal-settings.md).

**A private folder can't hold public items**

From 4.13.0, the navigation of the New Developer Portal doesn't let a public item sit under a private folder. An Automation API apply that declares a public item under a private folder fails with `400` and the message `Parent item with id <id> must be PUBLIC to create a public child item.` In the Console and Gravitee Gamma, making a folder private also makes everything inside it private, and an item under a private folder can't be made public.

Before you upgrade, check the visibility of the folders and items your Automation API configurations declare. For more information, see [Customize the navigation](../developer-portal/new-developer-portal/customize-the-navigation.md).
{% endhint %}

**Automation API and resource imports: Updating an object requires the update permission**

From 4.13.0, an Automation API apply, and the Management API v2 imports that create or update an object, check the update permission when the object already exists. Previously, they checked only the create permission. A service account that holds only the create permission now gets `403` when it applies a change to an existing object.

<table><thead><tr><th>Object</th><th>Create permission</th><th>Update permission</th></tr></thead><tbody><tr><td>API</td><td><code>ENVIRONMENT_API</code></td><td><code>API_DEFINITION</code> on the API</td></tr><tr><td>Application</td><td><code>ENVIRONMENT_APPLICATION</code></td><td><code>APPLICATION_DEFINITION</code> on the application</td></tr><tr><td>Group</td><td><code>ENVIRONMENT_GROUP</code></td><td><code>ENVIRONMENT_GROUP</code></td></tr><tr><td>Shared policy group</td><td><code>ENVIRONMENT_SHARED_POLICY_GROUP</code></td><td><code>ENVIRONMENT_SHARED_POLICY_GROUP</code></td></tr><tr><td>Dictionary</td><td><code>ENVIRONMENT_DICTIONARY</code></td><td><code>ENVIRONMENT_DICTIONARY</code></td></tr><tr><td>Portal, listing, link, and portal documentation</td><td><code>ENVIRONMENT_PORTAL</code></td><td><code>ENVIRONMENT_PORTAL</code></td></tr><tr><td>Theme</td><td><code>ENVIRONMENT_THEME</code></td><td><code>ENVIRONMENT_THEME</code></td></tr><tr><td>API documentation and link</td><td><code>API_DOCUMENTATION</code> on the API</td><td><code>API_DOCUMENTATION</code> on the API</td></tr><tr><td>Subscription</td><td><code>API_SUBSCRIPTION</code> on the API</td><td><code>API_SUBSCRIPTION</code> on the API</td></tr></tbody></table>

Changing the members of an API or application also requires `API_MEMBER[UPDATE]` or `APPLICATION_MEMBER[UPDATE]`. An apply that restates the current members doesn't. `PUT /applications/_import/crd` of the Management API v2 now requires `ENVIRONMENT_APPLICATION[CREATE]` instead of `ENVIRONMENT_API[CREATE]`.

Before you upgrade, review the permissions of the service accounts that the Gravitee Kubernetes Operator, the Terraform provider, and your pipelines use.

#### 4.12.0

**JSON Validation policy: response error keys corrected**

The JSON Validation policy now emits error keys that match their documented names for response-scope failures in V4 APIs. Previously, the keys were swapped: `JSON_INVALID_RESPONSE_FORMAT` was emitted for parse failures, and `JSON_INVALID_RESPONSE_PAYLOAD` for schema validation failures.

If you configured response templates using these error keys, you must update them to use the correct key names.

**`gravitee-resource-cache-redis` requires version 5.0.0**

If you use the `gravitee-resource-cache-redis` plugin, you must upgrade it to version 5.0.0 when upgrading to APIM 4.12. This plugin is not included in the default APIM bundle and must be managed independently. Running an older version of `gravitee-resource-cache-redis` with APIM 4.12 is not supported.

**Redis cache resource now uses a shared connection pool**

The Redis cache resource now uses a shared Redis client factory with gateway-wide connection pool and timeout settings. Previously, each API using a Redis cache resource maintained its own dedicated connection to Redis, so 100 APIs with a Redis cache resource resulted in 100 active Redis connections to the server.

If you use the `gravitee-resource-cache-redis` or `aiVectorStoreRedis` resource, review and adjust the following settings to suit your workload:

* `resources.aiVectorStoreRedis.maxPoolSize`
* `gateway.cacheRedis.maxPoolSize`
* Timeout settings for both resources

**v1 API definitions removed from the Management API v2 contract**

From 4.12.0, APIM no longer supports v1 APIs. The `ApiV1` and `Rule` schemas and the `V1` value of the `DefinitionVersion` enum are removed from the Management API v2 OpenAPI specification. Migrate any remaining v1 APIs to at least a v2 definition before you upgrade. For more information about how APIM handles v1 APIs, see [Support for v1 APIs](support-for-v1-apis.md).

**Automation API restricts shared policy group API types and phases**

The Automation API now accepts shared policy groups only for the `PROXY` and `MESSAGE` API types. The `apiType` property of a shared policy group no longer accepts `NATIVE`, `A2A_PROXY`, `LLM_PROXY`, or `MCP_PROXY`, and the `FlowPhase` schema no longer includes the `ENTRYPOINT_CONNECT` and `INTERACT` values. The Automation API rejects a shared policy group specification that uses one of the removed values.

This change affects Automation API clients, including the Gravitee Kubernetes Operator (GKO) and the Gravitee Terraform provider. These API types and phases remain available for shared policy groups in the Management API v2 and the Console.

**`hidden` property removed from the Automation API metadata schema**

The `Metadata` schema of the Automation API no longer includes the `hidden` property. This change affects API and application metadata that you manage through the Automation API. If you use the Terraform provider, see the migration steps in the [Terraform provider release notes](../terraform/release-notes.md).

**Cluster creation through the Management API v2 requires a cluster type**

The request body of the Create Cluster endpoint of the Management API v2 (`POST /environments/{envId}/clusters`) now requires a `type` property with one of the following values: `KAFKA_CLUSTER_STANDALONE`, `KAFKA_CLUSTER`, or `KAFKA_VIRTUAL_CLUSTER`. In earlier versions, the request body schema didn't include a `type` property. Update any clients or scripts that create clusters to include the `type` property.

#### 4.11.14

**API Key policy: the header name set on a plan takes precedence over the Gateway setting**

APIM 4.11.14 and later bundle version 6.0.0 or later of the API Key policy, which changes how the Gateway resolves the name of the header that carries the API key. The Gateway now applies the header name set on the plan whenever that value isn't empty, and it no longer checks the plan's `enableCustomApiKeyHeader` option. Previously, the Gateway applied the header name set on the plan only when `enableCustomApiKeyHeader` was `true`, and that option defaults to `false`, so a plan left at that default fell back to the `policy.api-key.header` value from `gravitee.yml`. V2 APIs that don't run on the emulation engine keep the earlier behavior and still require `enableCustomApiKeyHeader`.

When a plan stores a header name, that name now overrides `policy.api-key.header`. A request that sends the key only on the Gateway-level header returns `401 Unauthorized`, because the Gateway reads the header name set on the plan and then falls back to the `api-key` query parameter. Before you upgrade, open each API Key plan and check the **API Key Header** field. Set the field to the header name that your clients send, or clear it on plans that rely on the Gateway-level header.

APIM 4.12.0 and later also bundle version 6.x. For the full resolution order, see [API Key](../create-and-configure-apis/apply-policies/policy-reference/api-key.md).

#### 4.11.0

**A2A Proxy APIs architecture**

The A2A proxy architecture introduces the `A2A_PROXY` API type. With this change, you must create your A2A Proxy APIs again to avoid any issues and to align with the new architecture.

**Next-Gen Developer Portal APIs and documentation pages must be published again**

When you upgrade to APIM 4.11, any APIs and documentation pages that you published to the New Developer Portal are no longer published. After you upgrade to 4.11, publish your APIs and documentation pages again through the **Navigation items** section of the New Developer Portal settings.

**New Developer Portal subscriptions require published API pages**

When you upgrade to APIM 4.11, an API accepts subscriptions through the New Developer Portal only after you publish the API's pages. To enable subscriptions to an API, publish the API's pages through the **Navigation items** section of the New Developer Portal settings.


#### 4.10.0

**Kafka Native APIs Analytics**

Elasticsearch indices used by Kafka Native APIs have been modified for better compatibility with OpenSearch and better accuracy.

You might have to do a roll-over of your `gravitee-event-metrics` index.

Previous indexed document is deleted. However, they are no longer be taken into account in Gravitee Dashboards.

#### 4.9.0

**Update to OpenShift compatibility**

Before 4.9.0, users had to override the `runAsGroup`'s `securityContext` to set the GID to 1000.

With this update, the user must set the `runAsGroup`'s `securityContext` to `null` to allow OpenShift to select the root group.

**Customization on Federation ingress**

If the `integration-controller` ingress uses the same host as the `management` ingress, it no longer inherits the annotation of the `management` ingress. With 4.9.0, you must configure the `integration-controller` ingress with the following values:

```yaml
api:
  federation:
    ingress:
      enabled: true
      path: /integration-controller(/.*)?
      pathType: Prefix
      hosts:
        - apim.example.com
      annotations:
        kubernetes.io/ingress.class: nginx
        nginx.ingress.kubernetes.io/proxy-read-timeout: 3600   
```

If you want the `integration-controller` ingress to use the same host as the `management` ingress, set the same values for `hosts` and `tls` in the `integration-controller` ingress, `management` ingress, and `federation` ingress.

**Elasticsearch template updates required**

When you upgrade to 4.9.0, you must update Elasticsearch templates to support execution transparency analytics with error and warning component tracking. If you manage your own Elasticsearch installation, update index templates before you upgrade. Elasticsearch auto-generates templates if you do not manually update them, but this results in suboptimal field mappings. Gravitee-managed Elasticsearch or SaaS deployments update automatically.

#### 4.8.0

**APIM standalone components**

The APIM standalone components that were available to download from [Gravitee.io downloads - apim/components](https://download.gravitee.io/#graviteeio-apim/components/) are no longer available or supported.

You can use the full distribution .ZIP file instead. To download the full distribution .ZIP file, go to [Gravitee.io downloads - apim/distributions](https://download.gravitee.io/#graviteeio-apim/distributions/).

**Lucene update 10**

Lucene has been upgraded to 10. Before starting the Management API (mAPI), you must clean the `/data` directory in your `GRAVITEE_HOME` containing Lucene working files. Otherwise, the mAPI does not start. There is no impact. When mAPI restarts, it re-indexes.

**Custom plugin development**

If a plugin is referencing `io.gravitee.gateway.reactor.ReactableApi`, it needs to be recompiled with APIM 4.8 dependencies because `ReactableApi` it is now an interface rather than an abstract class. Without recompilation, the plugin throws a `java.lang.IncompatibleClassChangeError` .

#### 4.7.0

**Hazelcast**

During a rolling upgrade in Kubernetes, if a pod with the version about to be replaced is still running, mAPI throws these warnings:

`09:36:15.515 [graviteeio-node] WARN c.h.i.impl.HazelcastInstanceFactory - Hazelcast is starting in a Java modular environment (Java 9 and newer) but without proper access to required Java packages. Use additional Java arguments to provide Hazelcast access to Java internal API. The internal API access is used to get the best performance results. Arguments to be used: --add-modules <http://java.se|java.se> --add-exports java.base/jdk.internal.ref=ALL-UNNAMED --add-opens java.base/java.lang=ALL-UNNAMED --add-opens java.base/sun.nio.ch=ALL-UNNAMED --add-opens java.management/sun.management=ALL-UNNAMED --add-opens jdk.management/com.sun.management.internal=ALL-UNNAMED 09:36:24.589 [graviteeio-node] WARN c.h.kubernetes.KubernetesClient - Cannot fetch public IPs of Hazelcast Member PODs, you won't be able to use Hazelcast MULTI_MEMBER or ALL_MEMBERS routing Clients from outside of the Kubernetes network`

Once the pod is terminated, `cache-hazelcast` installs successfully. The upgrade process then continues as expected with the upgrader scripts, which means that there will be a brief downtime when upgrading to 4.7.x.

**Azure API Management update**

There is a new parameter for ingesting Azure APIs. To ingest Azure APIs, you must set `gravitee_integration_providers_0_configuration_subscriptionApprovalType` in your `docker-compose.yaml` and set the `SUBSCRIPTION_APPROVAL_TYPE` in your `.env` file to `AUTOMATIC` , `MANUAL` or `ALL` .

To keep the previous behavior of Azure API Management, set the `SUBSCRIPTION_APPROVAL_TYPE` to `AUTOMATIC` .

#### 4.6.0

**OpenTracing replaced by OpenTelemetry**

OpenTracing has been replaced by OpenTelemetry. If you use OpenTracing with the Jaeger plugin, you must update your configuration to target your OpenTelemetry endpoint.

#### 4.4.0

**gateway.management.http.trustall update**

The gateway.management.http.trustall has been renamed to trustALL. By default, trustAll is set to `false`. A public CA or a well configured continue to work.

**gateway|api.services.bridge.ssl.clientAuth no longer use a boolean value**

gateway|api.services.bridge.ssl.clientAuth no longer use a boolean value. Possible values are now the following values:

* `none`. This value was previously false
* `required`. Backward compatibility is maintained, true means required
* `request`.

#### 4.0.27

**ssl-redirect option changed to default**

In gateway ingress controller, the ssl-redirect option was changed from "false" to default. For more information about this change, go to [Server-side HTTPS enforcement through redirect](https://kubernetes.github.io/ingress-nginx/user-guide/nginx-configuration/annotations/#server-side-https-enforcement-through-redirect).

### Breaking changes from 3.X

Here are the breaking changes from versions 3.X of Gravitee.

#### 3.2.0

**Moved Probes configuration**

Probes configuration was moved under deployment.

**Probe default configuration**

Changed probe default configuration. For more information about the change to the default configuration, go to the following [GitHub pull request](https://github.com/gravitee-io/gravitee-api-management/pull/8885).

**Removed the apiSync parameter**

Under gateway.readinessProbe, the apiSync parameter was removed.

#### 3.1.55

**Use of smtp.properties.starttlsEnable**

Use smtp.properties.starttls.enable instead of smtp.properties.starttlsEnable.

## Deprecated functionality

Here is the deprecated functionality for 4.X versions of Gravitee and 3.X version of Gravitee.

### Deprecated functionality 4.X

Here is the deprecated functionality from 4.X of Gravitee

#### 4.13.0

**v2 APIs are deprecated**

From 4.13.0, v2 APIs are deprecated. The October 2027 release of APIM removes them. Migrate your v2 APIs to v4 before you upgrade to that release. For more information, see [Migrate APIs](../create-and-configure-apis/create-apis/migrate-apis.md).

**MongoDB and Elasticsearch subcharts are deprecated**

From 4.13.0, the `mongodb` and `elasticsearch` subcharts of the APIM Helm chart are deprecated, and APIM 4.15.0 removes them. They run `bitnamilegacy` images that no longer receive security updates. Both subcharts are disabled by default, and a deployment that uses an external MongoDB or Elasticsearch isn't affected.

If you enable either subchart, move your data to a MongoDB or Elasticsearch instance deployed outside the chart before you upgrade to 4.15.0. Point `mongo.*` or `es.*` at the new instance, and then set `mongodb.enabled` or `elasticsearch.enabled` to `false`. For more information, see the installation guide for [Vanilla Kubernetes](../self-hosted-installation-guides/kubernetes/vanilla-kubernetes/README.md), [AWS EKS](../self-hosted-installation-guides/kubernetes/aws-eks.md), [Azure AKS](../self-hosted-installation-guides/kubernetes/azure-aks.md), or [OpenShift](../self-hosted-installation-guides/kubernetes/openshift.md).

**The identity provider tokens returned at login will be hidden by default**

From 4.13.0, four settings decide whether the Management API returns the access token and the ID token of the identity provider when a user logs in to the Console or the Developer Portal with an identity provider: `console.authentication.expose.accessToken`, `console.authentication.expose.idToken`, `portal.authentication.expose.accessToken`, and `portal.authentication.expose.idToken`. In 4.13, each defaults to `true`, which keeps the behavior of earlier versions. APIM 4.14 changes their default to `false`.

If an integration reads these tokens from the login response, set the settings it needs to `true` before you upgrade to 4.14.

#### 4.4.0

**gateway.management.http.username deprecation**

To allow JWT auth to be configured, gateway.management.http.username and password have been deprecated to allow JWT auth to be configured. For more information about the deprecation, go to [Changelog](https://github.com/gravitee-io/gravitee-api-management/blob/master/helm/CHANGELOG.md).

### Deprecated functionality 3.X

Here is the deprecated functionality from 3.X of Gravitee

#### 3.20.28

**Deprecated api | gateway | ui | portal.security context is removed**

The deprecated api | gateway | ui | portal.security context has been removed.
