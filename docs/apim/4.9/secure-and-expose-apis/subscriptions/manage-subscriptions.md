# Manage Subscriptions

## Subscription management

To find an application's subscriptions, log in to your APIM Console, and then select **Applications** from the menu.

<figure><img src="../../.gitbook/assets/00 sub 1.png" alt=""><figcaption></figcaption></figure>

Select the application you're looking for, and then select **Subscriptions** from the menu.

From the **Subscriptions** header of this page, you can view, filter, and delete subscriptions. Subscriptions are tagged by security type, the plan and API they belong to, the times at which they were created, processed, started, and ended, and their status.&#x20;

<figure><img src="../../.gitbook/assets/1 app sub 1.png" alt=""><figcaption></figcaption></figure>

Use the eye icon to view subscription details.

<figure><img src="../../.gitbook/assets/1 app sub 3.png" alt=""><figcaption></figcaption></figure>

To filter subscriptions, use the **API** and **API Key** search fields and/or the **Status** drop-down menu. Subscriptions can have a status of accepted, closed, paused, pending, rejected, or resumed.

<figure><img src="../../.gitbook/assets/1 app sub 2.png" alt=""><figcaption></figcaption></figure>

To create a new subscription, click **+ Create a subscription** and search for the API you'd like to subscribe to. Refer to the [subscription](./) documentation for more information.

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
   *   If validating, fill out the **Validate your subscription** form, then click **Validate**&#x20;

       <figure><img src="../../.gitbook/assets/subscription_validate 2.png" alt=""><figcaption><p>Validate the subscription</p></figcaption></figure>

## Shared API Keys

Under the **Shared API Keys** header, you can view the API keys that are shared with all application subscriptions that have an API\_KEY plan.&#x20;

<figure><img src="../../.gitbook/assets/1 shared 1.png" alt=""><figcaption></figcaption></figure>

Click the **x** icon to revoke an API key, or the **Renew** button to renew it.

## API Key plans

Subscriptions to API Key plans include additional security management settings:

*   **Renew:** Generate a new API key or provide a custom API key. The existing API key will be automatically invalidated after two hours.&#x20;

    <figure><img src="../../.gitbook/assets/subscription_api key renew.png" alt=""><figcaption><p>Renew an API key</p></figcaption></figure>
*   **Revoke:** Immediately invalidate an existing API key. This option is reversible.&#x20;

    <figure><img src="../../.gitbook/assets/subscription_api key revoke.png" alt=""><figcaption><p>Revoke an API key</p></figcaption></figure>
*   **Expire:** Set a date/time to automatically invalidate an existing API key&#x20;

    <figure><img src="../../.gitbook/assets/subscription_api key expire.png" alt=""><figcaption><p>Expire an API key</p></figcaption></figure>
