---
description: An overview about response templates.
---

# Response Templates

## Overview

Response templates are used to override the default values sent in response to consumer calls to an API. They can be implemented for all v4 API HTTP entrypoints:

* HTTP GET
* HTTP POST
* HTTP proxy
* SSE
* Webhook
* WebSocket

{% hint style="info" %}
As of Gravitee 4.3, response templates cannot override message-level errors or be applied to TCP proxy entrypoints.
{% endhint %}

Response template overrides are triggered by error keys, which are specific to policies. Responses can be templatized if the errors raised during the request/response phase(s) are associated with a policy whose policy keys can be overridden. Each response template defines the new values to be returned for one or more status codes when the template is triggered.

## Configuration

### Prerequisites

Prior to defining a response template, verify:

* Which policies have been applied to the API. This can be viewed in the API's plan.
* Which error keys can be overridden per policy associated with your API.

Below are the policy error keys that you can override by configuring response templates:

<table><thead><tr><th width="417">Key</th><th>Policy</th></tr></thead><tbody><tr><td><code>API_KEY_MISSING</code></td><td>API key</td></tr><tr><td><code>API_KEY_INVALID</code></td><td>API key</td></tr><tr><td><code>QUOTA_TOO_MANY_REQUESTS</code></td><td>Rate limiting</td></tr><tr><td><code>RATE_LIMIT_TOO_MANY_REQUESTS</code></td><td>Rate limiting</td></tr><tr><td><code>REQUEST_CONTENT_LIMIT_TOO_LARGE</code></td><td>Request content limit</td></tr><tr><td><code>REQUEST_CONTENT_LIMIT_LENGTH_REQUIRED</code></td><td>Request content limit</td></tr><tr><td><code>REQUEST_TIMEOUT</code></td><td>Mock, Callout HTTP, Request validation</td></tr><tr><td><code>REQUEST_VALIDATION_INVALID</code></td><td>Request validation</td></tr><tr><td><code>RESOURCE_FILTERING_METHOD_NOT_ALLOWED</code></td><td>Resource filtering</td></tr><tr><td><code>RBAC_INVALID_USER_ROLES</code></td><td>Role-based access control</td></tr><tr><td><code>RESOURCE_FILTERING_FORBIDDEN</code></td><td>Resource filtering</td></tr><tr><td><code>RBAC_FORBIDDEN</code></td><td>Role-based access control</td></tr><tr><td><code>RBAC_NO_USER_ROLE</code></td><td>Role-based access control</td></tr><tr><td><code>OAUTH2_MISSING_SERVER</code></td><td>OAuth2</td></tr><tr><td><code>OAUTH2_MISSING_HEADER</code></td><td>OAuth2</td></tr><tr><td><code>OAUTH2_MISSING_ACCESS_TOKEN</code></td><td>OAuth2</td></tr><tr><td><code>OAUTH2_INVALID_ACCESS_TOKEN</code></td><td>OAuth2</td></tr><tr><td><code>OAUTH2_INSUFFICIENT_SCOPE</code></td><td>OAuth2</td></tr><tr><td><code>OAUTH2_INVALID_SERVER_RESPONSE</code></td><td>OAuth2</td></tr><tr><td><code>OAUTH2_SERVER_UNAVAILABLE</code></td><td>OAuth2</td></tr><tr><td><code>HTTP_SIGNATURE_INVALID_SIGNATURE</code></td><td>HTTP Signature</td></tr><tr><td><code>JWT_MISSING_TOKEN</code></td><td>JWT</td></tr><tr><td><code>JWT_INVALID_TOKEN</code></td><td>JWT</td></tr><tr><td><code>JSON_INVALID_PAYLOAD</code></td><td>JSON validation</td></tr><tr><td><code>JSON_INVALID_FORMAT</code></td><td>JSON validation</td></tr><tr><td><code>JSON_INVALID_RESPONSE_PAYLOAD</code></td><td>JSON validation</td></tr><tr><td><code>JSON_INVALID_RESPONSE_FORMAT</code></td><td>JSON validation</td></tr><tr><td><code>GATEWAY_INVALID_REQUEST</code></td><td>All</td></tr><tr><td><code>GATEWAY_INVALID_RESPONSE</code></td><td>All</td></tr><tr><td><code>GATEWAY_OAUTH2_ACCESS_DENIED</code></td><td>All</td></tr><tr><td><code>GATEWAY_OAUTH2_SERVER_ERROR</code></td><td>All</td></tr><tr><td><code>GATEWAY_OAUTH2_INVALID_CLIENT</code></td><td>All</td></tr><tr><td><code>GATEWAY_MISSING_SECURITY_PROVIDER</code></td><td>All</td></tr><tr><td><code>GATEWAY_PLAN_UNRESOLVABLE</code></td><td>All</td></tr><tr><td><code>GATEWAY_POLICY_INTERNAL_ERROR</code></td><td>All</td></tr></tbody></table>

### Create a response template

When creating response templates, you can define:

* Multiple templates for one API (for multiple policies and/or multiple error keys sent by the same policy)
* Multiple template definitions for the same error key in a single template (for different content types or status codes)

To configure a response template:

1. Log in to your APIM Management Console
2. Select **APIs** from the left nav
3. Select your API from the list
4. Select **Entrypoints** from the inner left nav
5. Click on the **Response Templates** header
6. Click on the **Add new Response Template** button
7.  Customize the **Create a new Response Template** form

    <figure><img src="../../.gitbook/assets/create response template.png" alt=""><figcaption><p>Configure a new response template</p></figcaption></figure>

    * **Template key:** Choose the template key via the **Template key** drop-down.
    * **Accept header to match:** Specify the requests header that should trigger use of the response template. The default value is `*/*`. To send the template override values only for JSON or XML requests, specify `JSON` or `XML.`
    * **Status code:** Specify the status code that to send to the API consumer via the **Status code** drop-down.
    * Specify the override values to send to the API consumer. These can either be:
      * One or more HTTP headers to include in the response
      * A response template body
8. Click **Create**
