# APIM 4.7

In Gravitee 4.7, we have released the following improvements and enhancements:

* Deprecation notice - APIM Standalone components.
* Updates to the Kafka Gateway and the new Developer Portal.
* Enhancements to webhook subscriptions.
* Added support for adding documentation to your APIs in Asciidoc format.&#x20;
* The addition of secret manager support for the RabbitMQ endpoint, the Solace endpoint, and the LDAP resource.
* The addition of Secret Manager support for the LDAP resource.
* Tenant support is extended to v4 APIs.
* Improvements to the import logic for v2 and v4 APIs.
* Improvements to the IBM API Connect federation agent.
* New Mulesoft federation agent.
* Updates to the API Score tech preview.
* Added support for custom headers in the IP Filtering and GeoIP Filtering policies.
* Added support for v4 APIs to the AWS Lambda policy.
* Added support for expression patterns to the Kafka ACL policy.

## Deprecation notice - APIM Standalone components

The APIM standalone components that you can download from [Gravitee.io downloads - apim/components](https://download.gravitee.io/#graviteeio-apim/components/) will no longer be available from the 4.8.0 version of APIM.

We continue to release the components for previously supported versions until the end of the support for the 4.7.x versions of APIM.

To prepare for the deprecation, you can use the full distribution .ZIP file instead. To download the full distribution .ZIP file, go to [Gravitee.io downloads - apim/distributions](https://download.gravitee.io/#graviteeio-apim/distributions/).

## Updates to the Kafka Gateway

In APIM 4.7, the Kafka Gateway feature set includes:

* Support for complex expressions in the API policy.
* Better support for connecting to Confluent Cloud over OAuth2.
* Better support for using the ACL policy and the topic mapping policy in the same flow.&#x20;

## Updates to the new Developer Portal

As of APIM 4.7, the new version of the Gravitee Developer Portal has the following enhancements:

* Categories can optionally be displayed as tabs (the existing default) or as tiles.
* Application-level logs show entries for v4 APIs.
* Webhook subscription details are fully visible and can be updated after creation. (The ability to create a subscription to a Push plan will come in a future release.)

## Improvements to Webhook subscriptions

You can now view and update the details of a Push plan subscription to a webhook entrypoint in the Console, both in the API and application subscription lists. When you edit the subscription, the changes are automatically deployed to the Gateway and no restart is required.

<figure><img src="https://lh7-qw.googleusercontent.com/docsz/AD_4nXexoLATr3nNdeN_nodhAlqWH2KRAkLz2v8c_g7_JmYS0bZE4olsiyZAO14KhJW5Da6KPV4rZj72RuKDXEFxxzG5J5x2G8AbqHRY3TX2nsRt37bRnCSIZzx8j0WNVtIERFLGA0paVA?key=vUeNGTqhmI_vGeq3U0sGHTvz" alt=""><figcaption></figcaption></figure>

<figure><img src="https://lh7-qw.googleusercontent.com/docsz/AD_4nXeCyY0vnVMQc6HJeT9-N-8WemthFeTRnxUdUT3FJ3jsM7fc3eoajclDe_xoruv0DtGKGqIZnoQwFsTcgE0lyTTuOLgrRV99PgxdVFFG5vQFqpNfN4Q-Y7y8NJr9VP-xYVTFUkhHPg?key=vUeNGTqhmI_vGeq3U0sGHTvz" alt=""><figcaption></figcaption></figure>

## Secret Support

In Gravitee APIM 4.4, we introduced secret managers to obscure sensitive information in the Gravitee Gateway configuration file. In Gravitee APIM 4.6, we extended this capability to API-Level configuration. In Gravitee 4.7, we have extended this capability again to the following endpoints and resources:

* RabbitMQ endpoint&#x20;
* Solace endpoint&#x20;
* The LDAP resource

## Asciidoc documentation

With Gravitee 4.7, you can add documentation in Asciidoc format, in addition to the previously-supported OpenAPI, AsyncAPI, and Markdown formats.

\


<figure><img src="https://lh7-qw.googleusercontent.com/docsz/AD_4nXfEhczS30H76u2oPk0WeSpz04vw2uJ8qBV267euCY4uSzZ2oHXfiBgbJggjCJJmgn1HKruN5Dc9V6YLZoYrals0k27zlchqtjjuUmVPKNKEKCOCHKEskD5vyCW4yH3pw5Gvoyq0Lg?key=vUeNGTqhmI_vGeq3U0sGHTvz" alt=""><figcaption></figcaption></figure>

## Tenant support&#x20;

[Tenants](https://documentation.gravitee.io/apim/gravitee-gateway/tenants#id-9c4f) are a way to leverage Gravitee's multi-endpoint capability, i.e., the ability to specify multiple upstream systems per single API. Gravitee allows you to assign endpoints and Gateways to specific tenants to control the endpoints to which requests are proxied.

Previously, support for tenants was restricted to v2 APIs. With Gravitee 4.7, tenants capabilities have been extended to v4 APIs.

## IBM API Connect Federation agent

With Gravitee 4.7, we have improved the capabilities of the IBM API Connect agent. With the agent you can now complete the following actions:

* When you configure the agent, you can use the `IBM_INSTANCE_TYPE=[cloud|cloud-reserved-instance|self-hosted]` to define your instance type. With the instance type `cloud-reserved-instance`, you pass only the API Key.&#x20;
* When you configure the agent, you can filter the catalogs that you ingest from.
* You can configure the agent to ingest APIs from Azure. Auto-approve is set to false on the API products using the `SUBSCRIPTION_APPROVAL_TYPE: [MANUAL|AUTOMATIC|ALL]` parameter. The default is `ALL`.&#x20;

## New Mulesoft Federation agent

With Gravitee 4.7, you can now ingest APIs from Mulesoft API Management to centrally catalog Mulesoft APIs alongside all your other Gravitee and Federated APIs. The Mulesoft federation agent discovers Mulesoft APIs that are published to Mulesoft Exchange.  Subscription support is coming soon.&#x20;

## Updates to the API Score tech preview

With the Gravitee 4.7 release, we’ve continued to improve the API Score technical preview. API Score now supports all Gravitee API types. When you evaluate an API’s score, any relevant piece of information about your API’s design and settings are sent to the scoring service. This includes the Gravitee API definition itself, which contains information like the API's plans, policies, entrypoints, endpoints, labels, categories, etc. Any OpenAPI or AsyncAPI doc pages attached to your APIs are also used for scoring. You can write custom rulesets against any of these assets, including support for custom JavaScript functions.&#x20;

<figure><img src="https://lh7-qw.googleusercontent.com/docsz/AD_4nXehDMsEV_VvIiBSrQp5YFBJnc4ti4BRU1tk3WTlQ-OFFckp9oKe3p3Vld8nhdtRQfWaaO27ij90nNqizB0BO8VFk-uRkdez6oUV2GuXkx2zVUzbTqbxgbQrgE_zmyJ9UWDe5gnRJQ?key=nM4vYrO1fYVCMxtagJYjXnLY" alt=""><figcaption></figcaption></figure>

API Score now also includes an in-app toggle to opt-in to using API Score. You can find it in your APIM Settings > API Quality menu.&#x20;

## Custom IP header support

For both the IP Filtering and GeoIP Filtering policies, you can toggle the Use custom IP address (support EL) option to filter forwarded IPs using a custom header.

![](https://lh7-qw.googleusercontent.com/docsz/AD_4nXcrV2CkBf9V7-bxAEmSUmCtMP6mbXd3Du3641i13SFwUiXVttiTsJaer5SEQrBEwR3uqUiP6ndieIHmTNN_FSiFknucMAk-on4FJHYzFnQyJ-b9JS52aC9ePhJIoCArOJF-cH97?key=vUeNGTqhmI_vGeq3U0sGHTvz)

You can use any header sent with the request if you are using a different header than X-Forwarded-For to represent the source IP.

## AWS Lambda policy supports v4 APIs

The AWS Lambda policy can now be applied to v2 APIs, v4 HTTP proxy APIs, and v4 message APIs. It cannot be applied to v4 TCP proxy APIs.

## Kafka ACL policy supports expression patterns

You can now specify an expression pattern on the Group, Topic, or Transactional ID resources to create a dynamic ACL that can match complicated conditions. To set the ACL to match an expression pattern, you can use wildcards.
