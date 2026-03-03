---
description: Documentation about transfer subscriptions in the context of APIs.
metaLinks:
  alternates:
    - transfer-subscriptions.md
---

# Transfer Subscriptions

API publishers can transfer active subscriptions to a new plan with the same security type. 
Subscriptions are associated with either an API or an [API Product](../api-products/README.md) through the `referenceType` and `referenceId` fields.
 The `api` field is deprecated since 4.11.0.

When `referenceType` is `API`, the subscription is linked to a standard API plan. When `referenceType` is `API_PRODUCT`, the subscription is linked to an API Product plan, allowing access to multiple bundled APIs through a single subscription.

To transfer a subscription:

1. Log in to your APIM Console
2. Select **APIs** from the left nav
3. Select the API with the subscription to transfer
4. Select **Consumers** from the inner left nav
5. Click the **Subscriptions** header tab
6. Click the pencil icon of the subscription you want to transfer
7.  At the bottom of the **Subscription details** section, click Transfer

    <figure><img src="../../.gitbook/assets/subscription_transfer (1).png" alt=""><figcaption><p>Transfer a subscription</p></figcaption></figure>
8.  Select the plan to transfer the subscription to, then click **Transfer**

    <figure><img src="../../.gitbook/assets/subscription_transfer confirm (1).png" alt=""><figcaption><p>Specify and confirm subscription transfer</p></figcaption></figure>
