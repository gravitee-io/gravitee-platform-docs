---
description: Guide on applying policies related to mtls.
metaLinks:
  alternates:
    - mtls.md
---

# mTLS

### Phase <a href="#user-content-phase" id="user-content-phase"></a>

| onRequest | onResponse |
| --------- | ---------- |
| X         |            |

### Description <a href="#user-content-description" id="user-content-description"></a>

You can use the `mtls` policy to verify a client certificate exists as part of the request.

This policy does not ensure that certificates are valid, since it is done directly by the server.

### Compatibility with APIM <a href="#user-content-compatibility-with-apim" id="user-content-compatibility-with-apim"></a>

| Plugin version | APIM version  |
| -------------- | ------------- |
| 2.x            | 4.10 to latest |
| 1.x            | 4.5 to 4.9    |

{% hint style="info" %}
**Kafka Native API Support**

mTLS policy version 2.0.0 or later supports Kafka Native APIs and is compatible with APIM 4.10+. Version 1.x does not support Kafka Native APIs.

mTLS for Kafka Native APIs is an Enterprise Edition feature.
{% endhint %}

### Errors <a href="#user-content-errors" id="user-content-errors"></a>

You can use the response template feature to override the default response provided by the policy. These templates must be defined at the API level (see the API Console **Response Templates** option in the API **Entrypoints > Response Templates** menu).

The error keys sent by this policy are as follows:

| Key                          | Parameters |
| ---------------------------- | ---------- |
| CLIENT\_CERTIFICATE\_MISSING | -          |
| CLIENT\_CERTIFICATE\_INVALID | -          |
| SSL\_SESSION\_REQUIRED       | -          |
