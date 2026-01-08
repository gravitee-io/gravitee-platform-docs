---
description: An overview about consumers.
metaLinks:
  alternates:
    - consumers.md
---

# Consumers

## Overview

The **Consumers** section lets you manage how your API is consumed through plans, subscriptions, or broadcasts.

## Plans

From the **Plans** tab, you can add, edit, publish, deprecate, or close a plan.

### Add a plan

To add a plan, click on **+ Add new plan**:

<figure><img src="../../../.gitbook/assets/A plan.png" alt=""><figcaption></figcaption></figure>

Kafka APIs support OAuth2, JWT, API Key, and Keyless (public) plans. For more information on each of these plans and configuration details, please see the following:

* [oauth2.md](../../../secure-and-expose-apis/plans/oauth2.md "mention")
* [jwt.md](../../../secure-and-expose-apis/plans/jwt.md "mention")
* [api-key.md](../../../secure-and-expose-apis/plans/api-key.md "mention")
* [keyless.md](../../../secure-and-expose-apis/plans/keyless.md "mention")

### Edit a plan

To edit a plan, click on the pencil icon:

<figure><img src="../../../.gitbook/assets/plan_edit (1).png" alt=""><figcaption><p>Edit a plan</p></figcaption></figure>

### Publish a plan

To publish a plan, click on the icon of a cloud with an arrow:

<figure><img src="../../../.gitbook/assets/plan_publish (1).png" alt=""><figcaption><p>Publish a plan</p></figcaption></figure>

Once a plan has been published, it must be redeployed.

### Deprecate a plan

To deprecate a plan, click on the icon of a cloud with an 'x':

<figure><img src="../../../.gitbook/assets/plan_deprecate (1).png" alt=""><figcaption><p>Deprecate a plan</p></figcaption></figure>

### Close a plan

To close a plan, click on the 'x' icon:

<figure><img src="../../../.gitbook/assets/plan_close (1).png" alt=""><figcaption><p>Close a plan</p></figcaption></figure>

## Subscriptions

Select the **Subscriptions** tab to manage your subscriptions. From here you can create, modify, or filter subscriptions. You can also export a subscription as a CSV.

<figure><img src="../../../.gitbook/assets/1 sub 1.png" alt=""><figcaption></figcaption></figure>

### Create a subscription

To create a subscription, you need to have at least one published plan whose type is not Keyless.

To create a new subscription, click the **+ Create a subscription** button. Select the application you want to use and the plan you want to subscribe to. The example below shows this for a subscription to an API Key plan.

<figure><img src="../../../.gitbook/assets/1 sub create 1.png" alt=""><figcaption></figcaption></figure>

You'll be taken to a screen that displays your subscription details.

<figure><img src="../../../.gitbook/assets/1 sub details.png" alt=""><figcaption></figcaption></figure>

From here you can transfer, pause, change the end date for, or close your subscription:

* To transfer a subscription, you must have another plan available to transfer your subscription to.
* If you pause a subscription, the application will no longer be able to consume the API.
* When changing the end date of your subscription, choose the date when the application should no longer have access to the API.
* If you close your subscription, the application will no longer be able to consume your API.

### Manage a subscription

Existing subscriptions can be managed from the **Subscriptions** header. From here you can use the filters to:

*   Display subscriptions based on plan selections

    <figure><img src="../../../.gitbook/assets/1 sub c.png" alt=""><figcaption></figcaption></figure>
*   Search for an application display subscriptions associated with a plan name

    <figure><img src="../../../.gitbook/assets/1 sub b.png" alt=""><figcaption></figcaption></figure>
*   Select subscription status options to display subscriptions matching that criteria

    <figure><img src="../../../.gitbook/assets/1 sub a.png" alt=""><figcaption></figcaption></figure>

If you click **Export as CSV**, all the subscriptions matching your filter selections will be exported in CSV format to the text editor of your choice.

## Broadcasts

From the **Broadcasts** tab, you can send messages to parties interested in your API to advertise updates, warn of upcoming changes, etc.

To configure message delivery mechanism, recipients, and content:

1. Select **APIs** from the left sidebar of the Management Console
2. Select the API you want to send a message about
3. Select **Consumers** from the inner left sidebar
4.  Select the **Broadcasts** tab

    <figure><img src="../../../.gitbook/assets/1 broadcast.png" alt=""><figcaption></figcaption></figure>
5. Specify the following:
   * **Channel:** Choose to send your message via **Email**, **Portal notifications**, or **POST HTTP message**
   * **Recipients:** From the drop-down menu, select message recipients based on member role and scope
   * **Title:** Enter a title for your message
   * **Text:** Enter the text of your message
6. Click **Send**
