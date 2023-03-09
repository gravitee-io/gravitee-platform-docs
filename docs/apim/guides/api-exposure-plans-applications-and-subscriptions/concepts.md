---
description: >-
  This page details all the core concepts around API exposure for both consumers
  and producers
---

# Concepts

### Plans

There are many possible types of API access scenarios, which can be difficult to encode into your APIs. Different types of access scenarios often require external tools. In Gravitee API Management (APIM), however, you can manage access with plans.

A plan provides a service and access layer on top of your APIs for consumer applications. A plan specifies access limits, subscription validation modes, and other configurations to tailor it to a specific application.&#x20;

The most important part of plan configuration is selecting the security type. APIM supports the following four security types:

* Keyless (public)
* API Key
* OAuth 2.0
* JWT

Exposing an API to a consumer requires at least one plan, but can support as many plans as needed. These are just some sample access scenarios APIM can manage with plans:

* Read-only access and limited request traffic, so potential customers can discover and try out your APIs.
* Premium access with public resources and access limits for your partners.
* Unlimited access to your internal enterprise applications.

<figure><img src="../../.gitbook/assets/plan-diagram.png" alt=""><figcaption><p>Plan diagram</p></figcaption></figure>





{% tabs %}
{% tab title="Interactive UI exploration" %}
{% @arcade/embed flowId="MBQnmOgspMcSFS0Gcm8J" url="https://app.arcade.software/share/MBQnmOgspMcSFS0Gcm8J" %}
{% endtab %}

{% tab title="Text descriptions" %}
You can create plans in APIM Console as part of the API creation process. You can also create them later with the **Portal > Plans** function. The workflow is as follows:

*   Step 1 - Create the basic plan definition.

    [Learn more about creating plan definitions](https://docs.gravitee.io/apim/3.x/apim\_publisherguide\_create\_plan.html)
*   Step 2 - Specify details of the plan security.

    [Learn more about configuring plan security](https://docs.gravitee.io/apim/3.x/apim\_publisherguide\_plan\_security.html)
*   Step 3 - (Optional) Specify details of plan restrictions.

    [Learn more about configuring plan restrictions](https://docs.gravitee.io/apim/3.x/apim\_publisherguide\_plan\_restrictions.html)
*   Step 4 - (Optional) Configure flows and policies.

    [Learn more about configuring plan policies](https://docs.gravitee.io/apim/3.x/apim\_publisherguide\_plan\_policies.html)
*   Step 5 - Publish the plan.

    [Learn more about publishing plans](https://docs.gravitee.io/apim/3.x/apim\_publisherguide\_plan\_publish.html)

\

{% endtab %}
{% endtabs %}

### Applications

To consume your APIs, developers must create an [application](https://docs.gravitee.io/apim/3.x/apim\_overview\_concepts.html#gravitee-concepts-application) linked to one of the API plans (unless the plan is keyless, as described above). They can then subscribe to the API. APIM uses the subscription to decide whether to accept or deny an incoming request.

Learn more about applications and subscriptions in the [API Consumer Guide](https://docs.gravitee.io/apim/3.x/apim\_consumerguide\_portal.html).





### Subscriptions



