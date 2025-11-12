---
description: Securely expose your APIs to consumers in a dedicated API catalog
---

# Developer Portal 101

{% hint style="warning" %}
This is the final section of the Quickstart Guide. By this point, you should already have [created a Gateway API](gateway-apis-101-traditional-and-message-proxies/) and added [plans and policies](plans-and-policies-101.md).
{% endhint %}

## Overview

So far, we've shown you how to create Gateway APIs and then how to augment and enhance those APIs with additional layers of security and functionality via plans and policies. These powerful tools allow you to effectively manage your backend API servers and message brokers in a unified interface.

However, these capabilities are wasted if there is no way to expose and catalog your APIs for consumers. Enter the Developer Portal.

The Developer Portal is a web application that provides a simplified, user-friendly interface tailored to the API consumption process. It acts as a centralized catalog where internal and external API consumers can find and subscribe to APIs that are developed, managed, and deployed by API publishers.

API consumers can easily discover and explore APIs, read documentation, test API endpoints, generate access tokens, view API analytics, and manage their API subscriptions in a single location. Additionally, administrators have significant control over the look and feel of the Developer Portal to deliver an accessible and on-brand experience to external API consumers.

***

## Publish your API

Before heading over to the Developer Portal, we need to make sure our Gateway API will be visible to consumers.&#x20;

### Access API

First, we need to open the API in the APIM Console. You may already have it open from the previous part of the Quickstart Guide. If not, head back over to the **APIs** homescreen and select the API you created.

<figure><img src="../../.gitbook/assets/Screenshot 2023-11-19 at 8.25.21 PM.png" alt=""><figcaption><p>APIs homescreen</p></figcaption></figure>

> * [x] Select **APIs** in the sidebar
> * [x] Select the API you created in Gateway APIs 101

### Publish API

This will take you straight to your API's **General Info** page. In the **Danger Zone**, we can update the visibility of the API:

* **Publish/Unpublish the API:** This is a toggle that controls the visibility of the API in the Developer Portal. Unless the API is also public, it is only visible to members of the API, which is controlled through **User and group access** in the inner sidebar.
* **Make Public/Private:** This is a toggle that makes the API visible to anyone with access to the Developer Portal. Note, this toggle only has an impact if the API is published.

<figure><img src="../../.gitbook/assets/Screenshot 2023-11-19 at 11.20.32 PM.png" alt=""><figcaption><p>API Danger Zone</p></figcaption></figure>

> * [x] Click **Publish the API**, then **Publish** in the modal to add the API to the Developer Portal
> * [x] Click **Make Public**, then **Make Public** again in the modal, to make the API visible to all API consumers

## Developer Portal

We're now ready to explore our published API in the Developer Portal.

### Access the Developer Portal

Enterprise trial users should be able to immediately access the Developer Portal from the APIM Console by selecting the **Developer Portal** link in the top left of the Console's nav bar.

<details>

<summary>Self-managed installation: Adding a Developer Portal link</summary>

The Developer Portal host of self-managed installations can easily be modified. You can manually add the **Portal URL** to see the Developer Portal link in the Console UI.

Your Developer Portal URL will depend on your deployment, so please reference the respective installation docs. For example, with the default Docker installation, you can access the Developer Portal at `http://localhost:8085` in your browser.

<img src="../../.gitbook/assets/Screenshot 2023-11-21 at 1.15.16 PM.png" alt="Update Developer Portal settings in the Console" data-size="original">

* [x] Click **Settings** in the sidebar
* [x] Click **Settings** in the inner sidebar
* [x] Scroll down to **Portal** settings and provide a **Portal URL** based on your deployment configuration
* [x] Scroll to the bottom of the page and click **Save**

</details>

<figure><img src="../../.gitbook/assets/Screenshot 2023-11-21 at 1.11.23 PM.png" alt=""><figcaption><p>Access Developer Portal from APIM Console</p></figcaption></figure>

> * [x] Select the **Developer Portal** link in the top left of your Console's nav bar

This will bring you to the homescreen of the Developer Portal.

<figure><img src="../../.gitbook/assets/Screenshot 2023-11-21 at 1.19.27 PM.png" alt=""><figcaption><p>Your default Developer Portal</p></figcaption></figure>

From here, you can immediately begin searching for APIs using the Developer Portal's full-context[^1] search. However, you will not be able to subscribe to any APIs until you create an application.

### Create an application

Now that we have access to the Developer Portal, we can take on the role of an API consumer. The next step is to create an application that is used to register and agree to plans.

<figure><img src="../../.gitbook/assets/Screenshot 2023-11-21 at 6.06.07 PM.png" alt=""><figcaption><p>Developer Portal Applications page</p></figcaption></figure>

> * [x] Select **Applications** in the top nav bar
> * [x] Select **+ Create an App** in the subnav bar

#### General step

This will open the application creation wizard. The **General** step is focused on providing application metadata.&#x20;

<figure><img src="../../.gitbook/assets/Screenshot 2023-11-21 at 6.18.07 PM.png" alt=""><figcaption><p>General step of application creation wizard</p></figcaption></figure>

> * [x] Provide a name and description, then click **Next**

#### Security step

