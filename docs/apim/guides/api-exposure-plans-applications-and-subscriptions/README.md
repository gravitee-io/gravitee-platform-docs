---
description: Overview of core concepts around API exposure for both consumers and producers
---

# API Exposure: Plans, Applications, & Subscriptions

### Introduction

API exposure in Gravitee API Management (APIM) revolves around three pillars: plans, applications, and subscriptions. Once a gateway API is started, deployed, and published, it will be visible in the developer portal, but can not be consumed until a plan is published. A plan with the keyless authentication type can be consumed immediately. However, all other types of authentication require the API consumer to register an application and subscribe to one of the published plans for that gateway API. This allows the API publisher to closely monitor and control access to their APIs at a much more granular level.&#x20;

### Plans

There are many possible types of API access scenarios, which can be difficult to encode into your APIs. Different types of access scenarios often require external tools and modifying your backend APIs. In APIM, however, gateway APIs are deployed with plans which allow the API publisher to quickly iterate on, and extend the functionality of, their backend APIs.

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

Similar to an API, a plan can also be published. Publishing is one of four stages of a plan: staging, published, deprecated, and closed.

* **Staging** - Generally, this is the first stage of a plan. View it as a draft mode. You can configure your plan but it won’t be accessible to users.
* **Published** - Once your plan is ready, you can publish it to let API consumers view and subscribe on the APIM Portal and consume the API through it. A published plan can still be edited.
* **Deprecated** - You can deprecate a plan so it won’t be available on the APIM portal and API Consumers won’t be able to subscribe to it. Existing subscriptions remain so it doesn’t impact your existing API consumers.
* **Closed** - Once a plan is closed, all associated subscriptions are closed too. This can not be undone. API consumers subscribed to this plan won’t be able to use your API.

<figure><img src="https://europe1.discourse-cdn.com/business20/uploads/graviteeforum/optimized/2X/6/6333ad2d86aae2ceb0cac422dd9015c75c3e6fb5_2_689x197.png" alt=""><figcaption><p>Four stages of a plan</p></figcaption></figure>

{% hint style="info" %}
**The Benefits of Deprecation**

Deprecating plans allow consumers of the API time to migrate without breaking their application while also ensuring new users do not subscribe to the deprecated plan.
{% endhint %}

### Applications

To access your APIs, consumers must register an application and subscribe to a published API plan (unless the plan is keyless, as described above). Typical applications are web applications, native applications, or bash/job applications that want to access data or functionality from backend APIs.

Applications are essential in allowing the API publishers to control and regulate access to their APIs by making them aware of all consumers of their API. If one consumer turns out to be a bad actor engaging in malicious activity, then API publishers require granular control to revoke access for that one consumer instead of shutting the API down for all consumers. Additionally, more advanced authentication methods like OAuth 2.0 require the client to provide information such as a client id when subscribing to an API.

Applications and plans go together like developers and repurposing code from stack overflow. Remember, plans are an access layer around APIs that provide the API publishers a method to secure, monitor, and transparently communicate details around access. An application allows an API consumer to register and agree to this plan. The result is a successful contract or _subscription_.

### Subscriptions

APIM uses the subscription to decide whether to accept or deny an incoming request. Subscriptions can be modified at any time by the API producer.
