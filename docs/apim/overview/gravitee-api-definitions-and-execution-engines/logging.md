---
description: This page focuses on legacy logging issues and improvements
---

# Logging

## Legacy execution engine behavior

The legacy execution engine presents logging issues:

* A `502` status code normally indicates that the server has responded with a `502` status code, but `502` is also returned for connection failures
* Consumer response headers are not displayed clearly

<figure><img src="https://docs.gravitee.io/images/apim/3.x/event-native/event-native-api-management-logging-1.png" alt=""><figcaption><p>Sample 502 log with the legacy execution engine</p></figcaption></figure>

## Reactive execution engine improvements

The reactive execution engine implements the following improvements:

* When a connectivity error occurs during a connection attempt to the backend endpoint, the Gateway response displays an HTTP status code `0` and no headers. This clarifies that no response has been received from the backend endpoint due to the connectivity error.
* Consumer response headers are displayed more clearly

<figure><img src="https://docs.gravitee.io/images/apim/3.x/event-native/event-native-api-management-logging-2.png" alt=""><figcaption><p>Sample 502 log with the reactive execution engine</p></figcaption></figure>
