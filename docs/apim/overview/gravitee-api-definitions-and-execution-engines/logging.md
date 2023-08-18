---
description: This page focuses on legacy logging issues and improvements
---

# Logging

## Overview

With the legacy execution engine, the following issues exist with logging:

* A `502` status code would normally indicate that the server has responded with a `502` status code; however, this is also shown for connection failures.
* Consumer response headers are not displayed clearly.

For example:

<figure><img src="https://docs.gravitee.io/images/apim/3.x/event-native/event-native-api-management-logging-1.png" alt=""><figcaption><p>Sample 502 log with legacy execution engine</p></figcaption></figure>

## Reactive execution engine improvements

With the reactive execution engine, the following improvements have been implemented:

* When a connectivity error occurs during a connection attempt to the backend endpoint, the Gateway response displays an HTTP status code `0` and no headers. This makes it clear that no response has been received from the backend endpoint due to the connectivity error.
* Consumer response headers are displayed more clearly.

For example:

<figure><img src="https://docs.gravitee.io/images/apim/3.x/event-native/event-native-api-management-logging-2.png" alt=""><figcaption><p>Sample 502 log with reactive execution engine</p></figcaption></figure>
