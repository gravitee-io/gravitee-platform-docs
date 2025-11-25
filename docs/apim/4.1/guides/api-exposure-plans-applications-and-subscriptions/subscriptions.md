---
description: Validating and managing subscriptions
---

# Subscriptions

A subscription is a successful contract between an API publisher and an API consumer. Subscriptions are created when an API consumer uses a registered application to create a subscription request to a published plan, and an API publisher either manually or automatically validates the subscription.

{% hint style="info" %}
**Keyless plan subscriptions**

APIs with keyless plans do not require the API consumer to create an application or submit a subscription request as no authorization is required to access the backend API.
{% endhint %}

## Subscription requests

After creating an application, API consumers can subscribe to APIs (with published plans) either in the Management Console or the Developer Portal. We will work through the Management Console as we have a separate guide dedicated to the Developer Portal.

{% hint style="info" %}
You can also subscribe to APIs during the [application creation process.](plans-1.md#create-an-application)
{% endhint %}

{% @arcade/embed url="https://app.arcade.software/share/GOpV3Hu4ggkF5On3jCy9" flowId="GOpV3Hu4ggkF5On3jCy9" %}

It is important to reiterate that API consumers can only request a subscription for APIs they have access to. This means they must either be a member of the API or the API must be made public.

## Manage subscriptions

When publishers create new plans, they can specify [auto-validation of subscriptions](plans.md#general), so consumers' subscription requests are immediately approved. Otherwise, the API publisher must approve all subscription requests.

{% hint style="info" %}
**Subscription request notifications**

You can enable mail or portal notifications so you can be notified when a subscription validation task requires your attention. Simply select your API, scroll down and select **Notifications**, select **Portal Notification** or **Default Mail Notifications**, and select the types of events you want to trigger notifications.

Portal notifications are delivered both inside of APIM's Management Console and the Developer Portal.
{% endhint %}

{% @arcade/embed url="https://app.arcade.software/share/nTazQcgGLNWVFwHEyerB" flowId="nTazQcgGLNWVFwHEyerB" %}

### Transfer subscriptions

API publishers can transfer active subscriptions to a new plan with the _same_ security type.

{% @arcade/embed url="https://app.arcade.software/share/UVhKz3t5HsY9e74hYms9" flowId="UVhKz3t5HsY9e74hYms9" %}

### Security: API key plans

API publishers have additional management settings for subscriptions to API key plans:

* **Renew:** generate a new API key or provide your own custom API key. The existing API key will be automatically invalidated after two hours.
* **Revoke:** immediately invalidate an existing API key. This option is reversible.
* **Set expiration date:** set a date and time to automatically invalidate an existing API key

<figure><img src="../../.gitbook/assets/api_key_subscripiton_management (1).png" alt=""><figcaption><p>API key plan subscription</p></figcaption></figure>
