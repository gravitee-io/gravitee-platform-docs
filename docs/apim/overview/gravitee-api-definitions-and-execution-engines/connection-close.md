---
description: This page discusses improvements to how the Gateway responds to a bad request
---

# Connection: close

## Overview

With the legacy execution engine, the Gateway handles a bad request by responding with a `Connection: close` response header and effectively closes the connection. This could happen repeatedly again if the client application sends requests to the Gateway with the same invalid data.

{% hint style="info" %}
The same behavior is in place for `404` "not found" errors.
{% endhint %}

Creating a connection is costly for the Gateway and such issues can dramatically impact performance - especially if the consumer sends a high volume of bad requests.

## Reactive execution engine improvements

The reactive execution engine does not close the connection if the bad request is due to a client-side error. The engine will only close the connection in case of a server-side error.
