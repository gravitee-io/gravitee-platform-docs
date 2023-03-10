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
* **Secure:** choose one of four authentication types to secure your API. You can learn more about configuring each of these authentication types here.
  * **Keyless:** allows public access to the API and bypasses any security mechanisms on the whole request process
  * **API key:** allows only apps with approved API keys to access your API. This plan type ensures that API keys are valid, are not revoked or expired, and are approved to consume the specific resources associated with your API.
  * **JSON web token (JWT):** open method for representing claims securely between two parties. JWT are digitally-signed using HMAC shared keys or RSA public/private key pairs. JWT plans allow you to verify the signature of the JWT and check if the JWT is still valid according to its expiry date.
  * **Oauth 2.0:** open standard that apps can use to provide client applications with secure delegated access. OAuth works over HTTPS and authorizes devices, APIs, servers, and applications with access tokens rather than credentials.
* **Restrictions:** policies to regulate access to your APIs. Like any policy, restrictions can also be applied to a plan through the design studio. You can learn more about configuring these particular policies here.
  * **Rate Limiting:** limit how many HTTP requests an application can make in a specified period of seconds or minutes. This policy is meant to help avoid unmanageable spikes in traffic.
  * **Quota:** specifies the number of requests allowed to call an API backend during a specified time interval. The policy is generally used to tier access to APIs based on subscription level.
  * **Resource Filtering:** limit access to a subset of API resources
{% endtab %}
{% endtabs %}

#### Publish a plan

{% tabs %}
{% tab title="Interactive UI exploration" %}
{% @arcade/embed flowId="vOBfQE9VInuyA1g7b4kF" url="https://app.arcade.software/share/vOBfQE9VInuyA1g7b4kF" %}
{% endtab %}

{% tab title="Text descriptions" %}
Similar to an API, a plan can also be published. Publishing is one of four stages of a plan: staging, published, deprecated, and closed.

* **Staging** - Generally, this is the first state of a plan. View it as a draft mode. You can configure your plan but it won’t be accessible to users.
* **Published** - Once your plan is ready, you can publish it to let API consumers view and subscribe on the APIM Portal and consume the API through it. A published plan can still be edited.
* **Deprecated** - You can deprecate a plan so it won’t be available on the APIM portal and API Consumers won’t be able to subscribe to it. Existing subscriptions remains so it doesn’t impact your existing API consumers.
* **Closed** - Once a plan is closed, all associated subscriptions are closed too. This can not be undone. API consumers subscribed to this plan won’t be able to use your API.

<figure><img src="https://europe1.discourse-cdn.com/business20/uploads/graviteeforum/optimized/2X/6/6333ad2d86aae2ceb0cac422dd9015c75c3e6fb5_2_689x197.png" alt=""><figcaption><p>Four stages of a plan</p></figcaption></figure>
{% endtab %}
{% endtabs %}

####

### Applications

To consume your APIs, developers must create an [application](https://docs.gravitee.io/apim/3.x/apim\_overview\_concepts.html#gravitee-concepts-application) linked to one of the API plans (unless the plan is keyless, as described above). They can then subscribe to the API. APIM uses the subscription to decide whether to accept or deny an incoming request.

Learn more about applications and subscriptions in the [API Consumer Guide](https://docs.gravitee.io/apim/3.x/apim\_consumerguide\_portal.html).





### Subscriptions



