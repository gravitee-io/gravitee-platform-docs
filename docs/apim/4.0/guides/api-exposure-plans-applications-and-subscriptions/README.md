---
description: Overview of core concepts around API exposure for both consumers and producers
---

# API Exposure: Plans, Applications, & Subscriptions

## Introduction

API exposure in Gravitee API Management (APIM) revolves around three pillars: plans, applications, and subscriptions. Once a Gateway API is started, deployed, and published, it will be visible in the Developer Portal, but can not be consumed until a plan is published. A plan with the keyless authentication type can be consumed immediately. However, all other types of authentication require the API consumer to register an application and subscribe to one of the published plans for that Gateway API. This allows the API publisher to closely monitor and control access to their APIs at a much more granular level.

## Plans

There are many possible types of API access scenarios, which can be difficult to encode into your APIs. Different types of access scenarios often require external tools and modifying your backend APIs. In APIM, however, Gateway APIs are deployed with plans which allow the API publisher to quickly iterate on, and extend the functionality of, their backend APIs.

A plan provides a service and access layer on top of your APIs for consumer applications. A plan specifies access limits, subscription validation modes, and other configurations to tailor it to a specific application.

The most important part of plan configuration is selecting the security type. APIM supports the following four security types:

* Keyless (public)
* API Key
* OAuth 2.0
* JWT
* Push

Exposing an API to a consumer requires at least one plan, but can support as many plans as needed. These are just some sample access scenarios APIM can manage with plans:

* Read-only access and limited request traffic, so potential customers can discover and try out your APIs.
* Premium access with public resources and access limits for your partners.
* Unlimited access to your internal enterprise applications.

<figure><img src="../../.gitbook/assets/plan-diagram (1).png" alt=""><figcaption><p>High-level plan diagram</p></figcaption></figure>

After creating a plan, it's initially in the first of the four stages of a plan: staging, published, deprecated, and closed.

* **Staging** - This is the first stage of a plan. View it as a draft mode. You can configure your plan but it won’t be accessible to users.
* **Published** - Once your plan is ready, you can publish it to let API consumers view and subscribe on the APIM Portal and consume the API through it. A published plan can still be edited.
* **Deprecated** - You can deprecate a plan so it won’t be available on the APIM portal and API Consumers won’t be able to subscribe to it. Existing subscriptions remain so it doesn’t impact your existing API consumers.
* **Closed** - Once a plan is closed, all associated subscriptions are closed too. This can not be undone. API consumers subscribed to this plan won’t be able to use your API.

<figure><img src="https://europe1.discourse-cdn.com/business20/uploads/graviteeforum/optimized/2X/6/6333ad2d86aae2ceb0cac422dd9015c75c3e6fb5_2_689x197.png" alt=""><figcaption><p>Four stages of a plan</p></figcaption></figure>

{% hint style="info" %}
**The Benefits of Deprecation**

Deprecating plans allow consumers of the API time to migrate without breaking their application while also ensuring new users do not subscribe to the deprecated plan.
{% endhint %}

## Applications

To access your APIs, consumers must register an application and subscribe to a published API plan (unless the plan is keyless, as described above). Typical applications are web applications, native applications, or bash/job applications that want to access data or functionality from backend APIs.

Applications are essential in allowing API publishers to control and regulate access to their APIs by providing visibility and granular control of all consumers of their APIs. If one consumer turns out to be a bad actor engaging in malicious activity, then API publishers strongly prefer to revoke access for that one consumer instead of shutting the API down for all consumers. Additionally, more advanced authentication methods like OAuth 2.0 require the client to provide information such as a client id when subscribing to an API.

Applications and plans go together like developers and repurposing code from stack overflow. Remember, plans are an access layer around APIs that provide the API publishers a method to secure, monitor, and transparently communicate details around access. An application allows an API consumer to register and agree to this plan. The result is a successful contract or _subscription_.

## Subscriptions

APIM uses the subscription to decide whether to accept or deny an incoming request. Subscriptions are created when an API consumer uses a registered application to create a subscription request to a published plan, and an API publisher either manually or automatically validates the subscription.

API producers can modify a subscription at any time which includes transferring to a different plan, pausing, setting an expiration date, or permanently closing a subscription. Additionally, authorization can be managed for individual subscriptions by, for example, setting an expiration date for, revoking, or renewing a subscribed application's API key.
