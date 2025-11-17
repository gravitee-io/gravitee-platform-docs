# APIM 4.4

{% hint style="danger" %}
**Make sure you upgrade your license file**

If you are an existing Gravitee Enterprise customer upgrading to 4.x, please make sure that you upgrade your Gravitee license file. Reach out to your Customer Success Manager or Support team in order to receive a new 4.x license.
{% endhint %}

## Gravitee API Management 4.4

In Gravitee API Management version 4.4, we’ve released the following new products and functionality:

* Federated API Management, with support for publishing and governing APIs from different API Gateways and Event brokers&#x20;
* More functionality for v4 APIs
* A new Azure Service Bus endpoint for protocol mediation APIs
* A new Developer Portal (Tech preview)
* And more!

Keep reading to learn more about each new set of functionality.

## Federated API Management (EE only)

Gravitee Federated API Management is comprised of the ability to discover, import, manage, and govern APIs from other API Gateways and Event brokers into a universal Gravitee API management and governance console and then publish those APIs as Gravitee APIs, with Gravitee subscription Plans, in a universal Gravitee Developer Portal. As of 4.4 we offer support:

* AWS API Gateway
* Solace Event Broker and Event Management\


As of 4.4, we have released the following functionality related to Federated API Management:

* The new Integrations component
* Federated API type
* Federation Agent
* Auto discovery and ingest for:
  * AWS API Gateway APIs
  * Solace Event APIs
* Subscription management for:
  * AWS API Gateway APIs
  * Solace Event APIs
* Universal Developer Portal support for:
  * AWS API Gateway APIs
  * Solace Event APIs\


If, at any point, you are interested in trying Gravitee Federated API Management, we recommend:

