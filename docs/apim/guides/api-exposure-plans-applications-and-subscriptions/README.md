---
description: Overview of core concepts around API exposure for both consumers and producers
---

# API Exposure: Plans, Applications, & Subscriptions

### Introduction

API exposure in Gravitee API Management (APIM) revolves around three pillars: plans, applications, and subscriptions. Once a gateway API is started, deployed, and published, it will be visible in the developer portal, but can not be consumed until a plan is published. A plan with the keyless authentication type can be consumed immediately. However, all other types of authentication require the API consumer to register an application and subscribe to one of the published plans for that gateway API. This allows the API producer to closely monitor and control access to their APIs at a much more granular level.&#x20;

### Plans

There are many possible types of API access scenarios, which can be difficult to encode into your APIs. Different types of access scenarios often require external tools and modifying your backend APIs. In APIM, however, gateway APIs are deployed with plans which allow the API producer to quickly iterate on, and extend the functionality of, their backend APIs.

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



<figure><img src="../../../images/apim/3.x/api-publisher-guide/plans-subscriptions/plan-diagram.png" alt=""><figcaption><p>High-level plan diagram</p></figcaption></figure>

### Applications

To access your APIs, developers must create an [application](https://docs.gravitee.io/apim/3.x/apim\_overview\_concepts.html#gravitee-concepts-application) linked to one of the API plans (unless the plan is keyless, as described above). They can then subscribe to the API. APIM uses the subscription to decide whether to accept or deny an incoming request.

Learn more about applications and subscriptions in the [API Consumer Guide](https://docs.gravitee.io/apim/3.x/apim\_consumerguide\_portal.html).





### Subscriptions
