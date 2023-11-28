---
description: Securely expose your APIs to consumers in a dedicated API catalog
---

# Developer Portal 101

{% hint style="warning" %}
This is the final section of the Quickstart Guide. By this point, you should already have [created a Gateway API](gateway-apis-101-traditional-and-message-proxies/) and added [plans and policies](plans-and-policies-101.md).
{% endhint %}

## Overview

You're almost there. This is the final section of the Quickstart guide.&#x20;

So far, we've shown you how to create Gateway APIs and then how to augment and enhance those APIs with plans and policies to add additional layers of security and functionality. These powerful tools allow you to effectively manage your backend API servers and message brokers in a unified interface.

However, these capabilities are wasted if there is no way to expose and catalog these APIs for consumers. Enter the Developer Portal.

The Developer Portal is a web application that provides a simplified, user-friendly interface tailored to the API consumption process. It acts as a centralized catalog where internal and external API consumers can find and subscribe to APIs that are developed, managed, and deployed by API publishers.

API consumers can easily discover and explore APIs, read documentation, test API endpoints, generate access tokens, view API analytics, and manage their API subscriptions in a single location. Additionally, administrators have significant control over the look and feel of the Developer Portal to deliver an accessible and on-brand experience to external API consumers.

***

## Publish your API

Before heading over to the Developer Portal, we need to make sure our Gateway API will be visible to consumers.&#x20;

### Access API

First, we need to open the API in the APIM Console. You may already have the API open from the previous part of the Quickstart guide.

If not, simply head back over to **APIs** home screen and select the API you created.

<figure><img src="../../.gitbook/assets/Screenshot 2023-11-19 at 8.25.21 PM.png" alt=""><figcaption><p>APIs homescreen</p></figcaption></figure>

> * [x] Select **APIs** in the sidebar
> * [x] Select the API you created in Gateway APIs 101

### Publish API

This will take you straight to your API's **General Info** page. In the **Danger Zone**, we can update the visibility of the API:

* **Publish/Unpublish the API:** this is a toggle that controls the visibility of the API in the Developer Portal. Unless the API is also public, it is only visible to members of the API which is controlled through the **User and group access** tab on the inner sidebar.
* **Make Public/Private:** this is a toggle that makes the API visible to anyone with access to the Developer Portal. Note, this toggle only has an impact if the API is published.

<figure><img src="../../.gitbook/assets/Screenshot 2023-11-19 at 11.20.32 PM.png" alt=""><figcaption><p>API Danger Zone</p></figcaption></figure>

> * [x] Select **Publish the API** and then **Publish** in the modal to add the API to the Developer Portal
> * [x] Select **Make Public** and then **Make Public** again in the modal so it's visible to all API consumers

## Developer Portal

We're now ready to explore our published API in the Developer Portal.

### Access the Developer Portal

Enterprise trial users should be able to immediately access the Developer Portal from the APIM Console by selecting the **Developer Portal** link in the top left of the Console's nav bar.

<details>

<summary>Self-managed installation: Adding a Developer Portal link</summary>

For self-managed installations, the Developer Portal host can be easily modified so you must manually add the **Portal URL** to see the Developer Portal link in the Console UI.

Your Developer Portal URL will depend on your deployment so please reference the respective installation docs. For example, with the default docker installation, you can access the Developer Portal at `http://localhost:8085` in your browser.

<img src="../../.gitbook/assets/Screenshot 2023-11-21 at 1.15.16 PM.png" alt="Update Developer Portal settings in the Console" data-size="original">

* [x] Select **Settings** in the sidebar
* [x] Select **Settings** in the inner sidebar
* [x] Scroll down to **Portal** settings and provide a **Portal URL** based on your deployment configuration
* [x] Scroll to the bottom of the page and select **Save**

</details>

<figure><img src="../../.gitbook/assets/Screenshot 2023-11-21 at 1.11.23 PM.png" alt=""><figcaption><p>Access Developer Portal from APIM Console</p></figcaption></figure>

> * [x] Select the **Developer Portal** link in the top left of your Console's nav bar

This will bring you to the home screen of the Developer Portal.

<figure><img src="../../.gitbook/assets/Screenshot 2023-11-21 at 1.19.27 PM.png" alt=""><figcaption><p>Your default Developer Portal</p></figcaption></figure>

From here, you can immediately begin searching for APIs using the Developer Portal's full-context[^1] search. However, you will not be able to subscribe to any APIs until you create an application.

### Create an application

Now that we have access to the Developer Portal, we can take on the role of an API consumer. The next step is to create an application that is used to register and agree to plans. Let's see how to go about creating an application.

<figure><img src="../../.gitbook/assets/Screenshot 2023-11-21 at 6.06.07 PM.png" alt=""><figcaption><p>Developer Portal Applications page</p></figcaption></figure>

> * [x] Select **Applications** in the top nav bar
> * [x] Select **+ Create an App** on the subnav bar

#### General step

This will open the application creation wizard. The **General** step is focused on providing application metadata.&#x20;

<figure><img src="../../.gitbook/assets/Screenshot 2023-11-21 at 6.18.07 PM.png" alt=""><figcaption><p>General step of application creation wizard</p></figcaption></figure>

> * [x] Provide a name and description then select **Next**

#### Security step