* Customers reach out to their CSM or CSA directly
* Non-customers [book a demo](https://www.gravitee.io/demo) and explore Federated API Management through a free POC with our Solutions Engineering team

Keep reading to learn more.&#x20;

### Automated API and subscription discovery via Gravitee Integrations

Integrations are a new component in the Gravitee API Management Console. The Integrations component will be where you manage many core Federated API Management capabilities. For example, the Integration component enables you to:

* Define which third party provider(s) you want to integrate Gravitee Federated API Management with (i.e., AWS, Solace)
* Manage the agent that establishes the connection between Gravitee and the third party provider
* Auto-discover and ingest API assets from those providers
* Auto discover and create subscription plans from those providers
* And more

<figure><img src="../../.gitbook/assets/Screenshot 2024-06-24 at 4.29.44 PM.png" alt=""><figcaption><p>Gravitee integrations</p></figcaption></figure>

\
Auto-discovery is quick and easy. Simply [install the Gravitee Agent](../../using-the-product/managing-your-apis-with-gravitee-api-management/federation/federation-agent.md) in your target environment, click Discover, and you’ll be met with a list of API assets that the Gravitee agent automatically discovers. Try out the new discovery functionality using the interactive tutorial below:

{% @arcade/embed flowId="GhNjFwtUcQ3THZnKCsVt" url="https://app.arcade.software/share/GhNjFwtUcQ3THZnKCsVt" %}

Once the APIs are discovered, you can choose to ingest, or import, those assets into Gravitee as Gravitee Federated APIs. If you had a usage plan already configured on the third party provider, Gravitee can discover certain kinds of usage plans and import those as well. For example, as of 4.4, Gravitee can discover existing AWS API Gateway API Key usage plans and import those as matching Gravitee API Key Plans.

In addition to usage plan discovery, Gravitee will also discover and import API documentation from supported third party providers.

{% hint style="info" %}
**Federated APIs are a new type of Gravitee API**&#x20;

These APIs will exist in Gravitee as API artifacts that can be managed and governed, but they will not be deployed to the Gravitee Gateway.&#x20;
{% endhint %}

To start using Federated API Management, refer to the [Federated API Management documentation](../../using-the-product/managing-your-apis-with-gravitee-api-management/federation/README.md).

### Publishing your Federated APIs to a universal Developer Portal

Once you have Federated APIs with Gravitee Plans discovered and ingested, you can–like with native Gravitee APIs–publish those APIs to your Gravitee Developer Portal. This means that you’ll have one Developer Portal where you can host APIs from:

* The Gravitee API Gateway
* AWS API Gateway
* Solace Event Management Platform
* Other third party solutions that we will add in the future

For API consumers, discovering and subscribing to these APIs works the same way as it always has for Gravitee APIs. To see it in action, check out the interactive tutorial below:

{% @arcade/embed flowId="59UqOt0D7NIGSVkavVby" url="https://app.arcade.software/share/59UqOt0D7NIGSVkavVby" %}

For API Publishers, managing Federated API subscription requests works the exact same way as it does for Gravitee APIs. You’ll manage subscriptions and your API plans via the Consumers tab on your Federated API. Subscriptions can be configured to require manual validation by the API Publisher before they are forwarded to the 3rd-party provider, or they can be set to automatic. \


For more information on how to create and publish Federated APIs with plans to the Developer Portal, please refer to the [Federated API Management documentation](../../using-the-product/managing-your-apis-with-gravitee-api-management/federation/federated-apis.md).&#x20;

{% hint style="info" %}
**Limitation**

As of Gravitee APIM 4.4, Gravitee Integrations does not support auto-updating API assets once they have been discovered. If you make a change to your API on the third party API Gateway or Event Broker, you will need to delete the discovered API and re-discover and import that API asset.
{% endhint %}

\
That's a wrap on our Federated APIM release notes. For more information on getting started with Federated API Management, we recommend either speaking with the Gravitee team, or browsing the Federated APIM docs.

<table data-view="cards"><thead><tr><th></th><th></th><th></th><th data-hidden data-card-target data-type="content-ref"></th></tr></thead><tbody><tr><td>Speak with the Gravitee team</td><td></td><td></td><td><a href="https://www.gravitee.io/demo">https://www.gravitee.io/demo</a></td></tr><tr><td>Read the Federated API Management docs</td><td></td><td></td><td><a href="../../using-the-product/managing-your-apis-with-gravitee-api-management/federation/">federation</a></td></tr></tbody></table>

## More functionality for v4 APIs

Gravitee offers two API definitions for API creation:

* **v4 API definition**: our most modern API definition that allows you expose and secure HTTP APIs, Event brokers as APIs, and TCP services as APIs via the Gateway. Federated APIs will also leverage the v4 API definition.
* **v2 API definition**: our legacy API definition that only supports exposing and securing HTTP APIs

{% hint style="info" %}
**Which version should you use?**

For new Gravitee users, we highly recommend using the Gravitee v4 API definition, as this API definition offers our most advanced features and will continue to do so going forward.&#x20;
{% endhint %}

Since we released the v4 API definition, we have been working to ensure that our customers wouldn’t lack any of the critical functionality that they have come to expect while working with Gravitee v2 APIs.&#x20;

\
The 4.4 release brings us multiple steps closer to complete feature parity, introducing v4 API support for:

* Import for v4 APIs
* Analytics for v4 APIs

As of Gravitee 4.4, you can now import API definition bundles as v4 APIs and create pages, members, groups, and other relevant resources at the time of import. This is done during the API creation phase.

![](<../../.gitbook/assets/Screenshot 2024-06-24 at 5.07.21 PM.png>)\


For v4 Proxy APIs, we also support importing OpenAPI specifications.&#x20;

{% hint style="info" %}
**Limitation**

As of APIM 4.4, you will not be presented with the same import options for OAS import. For more information, please refer to the Import APIs documentation.
{% endhint %}

### Analytics for v4 APIs

As of APIM 4.4, Gravitee offers the following analytics support for v4 APIs within the API Management console:

* Metrics on the number of API requests
* Metrics on message throughout for v4 message APIs
* HTTP response status
* Advanced entrypoint statistics

### Up-to-date feature parity chart for v4 and v2 APIs

Below is a table that outlines just how close we are to v2 and v4 feature parity:

<table data-header-hidden><thead><tr><th width="187">Functionality</th><th width="187">Supported in v2 proxy APIs</th><th>Supported in v4 proxy APIs</th><th>Supported in v4 message APIs</th></tr></thead><tbody><tr><td><strong>Functionality</strong></td><td><strong>Supported for v2 proxy APIs</strong></td><td><strong>Supported for v4 Proxy API</strong></td><td><p><strong>Supported for v4</strong> </p><p><strong>Message API</strong></p></td></tr><tr><td>User Permissions</td><td>✅</td><td>✅</td><td>✅</td></tr><tr><td>Properties</td><td>✅</td><td>✅</td><td>✅</td></tr><tr><td>Resources</td><td>✅</td><td>✅</td><td>✅</td></tr><tr><td>Notifications</td><td>✅</td><td>✅</td><td>✅</td></tr><tr><td>Categories</td><td>✅</td><td>✅</td><td>✅</td></tr><tr><td>Audit Logs</td><td>✅</td><td>✅</td><td>✅</td></tr><tr><td>Response Templates</td><td>✅</td><td>✅</td><td>✅</td></tr><tr><td>CORS</td><td>✅</td><td>✅</td><td>✅</td></tr><tr><td>Virtual Hosts</td><td>✅</td><td>✅</td><td>✅</td></tr><tr><td>Failover</td><td>✅</td><td>✅</td><td>⚠️ Depends on use case</td></tr><tr><td>Health Check</td><td>✅</td><td>✅</td><td>🚫</td></tr><tr><td>Health Check Dashboard</td><td>✅</td><td>🚫</td><td>🚫</td></tr><tr><td>Improved Policy Studio</td><td>🚫</td><td>✅</td><td>✅</td></tr><tr><td>Debug Mode</td><td>✅</td><td>🚫</td><td>🚫</td></tr><tr><td>Plans</td><td>✅</td><td>✅</td><td>✅</td></tr><tr><td>Subscriptions</td><td>✅</td><td>✅</td><td>✅</td></tr><tr><td>Messages / Broadcasts</td><td>✅</td><td>✅</td><td>✅</td></tr><tr><td>Documentation - Markdown</td><td>✅</td><td>✅</td><td>✅</td></tr><tr><td>Documentation - OAS</td><td>✅</td><td>✅</td><td>✅</td></tr><tr><td>Documentation - AsyncAPI</td><td>✅</td><td>✅</td><td>✅</td></tr><tr><td>Documentation - AsciiDoc</td><td>✅</td><td>🚫</td><td>🚫</td></tr><tr><td>Documentation - Home Page</td><td>✅</td><td>⚠️ Set via API</td><td>✅</td></tr><tr><td>Documentation - Metadata</td><td>✅</td><td>✅</td><td>✅</td></tr><tr><td>Documentation - Translations</td><td>✅</td><td>🚫</td><td>🚫</td></tr><tr><td>Documentation - Group Access Control</td><td>✅</td><td>🚫</td><td>🚫</td></tr><tr><td>Documentation - Role Access Control</td><td>✅</td><td>🚫</td><td>🚫</td></tr><tr><td>Documentation - Swagger vs. Redoc Control</td><td>✅</td><td>🚫</td><td>🚫</td></tr><tr><td>Documentation - Try It Configuration</td><td>✅</td><td>🚫</td><td>🚫</td></tr><tr><td>Documentation - Nested Folder Creation</td><td>✅</td><td>✅</td><td>✅</td></tr><tr><td>Terms &#x26; Conditions on a Plan</td><td>✅</td><td>✅</td><td>✅</td></tr><tr><td>Sharding Tags</td><td>✅</td><td>✅</td><td>✅</td></tr><tr><td>Deployment History</td><td>✅</td><td>✅</td><td>✅</td></tr><tr><td>Rollback</td><td>✅</td><td>✅</td><td>✅</td></tr><tr><td>Compare API to Previous Versions</td><td>✅</td><td>✅</td><td>✅</td></tr><tr><td>Analytics</td><td>✅</td><td>⚠️ WIP</td><td>⚠️ WIP</td></tr><tr><td>Custom Dashboards</td><td>✅</td><td>🚫</td><td>🚫</td></tr><tr><td>Path Mappings</td><td>✅</td><td>🚫</td><td>🚫</td></tr><tr><td>Logs</td><td>✅</td><td>✅</td><td>✅</td></tr><tr><td>API Quality</td><td>✅</td><td>🚫</td><td>🚫</td></tr><tr><td>API Review</td><td>✅</td><td>✅</td><td>✅</td></tr><tr><td>Export API as Gravitee def (+options)</td><td>✅</td><td>✅</td><td>✅</td></tr><tr><td>Export API as GKO spec</td><td>✅</td><td>✅</td><td>✅</td></tr><tr><td>Import API from Gravitee def (+options)</td><td>✅</td><td>✅</td><td>✅</td></tr></tbody></table>



## The new Gravitee API Developer Portal (Tech preview) (EE only)

We’ve also released a new tech preview version of our advanced Gravitee Developer Portal. This new Developer Portal offers the following features and functionality:

* Updated UX and new UI components
* Catalog page has pagination and infinite scroll
* The ability to view and filter subscriptions for your APIs
* API search
* Portal customization

{% hint style="info" %}
**Limitations**

This Developer Portal is only a tech preview. For production use cases, we still recommend using the legacy Developer Portal. If you’d like to try out the new Developer Portal, we recommend that:

* Customers work directly with their CSM or CSA
* Non-customers book some time to chat with the [Gravitee Solutions Engineering team for a demo and/or free POC](https://www.gravitee.io/demo)
{% endhint %}

{% embed url="https://www.loom.com/share/4ad001465e5840648a6a44af011f672b?sid=aaea418b-a8bb-41df-bd87-4e22b8ffd29a" %}

## More Gravitee API Management updates

While Federated APIs, feature party work for v4 APIs, and a brand new Developer Portal are the major highlights of this release, that’s not all that we’ve been up to for the last quarter! We’ve also released the following new functionality:

* OpenTelemetry plugin
* Azure Service Bus endpoint
* The ability to customize the order of APIs within a category in the portal
* Add token option to body of MAPI token exchange endpoint
* Support for 500 responses in DLQ
* Hide delete account button when external auth is enabled

### The OpenTelemetry plugin

Using the new OpenTelemetry plugin, Gravitee APIs can now generate OpenTelemetry data and export it to the tool of their choice using the built-in OpenTelemetry exporter. This enables our customers to utilize their existing telemetry infrastructure using the industry standard. This functionality supersedes our existing Jaeger support.

### More protocol mediation support: Azure Service Bus endpoint

Gravitee’s protocol mediation enables teams to expose message and event-based backends as client-side APIs that use more consumer-friendly protocols. Before 4.4, Gravitee teams could expose Kafka, MQTT brokers, Solace, and RabbitMQ as:

* HTTP POST / GET
* WebSocket
* Webhooks
* SSE



Gravitee 4.4 introduces a new backend endpoint, Azure Service Bus. Now, you can expose events and messages from Azure Service Bus via the already-existing API entrypoints.&#x20;

<figure><img src="../../.gitbook/assets/Screenshot 2024-06-24 at 5.14.21 PM.png" alt=""><figcaption></figcaption></figure>

We’ve also introduced a UI/UX improvement to the Developer Portal. As the API Publisher, you can now define the order in which your APIs are presented to your API consumers. This is all done on a per-category basis.

### Add token option to body of MAPI token exchange endpoint

If you’re using JWT authorization, you can now configure the token for the MAPI token exchange endpoint in the request body in addition to the head body.&#x20;

### Support for 500 responses in DLQ

In Gravitee, the Dead letter queue (DLQ) functionality enables you to define a queue for unsent messages when working with v4 message APIs. Historically, you’ve only been able to handle up to 400 responses in a single queue. This has been increased to 500, giving you more flexibility for your DLQ and replay strategy.

## Wrapping up

Between Federated API Management, new message broker support, and a brand new Developer Portal, Gravitee API Management 4.4 is one of the largest, most exciting releases that we’ve pushed in a while. To learn more about the new functionality, please refer to the linked documentation throughout these release notes, and, if interested in any of the tech preview functionality, please work directly with your CSM (if you’re a Gravitee customer) or [book a demo with an Engineer](https://www.gravitee.io/demo) if you are not yet a Gravitee Enterprise user.&#x20;

\
\
