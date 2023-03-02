# developer-subscribe

## Overview

APIM Portal exposes published APIs to developers so they can browse the APIs, request access, generate subscriptions to secure access and identify consumers for monitoring and analytics.

To access the APIs and start interacting with them, consumers must first subscribe to an link:\{{ _/apim/3.x/apim\_publisherguide\_plans\_subscriptions.html_ | relative\_url \}}\[API plan] with their registered application.

Consumers must have a link:\{{ _/apim/3.x/apim\_consumerguide\_create\_account.html_ | relative\_url \}}\[user account] to register an application and subscribe to an API.

### Plan security type

Depending on the plan security type (API-Key, OAuth 2.0, JWT), you need to set proper HTTP headers to call the API (for more details, see [Create a plan](developer-subscribe.md#apim\_publisherguide\_plans\_subscriptions.adoc#create-a-plan)).

**API Key**

```
curl -X GET "https://api.company.com/amazing-api" -H "X-Gravitee-Api-Key: xxxx-xxxx-xxxx-xxxx"
```

**OAuth 2.0/JWT**

You need to get an access token from the authorization server before you can consume the API.

```
curl -X GET "https://api.company.com/amazing-api" -H "Authorization: Bearer xxxx-xxxx-xxxx-xxxx"
```

## Create an application

Consumers wanting to subscribe to APIs need to register an application first, so that API publishers can control and regulate access to their APIs. Applications can be web applications, native application, bash/job applications and other applications needing to access sensitive data.

For more information, see [Create your application with APIM Portal](developer-subscribe.md#apim\_quickstart\_consume\_ui.adoc#create-your-application-with-apim-portal).

## Subscribe to an API

1. Log in to APIM Portal.
2. Click **Catalog** in the top menu.
3.  Browse the API categories or search for an API using keywords.

    image::\{% link images/apim/3.x/api-consumer-guide/developer-subscribe/subscribe-search-an-api.png %\}\[]
4.  Select the API you want to subscribe to.

    image::\{% link images/apim/3.x/api-consumer-guide/developer-subscribe/subscribe-select-an-api.png %\}\[]
5.  Click **SUBSCRIBE** in the sub-menu and choose the API plan.

    image::\{% link images/apim/3.x/api-consumer-guide/developer-subscribe/subscribe-to-an-api.png %\}\[]
6.  Select your application.

    image::\{% link images/apim/3.x/api-consumer-guide/developer-subscribe/subscribe-select-an-application.png %\}\[]

    Remember, if you choose an OAuth 2.0 plan, the application must have a `client_id` set.
7. Click **NEXT**. You can check your information before validating the request.
8.  When you are ready, click **VALIDATE THE REQUEST**.

    image::\{% link images/apim/3.x/api-consumer-guide/developer-subscribe/subscribe-confirmation-before-validation.png %\}\[]

    If there are general conditions for the selected plan, you need to accept them before validating the subscription.

    image::\{% link images/apim/3.x/api-consumer-guide/developer-subscribe/subscribe-general-conditions-acceptance.png %\}\[]

    If validation is automatic, the following message is displayed:

    image::\{% link images/apim/3.x/api-consumer-guide/developer-subscribe/subscribe-validation.png %\}\[]

    If the API publisher chose to manually validate application subscriptions, you must await approval to use the API.

    image::\{% link images/apim/3.x/api-consumer-guide/developer-subscribe/subscribe-wait-for-validation.png %\}\[]

### Sharing key across API subscriptions

Since 3.17, an option can be activated to enable API consumers to subscribe to multiple APIs with the same API key.

Refer to link:\{{ _/apim/3.x/apim\_publisherguide\_plan\_security.html#use\_a\_shared\_api\_key_ \}}\[this section] to learn how to enable this feature.

This option is only offered during the second subscription to an API (via an API Key plan). If activated the second subscription will share the same key generated during subscription to the 1st API.

1. Go to the **API Catalog** and select an API (that can be subscribed through an API key plan).
2. Click **SUBSCRIBE**.
3.  Select a plan (with **Personal Key** as attribute).

    image::\{% link images/apim/3.x/api-consumer-guide/developer-subscribe/subscribe-shared-key-choose-plan.png %\}\[]
4.  Select an Application (already subscribed once to an API through an API Key plan).

    image::\{% link images/apim/3.x/api-consumer-guide/developer-subscribe/subscribe-shared-key-select-app.png %\}\[]
5.  You are now prompted to select the API key mode you want to use.

    image::\{% link images/apim/3.x/api-consumer-guide/developer-subscribe/subscribe-shared-key-confirm-key-mode.png %\}\[]
6.  Select **Shared API Key** and click **NEXT**.

    image::\{% link images/apim/3.x/api-consumer-guide/developer-subscribe/subscribe-shared-key-validate-subscription-request.png %\}\[]
7. Click **VALIDATE THE REQUEST**.

Once the API key mode is chosen for an application, it cannot be changed. All subsequent subscriptions to APIs will be reusing the same key shared across all subscriptions.

## Manage subscriptions

To view your subscriptions and their current status:

1. Go to the **Applications** page.
2. Choose an application. In the **Subscriptions** section you will see all your subscriptions with their status (for example, **Accepted** or **Pending**).
3.  Click on a specific subscription to see the details.

    image::\{% link images/apim/3.x/api-consumer-guide/developer-subscribe/subscribe-manage-subscriptions.png %\}\[]

    For API-Key plans, you can retrieve the API-Key value and also renew or revoke subscriptions.

### Manage subscriptions with Shared key

When an application uses a Shared API key, all subscripitions sharing the API Key are identifiable by a **SHARED** tag:

image::\{% link images/apim/3.x/api-consumer-guide/developer-subscribe/subscribe-shared-key-subscription-list.png %\}\[]

## Analytics

For each API you are subscribed to, APIM provides some analytics to show API usage in your application. For a list of the analytics available, see [Analytics](developer-subscribe.md#apim\_consumerguide\_manage\_applications.adoc#analytics).
