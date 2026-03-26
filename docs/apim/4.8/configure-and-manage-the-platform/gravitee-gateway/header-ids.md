---
description: Configuration guide for header ids.
---

# Header IDs

By default, the APIM Gateway will generate an id for each request and set it in the following headers:

* `X-Gravitee-Transaction-Id`: This header represents the identifier for the entire transaction, which typically encompasses multiple calls or requests. It allows the tracking of a series of related requests and responses that are part of a larger transaction.
* `X-Gravitee-Request-Id`: This header represents the identifier for a single call or request within the transaction. Every individual request receives a unique identifier, which allows each request to be tracked separately.

Both of these headers can be customized. You can provide your own header names:

```yaml
handlers:
  request:
    transaction:
      header: X-Custom-Transaction-Id
    request:
      header: X-Custom-Request-Id
```

Also, you can configure the APIM Gateway behavior when the backend itself sets the same headers. To do so you need to set the `overrideMode` attribute. The following values are available:

* `override`: The header set by the APIM Gateway will override the one provided by the backend
* `merge`: Both headers set by the APIM Gateway and the backend will be kept (as headers can be multivalued)
* `keep`: The header set by the backend will be kept and the one provided by the APIM Gateway discarded

Both transaction and request headers can be configured independently:

```yaml
handlers:
  request:
    transaction:
      header: X-Custom-Transaction-Id
      overrideMode: merge
    request:
      header: X-Custom-Request-Id
      overrideMode: keep
```
