---
description: An overview about plans and policies overview.
---

# Plans and Policies overview

## Overview

The next two core Gravitee API Management (APIM) concepts we will focus on are plans and policies:

* **Plan:** Provides a service and access layer on top of your API that specifies access limits, subscription validation modes, and other configurations to tailor your API to a specific subset of API consumers. An API consumer always accesses an API by subscribing to one of the available plans.
* **Policies:** Customizable rules or logic the Gateway executes during an API transaction. Policies generally fall into the categories of security, transformation, restrictions, performance, routing, or monitoring & testing.

Plans and policies are managed by the API publisher to add different layers of security and functionality to the backend resources they own.

<img src="../../../../../../../.gitbook/assets/file.excalidraw (5) (1).svg" alt="Gateway plans and policies" class="gitbook-drawing">

### Plans

There are many possible API access scenarios, any of which can be difficult to encode into your backend services. Plans are a powerful way to decouple the business logic from the access control of your backend services.

In APIM, all APIs require at least one plan before they can be deployed on the Gateway. The most important part of plan configuration is selecting the security type. APIM supports the following five security types:

* Keyless (public)
* Push
* API Key
* OAuth 2.0
* JWT

APIM intelligently routes API consumers to plans [based on specific criteria](../../../managing-your-apis/preparing-apis-for-subscribers/plans/#plan-selection) in the API request. APIM then uses an application-based subscription model to decide whether to accept or deny an incoming API request.

<details>

<summary>Applications and subscriptions</summary>

Plans are an access layer around APIs. An _application_ allows an API consumer to register and agree to this plan. If the registration is approved by the API publisher, the result is a successful contract, or _subscription_.

To access your APIs, consumers must register an application and submit a subscription request to a published API plan. Applications act on behalf of the user to request tokens, provide user identity information, and retrieve protected resources from remote services and APIs.

API publishers can modify a subscription at any time, which includes transferring API consumers to a different plan, pausing the subscription, setting an expiration date, or permanently closing a subscription.

**Keyless plan subscriptions**

Because keyless plans do not require authorization, APIs with keyless plans do not require the API consumer to create an application or submit a subscription request. Deployed APIs with a keyless plan will be publicly available on the Gateway's network.

</details>

### Policies

A policy modifies the behavior of the request or response handled by APIM Gateway. Policies can be considered a proxy controller, guaranteeing that a given business rule is fulfilled during request/response processing.

The request and response of an API transaction are broken up into _phases_. Policies can be applied to these phases in policy chains of arbitrary length.

<details>

<summary>Phases</summary>

Gateway APIs have the following phases:

* **Request:** For both traditional and message proxy APIs, this phase is executed before invoking the backend service. Policies can act on the headers and content of traditional proxy APIs.
* **Publish:** This phase occurs after the request phase and allows policies to act on each incoming message before it is sent to the backend service. This phase only applies to message proxy APIs.
* **Response:** For both traditional proxy and message proxy APIs, this phase is executed after invoking the backend service. Policies can act on the headers and content of traditional proxy APIs.
* **Subscribe:** This phase is executed after the response phase and allows policies to act on each outgoing message before it is sent to the client application. This phase only applies to message proxy APIs.

</details>

Policies are scoped to different API consumers through _flows_. Flows are a method to control where, and under what conditions, a group of policies act on an API transaction.

### Example

Let's say you have a backend API server architected around flight data. This data is not sensitive and you want to allow anyone to easily access it. However, because the data is supplied by verified airlines, you want to limit data modifications to specific API consumers who are explicitly granted permission.

This is easily achieved with APIM and does not require any changes to the backend API server.

First, you could create two plans in APIM: A keyless plan and a JWT plan. The keyless plan does not require API consumers to create an application or submit a subscription request and allows API consumers on the Gateway's network to immediately begin sending requests through the available entrypoints.

However, you would also configure the keyless plan with a flow containing a resource filtering policy applied to the request phase. This policy would be configured to grant read access only to the backend API. All other types of API requests (e.g., POST, PUT, DELETE, etc.) would be denied.

The flow with the resource filtering policy does not apply to the JWT plan and API consumers subscribed to it could modify data associated with their airline. However, to be granted access to the JWT plan, users need to first create an application and submit a subscription request that must be approved by you, the API publisher.
