---
description: This article covers the new features released in Gravitee API Management 4.3
---

# APIM 4.3

{% hint style="danger" %}
**Make sure you upgrade your license file**

If you are an existing Gravitee Enterprise customer upgrading to 4.x, please make sure that you upgrade your Gravitee license file. Reach out to your Customer Success Manager or Support team in order to receive a new 4.x license.
{% endhint %}

## Introduction

Gravitee 4.3 was released on March 31st, 2024. Feature updates include new API documentation capabilities, sharding tags for v4 APIs, a UI for TCP proxy API creation/configuration, entrypoint/endpoint enhancements, and much more! See the sections below for details.

* [API descriptions](apim-4.3.md#api-descriptions)
* [API documentation](apim-4.3.md#api-documentation)
* [API properties](apim-4.3.md#api-properties)
* [Audit logs](apim-4.3.md#audit-logs)
* [Developer Portal](apim-4.3.md#developer-portal)
* [Endpoint configuration](apim-4.3.md#endpoint-configuration)
* [Entrypoint configuration](apim-4.3.md#entrypoint-configuration)
* [Gravitee Expression Language](apim-4.3.md#gravitee-expression-language)
* [Notifications](apim-4.3.md#notifications)
* [Policies](apim-4.3.md#policies)
* [Sharding tags](apim-4.3.md#sharding-tags)
* [TCP proxy support](apim-4.3.md#tcp-proxy-support)
* [TCP reporter](apim-4.3.md#tcp-reporter)

## API descriptions

In keeping with the OpenAPI Specification's support for Markdown in the Description field, Markdown can be entered in the description field of Gravitee API.

An API description will be rendered as Markdown in the Developer Portal UI if:

* An OpenAPI spec is imported and contains Markdown in the Description field
* Markdown is entered for the description of an API

To learn more about importing an API, see the [documentation](../../guides/create-apis/import-apis/).

## API documentation

Gravitee 4.3 includes numerous API documentation enhancements:

* v4 API documentation supports templating via the **Fill in the content myself** editor, where API properties can be used to access the API data in your documentation.
* YAML or JSON can be entered into the **Fill in the content myself** editor to create an API docs page from either an OpenAPI or AsyncAPI spec. The OpenAPI spec for a documentation page is shown in the APIM Console and reflects how the API documentation is rendered in the Developer Portal.
* To automate the process of creating OpenAPI or AsyncAPI docs pages for v4 APIs, you can make a Management API endpoint REST call to create a docs page from an OpenAPI or AsyncAPI spec.
*   Markdown, OpenAPI, and AsyncAPI files can be uploaded as v4 API documentation pages via the Console.

    <figure><img src="../../.gitbook/assets/docs_content 1 (1).png" alt=""><figcaption><p>Upload a Markdown file as a documentation page</p></figcaption></figure>

    <figure><img src="../../.gitbook/assets/docs_markdown content (1).png" alt=""><figcaption><p>Uploaded Markdown content</p></figcaption></figure>
*   Like user-created content, imported content can be edited via the Markdown editor, and by enabling **Toggle preview**, you can view the content you enter and the rendered page side-by-side.

    <figure><img src="../../.gitbook/assets/edit imported content 1 (1).png" alt=""><figcaption><p>Use the editor to modify imported content</p></figcaption></figure>
* Page referencing allows documentation pages to be reused and easily exported between environments. Within an API's documentation, you can link to one page from another via special syntax.
* In addition to making API documentation available via the Developer Portal, you can send messages to parties interested in your API to advertise updates, warn of upcoming changes, etc. Message delivery mechanism, recipients, and content can be configured in the APIM Console.
*   Dynamic v4 API documentation pages can be created by adding metadata keys and values.

    <figure><img src="../../.gitbook/assets/metadata_screen (1).png" alt=""><figcaption><p>API metadata</p></figcaption></figure>

Refer to the [API Documentation](../../guides/api-configuration/v4-api-configuration/documentation.md) section for more information.

## API properties

v4 API properties can be dynamically managed via the **Properties** tab of the API Management Console's **Configuration** screen\*\*.\*\* To learn more about properties and how to set them, see the [documentation](../../guides/policy-studio/v4-api-policy-studio.md#api-properties).

<figure><img src="../../.gitbook/assets/api properties_dynamically manage (1).png" alt=""><figcaption><p>Dynamically manage properties</p></figcaption></figure>

## Audit logs

Events and audit entries are now captured at the API level for v4 APIs. These are listed in table format and can be filtered by event type and date range.

<figure><img src="../../.gitbook/assets/audit logs_v4 apis (1).png" alt=""><figcaption><p>Events and audit logs</p></figcaption></figure>

See the [Audit Logs](../../guides/api-configuration/v4-api-configuration/audit-logs.md) documentation for more information.

## Developer Portal

### Catalog descriptions

Markdown support has been extended to the **Description** field in the API Catalog. The rendered Markdown will appear in the Developer Portal.

<figure><img src="../../.gitbook/assets/catalog description (1).png" alt=""><figcaption><p>Using Markdown for the Description in the Catalog</p></figcaption></figure>

### Documentation

If incorrect templating is applied to the Markdown page of an API, errors alert the user that the page will not be formatted as intended when published to the Developer Portal.

<figure><img src="../../.gitbook/assets/incorrect templating (1).png" alt=""><figcaption><p>Example of incorrect templating</p></figcaption></figure>

For more information on how to configure documentation for the Developer Portal, see [this section](../../guides/developer-portal/configuration/documentation.md).

## Endpoint configuration

### Health-check

The Management Console's Health-check feature can be used for v4 HTTP proxy APIs to monitor the availability and health of your endpoints and/or your API Gateways.

<figure><img src="../../.gitbook/assets/health-check config form (1).png" alt=""><figcaption><p>Health-check configuration settings for v4 HTTP proxy APIs</p></figcaption></figure>

For more information, see [Health-check](../../guides/api-configuration/v4-api-configuration/endpoints/health-check.md).

### Version history

The Management Console's Version History feature allows you to view a v4 API's deployment history and the JSON definition of each API version.

<figure><img src="../../.gitbook/assets/deployment_version history details (1).png" alt=""><figcaption><p>JSON definition of an API version</p></figcaption></figure>

For more information, see [Version History](../../guides/api-configuration/v4-api-configuration/version-history.md).

### Webhook

If no pre-existing and supported endpoint or endpoint group is available to use for the DLQ, you can create one by clicking **Create new endpoint**:

<figure><img src="../../.gitbook/assets/DLQ_create endpoint (1).png" alt=""><figcaption><p>Create an endpoint to use for DLQ</p></figcaption></figure>

For more information, see the [Webhook entrypoint configuration ](../../guides/api-configuration/v4-api-configuration/entrypoints/v4-message-api-entrypoints/webhook.md)section.

## Entrypoint configuration

### CORS

CORS support has been extended to v4 message and proxy APIs. For CORS to be applied, an API must contain at least one HTTP GET, HTTP POST, HTTP Proxy, or SSE entrypoint. WebSocket entrypoints do not support CORS.

To learn more, see the [v4 CORS configuration](../../guides/api-configuration/v4-api-configuration/entrypoints/cors.md) documentation.

### Response templates

[Response templates](../../guides/api-configuration/v4-api-configuration/entrypoints/response-templates.md) can be implemented for all v4 API HTTP entrypoints:

* HTTP GET
* HTTP POST
* HTTP proxy
* SSE
* Webhook
* WebSocket

Responses can be templatized if the errors raised during the request/response phase(s) are associated with a policy whose policy keys can be overridden. Multiple templates can be created for one API, for multiple policies and/or multiple error keys sent by the same policy. Multiple template definitions can be created for the same error key in a single template, for different content types or status codes.

<figure><img src="../../.gitbook/assets/create response template (1).png" alt=""><figcaption><p>Create a response template</p></figcaption></figure>

## Gravitee Expression Language

Gravitee Expression Language can get the raw text of a path mapping to compare the path parameters to what was actually evaluated. Calling `request.pathParamsRaw()` will evaluate to the correct, expected value when used in a policy.

To learn more about Gravitee EL, see [this page](../../guides/gravitee-expression-language.md).

## Notifications

Portal, API, and application notifications can be configured for v4 APIs via Portal, Email, and/or Webhook notifiers. For each notification type, default notifications can be edited and new notifications can be added.

<figure><img src="../../.gitbook/assets/notifications api_base (1).png" alt=""><figcaption><p>Notifications configuration</p></figcaption></figure>

For more information, refer to the [Notifications](../../getting-started/configuration/notifications.md) documentation.

## Policies

### AVRO <> Protobuf

You can use the [`avro-protobuf` policy](../../reference/policy-reference/avro-to-protobuf.md) to apply a transformation (or mapping) on the request, and/or response, and/or message content of an API call.

AVRO to Protobuf conversion:

* Producing a message directly in the AVRO topic (in JSON format) is captured by the AVRO topic and serialized to AVRO
* Checking the Protobuf topic, the user can see data was captured and is in binary format, indicating that the serialization to Protobuf was successful
* This transformation can also be applied in the body

Protobuf to AVRO conversion:

* If the caller of an API sends a message in JSON format to a backend with a specified schema, the message will reach the backend in Avro format with the data in binary
* Checking both topics (Protobuf and Avro), the user sees data in binary in both topics, which confirms serialization was successful
* This transformation can also be applied in the body

### GraphQL Rate Limit

The [`graphql-rate-limit` policy](../../reference/policy-reference/graphql-rate-limit.md) has been added to limit the load placed on the GraphQL server so that GraphQL resources can be served reliably without overloading the system. It is a Gravitee Enterprise Edition feature and requires a [license](https://documentation.gravitee.io/platform-overview/gravitee-platform/gravitee-offerings-ce-vs-ee/enterprise-edition-licensing)​.

The Gravitee Gateway evaluates query costs by introspecting schema and analyzing the query, then applying a rate-limiting strategy based on a computed/weighted score. This protects the backend GraphQL server from having to process costly GraphQL requests.

### Protobuf <> JSON

You can use the [`protobuf-json` policy](../../reference/policy-reference/protobuf-to-json.md) to apply a transformation (or mapping) on the request, and/or response, and/or message content of an API call.

Protobuf to JSON conversion:

* If the caller of an API sends a message in JSON format to a backend with a specified schema, the message will reach the backend in Avro format with the data in binary. The caller of the API can then consume the message back in JSON format, and the Avro schema will be specified directly in the policy.
* This transformation can also be applied in the body
* If the user makes a POST request with an incorrect body, the response returns an error

JSON to Protobuf conversion:

* If the caller of an API sends a message in JSON format to a backend with a specified schema, the message will reach the backend in Protobuf format with the data in binary. The caller of the API can then consume the message back in JSON format, and the Protobuf schema will be specified directly in the policy.
* This transformation can also be applied in the body

### Rate Limit

For any [`rate-limit` policy](../../reference/policy-reference/rate-limit.md) and irrespective of plan, the user can select the option to ignore the IP address and subscription of the caller and only use a custom key for the quota. Users can then share an API's rate limit calculations across machines to enforce the limit regardless of caller IP or subscriber ID. Using a custom key, the quota will increment after each call to the API across multiple hosts.

To dynamically set the custom key, it can be defined using Gravitee Expression Language.

### SSL Enforcement

Instead of accessing a client certificate via API call during an active TLS session, a reverse proxy (e.g., NGINX, Apache) can pass the client certificate using a specified header. This option requires the user to specify which header contains the certificate, which is base64-encoded. The `ssl-enforcement` policy uses the base64-encoded text of the certificate to validate whether the certificate is valid.

Refer to the [`ssl-enforcement` policy](../../reference/policy-reference/ssl-enforcement.md) for additional details.

## Sharding tags

Gravitee 4.3 allows sharding tags to be set for v4 APIs via the Management Console. Sharding tags are added to an organization and mapped to entrypoints from the **Organization** menu option. Sharding tags are defined in an API on the **Deployment** page.

<figure><img src="../../.gitbook/assets/deployment_sharding tag (1).png" alt=""><figcaption><p>v4 sharding tag configuration</p></figcaption></figure>

To learn more about how to configure and use sharding tags, see the [documentation](../../getting-started/configuration/apim-gateway/sharding-tags.md).

## TCP proxy support

Gravitee 4.3 supports a UI for TCP proxy API creation and configuration via the APIM Console.

<figure><img src="../../.gitbook/assets/create proxy api_step 2 http or tcp 1 (1).png" alt=""><figcaption><p>v4 API creation wizard: HTTP or TCP as a backend entrypoint</p></figcaption></figure>

To learn how to create a TCP proxy API, see the [v4 API creation wizard](../../guides/create-apis/the-api-creation-wizard/v4-api-creation-wizard.md). To learn how to configure a TCP proxy API, see the documentation on [v4 proxy API entrypoints](../../guides/api-configuration/v4-api-configuration/entrypoints/v4-proxy-api-entrypoints.md) and [v4 proxy API endpoints](../../guides/api-configuration/v4-api-configuration/endpoints/v4-proxy-api-endpoints.md).

## TCP reporter

The TCP reporter can be configured to use TLS when connecting to the target so that the entire communication is TLS-encrypted end-to-end. The user can configure the reporter to use TLS either with or without client verification enabled.

For more details, see the [TCP reporter documentation](../../getting-started/configuration/reporters/#tcp-reporter).
