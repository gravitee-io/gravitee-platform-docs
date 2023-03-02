# Overview

The following sections describe how you can promote an API from one
environment to another.

For a quick introduction on how to create an API in APIM, see link:{{
*/apim/3.x/apim\_publisherguide\_create\_apis.html* | relative\_url
}}\[Create an API^\].

This feature is available starting in version APIM 3.10.0 and requires
that your installation is linked to Cockpit. For more information about
Cockpit, see link:{{ */cockpit/3.x/cockpit\_overview\_introduction.html*
| relative\_url }}\[Cockpit\].

**APIs can only be promoted to environments belonging to the same
organization.**

# Context

-   Two installations

    -   One linked to Demo and Production environments.

    -   Another one linked to Dev and QA environments.

    -   An API to promote.

        image::{% link
        images/apim/3.x/api-publisher-guide/promote-apis/graviteeio-promote-api-cockpit-graph.png
        %}\[Map of installations in Cockpit\]

# Request Promotion For An API

Here, we will see how to promote our API from environment `DEV` to
environment `QA`.

To request a promotion, you only need to have **API-DEFINITION** link:{{
*/apim/3.x/apim\_adminguide\_roles\_and\_permissions.html* |
relative\_url }}\[permissions^\].

Promotion requests are logged in link:{{
*/apim/3.x/apim\_publisherguide\_audit.html* | relative\_url }}\[Audits
trail^\].

The following actions must be done with an API Publisher on `DEV`
environment.

1.  Go to the API to promote and click the image:{% link
    images/icons/promote-button.png %}\[role="icon"\] button.

    image::{% link
    images/apim/3.x/api-publisher-guide/promote-apis/graviteeio-promote-api-promote-1.png
    %}\[Promote button\]

2.  A window listing the available environments for the API promotion
    will pop up

    image::{% link
    images/apim/3.x/api-publisher-guide/promote-apis/graviteeio-promote-api-promote-2.png
    %}\[Target environments list\]

    If a promotion request already exists for your API on an
    environment, you cannot do another request until the previous one is
    rejected or accepted.

    image::{% link
    images/apim/3.x/api-publisher-guide/promote-apis/graviteeio-promote-api-promote-2-bis.png
    %}\[Target environments list\]

3.  Choose the environment you want to promote the API on, then click on
    **PROMOTE** button

When promoting an API, **members** and **groups** information are lost.

If a promotion has already been accepted for an API, you can request a
new one on the same target environment. Once this promotion is accepted,
the API on the target environment will be updated.

# Accepting Or Rejecting A Promotion

To be able to accept or reject a promotion, you need to have
**ENVIRONMENT-API** link:{{
*/apim/3.x/apim\_adminguide\_roles\_and\_permissions.html* |
relative\_url }}\[permissions^\].

As a user of `QA` environment, promotion requests are visible in the
**Tasks** section.

1.  Go to the **Tasks** section.

    image::{% link
    images/apim/3.x/api-publisher-guide/promote-apis/graviteeio-promote-api-promote-3.png
    %}\[Promotion tasks\]

2.  You can choose to accept or reject the promotion.

    -   Rejecting the promotion will Remove the task.

    -   Accepting the promotion will:

        -   Create or update the API (depending on if it has already
            been promoted or not).

        -   Remove the task.
