---
description: This page discusses improvements to flow conditions and interruptions
---

# Flow

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
