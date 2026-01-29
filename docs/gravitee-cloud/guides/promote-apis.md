---
description: Overview of Promote APIs.
---

# Promote APIs

## Overview

The following sections describe how to promote an API from one environment to another. This feature requires that your installation is linked to Gravitee Cloud.

{% hint style="info" %}
For detailed information on API promotion, including supported features, limitations, and step-by-step instructions, see  [APIM API Promotion](https://documentation.gravitee.io/apim/create-and-configure-apis/create-apis/promote-apis)
{% endhint %}

## How to promote an API

### Context

To promote an API requires:

* Two installations:
  * One linked to demo and production environments
  * Another linked to Dev and QA environments
* An API to promote

![Map of installations in Cockpit](https://docs.gravitee.io/images/apim/3.x/api-publisher-guide/promote-apis/graviteeio-promote-api-cockpit-graph.png)

### Request promotion for an API

To request a promotion, you need to have API `DEFINITION` [permissions](https://documentation.gravitee.io/apim/configure-and-manage-the-platform/manage-organizations-and-environments/user-management#permissions). Promotion requests are logged in the [Audit trail](https://documentation.gravitee.io/apim/guides/api-measurement-tracking-and-analytics#the-audit-trail).

The following example shows how to promote an API from environment `DEV` to environment `QA`. These steps must be performed with an API Publisher on the `DEV` environment.

1. Go to the API you want to promote and click the **PROMOTE** button:

![Promote button](https://docs.gravitee.io/images/apim/3.x/api-publisher-guide/promote-apis/graviteeio-promote-api-promote-1.png)

2. A window listing the available environments for the API promotion will appear:

![Target environments list](https://docs.gravitee.io/images/apim/3.x/api-publisher-guide/promote-apis/graviteeio-promote-api-promote-2.png)

{% hint style="info" %}
If a promotion request for your API already exists on an environment, you cannot make another request on the same target environment until the promotion is either rejected or accepted.

<img src="https://docs.gravitee.io/images/apim/3.x/api-publisher-guide/promote-apis/graviteeio-promote-api-promote-2-bis.png" alt="Target environments list" data-size="original">
{% endhint %}

3. Choose the environment on which to promote the API, then click **PROMOTE**:

* When an API is promoted, **members** and **groups** information is lost
* Once the promotion is accepted, the API on the target environment will be updated

### Accept or reject a promotion

To accept or reject a promotion, you need to have environment `API` [permissions](https://documentation.gravitee.io/apim/configure-and-manage-the-platform/manage-organizations-and-environments/user-management#permissions).

To continue with our example, a user of the `QA` environment will see the promotion request in the **Tasks** section. Follow the steps below to accept or reject the promotion.

1. Go to the **Tasks** section.

![Promotion tasks](https://docs.gravitee.io/images/apim/3.x/api-publisher-guide/promote-apis/graviteeio-promote-api-promote-3.png)

2. Accept or reject the promotion:

* Rejecting the promotion will remove the task
* Accepting the promotion will:
  * Create or update the API (depending on if it has already been promoted)
  * Remove the task

{% hint style="info" %}
For a quick introduction on how to create an API in APIM, see [Create APIs](https://documentation.gravitee.io/apim/create-and-configure-apis/create-apis).
{% endhint %}
