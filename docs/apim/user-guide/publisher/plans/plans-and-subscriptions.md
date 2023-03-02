# plans-and-subscriptions

## Overview

Once an API is registered and made public, you can manage subscriptions to it through APIM plans. Managing subscriptions and plans is a key feature of APIM that publishers can use to provide and regulate access to APIs.

## What is a plan?

A plan provides a service and access layer on top of your APIs for consumer link:\{{ _/apim/3.x/apim\_overview\_concepts.html#gravitee-concepts-application_ | relative\_url \}}\[applications]. A plan specifies access limits, subscription validation modes and other configuration to tailor it to a specific application.

image::\{% link images/apim/3.x/api-publisher-guide/plans-subscriptions/plan-diagram.png %\}\[Gravitee.io - Plan diagram, 873, 530, align=center, title-align=center]

To get your consumers up and running with your APIs quickly, you can create a keyless plan with no security, bypassing the need for an application/subscription.

link:\{{ _/apim/3.x/apim\_publisherguide\_plan\_security.html#keyless\_plans_ | relative\_url \}}\[Learn more about keyless plans]

The concept of **API as a Product** is at the core of the APIM approach to API management. We’re not just in the business of providing tools for managing your APIs, we also understand that business and service are of paramount importance when consumers leverage your product lines.

There are many possible types of API access scenarios, which can be difficult to encode into your APIs. Different types of access scenarios very often require external tools. In APIM, however, you can manage access with plans.

These are just some of the access scenarios APIM manages with plans:

* Read-only access and limited request traffic, so potential customers can discover and try out your APIs.
* Premium access with public resources and access limits for your partners.
* Unlimited access to your internal enterprise applications.

To consume your APIs, developers must create an link:\{{ _/apim/3.x/apim\_overview\_concepts.html#gravitee-concepts-application_ | relative\_url \}}\[application] linked to one of the API plans (unless the plan is keyless, as described above). They can then subscribe to the API. APIM uses the subscription to decide whether to accept or deny an incoming request.

Learn more about applications and subscriptions in the link:\{{ _/apim/3.x/apim\_consumerguide\_portal.html_ | relative\_url \}}\[API Consumer Guide^].

## How to create a plan

You can create plans in APIM Console as part of the API creation process. You can also create them later with the **Portal > Plans** function. The workflow is as follows:

*   Step 1 - Create the basic plan definition.

    link:\{{ _/apim/3.x/apim\_publisherguide\_create\_plan.html_ | relative\_url \}}\[Learn more about creating plan definitions] \* Step 2 - Specify details of the plan security.

    link:\{{ _/apim/3.x/apim\_publisherguide\_plan\_security.html_ | relative\_url \}}\[Learn more about configuring plan security] \* Step 3 - (Optional) Specify details of plan restrictions.

    link:\{{ _/apim/3.x/apim\_publisherguide\_plan\_restrictions.html_ | relative\_url \}}\[Learn more about configuring plan restrictions] \* Step 4 - (Optional) Configure flows and policies.

    link:\{{ _/apim/3.x/apim\_publisherguide\_plan\_policies.html_ | relative\_url \}}\[Learn more about configuring plan policies] \* Step 5 - Publish the plan.

    link:\{{ _/apim/3.x/apim\_publisherguide\_plan\_publish.html_ | relative\_url \}}\[Learn more about publishing plans]
