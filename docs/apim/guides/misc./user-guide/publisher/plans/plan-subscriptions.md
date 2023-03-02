# Overview

Consumers use plans to request subscriptions and access your APIs. They
subscribe to plans in APIM Portal:

image::{% link
images/apim/3.x/api-publisher-guide/plans-subscriptions/plans-subscriptions.png
%}\[\]

The following sections describe how to manage subscription requests from
consumers.

## Approve a subscription

When publishers create new plans, they can specify auto validation of
subscriptions, so consumers are ready to access the API as soon as they
subscribe to the plan. If you set manual approval on a plan, however,
you must approve subscriptions by following these steps.

You can enable mail or portal notifications so you can be notified when
a subscription validation task requires your attention.

1.  Go to your API in APIM Management and click **Portal &gt;
    Subscriptions**.

2.  Select the **Pending** subscription.

3.  Click **ACCEPT**, then enter the start and end dates (no end date
    means forever) of subscription approval.

    image::{% link
    images/apim/3.x/api-publisher-guide/plans-subscriptions/approve-subscription.png
    %}\[\]

## Revoke a subscription

You can revoke a subscription to remove access to APIs.

1.  Go to your API in APIM Management and click **Portal &gt;
    Subscriptions**.

2.  Select the subscription you want to revoke and click **CLOSE**.

    image::{% link
    images/apim/3.x/api-publisher-guide/plans-subscriptions/revoke-subscription.png
    %}\[\]
