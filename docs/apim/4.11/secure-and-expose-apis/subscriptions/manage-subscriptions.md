---
description: Documentation about manage subscriptions in the context of APIs.
metaLinks:
  alternates:
    - manage-subscriptions.md
---

# Manage Subscriptions

## Subscription management

To find an application's subscriptions, log in to your APIM Console, and then select **Applications** from the menu.

<figure><img src="../../.gitbook/assets/00 sub 1.png" alt=""><figcaption></figcaption></figure>

Select the application you're looking for, and then select **Subscriptions** from the menu.

From the **Subscriptions** header of this page, you can view, filter, and delete subscriptions. Subscriptions are tagged by security type, the plan and API or API Product they belong to, the times at which they were created, processed, started, and ended, and their status.

### Subscription reference model

As of version 4.11.0, subscriptions use a reference model that supports both API and API Product subscriptions. Each subscription includes a `referenceType` field (`API` or `API_PRODUCT`) and a `referenceId` pointing to the parent resource. The legacy `api` field is deprecated as of version 4.11.0 and shouldn't be used for new subscriptions.

When validating subscriptions, the gateway checks API Product subscriptions first before checking API-level plans. This allows organizations to manage access at the API Product level while maintaining backward compatibility with existing API subscriptions.

<figure><img src="../../.gitbook/assets/1 app sub 1.png" alt=""><figcaption></figcaption></figure>

Use the eye icon to view subscription details.

<figure><img src="../../.gitbook/assets/1 app sub 3.png" alt=""><figcaption></figcaption></figure>

To filter subscriptions, use the **API** and **API Key** search fields and/or the **Status** drop-down menu. Subscriptions can have a status of accepted, closed, paused, pending, rejected, or resumed.

<figure><img src="../../.gitbook/assets/1 app sub 2.png" alt=""><figcaption></figcaption></figure>

To create a new subscription, click **+ Create a subscription** and search for the API you'd like to subscribe to. Refer to the [subscription](README.md) documentation for more information.

## Subscription validation

When creating a plan, you can enable subscription auto-validation to immediately approve subscription requests. If **Auto validate subscription** is disabled, the API publisher must approve all subscription requests.

{% hint style="info" %}
To be notified of subscription validation tasks, enable [Notifications](../../configure-and-manage-the-platform/gravitee-gateway/notifications.md)
{% endhint %}

To manage subscriptions in APIM Console:

1. Log in to your APIM Console
2. Select **APIs** from the left nav
3. Select the API with subscriptions to manage
4. Select **Consumers** from the inner left nav
5. Click the **Subscriptions** header tab
6. Select the request or subscription you want to manage
7. Validate or reject the subscription
   *   If validating, fill out the **Validate your subscription** form, then click **Validate**

       <figure><img src="../../.gitbook/assets/subscription_validate 2.png" alt=""><figcaption><p>Validate the subscription</p></figcaption></figure>

## Shared API Keys

Under the **Shared API Keys** header, you can view the API keys that are shared with all application subscriptions that have an API\_KEY plan.

<figure><img src="../../.gitbook/assets/1 shared 1.png" alt=""><figcaption></figcaption></figure>

Click the **x** icon to revoke an API key, or the **Renew** button to renew it. Renewing a shared API key applies the same two-hour grace period described in [API Key plans](manage-subscriptions.md#api-key-plans), and affects every subscription of the application at once.

{% hint style="info" %}
Manage shared API keys from the application. The subscription-level **Renew**, **Revoke**, and **Expire** actions apply only to applications that use the `EXCLUSIVE` API key mode. For the equivalent API operations, see [Modifying shared API keys](../plans/api-key.md#modifying-shared-api-keys).
{% endhint %}

## API Key plans

Subscriptions to API Key plans include additional security management settings:

*   **Renew:** Generate a new API key or provide a custom API key. The previous key stays valid for a two-hour grace period, measured from the moment the new key is created, so that consumers have time to switch over. It then expires automatically. The grace period is fixed and can't be configured.

    <figure><img src="../../.gitbook/assets/subscription_api key renew.png" alt=""><figcaption><p>Renew an API key</p></figcaption></figure>
*   **Revoke:** Immediately invalidate an existing API key. This option is reversible.

    <figure><img src="../../.gitbook/assets/subscription_api key revoke.png" alt=""><figcaption><p>Revoke an API key</p></figcaption></figure>
*   **Expire:** Set a date/time to automatically invalidate an existing API key

    <figure><img src="../../.gitbook/assets/subscription_api key expire.png" alt=""><figcaption><p>Expire an API key</p></figcaption></figure>