The next step is focused on **Security**. This page may look different depending on your **Client Registration** settings which are configured in the APIM console.

However, everyone should have the option to create a **Simple** application.&#x20;

{% hint style="info" %}
**Dynamic Client Registration**

A **Simple** application allows API consumers to define their own `client_id`. However, this is not secure and should not be used outside of testing. Therefore, Gravitee allows you to disable **Simple** applications and [use dynamic client registration (DCR) to create advanced applications](https://documentation.gravitee.io/apim/guides/api-exposure-plans-applications-and-subscriptions/plans-1#advanced-application-configuration) with the identity provider of their choosing.&#x20;
{% endhint %}

<figure><img src="../../.gitbook/assets/Screenshot 2023-11-21 at 6.29.05 PM.png" alt=""><figcaption><p>Security step of appliation creation wizard</p></figcaption></figure>

> * [x] Select a **Simple** application and then select **Next**

#### Subscription step

The **Subscription** step of the application creation process allows you to send API subscription requests as you are creating the application. You will be able to search for any published APIs you have access to and view the available plans.

Once we finish creating the app, the request will be sent for review and approval by the API publisher.

<figure><img src="../../.gitbook/assets/Screenshot 2023-11-21 at 6.33.09 PM.png" alt=""><figcaption><p>Subscription step of application creation wizard</p></figcaption></figure>

> * [x] Search for the API you published and select it
> * [x] Select **Subscribe** under the API Key Plan and then select **Next**

#### Validation step

Finally, we just need to complete the **Validation** step. Review your application details and subscription request. If everything looks good, go ahead and create your app!

<figure><img src="../../.gitbook/assets/Screenshot 2023-11-21 at 6.36.14 PM.png" alt=""><figcaption><p>Validation step of application creation wizard</p></figcaption></figure>

> * [x] Select **Create the App**

You should receive validation that your app was successfully created. Feel free to open your app and explore the different tabs.

## Managing subscriptions

It's time to resume our previous role as an API publisher. Let's return to the APIM Console to manage the subscription request we just submitted. It should have come through as a new **Task**.

<figure><img src="../../.gitbook/assets/Screenshot 2023-11-21 at 7.34.03 PM.png" alt=""><figcaption><p>View your tasks in the Console</p></figcaption></figure>

> * [x] Select your profile in the top right
> * [x] Select **Task** in the dropdown

This will bring you to a list of all your current tasks. Currently, this should just be a subscription request from the application you just created to your API.

<figure><img src="../../.gitbook/assets/Screenshot 2023-11-21 at 7.35.20 PM.png" alt=""><figcaption><p>A list of your tasks in the console</p></figcaption></figure>

> * [x] Select Validate under the subscription request

This will not immediately validate the request but rather navigate you to part of the Console where you can validate the subscription.

{% hint style="info" %}
This was essentially a shortcut to our APIs subscription screen. You can always navigate here by selecting your API, selecting **Plans** in the inner sidebar, and then selecting the **Subscriptions** tab.
{% endhint %}

Here we can see all the metadata (e.g. user, application, plan, etc.) for the request and decide on an action. Once you validate, you will have additional options for managing the subscription.

<figure><img src="../../.gitbook/assets/Screenshot 2023-11-21 at 7.41.45 PM.png" alt=""><figcaption><p>Subscription validation screen</p></figcaption></figure>

> * [x] Select **Validate subscription**
> * [x] Leave the defaults and select **Validate** in the modal

The subscription is now active! However, as the API publisher, you have a number of different options for managing this subscription:

* **Transfer:** move this subscription to a different plan
* **Pause:** temporarily suspend the subscription. Be careful with this as the consumer's API requests will fail when their subscription is paused
* **Change end date:** change or set the expiration date on all the API keys provisioned
* **Close:** permanently end the subscription. The API consumer will need to subscribe again to have access to this API

At the bottom of the screen, you will see the API key that has been randomly generated and provisioned for this user. APIM allows you to customize this behavior including providing your own API key and allowing the API consumer to share API keys between subscriptions.

For now, simply copy that API key to your clipboard.

<figure><img src="../../.gitbook/assets/Screenshot 2023-11-21 at 7.47.19 PM.png" alt=""><figcaption><p>Subscription management </p></figcaption></figure>

> * [x] Select the **Copy to clipboard** icon next to the API key

## Test API

For the final time, let's send the same request but with one small modification. We need to pass our new API key to act as the authorization token for our request. To do this, we will use the `X-Gravitee-API-Key` header.

{% hint style="info" %}
This is the default header to pass the API key but it can be modified. Additionally, you can pass the API key with the query parameter `api-key`, if preferred.
{% endhint %}

{% code overflow="wrap" %}
```sh
curl -X GET -i "https://your-gateway-server/your-context-path" -H "X-Gravitee-API-Key: your-key-here"
```
{% endcode %}

{% hint style="success" %}
You should receive a **`200 OK`** success status response code along with the custom payload you configured using the Assign Content policy in the previous section.

Congrats! You have successfully completed the Quickstart guide! Head on over to our [What's Next](whats-next.md) section if you're looking for suggestions on how to learn about more advanced Gravitee topics.&#x20;
{% endhint %}

[^1]: Full-context meaning it searches through the definition and metadata of all published APIs that you have access to
