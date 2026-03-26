---
description: Configuration guide for Timeout management.
---

# Timeout management

## Legacy execution engine behavior

When using the legacy execution engine, if a timeout is configured (`http.requestTimeout`) and triggered due to a request that is too slow or a policy that is taking too much time to execute, the API platform flows are always skipped and a `504` status is sent as a response to the client.

## Reactive execution engine improvements

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

The reactive execution engine interprets timeout values less than or equal to `0` as "no timeout" (same as the legacy engine).

If you configure the timeout with a positive value, then it will act normally.

If no configuration is provided, a default configuration is set to default to 30000 ms timeout.
{% endhint %}

## **Examples**

The example below shows timelines indicating when a timeout should occur depending on the duration of the API flow and the response platform flows:

* We assume that there is no timeout defined for the backend in the API’s endpoint configuration.
  * In real life, those timeout values should be shorter than `http.requestTimeout` and should interrupt the flow at the invoker level.
* We are using `http.requestTimeout=2000ms` and `http.requestTimeoutGraceDelay=30ms`.

<figure><img src="https://docs.gravitee.io/images/apim/3.x/event-native/event-native-api-management-timeout.png" alt=""><figcaption><p>Reactive engine timeout management</p></figcaption></figure>
