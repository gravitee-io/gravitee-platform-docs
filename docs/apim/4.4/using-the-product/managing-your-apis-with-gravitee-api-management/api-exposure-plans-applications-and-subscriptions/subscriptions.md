---
description: Validating and managing subscriptions
---

# Managing and transferring Subscriptions

## Introduction

A subscription is a successful contract between an API publisher and an API consumer. A subscription is created when an API consumer uses a registered application to make a subscription request to a published plan and an API publisher either manually or automatically validates the subscription.

{% hint style="info" %}
**Keyless plan subscriptions**

APIs with Keyless plans do not require the API consumer to create an application or submit a subscription request because no authorization is required to access the backend API.
{% endhint %}

This page includes the following sections:

* [Subscription requests](subscriptions.md#subscription-requests)
* [Manage subscriptions](subscriptions.md#manage-subscriptions)
* [Transfer subscriptions](subscriptions.md#transfer-subscriptions)

## Subscription requests

API consumers can subscribe to APIs with published plans during the [application creation process](applications.md#create-an-application), or after the application is created, through the APIM Console or Developer Portal.

{% hint style="info" %}
Whether an application has an associated `client_id` depends on how it was configured. To subscribe to OAuth2 or JWT plans, the application must have a `client_id`.
{% endhint %}

To subscribe to an API via the APIM Console:

1. Log in to your APIM Console
2. Select **Applications** from the left nav
3. Select **Subscriptions** from the inner left nav
4.  Click the **+ Create a subscription** button

    <figure><img src="../../../.gitbook/assets/subscription_create 2.png" alt=""><figcaption><p>Create a subscription</p></figcaption></figure>
5. Search for the API you want to subscribe to. To be searchable the API consumer must have access to the API, i.e., the API must be public or the API consumer must be a member of it.
6.  Select the plan you would like to request a subscription to

    <figure><img src="../../../.gitbook/assets/subscription_create.png" alt=""><figcaption><p>Select the subscription plan</p></figcaption></figure>
7. Click **Create** to see the subscription details

## Manage subscriptions

When creating a plan, you can enable subscription auto-validation to immediately approve subscription requests. If **Auto validate subscription** is disabled, the API publisher must approve all subscription requests.

{% hint style="info" %}
To be notified of subscription validation tasks, enable [Notifications](../../using-the-gravitee-api-management-components/apim-console/notifications.md)
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

       <figure><img src="../../../.gitbook/assets/subscription_validate 2.png" alt=""><figcaption><p>Validate the subscription</p></figcaption></figure>

### API Key plans

Subscriptions to API Key plans include additional security management settings:

*   **Renew:** Generate a new API key or provide a custom API key. The existing API key will be automatically invalidated after two hours.

    <figure><img src="../../../.gitbook/assets/subscription_api key renew.png" alt=""><figcaption><p>Renew an API key</p></figcaption></figure>
*   **Revoke:** Immediately invalidate an existing API key. This option is reversible.

    <figure><img src="../../../.gitbook/assets/subscription_api key revoke.png" alt=""><figcaption><p>Revoke an API key</p></figcaption></figure>
*   **Expire:** Set a date/time to automatically invalidate an existing API key

    <figure><img src="../../../.gitbook/assets/subscription_api key expire.png" alt=""><figcaption><p>Expire an API key</p></figcaption></figure>

## Transfer subscriptions

API publishers can transfer active subscriptions to a new plan with the same security type:

1. Log in to your APIM Console
2. Select **APIs** from the left nav
3. Select the API with the subscription to transfer
4. Select **Consumers** from the inner left nav
5. Click the **Subscriptions** header tab
6. Click the pencil icon of the subscription you want to transfer
7.  At the bottom of the **Subscription details** section, click Transfer

    <figure><img src="../../../.gitbook/assets/subscription_transfer.png" alt=""><figcaption><p>Transfer a subscription</p></figcaption></figure>
8.  Select the plan to transfer the subscription to, then click **Transfer**

    <figure><img src="../../../.gitbook/assets/subscription_transfer confirm.png" alt=""><figcaption><p>Specify and confirm subscription transfer</p></figcaption></figure>
