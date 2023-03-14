---
description: Core concepts around API exposure for both consumers and producers
---

# API Exposure: Plans, Applications, & Subscriptions

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



<figure><img src="../../../images/apim/3.x/api-publisher-guide/plans-subscriptions/plan-diagram.png" alt=""><figcaption><p>Plan diagram</p></figcaption></figure>

### Applications

To consume your APIs, developers must create an [application](https://docs.gravitee.io/apim/3.x/apim\_overview\_concepts.html#gravitee-concepts-application) linked to one of the API plans (unless the plan is keyless, as described above). They can then subscribe to the API. APIM uses the subscription to decide whether to accept or deny an incoming request.

Learn more about applications and subscriptions in the [API Consumer Guide](https://docs.gravitee.io/apim/3.x/apim\_consumerguide\_portal.html).





### Subscriptions
