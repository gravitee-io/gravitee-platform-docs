# Overview

You can configure some more advanced features to restrict plans.

image::{% link
images/apim/3.x/api-publisher-guide/plans-subscriptions/add-plan-restrictions.png
%}\[\]

# Configure restrictions

You configure restrictions on the **Restrictions** page of a new or
existing plan.

1.  To edit an existing plan:

    1.  In APIM Console, select your API.

    2.  Click **Portal &gt; Plans**.

    3.  Click the edit icon image::{% link images/icons/edit-icon.png
        %}\[role="icon"\]

2.  On the **Restrictions** page, configure the restrictions for the
    plan, as described in the sections below.

3.  Click **SAVE** to save your plan.

    For some APIs created in earlier versions of APIM, you can click
    **NEXT** to configure plan policies.

    APIM adds the plan to the list of **Staging** plans.

image::{% link
images/apim/3.x/api-publisher-guide/plans-subscriptions/staging-plan.png
%}\[\]

You can now: \* link:{{
*/apim/3.x/apim\_publisherguide\_plan\_policies.html* | relative\_url
}}\[Configure flows and policies for your plan\]. \* link:{{
*/apim/3.x/apim\_publisherguide\_plan\_publish.html* | relative\_url
}}\[Publish your plan\]

## Limit request traffic

Plans provide tools for maintaining and optimizing traffic management
and protecting the health of the API backend.

### Rate-limiting

You can rate limit how many HTTP requests an application can make in a
specified period of seconds or minutes.

In the following example, the plan enforces a limit of 1000 requests per
minute:

image::{% link
images/apim/3.x/api-publisher-guide/plans-subscriptions/create-plan-rate-limit.png
%}\[\]

Rate-limiting helps you prevent sudden increases in the number of
requests at any point in time.

### Quotas

A quota specifies the number of requests allowed to call an API backend
during a specified time interval.

In the following example, the plan enforces a limit of 100000 requests
per day:

image::{% link
images/apim/3.x/api-publisher-guide/plans-subscriptions/create-plan-quota.png
%}\[\]

You can use quotas to enforce business or financial requirements to
limit the number of calls partner or third-party apps can make in a
period of time.

## Resource filtering

You can use resource filtering to limit access to a subset of API
resources.

In the following example, the plan only allows GET requests:

image::{% link
images/apim/3.x/api-publisher-guide/plans-subscriptions/create-plan-path-authorization.png
%}\[\]

You can use resource filtering to make an API read-only for public
members and give premium members access to more resources.
