---
description: API documentation for calling an api with mtls.
---

# Calling an API with mTLS

## Before you begin

* You must have the client certificate
* You must have the private key

## Procedure

* To call an API with mTLS, use the following command:

```bash
$ curl –-cert  <client.cer> --key <client.key> https://my-gateway.com/mtls-api
```

* Replace \<client.cer> and \<client.key> with the name of the files where you have stored your client certificate and the file where you have stored the client key.

Also, this requires that your client trusts the certificate sent by the gateway.
