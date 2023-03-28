---
description: Creating and managing subscriptions
---

# Subscriptions

A subscription is a successful contract between an API publisher and an API consumer. Subscriptions are created when an API consumer uses a registered application to create a subscription request to a published plan, and an API publisher either manually or automatically accepts the subscription.

{% hint style="info" %}
**Keyless plan subscriptions**

APIs with keyless plans do not require the API consumer to create an application or submit as subscription request as no authentication is required to access the backend API.
{% endhint %}

## Subscribe to APIs

After creating an application, API consumers can subscribe to APIs (with published plans) either in the management UI or the developer portal. We will work through the management UI as we have a separate guide dedicated to the developer portal.

{% hint style="info" %}
You can also subscribe to APIs during the application creation process.
{% endhint %}

Arcade here

## Manage subscriptions

Consumers use plans to request subscriptions and access your APIs. They subscribe to plans in APIM Portal:

![plans subscriptions](https://docs.gravitee.io/images/apim/3.x/api-publisher-guide/plans-subscriptions/plans-subscriptions.png)

The following sections describe how to manage subscription requests from consumers.

#### Approve a subscription

When publishers create new plans, they can specify auto validation of subscriptions, so consumers are ready to access the API as soon as they subscribe to the plan. If you set manual approval on a plan, however, you must approve subscriptions by following these steps.

|   | You can enable mail or portal notifications so you can be notified when a subscription validation task requires your attention. |
| - | ------------------------------------------------------------------------------------------------------------------------------- |

1. Go to your API in APIM Management and click **Portal > Subscriptions**.
2. Select the **Pending** subscription.
3.  Click **ACCEPT**, then enter the start and end dates (no end date means forever) of subscription approval.

    ![approve subscription](https://docs.gravitee.io/images/apim/3.x/api-publisher-guide/plans-subscriptions/approve-subscription.png)

#### Revoke a subscription

You can revoke a subscription to remove access to APIs.

1. Go to your API in APIM Management and click **Portal > Subscriptions**.
2.  Select the subscription you want to revoke and click **CLOSE**.

    ![revoke subscription](https://docs.gravitee.io/images/apim/3.x/api-publisher-guide/plans-subscriptions/revoke-subscription.png)

\
