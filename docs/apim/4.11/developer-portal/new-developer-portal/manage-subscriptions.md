---
description: Subscribe to APIs and manage your subscriptions in the New Developer Portal 4.11. Follow the steps unless the API is keyless.
---

# Manage Subscriptions

### Overview <a href="#overview" id="overview"></a>

You can subscribe to APIs and manage your subscriptions with the New Developer Portal. Unless the API has a keyless plan, a consumer must create an application and subscribe to a published API plan to access an API. Applications act on behalf of the user.

### Prerequisites <a href="#prerequisites" id="prerequisites"></a>

* Enable the New Developer Portal. For more information about enabling the New Developer Portal, see [Enable the New Developer Portal](configure-the-new-portal.md).
* Create an application in the New Developer Portal. For more information about creating applications in the New Developer Portal, see [create-an-application.md](create-an-application.md "mention")

### Subscribe to an API <a href="#create-an-application" id="create-an-application"></a>

To subscribe to an API, complete the following steps:

1. Navigate to the Catalog.
2. Choose an API and navigate its documentation page

<figure><img src="../../.gitbook/assets/devportal-new-portal-manage-subscri-0.png" alt="The developer portal Catalog in cards view, showing five API cards with a top bar that includes example page and folder links."><figcaption></figcaption></figure>

2. Click Subscribe to navigate to the Subscription page

<figure><img src="../../.gitbook/assets/devportal-new-portal-manage-subscri-1.png" alt="An API documentation page in the developer portal, showing a placeholder page with overview, example, use case, and next steps sections beside an API navigation tree."><figcaption></figcaption></figure>

3. Select a Plan

<figure><img src="../../.gitbook/assets/devportal-new-portal-manage-subscri-2.png" alt="Step 1 of the developer portal subscription wizard, offering a default keyless plan, a JWT plan, and a standard API key plan, none selected."><figcaption></figcaption></figure>

4. Select an application

<figure><img src="../../.gitbook/assets/devportal-new-portal-manage-subscri-3.png" alt="Step 2 of the subscription wizard, showing default, my, and staging application cards, none selected."><figcaption></figcaption></figure>

5. Confirm the subscription

<figure><img src="../../.gitbook/assets/devportal-new-portal-manage-subscri-4.png" alt="Step 3 of the subscription wizard, summarising the subscription as under admin review with its API, application, and API key plan."><figcaption></figcaption></figure>

6. You will be redirected to the [#subscription-details](manage-subscriptions.md#subscription-details "mention")

<figure><img src="../../.gitbook/assets/devportal-new-portal-manage-subscri-6.png" alt="A pending subscription detail page in the developer portal, showing its API, application, timestamps, identifier, and plan above a notice that the request is being validated."><figcaption></figcaption></figure>

### View existing subscriptions

You can manage all existing subscriptions from the subscriptions dashboard.

1. Using the dropdown menu at the top right corner of the screen, navigate to the Subscriptions page

This page shows all subscriptions **across all APIs and Applications**. You can filter subscriptions by API, Application, and Subscription Status.

2. Click on a subscription in the subscription list, and you will be redirected to [#subscription-details](manage-subscriptions.md#subscription-details "mention")

<figure><img src="../../.gitbook/assets/devportal-new-portal-manage-subscri-7.png" alt="The Subscriptions page of the developer portal, listing three subscriptions with their API, plan, application, creation date, and status."><figcaption></figcaption></figure>

### Subscription details

This page allows you to manage an individual subscription.

* View subscription properties
* Navigate to the API Page
* Navigate to the Application page
* Close subscription

<figure><img src="../../.gitbook/assets/devportal-new-portal-manage-subscri-9.png" alt="An accepted subscription detail page, showing the active API key and a base URL with a matching curl command, above a Close subscription button."><figcaption></figcaption></figure>

#### Close subscription

To close a subscription, click on Close subscription button at the top right corner of the screen.

<figure><img src="../../.gitbook/assets/devportal-new-portal-manage-subscri-10.png" alt="The Close this subscription dialog, warning that access to the API will be lost."><figcaption></figcaption></figure>

Once closed, the subscription status is updated and access information is no longer visible.

<figure><img src="../../.gitbook/assets/devportal-new-portal-manage-subscri-11.png" alt="A closed subscription detail page, showing its API, application, timestamps, and plan above a notice reading &quot;Subscription closed&quot;."><figcaption></figcaption></figure>
