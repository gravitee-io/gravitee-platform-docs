---
description: Secure, transform, restrict, and monitor your APIs
---

# Policy Reference

### Overview

Gravitee API Management (APIM) encompasses API design, API security and access management, API reliability, API delivery, and API productization. At the core of this sphere of responsibility sits the API Gateway which is a reverse proxy that sits in front of your APIs and helps route requests to the appropriate backend service while also performing various tasks such as rate limiting, authentication, and transformation of requests and responses. Typically, the primary method of enforcing security, reliability, and the proper movement of data is **policies**.

Policies are rules or logic that can be executed by the API gateway during the request or the response of an API call. APIM is delivered with some default _Gravitee-maintained_ policies to control how an API is consumed. You can also customize APIM by adding your own or _community-maintained_ policies through plugins. Plugins are components that additional functionality by _plugging into_ the Gravitee ecosystem. Policies are simply a type of plugin. You can learn more about how to implement custom policies in our plugins guide.

Policies can be used for a variety of reasons and objectives, ranging from making APIs more secure to making them reliable to making them profit drivers in the case of API Monetization. Here are the major categories of policies:

* **Security:** enforce authentication methods to verify an API consumer before proxying their request to your backend APIs
  * For example, you could use an API key authentication policy to limit API consumption to a set of client applications that are able to pass a specific, unique API key with each request.
* **Transformation:** strip, shape, or otherwise alter network traffic so as to make consumption of APIs and the movement of data more secure, reliable, performant, or efficient
  * For example, you could use an assign content policy to strip sensitive information as data is brokered by the gateway and sent to specific client applications.
* **Restrictions:** limit and/or throttle the number of requests over a set time period
  * For example, you could use a rate-limiting policy to limit your API to a maximum of 100 calls/min/consumer
* **Performance:** cache responses from backend APIs to eliminate the need for subsequent calls to the backend
  * For example, you could use a cache policy to cache the response of a particular backend API for one hour or until the user manually bypasses the cache.
* **Routing**: dispatch inbound calls to different targets/endpoints or rewrite URIs
  * For example, you could use a dynamic routing policy to redirect requests from `http://gateway/apis/store/12/info` to `http://backend_store12/info`
* **Monitoring, Validation, & Testing**
  * For example,

<table data-view="cards"><thead><tr><th></th><th></th><th></th><th data-hidden data-type="content-ref"></th><th data-hidden data-card-target data-type="content-ref"></th></tr></thead><tbody><tr><td><strong>Full Policy Reference</strong></td><td>All policies listed in alphabetical order</td><td></td><td></td><td><a href="full-policy-reference.md">full-policy-reference.md</a></td></tr><tr><td><strong>Gravitee Policies</strong></td><td>Learn more about the current Gravitee-maintained policies</td><td></td><td><a href="gravitee-policies/">gravitee-policies</a></td><td><a href="gravitee-policies/">gravitee-policies</a></td></tr><tr><td><strong>Community Policies</strong></td><td>Learn more about community policies and see the current list</td><td></td><td><a href="community-policies.md">community-policies.md</a></td><td><a href="community-policies.md">community-policies.md</a></td></tr></tbody></table>

### See also

#### Ant notation

APIM frequently uses Ant notation for path matching:

* `?` matches one character
* `\*` matches zero or more characters
* `**` matches zero or more directories in a path

#### Related learning

For details of how policies are defined and used in APIM, see also:

* Plans and subscriptions in the API Publisher Guide to learn how to configure policies for API plans in APIM Console
* Expression Language in the API Publisher Guide to learn more about using the Gravitee Expression Language with policies
* Policies in the Developer Guide to learn how to create custom policies
* Pluginsin the Developer Guide to learn how to deploy plugins (of which policies are one type)
* Platform policies in the Admin Guide to learn how to use policies at the organization level
