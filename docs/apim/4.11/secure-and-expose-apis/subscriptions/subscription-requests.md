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

### Subscribe via APIM Console

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

### Subscribe via Developer Portal with subscription forms

When an enabled subscription form exists and the selected plan is not `KEY_LESS`, the form appears during subscription checkout in the Developer Portal.

1. Select an application and plan.
2. Complete all required fields in the subscription form. The **Subscribe** button is disabled until all fields pass validation.
3. Click **Subscribe**. Form values are extracted, empty values are filtered out, and the metadata is submitted with the subscription request.
4. View submitted metadata in the subscription details page under the **Metadata** section, displayed as read-only JSON.

## Subscription metadata


Subscription metadata is collected through [subscription forms](subscription-forms.md) and attached to subscription requests.
 Metadata is only sent when a subscription form exists, is enabled, and the plan security is not `KEY_LESS`. Empty metadata values (null or whitespace-only) are filtered out before submission. Metadata keys must be valid (alphanumeric, underscores, hyphens).

## Validation

Portal page content validation logic has been refactored into the `GraviteeMarkdownValidator` domain service. The exception `EmptyPortalPageContentException` has been replaced with `GraviteeMarkdownContentEmptyException`. This validation now applies to both portal pages and subscription forms.
