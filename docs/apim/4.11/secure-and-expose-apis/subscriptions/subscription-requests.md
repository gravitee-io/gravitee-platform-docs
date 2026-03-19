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

### Prerequisites

Before creating a subscription, ensure the following requirements are met:

* The API consumer must have access to the API (the API must be public or the API consumer must be a member of it)
* For subscription forms: User must have `environment-metadata-r` permission to view subscription forms
* For subscription forms: Database schema migration `08_add_subscription_forms_table.yml` must be applied
* For subscription forms: Portal API authentication must be configured for consumer access

### Create a subscription via APIM Console

To subscribe to an API via the APIM Console:

1. Log in to your APIM Console
2. Select **Applications** from the left nav
3. Select **Subscriptions** from the inner left nav
4.  Click the **+ Create a subscription** button

    <figure><img src="../../.gitbook/assets/subscription_create 2.png" alt=""><figcaption><p>Create a subscription</p></figcaption></figure>
5. Search for the API you want to subscribe to. To be searchable the API consumer must have access to the API, i.e., the API must be public or the API consumer must be a member of it.
6.  Select the plan you would like to request a subscription to

    <figure><img src="../../.gitbook/assets/subscription_create.png" alt=""><figcaption><p>Select the subscription plan</p></figcaption></figure>
7. If a subscription form is configured and enabled for the environment, and the selected plan's security type is not `KEY_LESS`, the form appears as step 4 (Checkout) in the subscription wizard, replacing the legacy "Add a comment" card. Complete the form fields to provide metadata for the subscription request. The **Next** button is disabled until all required fields are valid.
8. Click **Create** to see the subscription details

### Consumer subscription flow

When a consumer subscribes to an API with an enabled subscription form, the form values are filtered to remove empty or whitespace-only entries, then attached to the subscription as metadata. If the plan security type is `KEY_LESS`, the form is skipped entirely regardless of configuration.

#### Subscription form display conditions

The subscription form is shown when:

* The subscription form exists and has `gmdContent`
* The form is enabled
* The plan security type is not `KEY_LESS`

#### Metadata filtering

Empty or whitespace-only metadata values are excluded from subscription creation. The filtering logic removes any key-value pair where the value is `null` or contains only whitespace characters.

#### Form validation

The **Next** button in the subscription wizard is disabled when:

* The subscription form is present and contains invalid fields
* Required fields are empty or incomplete

#### Metadata attachment

Metadata is included in the subscription creation request when:

1. A subscription form exists and has `gmdContent`
2. The plan security type is not `KEY_LESS`
3. The metadata object has at least one non-empty key-value pair after filtering
