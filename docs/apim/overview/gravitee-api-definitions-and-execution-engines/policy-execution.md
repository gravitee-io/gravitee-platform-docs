---
description: >-
  This page discusses improvements to policy execution phases and execution
  order
---

# Policy execution

## Overview

With the legacy execution engine, different execution scopes are required in order to indicate at which level a policy will work, as follows:

* `REQUEST`: The policy only works on request headers. It never accesses the request body.
* `REQUEST_CONTENT`: The policy works at request content level and can access the request body.
* `RESPONSE`: The policy only works on response headers. It never accesses the response body.
* `RESPONSE_CONTENT`: The policy works at response content level and can access the response body.

As a result, all policies working on the body content are postponed to be executed after the policies working on headers. This leads to an execution order that is often different than the one originally designed, as shown in the following diagram:

<figure><img src="https://docs.gravitee.io/images/apim/3.x/event-native/event-native-api-management-execution-scopes-1.png" alt=""><figcaption><p>Legacy engine execution order</p></figcaption></figure>

## Reactive execution engine improvements

With the reactive execution engine, the `REQUEST_CONTENT` and `RESPONSE_CONTENT` phases are no longer considered - all policies are executed in the exact order of design, regardless of whether they work on the content or not. This is shown in the following diagram:

<figure><img src="https://docs.gravitee.io/images/apim/3.x/event-native/event-native-api-management-execution-scopes-2.png" alt=""><figcaption><p>Reactive engine execution order</p></figcaption></figure>

## Migration considerations

If you have designed your APIs with legacy policy execution engine mode ordering in mind, you must take care to review your existing flows when enabling compatibility mode or migrating to a v4 API definition. There may be policy execution behavior changes due to the changes in execution order at runtime.

To smooth the transition process, you can use the debug mode to test the new behavior and adapt your APIs, so they can be safely redeployed.