The next step is focused on **Security**. This page may look different depending on your **Client Registration** settings, which are configured in the APIM console. However, everyone should have the option to create a **Simple** application.&#x20;

{% hint style="info" %}
**Dynamic Client Registration**

A **Simple** application allows an API consumer to define their own `client_id`, but this is not secure and should not be used outside of testing. Therefore, Gravitee allows you to disable **Simple** applications and [use dynamic client registration (DCR) to create advanced applications](/apim/guides/api-exposure-plans-applications-and-subscriptions/plans-1#advanced-application-configuration) with the identity provider of your choosing.&#x20;
{% endhint %}

<figure><img src="../../.gitbook/assets/Screenshot 2023-11-21 at 6.29.05 PM.png" alt=""><figcaption><p>Security step of application creation wizard</p></figcaption></figure>

> * [x] Select a **Simple** application, then click **Next**

#### Subscription step

The **Subscription** step allows you to send API subscription requests as you are creating the application. You will be able to search for published APIs you have access to and view the available plans.

Once we finish creating the app, the request will be sent for review and approval by the API publisher.

<figure><img src="../../.gitbook/assets/Screenshot 2023-11-21 at 6.33.09 PM.png" alt=""><figcaption><p>Subscription step of application creation wizard</p></figcaption></figure>

> * [x] Search for the API you published and select it
> * [x] Select **Subscribe** under the API Key Plan, then click **Next**

#### Validation step

Finally, we just need to complete the **Validation** step. Review your application details and subscription request. If everything looks good, go ahead and create your app!

<figure><img src="../../.gitbook/assets/Screenshot 2023-11-21 at 6.36.14 PM.png" alt=""><figcaption><p>Validation step of application creation wizard</p></figcaption></figure>

> * [x] Click **Create the App**

You should receive confirmation that your app was successfully created. Feel free to open your app and explore the different tabs.

## Managing subscriptions

It's time to resume our previous role as an API publisher. Let's return to the APIM Console to manage the subscription request we just submitted. It should have come through as a new **Task**.

<figure><img src="../../.gitbook/assets/Screenshot 2023-11-21 at 7.34.03 PM.png" alt=""><figcaption><p>View your tasks in the Console</p></figcaption></figure>

> * [x] Select your profile in the top right
> * [x] Select **Task** from the drop-down menu

This will bring you to a list of all your current tasks, which should consist of a subscription request from the application to your API you just created.

<figure><img src="../../.gitbook/assets/Screenshot 2023-11-21 at 7.35.20 PM.png" alt=""><figcaption><p>A list of your tasks in the Console</p></figcaption></figure>

> * [x] Click Validate under the subscription request

This will not immediately validate the request, but instead navigate you to the part of the Console where you can validate the subscription.

{% hint style="info" %}
This was essentially a shortcut to our API's subscription screen. You can always navigate here by selecting your API, selecting **Plans** from the inner sidebar, and then selecting the **Subscriptions** tab.
{% endhint %}

Here, you can see all the metadata (e.g., user, application, plan, etc.) for the request and decide on an action. Once you validate, you will have additional options for managing the subscription.

<figure><img src="../../.gitbook/assets/Screenshot 2023-11-21 at 7.41.45 PM.png" alt=""><figcaption><p>Subscription validation screen</p></figcaption></figure>

> * [x] Click **Validate subscription**
> * [x] Leave the defaults and click **Validate** in the modal

The subscription is now active! However, as the API publisher, you have a number of different options for managing this subscription:

* **Transfer:** Move the subscription to a different plan
* **Pause:** Temporarily suspend the subscription. Be careful with this, because the consumer's API requests will fail when their subscription is paused.
* **Change end date:** Change or set the expiration date on the provisioned API keys.
* **Close:** Permanently end the subscription. The API consumer will need to subscribe again to have access to this API.

At the bottom of the screen, you will see the API key that has been randomly generated and provisioned for this user. APIM allows you to customize this behavior, including providing your own API key and allowing the API consumer to share API keys between subscriptions.

For now, simply copy that API key to your clipboard.

<figure><img src="../../.gitbook/assets/Screenshot 2023-11-21 at 7.47.19 PM.png" alt=""><figcaption><p>Subscription management </p></figcaption></figure>

> * [x] Select the **Copy to clipboard** icon next to the API key

## Test API

For the final time, let's send the same request but with one small modification. We need to pass our new API key to act as the authorization token for our request. To do this, we will use the `X-Gravitee-API-Key` header.

{% hint style="info" %}
`X-Gravitee-API-Key` is the default header to pass the API key, but it can be modified. Additionally, you can pass the API key with the query parameter `api-key`, if preferred.
{% endhint %}

{% code overflow="wrap" %}
```sh
curl -X GET -i "https://your-gateway-server/your-context-path" -H "X-Gravitee-API-Key: your-key-here"
```
{% endcode %}

{% hint style="success" %}
You should receive a **`200 OK`** success status response code, along with the custom payload you configured in the previous section using the Assign Content policy.

Congrats! You have successfully completed the Quickstart Guide! Head on over to our [What's Next](whats-next.md) section if you're looking for suggestions for learning about more advanced Gravitee topics.&#x20;
{% endhint %}

[^1]: Full-context meaning it searches through the definition and metadata of all published APIs that you have access to
