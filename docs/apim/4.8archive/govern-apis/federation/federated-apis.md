# Federated APIs

## Overview

Federated APIs join proxy and message APIs as one of the three main types of v4 Gravitee APIs. Federated APIs are created based on assets discovered by integrations with 3rd-party API gateway or event broker providers.&#x20;

{% hint style="info" %}
**Federated API feature limitations**

The data plane of a federated API is managed by the underlying 3rd-party provider. This means that Federated APIs don't include some of the features available on other API types, such as:

* Backend services, policies, proxy settings are unavailable
* Cannot be started, stopped, or deployed to the Gravitee API Gateway
{% endhint %}

## Create federated APIs

Gravitee Federated APIs cannot be created manually, they can only be discovered and ingested by the [Discovery](discovery.md) process.

After running Discovery, you'll end up with a number of new federated APIs in Gravitee.

If you open one, you'll be able to view that API's details, add additional documentation and metadata, and publish that API to your Gravitee Developer portal, just like you can for a native Gravitee Gateway API.

{% hint style="info" %}
When Gravitee APIs are created from integrations, 3rd-party provider API attributes are mapped into Gravitee API attributes. Which attributes are available and how they are imported depends on the provider. See the [provider documentation](3rd-party-providers/) for more information.
{% endhint %}

## Configure federated APIs

Compared to traditional Gravitee v2 and v4 APIs, the configuration options available to federated APIs are limited. However, the APIM Console offers a subset of identical configuration pages and capabilities regardless of API type.

To access federated API configuration options:

1. Log in to your APIM Console
2. Select **APIs** from the left nav
3. Click on the federated API you're interested in
4. Select a configuration category from the inner left nav: **Configuration**, **Consumers**, or **Documentation**

Follow the links below to visit the documentation for each configuration page.

| Configuration category | Configuration page                                                                                                                                                                                                                                                                                     | Comments                                         |
| ---------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ | ------------------------------------------------ |
| Configuration          | <p><a href="../../create-and-configure-apis/configure-v4-apis/general-settings.md">General</a><br><a href="../../create-and-configure-apis/configure-v4-apis/user-permissions.md">User Permissions</a><br><a href="../../create-and-configure-apis/configure-v4-apis/audit-logs.md">Audit Logs</a></p> |                                                  |
| Consumers              | <p><a href="../../secure-and-expose-apis/plans/">Plans</a><br><a href="../../secure-and-expose-apis/subscriptions/">Subscriptions</a><br><a href="../../create-and-configure-apis/configure-v4-apis/documentation.md#send-messages">Broadcasts</a></p>                                                 | Plans cannot be manually added to federated APIs |
| Documentation          | <p><a href="../../create-and-configure-apis/configure-v4-apis/documentation.md">Pages</a><br><a href="../../create-and-configure-apis/configure-v4-apis/documentation.md#add-metadata">Metadata</a></p>                                                                                                |                                                  |

## Federated API plans, applications, and subscriptions

Plans for federated APIs are based on API products, usage plans, and similar concepts already defined and automatically imported from 3rd-party providers. A plan only exists to the extent that a matching concept exists in the 3rd-party provider.

When Gravitee API plans are ingested from a 3rd-party provider, they enable subscriptions to the 3rd-party APIs be managed directly from within Gravitee. Under the hood, the federation agent will integrate with the third partie's management API to create the required objects that will enable the requested subscription. This may result in an API key being returned to the user in Gravitee APIM or in the Gravitee Developer portal. In other cases, it will simply create the right permissions on the third party, while access control is done using a 3rd-party OAuth server for instance.

To manage your federated API's plans and their subscriptions, go to the **Consumers** tab for your federated API.

<figure><img src="../../.gitbook/assets/Screenshot 2024-06-18 at 4.12.15 PM.png" alt=""><figcaption></figcaption></figure>

Under the **Plans** tab, you'll see all of the plans for your API that are either in staging, published, deprecated or closed. You will only be able to alter your federated API plans as it pertains to:

* Deprecation, publishing, closing your plans (deprecating or closing the plan will not alter the state of the usage plan in the third party provider, but will only stop the correlate Gravitee plan)
* Defining general plan information, such as name, description, characteristics, and general conditions
* **Subscription options**: either allowing auto-validation of all subscription requests, or, enforcing API consumers to submit a request for manual approval by the API Publisher
* Defining certain groups that can or cannot subscribe to your API via Gravitee groups

<figure><img src="../../.gitbook/assets/Screenshot 2024-06-18 at 4.10.09 PM.png" alt=""><figcaption></figcaption></figure>

{% hint style="info" %}
By default, the plan state is set to published and the subscription validation policy is set to manual (subscription auto-validation is not enabled).
{% endhint %}

