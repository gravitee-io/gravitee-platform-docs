---
description: API consumers configure their webhook subscriptions from the Developer Portal 4.12. Learn what the configuration involves for them.
metaLinks:
  alternates:
    - webhook-subscriptions.md
---

# Webhook Subscriptions

## Overview

{% hint style="warning" %}
If you use the New Developer Portal and want to configure webhook subscriptions, follow the [configure-webhook-subscriptions.md](../new-developer-portal/configure-webhook-subscriptions.md "mention") guide.
{% endhint %}

API consumers can configure their webhook subscriptions from the Developer Portal. Configuration involves adding a callback URL, choosing an application, and validating the request.

## Configuration

Before you can define and configure your Webhook subscription, you'll need to find it in the Developer Portal:

1. Click on **Catalog** in the header
2.  (Optional) Use the search field

    <figure><img src="../../.gitbook/assets/webhook_catalog.png" alt="The portal Catalog with a search for webhook open, showing matching APIs and their owners above the category tiles."><figcaption><p>Find your Webhook subscription in the Developer Portal</p></figcaption></figure>
3.  Click on the subscription, then on **Subscribe**

    <figure><img src="../../.gitbook/assets/webhook_subscribe.png" alt="The portal page for a webhook API, with its general information tabs and a Subscribe button."><figcaption><p>Subscribe to your Webhook subscription</p></figcaption></figure>
4.  Choose a **PUSH plan.** A PUSH plan is limited to Webhooks and enables you to subscribe to APIs that have a subscription listener (currently also limited to Webhooks).

    <figure><img src="../../.gitbook/assets/webhook_push plan.png" alt="The choice of plan step of the subscription wizard, with the default push plan selected."><figcaption><p>Choose a PUSH plan</p></figcaption></figure>
5. Next, select your subscription channel and Webhook entrypoint, then define:
   * Callback URL
   * HTTP headers
   * Security config
   * Security type (basic, token, or OAuth2)
   * SSL options:
     * Enable or disable **Verify Host**
     * Enable or disable **Trust all**
     * Define your **Trust store**
     * Define your **Key store**

<figure><img src="../../.gitbook/assets/webhook_configure subscription.png" alt="The configure subscription step, with the entrypoint set to Webhook above the callback URL, HTTP headers, security and SSL options."><figcaption><p>Define your Webhook subscription settings</p></figcaption></figure>

6.  Next, choose which application will be the subscriber and (optionally) leave a message for the API Owner.

    <figure><img src="../../.gitbook/assets/webhook_choose application.png" alt="The choice of application step of the subscription wizard, with an application list and a comment field for the API owner."><figcaption><p>Choose the subscriber application</p></figcaption></figure>
7.  Select **Next** to validate your subscription request

    <figure><img src="../../.gitbook/assets/webhook_validate.png" alt="The validation step of the subscription wizard, confirming the application, plan and API and noting that the owner must approve."><figcaption><p>Submit to validate your Webhook subscription</p></figcaption></figure>
