---
description: This page discusses improvements to how the Gateway responds to a bad request
---

# Connection: close

## Legacy execution engine behavior

A Gateway running on the legacy execution engine handles a bad request by responding with a `Connection: close` response header and effectively closing the connection. The same behavior is in place for `404` "not found" errors and could occur repeatedly if the client application resends requests with invalid data.

Creating a connection is costly for the Gateway and sending invalid data can dramatically impact performance, especially if the consumer sends a high volume of bad requests.

## Reactive execution engine improvements

The reactive execution engine does not close the connection if the bad request is due to a client-side error. The engine will only close the connection if there is a server-side error.
