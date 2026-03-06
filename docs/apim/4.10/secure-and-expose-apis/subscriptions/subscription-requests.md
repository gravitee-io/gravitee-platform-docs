---
description: An overview about subscription requests.
metaLinks:
  alternates:
    - subscription-requests.md
---

# Subscription Requests

## Overview

From a configuration perspective, a subscription is a successful contract between an API publisher and an API consumer. A subscription is created when an API consumer uses a registered application to make a subscription request to a published plan and an API publisher either manually or automatically validates the subscription.

{% hint style="info" %}
**Keyless plan subscriptions**

APIs with Keyless plans do not require the API consumer to create an application or submit a subscription request because no authorization is required to access the backend API.
{% endhint %}

## Configure subscriptions

API consumers can subscribe to APIs with published plans during the application creation process, or after the application is created, through the APIM Console or Developer Portal.

{% hint style="info" %}
Whether an application has an associated `client_id` depends on how it was configured. To subscribe to OAuth2 or JWT plans, the application must have a `client_id`.
{% endhint %}

### Subscribe to an API

To subscribe to an API via the APIM Console:

1. Log in to your APIM Console
2. Select **Applications** from the left nav
3. Select **Subscriptions** from the inner left nav
4.  Click the **+ Create a subscription** button

    <figure><img src="../../.gitbook/assets/subscription_create 2.png" alt=""><figcaption><p>Create a subscription</p></figcaption></figure>
5. Search for the API you want to subscribe to. To be searchable the API consumer must have access to the API, i.e., the API must be public or the API consumer must be a member of it.
6.  Select the plan you would like to request a subscription to

    <figure><img src="../../.gitbook/assets/subscription_create.png" alt=""><figcaption><p>Select the subscription plan</p></figcaption></figure>
7. Click **Create** to see the subscription details

### Subscribe to an API Product

Consumers subscribe to API Products through the application subscription workflow.

1. Navigate to the application and click **+ Create a subscription**.
2. Search for the API Product you want to subscribe to. API Products are labeled "API Product" in the reference type column of the subscription dialog.
3. Select a plan associated with the API Product.
4. Click **Create** to submit the subscription request. The system creates a subscription with `referenceType=API_PRODUCT` and `referenceId` set to the product ID.
5. If the plan uses API Key security, the system generates keys linked to the product subscription.
6. The subscription grants access to all APIs bundled in the product.

{% hint style="info" %}
Removing an API from a product does not invalidate existing subscriptions, but new subscriptions will only grant access to the updated API set.
{% endhint %}
