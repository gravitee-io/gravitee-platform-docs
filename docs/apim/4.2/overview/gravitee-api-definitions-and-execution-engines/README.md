---
layout:
  title:
    visible: true
  description:
    visible: false
  tableOfContents:
    visible: true
  outline:
    visible: true
  pagination:
    visible: true
---

# Gravitee API Definitions and Execution Engines

## Overview

A Gravitee API definition is very similar to an API specification (e.g., OpenAPI, AsyncAPI) except it is a specification for your Gravitee API Management (APIM) Gateway_._ It’s a JSON representation of everything that the APIM Gateway needs to know for it to proxy, apply policies to, create plans for, etc., your APIs and their traffic.

To execute your Gateway APIs and policy flows, the Gateway needs a runtime environment, or engine. This is generally referred to as the execution engine. As of APIM 4.0, there is support for both the v2 and v4 Gravitee API definitions, where v2 API definitions run on the legacy execution engine and v4 API definitions run on the reactive execution engine.

{% hint style="warning" %}
You can run v2 Gateway APIs in [emulation mode](reactive-execution-engine.md#v2-gateway-api-emulation-mode), which emulates some of the execution flow improvements of the reactive execution engine.&#x20;
{% endhint %}

The [v2 API Creation Wizard ](../../guides/create-apis/the-api-creation-wizard/v2-api-creation-wizard.md)creates v2 Gateway APIs compatible with the legacy execution engine that can be augmented with flows designed in the [v2 Policy Studio](../../guides/policy-studio/v2-api-policy-studio.md). The [v4 API Creation Wizard](../../guides/create-apis/the-api-creation-wizard/v4-api-creation-wizard.md) creates v4 APIs compatible with the reactive execution engine that can be augmented with flows designed in the [v4 Policy Studio](../../guides/policy-studio/v4-api-policy-studio.md).

This guide is a deep dive into the differences between the new reactive execution engine and the existing legacy execution engine. Additionally, guidance is provided on managing changes in system behavior when switching to the reactive policy execution engine or enabling compatibility mode with a v2 API. The information is grouped by functional area.

## Comparisons

The following comparisons can be made between the reactive and legacy execution engines:

* [Policy execution](README.md#policy-execution)
* [Plan selection](README.md#plan-selection)
* [Flow](README.md#flow)
* [Logging](README.md#logging)
* [Expression Language](README.md#expression-language)
* [Bad requests](README.md#bad-requests)
* [Origin validation](README.md#origin-validation)
* [Timeout management](README.md#timeout-management)

### Policy execution

{% tabs %}
{% tab title="Legacy engine behavior" %}
The legacy execution engine requires execution scopes to indicate the level at which a policy will work:

* `REQUEST`: The policy only works on request headers. It never accesses the request body.
* `REQUEST_CONTENT`: The policy works at the request content level and can access the request body.
* `RESPONSE`: The policy only works on response headers. It never accesses the response body.
* `RESPONSE_CONTENT`: The policy works at the response content level and can access the response body.

Execution of all policies working on the body content are postponed until the policies working on headers have been executed. This leads to an execution order that is often different than the one originally designed.

<figure><img src="https://docs.gravitee.io/images/apim/3.x/event-native/event-native-api-management-execution-scopes-1.png" alt=""><figcaption><p>Legacy engine execution order</p></figcaption></figure>
{% endtab %}

{% tab title="Reactive engine improvements" %}
The reactive execution engine does not consider the `REQUEST_CONTENT` and `RESPONSE_CONTENT` phases. All policies are executed in the exact order of the design, regardless of whether they work on the content or not.

<figure><img src="https://docs.gravitee.io/images/apim/3.x/event-native/event-native-api-management-execution-scopes-2.png" alt=""><figcaption><p>Reactive engine execution order</p></figcaption></figure>
{% endtab %}
{% endtabs %}

{% hint style="info" %}
**Migration considerations**

If you have designed your APIs assuming the policy ordering imposed by the legacy execution engine, you must review your existing flows when enabling compatibility mode or migrating to a v4 API definition. There may be policy execution behavior changes due to the changes in execution order at runtime. You can use the debug mode to test the new behavior and adapt your APIs to ensure they are safely redeployed.
{% endhint %}

### Plan selection

For both execution engines, the plan selection workflow parses all published plans in the following order: JWT, OAuth2, API Key, Keyless. Each plan type has specific rules.

<details>

<summary>JWT</summary>

* Retrieve JWT from `Authorization` Header or query parameters
* Ignore empty `Authorization` Header or any type other than Bearer
* While it was previously ignored, **an empty Bearer token is now considered invalid**

</details>

<details>

<summary>OAuth2</summary>

* Retrieve OAuth2 from `Authorization` Header or query parameters
* Ignore empty `Authorization` Header or any type other than Bearer
* While it was previously ignored, **an empty Bearer token is now considered invalid**

</details>

<details>

<summary>API Key</summary>

* Retrieve the API key from the request header or query parameters (default header: `X-Gravitee-Api-Key` and default query parameter: `api-key`)
* While it was previously ignored, **an empty API key is now considered invalid**

</details>

<details>

<summary>Keyless</summary>

* Will ignore any type of security (API key, Bearer token, etc.)
* **If another plan has detected a security token, valid or invalid, all flows assigned to the Keyless plan will be ignored.** Therefore, if an API has multiple plans of different types and the incoming request contains a token or an API key that does not match any of the existing plans, then the Keyless plan will not be activated and the user will receive a generic `401` response without any details.

</details>

The parsed plan is selected for execution if all the following conditions are met:

* The request contains a token corresponding to the plan type (e.g., `X-Gravitee-Api-Key` header for API Key plans)
* The plan condition rule is valid or not set
* There is an active subscription matching the incoming request

{% hint style="warning" %}
There is an exception for OAuth2 plans executed on the legacy engine as detailed in the next section.
{% endhint %}

{% tabs %}
{% tab title="Legacy engine behavior" %}
With the legacy execution engine, the OAuth2 plan is selected even if the incoming request does not match a subscription.

No JWT token introspection is done during OAuth2 plan selection.

Multiple OAuth2 plans can lead to the selection of the wrong plan.
{% endtab %}

{% tab title="Reactive engine improvements" %}
When using the reactive execution engine, the OAuth2 plan is _not_ selected if the incoming request does not match a subscription.

During OAuth2 plan selection, a token introspection is completed to retrieve the `client_id`, which allows searching for a subscription.

If there are performance concerns, a cache system is available to avoid completing the same token introspection multiple times. Where possible, it is recommended to use selection rules if there are multiple OAuth2 plans to avoid any unnecessary token introspection.
{% endtab %}
{% endtabs %}

### Flow

{% hint style="info" %}
Flows can be scoped to different execution contexts:

* **plan:** A flow scoped to a plan only executes for subscribers
* **API:** A flow scoped to an API executes for all consumers of that API
* **platform:** A flow scoped to the platform executes for all API consumers using the Gateway
{% endhint %}

#### Flow conditions

{% tabs %}
{% tab title="Legacy engine behavior" %}
When using the legacy execution engine, a condition can be defined once for the whole flow, but the condition is evaluated before executing each phase of the flow (`REQUEST` and `RESPONSE` phases). This could lead to a partial flow execution.

For example, a condition could be defined based on a request header that is removed during the `REQUEST` phase (e.g., the user does not want the request header to be transmitted to the backend). The condition is then re-evaluated and the `RESPONSE` phase is skipped completely, as shown below:

<figure><img src="https://docs.gravitee.io/images/apim/3.x/event-native/event-native-api-management-flow-condition-1.png" alt=""><figcaption><p>Partial flow execution example</p></figcaption></figure>
{% endtab %}

{% tab title="Reactive engine improvements" %}
When using the reactive execution engine, the flow condition will be applied once for the whole flow. If the condition is evaluated as `true`, then both the `REQUEST` and the `RESPONSE` phases will be executed, as shown below:

<figure><img src="https://docs.gravitee.io/images/apim/3.x/event-native/event-native-api-management-flow-condition-2.png" alt=""><figcaption><p>Reactive execution engine flow condition improvements</p></figcaption></figure>
{% endtab %}
{% endtabs %}

{% hint style="info" %}
**Migration considerations**

If you expect the `RESPONSE` phase to be skipped in the scenario described above, you must refactor your flows since both the `REQUEST` and `RESPONSE` phases will be executed as long as the condition is evaluated as `true`.

To mimic the legacy engine behavior with the reactive engine, you can remove the flow condition from the flow configuration and add it directly to the policies themselves.
{% endhint %}

#### Flow interruption

{% tabs %}
{% tab title="Legacy engine behavior" %}
When using the legacy execution engine, if a policy fails, the execution flow is interrupted and the response is returned to the client application. As a result, the platform flow response is also skipped. This leads to unexpected behavior, especially when `POST` actions are expected, e.g., in a custom metrics reporter.
{% endtab %}

{% tab title="Reactive engine improvements" %}
The reactive execution engine ensures that platform flows are always executed, except in the case of an irrecoverable error. This allows the API to fail without skipping important steps in the flow occurring at a higher level.
{% endtab %}
{% endtabs %}

To learn more about flows, see [Message Flow Control](message-flow-control.md).

### Logging

{% tabs %}
{% tab title="Legacy engine behavior" %}
The legacy execution engine presents logging issues:

* A `502` status code normally indicates that the server has responded with a `502` status code, but `502` is also returned for connection failures
* Consumer response headers are not displayed clearly

<figure><img src="https://docs.gravitee.io/images/apim/3.x/event-native/event-native-api-management-logging-1.png" alt=""><figcaption><p>Sample 502 log with the legacy execution engine</p></figcaption></figure>
{% endtab %}

{% tab title="Reactive engine improvements" %}
The reactive execution engine implements the following improvements:

* When a connectivity error occurs during a connection attempt to the backend endpoint, the Gateway response displays an HTTP status code `0` and no headers. This clarifies that no response has been received from the backend endpoint due to the connectivity error.
* Consumer response headers are displayed more clearly

<figure><img src="https://docs.gravitee.io/images/apim/3.x/event-native/event-native-api-management-logging-2.png" alt=""><figcaption><p>Sample 502 log with the reactive execution engine</p></figcaption></figure>
{% endtab %}
{% endtabs %}

### Expression Language

#### EL condition evaluation

{% tabs %}
{% tab title="Legacy engine behavior" %}
The Gateway returns a `500` error with an obscure message when the legacy execution engine fails to evaluate a valid Gravitee Expression Language (EL) expression because it is trying to access missing data.

<figure><img src="https://docs.gravitee.io/images/apim/3.x/event-native/event-native-api-management-condition-evaluation-1.png" alt=""><figcaption><p>Sample EL condition evaluation error with legacy engine</p></figcaption></figure>
{% endtab %}

{% tab title="Reactive engine improvements" %}
The reactive execution engine executes a policy (or flow) when a valid EL expression evaluates as `true`. Otherwise, the policy is skipped because the EL expression evaluates as `false`.

<figure><img src="https://docs.gravitee.io/images/apim/3.x/event-native/event-native-api-management-condition-evaluation-2.png" alt=""><figcaption><p>Sample EL condition skipping behavior with reactive engine</p></figcaption></figure>

The reactive execution engine ensures EL expressions that attempt to access missing data are evaluated as `false`. For example, `{#request.headers['X-Test'][0] == 'something'}` will skip execution even if the request header `X-Test` is not specified.

The execution will fail and throw an error if the provided EL expression cannot be parsed, e.g., if it is syntactically invalid. The error message details why the EL expression cannot be parsed.

<figure><img src="https://docs.gravitee.io/images/apim/3.x/event-native/event-native-api-management-condition-evaluation-3.png" alt=""><figcaption><p>Sample EL condition error with reactive engine</p></figcaption></figure>
{% endtab %}
{% endtabs %}

#### EL expression parsing

{% tabs %}
{% tab title="Legacy engine behavior" %}
The legacy execution engine parses an EL expression each time it is evaluated.
{% endtab %}

{% tab title="Reactive engine improvements" %}
The reactive execution engine employs a new caching mechanism that allows the Gateway to cache the parsed EL expression for reuse, thereby improving performance.
{% endtab %}
{% endtabs %}

#### EL body expressions

{% tabs %}
{% tab title="Legacy engine behavior" %}
The legacy execution engine limits use of EL expressions such as `{#request.content == 'something'}` to policies working at the `REQUEST_CONTENT` or `RESPONSE_CONTENT` phases (e.g., Assign Metrics, Assign Content, Request Validation, etc.).

However, defining a policy or a flow condition based on the request or response body is not supported.
{% endtab %}

{% tab title="Reactive engine improvements" %}
Using the reactive execution engine, it is possible to define a condition based on the request or response body. For example, you can create a condition such as `{#request.content == 'something'}`.

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
{% endtab %}
{% endtabs %}

{% hint style="warning" %}
**Migration considerations**

Use this feature with caution. EL body-based expressions are resource-heavy and should be avoided when performance is a concern. Working with request or response content can significantly degrade performance and consumes substantially more memory on the Gateway.
{% endhint %}

### Bad requests

{% tabs %}
{% tab title="Legacy engine behavior" %}
A Gateway running on the legacy execution engine handles a bad request by responding with a `Connection: close` response header and effectively closing the connection. The same behavior is in place for `404` "not found" errors and could occur repeatedly if the client application resends requests with invalid data.

Creating a connection is costly for the Gateway and sending invalid data can dramatically impact performance, especially if the consumer sends a high volume of bad requests.
{% endtab %}

{% tab title="Reactive engine improvements" %}
The reactive execution engine does not close the connection if the bad request is due to a client-side error. The engine will only close the connection if there is a server-side error.
{% endtab %}
{% endtabs %}

### Origin validation

{% tabs %}
{% tab title="Legacy engine behavior" %}
When using the legacy execution engine, you can configure Cross-Origin Resource Sharing (CORS) to allow a specific subset of origins. Regardless of the actual configuration, the Gateway properly validates the origin but returns `Access-Control-Allowed-Origin: *` in the response header.
{% endtab %}

{% tab title="Reactive engine improvements" %}
When using the reactive execution engine, the allowed origin(s) you specify is returned instead of `*`. For example, in the configuration shown below, `Access-Control-Allowed-Origin: https://test.gravitee.io`.

<figure><img src="https://docs.gravitee.io/images/apim/3.x/event-native/event-native-api-management-cors.png" alt=""><figcaption><p>Sample CORS configuration</p></figcaption></figure>
{% endtab %}
{% endtabs %}

### Timeout management

{% tabs %}
{% tab title="Legacy engine behavior" %}
When using the legacy execution engine, if a timeout is configured (`http.requestTimeout`) and triggered due to a request that is too slow or a policy that is taking too much time to execute, the API platform flows are always skipped and a `504` status is sent as a response to the client.
{% endtab %}

{% tab title="Reactive engine improvements" %}
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

The reactive execution engine interprets timeout values less than or equal to `0` as "no timeout" (same as the legacy engine).&#x20;

If you configure the timeout with a positive value, then it will act normally.

If no configuration is provided, a default configuration is set to default to 30000 ms timeout.
{% endhint %}
{% endtab %}
{% endtabs %}

#### **Example**

The example below shows timelines indicating when a timeout should occur depending on the duration of the API flow and the response platform flows:

* We assume that there is no timeout defined for the backend in the API’s endpoint configuration.&#x20;
  * In real life, those timeout values should be shorter than `http.requestTimeout` and should interrupt the flow at the invoker level.
* We are using `http.requestTimeout=2000ms` and `http.requestTimeoutGraceDelay=30ms`.

<div align="center">

<figure><img src="https://docs.gravitee.io/images/apim/3.x/event-native/event-native-api-management-timeout.png" alt="" width="563"><figcaption><p>Reactive engine timeout management</p></figcaption></figure>

</div>
