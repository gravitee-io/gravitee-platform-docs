---
description: WORK IN PROGRESS
---

# Gravitee API Definitions and Execution Engines

## Overview

A Gravitee API definition is a specification for your Gravitee API Management (APIM) Gateway. A Gravitee API definition is very similar to an API specification (OpenAPI, AsynAPI, etc.) except it is a specification _for your Gravitee Gateway._ It’s a JSON representation of everything that the APIM Gateway needs to know for it to proxy, apply policies to, create plans for, etc., your APIs and their traffic.

To execute your Gateway APIs and policy flows, the Gateway needs a runtime environment or engine. This is generally referred to as the execution engine.

Since APIM 4.0, there is support for both the v2 and v4 Gravitee API definitions through the legacy and reactive Gateway execution engines. You can think of these in pairs: v2 API definitions run on the legacy execution engine and v4 API definitions run on the reactive execution engine.

This guide is a deep dive into the difference between the two engines. In short, the reactive execution engine enables an improved execution flow for synchronous APIs and supports event-driven policy execution for asynchronous APIs. This adds features such as native support for Pub/Sub (Publish-Subscribe) design and enabling policies at the message level.

{% hint style="warning" %}
You can also run v2 Gateway APIs in **compatibility mode** which emulates some of the execution flow improvements of the reactive execution engine. This is detailed in the [v2 Gateway API compatibility mode](gravitee-api-definitions-and-execution-engines.md#v2-gateway-api-compatibility-mode) section below.
{% endhint %}

APIM fully supports both API definitions and execution engines. The [v2 API Creation Wizard ](create-apis/how-to/v2-api-creation-wizard.md)creates v2 Gateway APIs compatible with the legacy execution engine that can be augmented with flows designed in the [v2 Policy Studio](policy-design/v2-api-policy-design-studio.md). The [v4 API Creation Wizard](create-apis/how-to/v4-api-creation-wizard.md) creates v4 APIs compatible with the reactive execution engine that can be augmented with flows designed in the [v4 Policy Studio](policy-design/v4-api-policy-design-studio.md).

To summarize, here is a table outlining the key differences in day-to-day usage:

| Placeholder |   |   |
| ----------- | - | - |
|             |   |   |
|             |   |   |
|             |   |   |

### Key improvements

The reactive execution engine enables an improved execution flow for synchronous APIs and supports event-driven policy execution for asynchronous APIs. It is based on a modern and fully reactive architecture designed to address a number of challenges Gravitee users have been facing with the existing, legacy execution engine, available with the Gravitee’s v2 API definition.

The new reactive engine provides the following capabilities:

* The ability to execute policies in the exact order in which they have been placed in the Policy Studio. This addresses some issues experienced by users related to the order in which policies are executed by the legacy engine where policies interacting with the Head part of the request are always executed first, even when placed in a different order in the Policy Studio during the design phase. With the new reactive execution engine, it is possible to apply logic on a head policy based on the payload of the request - for example, to apply dynamic routing based on the request payload.

{% hint style="warning" %}
v2 Gateway APIs have this capability when [compatibility mode](gravitee-api-definitions-and-execution-engines.md#v2-gateway-api-compatibility-mode) is enabled.
{% endhint %}

* Proper isolation between platform-level policies and API-level policies during policy execution. This ensures that platform-level policies are always executed prior to any API-level policies during the request stage and after any API-level policies during the response stage.

{% hint style="warning" %}
v2 Gateway APIs have this capability when [compatibility mode](gravitee-api-definitions-and-execution-engines.md#v2-gateway-api-compatibility-mode) is enabled.
{% endhint %}

* Removal of the need to define a scope for policies (`onRequest`, `onRequestContent`, `onResponse`, `onResponseContent`).

{% hint style="warning" %}
v2 Gateway APIs have this capability when [compatibility mode](gravitee-api-definitions-and-execution-engines.md#v2-gateway-api-compatibility-mode) is enabled.
{% endhint %}

* Support for message-based, asynchronous APIs such as Kafka, MQTT, WebSocket, SSE, and Webhook.

In this section, you can learn about all the differences between the new reactive execution engine and the existing legacy execution engine. Additionally, guidance is provided on managing changes in system behavior when switching to the reactive policy execution engine or enabling compatibility mode with a v2 API. The information is grouped by functional area in the sub-sections below.

### Policy support

With the legacy execution engine, all existing supported policies will continue to work as before without a change.

Over time, all policies will be migrated to support the new reactive execution engine. Each policy in the [Policy Reference](../reference/policy-reference/) guide will include a compatibility table.

### v2 Gateway API compatibility mode

Need dev input

## Policy execution phases and execution order

With the legacy execution engine, different execution scopes are required in order to indicate at which level a policy will work, as follows:

* `REQUEST`: The policy only works on request headers. It never accesses the request body.
* `REQUEST_CONTENT`: The policy works at request content level and can access the request body.
* `RESPONSE`: The policy only works on response headers. It never accesses the response body.
* `RESPONSE_CONTENT`: The policy works at response content level and can access the response body.

As a result, all policies working on the body content are postponed to be executed after the policies working on headers. This leads to an execution order that is often different than the one originally designed, as shown in the following diagram:

<figure><img src="https://docs.gravitee.io/images/apim/3.x/event-native/event-native-api-management-execution-scopes-1.png" alt=""><figcaption><p>Legacy engine execution order</p></figcaption></figure>

### Reactive execution engine improvements

With the reactive execution engine, the `REQUEST_CONTENT` and `RESPONSE_CONTENT` phases are no longer considered - all policies are executed in the exact order of design, regardless of whether they work on the content or not. This is shown in the following diagram:

<figure><img src="https://docs.gravitee.io/images/apim/3.x/event-native/event-native-api-management-execution-scopes-2.png" alt=""><figcaption><p>Reactive engine execution order</p></figcaption></figure>

### Migration considerations

If you have designed your APIs with legacy policy execution engine mode ordering in mind, you must take care to review your existing flows when enabling compatibility mode or migrating to a v4 API definition. There may be policy execution behavior changes due to the changes in execution order at runtime.

To smooth the transition process, you can use the debug mode to test the new behavior and adapt your APIs, so they can be safely redeployed.

## Logging

With the legacy execution engine, the following issues exist with logging:

* A `502` status code would normally indicate that the server has responded with a `502` status code; however, this is also shown for connection failures.
* Consumer response headers are not displayed clearly.

For example:

<figure><img src="https://docs.gravitee.io/images/apim/3.x/event-native/event-native-api-management-logging-1.png" alt=""><figcaption><p>Sample 502 log with legacy execution engine</p></figcaption></figure>

### Reactive execution engine improvements

With the reactive execution engine, the following improvements have been implemented:

* When a connectivity error occurs during a connection attempt to the backend endpoint, the Gateway response displays an HTTP status code `0` and no headers. This makes it clear that no response has been received from the backend endpoint due to the connectivity error.
* Consumer response headers are displayed more clearly.

For example:

<figure><img src="https://docs.gravitee.io/images/apim/3.x/event-native/event-native-api-management-logging-2.png" alt=""><figcaption><p>Sample 502 log with reactive execution engine</p></figcaption></figure>

## EL condition evaluation

With the legacy execution engine, the Gateway returns a `500` error with an obscure message when the Gateway provides a valid Gravitee Expression Language (EL) expression that fails to be evaluated because it is trying to access missing data.

For example:

<figure><img src="https://docs.gravitee.io/images/apim/3.x/event-native/event-native-api-management-condition-evaluation-1.png" alt=""><figcaption><p>Sample EL condition evaluation error with legacy engine</p></figcaption></figure>

### Reactive execution engine improvements

With the reactive execution engine, the policy (or flow) is executed when a valid EL expression is evaluated as `true`. Otherwise, it is skipped.

A policy is skipped when:

* The EL expression is evaluated as `false`.
* The EL expression evaluation fails because the expected data tested is missing.

This is shown in the example below:

<figure><img src="https://docs.gravitee.io/images/apim/3.x/event-native/event-native-api-management-condition-evaluation-2.png" alt=""><figcaption><p>Sample EL condition skipping behavior with reactive engine</p></figcaption></figure>

Mastering EL expressions can be challenging. The new mode eases the learning curve by ensuring EL expressions that attempt to access missing data are evaluated as `false` instead of returning an obscure error. For example, `{#request.headers['X-Test'][0] == 'something'}` will skip execution even if the request header `X-Test` is not specified.

However, the execution will fail and throw an error if the provided EL expression cannot be parsed (for example, if it is syntactically invalid). The error message details why the EL expression cannot be parsed.

<figure><img src="https://docs.gravitee.io/images/apim/3.x/event-native/event-native-api-management-condition-evaluation-3.png" alt=""><figcaption><p>Sample EL condition error with reactive engine</p></figcaption></figure>

## Connection: close

With the legacy execution engine, the Gateway handles a bad request by responding with a `Connection: close` response header and effectively closes the connection. This could happen repeatedly again if the client application sends requests to the Gateway with the same invalid data.

{% hint style="info" %}
The same behavior is in place for `404` "not found" errors.
{% endhint %}

Creating a connection is costly for the Gateway and such issues can dramatically impact performance - especially if the consumer sends a high volume of bad requests.

### Reactive execution engine improvements

The reactive execution engine does not close the connection if the bad request is due to a client-side error. The engine will only close the connection in case of a server-side error.

## Flow conditions

With the legacy execution engine, a condition can be defined once for the whole flow, but the condition is evaluated before executing each phase of the flow (`REQUEST` and `RESPONSE` phases). This could lead to a partial flow execution.

For instance, a condition could be defined based on a request header that is removed during the `REQUEST` phase (e.g. the user does not want the request header to be transmitted to the backend). In such cases, the condition is re-evaluated and the `RESPONSE` phase is skipped completely.

{% hint style="info" %}
This could also occur with a platform flow.
{% endhint %}

The example illustrates this behavior:

<figure><img src="https://docs.gravitee.io/images/apim/3.x/event-native/event-native-api-management-flow-condition-1.png" alt=""><figcaption><p>Partial flow execution example</p></figcaption></figure>

### Reactive execution engine improvements

With the reactive execution engine, the flow condition will be applied once for the whole flow. If the condition is evaluated as `true`, then both the `REQUEST` and the `RESPONSE` phases will be executed.

The example below shows the new behavior:

<figure><img src="https://docs.gravitee.io/images/apim/3.x/event-native/event-native-api-management-flow-condition-2.png" alt=""><figcaption><p>Reactive exectution engine flow condition improvements</p></figcaption></figure>

### Migration considerations

If you expect the `RESPONSE` phase to be skipped in the scenario described above, you must refactor your flows since both the `REQUEST` and `RESPONSE` phases will be executed as long as the condition is evaluated as `true`.

To mimic the legacy engine behavior with the reactive engine, you can remove the flow condition from the flow configuration and add it directly to the policies themselves.

## Flow interruption

With the legacy execution engine, when a policy fails, the execution flow is interrupted and the response is returned to the client application. As a result, the platform flow response is also skipped. This leads to unexpected behavior, especially when `POST` actions are expected like in a custom metrics reporter.

### Reactive execution engine improvements

The reactive execution engine ensures that platform flows are always executed, except in the case of an irrecoverable error. This allows the API to fail without skipping important steps in the flow occurring at a higher level.

## Access-control-allowed-origin

With the legacy execution engine, you can configure Cross-Origin Resource Sharing (CORS) to allow a specific subset of origins. The Gateway properly validates the origin but returns `Access-Control-Allowed-Origin: *` in the response header regardless of the actual configuration.

### Reactive execution engine improvements

With the reactive execution engine, the allowed origin(s) you specify is returned instead of `*` - for example, `Access-Control-Allowed-Origin:` [`https://test.gravitee.io`](https://test.gravitee.io/) for the configuration shown below.

<figure><img src="https://docs.gravitee.io/images/apim/3.x/event-native/event-native-api-management-cors.png" alt=""><figcaption><p>Sample CORS configuration</p></figcaption></figure>

## EL expression parsing

With the legacy execution engine, an EL expression is parsed each time it is evaluated.

### Reactive execution engine improvements

With the reactive execution engine, a new caching mechanism allows the Gateway to cache the parsed EL expression for reuse and thereby improve performance.

## EL body expressions

With the legacy execution engine, using an EL expression such as `{#request.content == 'something'}` is limited to policies working at `REQUEST_CONTENT` or `RESPONSE_CONTENT` phases (e.g. Assign Metrics, Assign Content, Request Validation, etc.).

However, defining a policy or a flow condition based on the request or response body is not supported.

### Reactive execution engine improvements

With the reactive execution engine, it is possible to define a condition based on the request or response body. For example, you can create a condition such as `{#request.content == 'something'}`.

Depending on the expected content type, it is also possible to define a condition based on JSON such as `{#request.jsonContent.foo.bar == 'something'}` where the request body looks like this:

```json
{
  "foo": {
      "bar": "something"
  }
}
```

The same applies to XML content using `{#request.xmlContent.foo.bar == 'something'}`:

```xml
<foo>
  <bar>something</bar>
</foo>
```

### Migration considerations

Use this feature with caution - an EL body-based expression is resource heavy and should be avoided when performance is a concern. Working with request or response content can significantly degrade performance and consumes substantially more memory on the Gateway.

## Timeout management

With the legacy execution engine, when a timeout is configured (`http.requestTimeout`) and triggered due to a request that is too slow (or a policy taking too much time to execute), the API platform flows are always skipped and a `504` status is sent as a response to the client.

### Reactive execution engine improvements

A timeout can now be triggered at two places in the chain:

* The flow can be interrupted between the beginning of a Gateway API's request phase and the end of the response phase. In this case, a platform response flow will still be executed.
* The flow can be interrupted during the platform response flow when the overall request time is too long. This results in a `504` response and the platform response flow is interrupted.

Two properties are available to configure these triggers:

* `http.requestTimeout`: The duration used to configure the timeout of the request
* `http.requestTimeoutGraceDelay`: Additional time used to give the platform response flow a chance to execute

The timeout value is calculated from the following two properties:

* `Timeout = Max(http.requestTimeoutGraceDelay, http.requestTimeout - apiElapsedTime)`
* With `apiElapsedTime = System.currentTimeMillis() - request().timestamp()`

{% hint style="info" %}
**Timeout configuration**

With the reactive execution engine, timeout values of `0` and less are treated as meaning 'no timeout' (like the legacy engine). If you configure the timeout with a positive value, then it will act normally.

If no configuration is provided, a default configuration is set to default to 30000 ms timeout.
{% endhint %}

### **Examples**

In the following examples, we assume that there is no timeout defined for the backend in the API’s endpoint configuration. In real life, those timeout values should be shorter than `http.requestTimeout`, and should interrupt the flow at the invoker level.

We will use `http.requestTimeout=2000ms` and `http.requestTimeoutGraceDelay=30ms`.

The example below shows timelines indicating when a timeout should occur depending on the duration of the API flow and the response platform flows:

<figure><img src="https://docs.gravitee.io/images/apim/3.x/event-native/event-native-api-management-timeout.png" alt=""><figcaption><p>Reactive engine timeout management</p></figcaption></figure>

## Plan selection

For both execution engines, the plan selection workflow parses all the published plans in the following order: JWT, OAuth2, ApiKey, Keyless.

The parsed plan is selected for execution if all the following conditions are met:

* The request contains a token corresponding to this plan type (`api-key` or authorization header).
* The plan condition rule is either not set or is set incorrectly.
* There is an active subscription matching the incoming request.

{% hint style="warning" %}
There is an exception for OAuth2 plans executed on the v3 engine as detailed in the next section.
{% endhint %}

### Legacy execution engine behavior

With the legacy execution engine, the OAuth2 plan is selected even if the incoming request does not match a subscription.

No JWT token introspection is done during OAuth2 plan selection.

If there are multiple OAuth2 plans, that could lead to the selection of the wrong plan.

### Reactive execution engine improvements

With the reactive execution engine, the Oauth2 plan is _not_ selected if the incoming request does not match a subscription.

During the OAuth2 plan selection, a token introspection is completed to retrieve the `client_id` which allows searching for a subscription.

If there are performance concerns, a cache system is available to avoid completing the same token introspection multiple times. Where possible, it is recommended to use selection rules if there are multiple OAuth2 plans to avoid any unnecessary token introspection.

Additionally, the plan selection workflow has been changed for the Keyless plan - its activation is now prevented when a security token has been detected in the incoming request. Therefore, if an API has multiple plans (JWT, OAuth2, Apikey, Keyless) and the incoming request contains a token or an API key that does not match any of the existing plans, then the Keyless plan will not be activated and the user will receive a generic `401` response without any details.
