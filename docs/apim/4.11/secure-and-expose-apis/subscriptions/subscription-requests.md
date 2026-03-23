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
Whether an application has an `client_id` depends on how it was configured. To subscribe to OAuth2 or JWT plans, the application must have a `client_id`.
{% endhint %}

### Subscription Workflow Steps

The subscription process uses four distinct steps identified by the `SubscribeStep` enum:

* `PLAN_SELECTION`: Choose a plan
* `APP_SELECTION`: Choose an application
* `PUSH_DETAILS`: Configure Consumer (push-mode plans only)
* `REVIEW`: Review (formerly "Checkout")

Each step includes a numbered badge and descriptive header.

**Step 1: Choose a plan**

A plan lets an application access an API. Once subscribed and approved, the application gets credentials to use it.

**Step 2: Choose an application**

An application represents a developer's project that interacts with the API. Keyless plans skip this step and proceed directly to review.

**Step 3: Configure Consumer**

This step appears only for push-mode plans.

**Step 4: Review**

The final step before submission.

### Application Selection Validation

Applications are disabled for selection when:

* A valid subscription already exists for the chosen plan
* The application uses shared key mode and already has an active API key subscription for the target API

The validation message reads: "A subscription already exists for this plan"

### Prerequisites

Before you configure API subscriptions, ensure you have the following:

* Gravitee API Management portal
* Existing API catalog with published APIs
* Applications configured for subscription

{% hint style="info" %}
Applications are not required for keyless plans.
{% endhint %}

### Subscribe to an API via APIM Console

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

### Subscribe to an API via Developer Portal

Navigate to the catalog at `/catalog`, select an API, and choose a plan. The subscription wizard displays step 1 ("Choose a plan") with a description explaining that plans grant application access and provide credentials. After selecting a plan, proceed to step 2 ("Choose an application").

The subscription comment dialog displays the subtitle: "Briefly explain why you need this API so the owner can review your request."

The subscription info layout uses a column direction for improved vertical stacking.