Before publishing your federated API to the Developer Portal, make sure that your plan is published. Otherwise, there will be no way for API consumers to subscribe to your federated API.

## Federated API documentation

Federation enables a centralized location where API consumers can discover unified API documentation for diverse API gateways and event brokers. While an integration is syncing, available assets (e.g., OAS/AsyncAPI definitions or Markdown files) are automatically imported from the 3rd-party provider to form the basis of the API's documentation published to the Developer Portal. New documentation pages and assets can also be created directly within Gravitee.

To view or add documentation to an existing federated API:

1. Log in to your APIM Console
2. Select **APIs** from the left nav
3. Click on the federated API you're interested in
4. Select **Documentation** from the inner left nav

<figure><img src="../../.gitbook/assets/jonathan demo documentation.png" alt=""><figcaption></figcaption></figure>

{% hint style="info" %}
By default, the page is published with private visibility.
{% endhint %}

Refer to the Developer Portal documentation for information on how to create and manage API documentation.

## Publish federated APIs to the Developer Portal

APIs federated from multiple vendors can be published in a single Gravitee Developer Portal. This acts as a centralized location from which API consumers can access documentation and subscriptions. By default, federated APIs imported from an integration are not published to the portal.

To publish an existing federated API:

1. Log in to your APIM Console
2. Select **APIs** from the left nav
3. Click on the API you want to publish
4. Select **Configuration** from the inner left nav
5. In the **Danger Zone**, click **Publish the API**

<figure><img src="../../.gitbook/assets/jonathan demo publish api.png" alt=""><figcaption></figcaption></figure>

### View your API in the Developer Portal

To view the API that you just published, select **Developer Portal.** This will open your Gravitee Developer Portal in a new window. From here, you should be able to view your API, its documentation, and its subscription plan options.

## (For API consumers) Discover and subscribe to federated APIs in the Gravitee Developer Portal

From here, API consumers can access their Gravitee Developer Portal and search for the federated APIs that API Publishers have published. Simply access the url of the Developer Portal and either search for the specific API or browse the larger catalog of APIs have been published from the Gravitee API Gateway. From here, consumers can:

* View API documentation
* Interface directly with the API Publisher
* Self-service subscribe
* View tickets
* And more

### Subscribe to APIs

1.  When you've found the API that you want to subscribe to, click the **SUBSCRIBE** button

    <figure><img src="../../.gitbook/assets/jonathan demo subscribe.png" alt=""><figcaption></figcaption></figure>
2.  Select the plan you want to subscribe to, then click **Next**

    <figure><img src="../../.gitbook/assets/jonathan demo plan.png" alt=""><figcaption></figcaption></figure>
3.  Use the **Choose an application** drop-down menu to select an application to use for the subscription, then click **Next.** If you do not yet have an application, please refer to the [Applications](../../developer-portal/classic-developer-portal/create-an-application.md) documentation to create a Gravitee Application.

    <figure><img src="../../.gitbook/assets/jonathan demo choose app.png" alt=""><figcaption></figcaption></figure>

Depending on the subscription configuration, the application will either auto-validate or require approval.

{% hint style="info" %}
* For more information on how to create and manage applications in APIM, see [Applications](../../developer-portal/classic-developer-portal/create-an-application.md).
* For more information on how to create and manage subscriptions in APIM, see [Subscriptions](../../secure-and-expose-apis/subscriptions/).
{% endhint %}

## Delete federated APIs

Deleting a federated API will close or delete all objects inside of it such as plans, documentation pages, and subscriptions.

{% hint style="info" %}
**Deletion only applies to Gravitee APIs**

When you delete a federated API in Gravitee, you are not deleting the original API asset on the side of the third party provider. You will only delete the federated API within Gravitee.
{% endhint %}

To delete a federated API:

1. Access the Federated API that you want to delete either from the **APIs** menu or the **Integrations** tab.
2. Select **Configuration** from the inner left nav
3. Select the **General** header tab
4.  In the **Danger Zone** section, click **Delete**

    <figure><img src="../../.gitbook/assets/delete single API.png" alt=""><figcaption></figcaption></figure>

To delete all of an integration's federated APIs as a group:

1. Log in to your APIM Console
2. Select **Integrations** from the left nav
3. Click on the integration you're interested in
4. Select **Configuration** from the inner left nav
5.  In the **Danger Zone** section, click **Delete APIs**

    <figure><img src="../../.gitbook/assets/integration delete.png" alt=""><figcaption></figcaption></figure>

{% hint style="info" %}
Federated APIs cannot be deleted if they are published. The **Delete APIs** action will delete unpublished APIs but ignore published APIs.
{% endhint %}
