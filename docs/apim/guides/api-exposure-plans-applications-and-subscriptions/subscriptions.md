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

After creating an application, API consumers can subscribe to APIs (with published plans) either in the management UI or the developer portal. We will work through the management UI as we have a separate guide dedicated to the developer portal.

{% hint style="info" %}
You can also subscribe to APIs during the [application creation process.](plans-1.md#create-an-application)
{% endhint %}

{% @arcade/embed flowId="GOpV3Hu4ggkF5On3jCy9" url="https://app.arcade.software/share/GOpV3Hu4ggkF5On3jCy9" %}

It is important to reiterate that API consumers can only request a subscription for APIs they have access to. This means they must either be a member of the API or the API must be made public.

## Manage subscriptions

The following sections describe how to manage subscription requests from consumers.

### Approve a subscription

When publishers create new plans, they can specify a[uto-validation of subscriptions](plans.md#general), so consumers are ready to access the API as soon as they subscribe to the plan. If you set manual approval on a plan, however, you must approve all subscription requests.

{% hint style="info" %}
**Subscription request notifications**

You can enable mail or portal notifications so you can be notified when a subscription validation task requires your attention. Simply select your API, scroll down and select **Notifications**, select **Portal Notification** or **Default Mail Notifications**, and select the types of events you want to trigger notifications.&#x20;

Portal notifications are delivered both inside of APIM's management UI and the developer portal.
{% endhint %}

1. Go to your API in APIM Management and click **Portal > Subscriptions**.
2. Select the **Pending** subscription.
3.  Click **ACCEPT**, then enter the start and end dates (no end date means forever) of subscription approval.



    <figure><img src="https://docs.gravitee.io/images/apim/3.x/api-publisher-guide/plans-subscriptions/approve-subscription.png" alt=""><figcaption></figcaption></figure>

### Revoke a subscription

You can revoke a subscription to remove access to APIs.

1. Go to your API in APIM Management and click **Portal > Subscriptions**.
2.  Select the subscription you want to revoke and click **CLOSE**.



    <figure><img src="https://docs.gravitee.io/images/apim/3.x/api-publisher-guide/plans-subscriptions/revoke-subscription.png" alt=""><figcaption></figcaption></figure>

\
