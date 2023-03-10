---
description: >-
  This page details all the core concepts around API exposure for both consumers
  and producers
---

# Concepts

API exposure revolves around three core components: plans, applications, and subscriptions. Once an API is started and published, it will be visible in the developer portal, but can not be consumed until a plan is published. A plan with no authentication can be consumed immediately. However, adding any form of authentication requires the API consumer to register an application and subscribe to one of the published plans for that API. This allows the API producer to closely monitor and control access to their APIs at a much more granular level.&#x20;

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

#### Create a plan

You can create plans in the management UI as part of the [API creation process](../../user-guide/publisher/create-api.md#create-an-api-from-scratch). You can also create them later with the **Portal > Plans** function.&#x20;

{% tabs %}
{% tab title="Interactive UI exploration" %}
{% @arcade/embed flowId="L3b4AWtxtYkNE89ZiR2Y" url="https://app.arcade.software/share/L3b4AWtxtYkNE89ZiR2Y" %}
{% endtab %}

{% tab title="Text descriptions" %}
Creating a plan is broken down into three main stages:

* **General:** enter basic details about your plan. The only requirement for this stage is proving a name for your plan.
  * The initial section lets you set a name, description, and characteristics for your plan. Characteristics are optional labels you can use to tag your plan. &#x20;
  * **Conditions:** select a page containing the general conditions for use of your plan. You can learn more about creating general condition pages here.
  * **Subscriptions:** modify basic settings around a subscription for plans requiring authentication&#x20;
    * **Auto validate subscription:** accepts any and all subscriptions to a plan without the API publisher's review. These subscriptions can still be revoked at any time
    * The API publisher can require all subscription requests from API consumers to include a comment detailing their request. Additionally, with this option enabled, the API publisher can leave a default message explaining what is expected in the API consumer's comment
  * **Deployment:** the plan can be selectively deployed to particular APIs using sharding tags which you can learn more about [here](../../getting-started/configuration/configure-sharding-tags-for-your-gravitee-api-gateways.md).
  * **Access-Control:** exclude certain groups from accessing this plan. You can learn more about user management and how to configure groups here.
* **Security**
* **Restrictions**
{% endtab %}
{% endtabs %}



#### Configure policies on a plan

#### Publish a plan



### Applications

To consume your APIs, developers must create an [application](https://docs.gravitee.io/apim/3.x/apim\_overview\_concepts.html#gravitee-concepts-application) linked to one of the API plans (unless the plan is keyless, as described above). They can then subscribe to the API. APIM uses the subscription to decide whether to accept or deny an incoming request.

Learn more about applications and subscriptions in the [API Consumer Guide](https://docs.gravitee.io/apim/3.x/apim\_consumerguide\_portal.html).





### Subscriptions



