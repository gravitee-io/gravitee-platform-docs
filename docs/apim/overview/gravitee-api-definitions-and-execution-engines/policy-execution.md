---
description: >-
  This page discusses improvements to policy execution phases and execution
  order
---

# Policy execution

## Legacy execution engine behavior

The legacy execution engine requires execution scopes to indicate the level at which a policy will work:

* `REQUEST`: The policy only works on request headers. It never accesses the request body.
* `REQUEST_CONTENT`: The policy works at the request content level and can access the request body.
* `RESPONSE`: The policy only works on response headers. It never accesses the response body.
* `RESPONSE_CONTENT`: The policy works at the response content level and can access the response body.

Execution of all policies working on the body content are postponed until the policies working on headers have been executed. This leads to an execution order that is often different than the one originally designed.

<figure><img src="https://docs.gravitee.io/images/apim/3.x/event-native/event-native-api-management-execution-scopes-1.png" alt=""><figcaption><p>Legacy engine execution order</p></figcaption></figure>

## Reactive execution engine improvements

The reactive execution engine does not consider the `REQUEST_CONTENT` and `RESPONSE_CONTENT` phases. All policies are executed in the exact order of the design, regardless of whether they work on the content or not.

<figure><img src="https://docs.gravitee.io/images/apim/3.x/event-native/event-native-api-management-execution-scopes-2.png" alt=""><figcaption><p>Reactive engine execution order</p></figcaption></figure>

## Migration considerations

If you have designed your APIs assuming the policy ordering provided by the legacy execution engine, you must review your existing flows when enabling compatibility mode or migrating to a v4 API definition. There may be policy execution behavior changes due to the changes in execution order at runtime. You can use the debug mode to test the new behavior and adapt your APIs to ensure they are safely redeployed.
