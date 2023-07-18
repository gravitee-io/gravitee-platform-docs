---
description: This page provides the technical details of the JSON Web Signature policy
---

# JSON Web Signature (JWS)

## Overview

Functional and implementation information for the JWS policy is organized into the following sections:

* [Examples](template-policy-rework-structure-12.md#examples)
* [Configuration](template-policy-rework-structure-12.md#configuration)
* [Errors](template-policy-rework-structure-12.md#errors)
* [Changelogs](template-policy-rework-structure-12.md#changelogs)

## Examples

You can use the `jws-validator` policy to validate the JWS token signature, certificate information, and expiration date before sending the API call to the target backend.

JWT in JWS format enables secure content to be shared across security domains. The RFC standards are as follows:

* JWS (Json Web Signature) standard RFC: [https://tools.ietf.org/html/rfc7515](https://tools.ietf.org/html/rfc7515)
* JOSE Header standard RFC: [https://tools.ietf.org/html/rfc7515#section-4](https://tools.ietf.org/html/rfc7515#section-4)
* JWT (Json Web Token) standard RFC: [https://tools.ietf.org/html/rfc7519](https://tools.ietf.org/html/rfc7519)

### JWT

A JWT is composed of three parts: a header, a payload and a signature. You can see some examples here: [http://jwt.io](http://jwt.io/).

* The header contains attributes indicating the algorithm used to sign the token.
* The payload contains some information inserted by the AS (Authorization Server), such as the expiration date and UID of the user.

Both the header and payload are encoded with Base64, so anyone can read the content.

* The third and last part is the signature (for more details, see the RFC).

### Input

```
======================= =================================================
Request Method          POST
Request Content-Type    application/jose+json
Request Body            eyJ0....ifQ.eyJzdWIiOiI...lIiwiYWRtaW4iOnRydWV9.TJVA95...h7HgQ
Response Codes          Backend response or 401 Unauthorized
======================= =================================================
```

According to the [JWS RFC](https://tools.ietf.org/html/rfc7515#section-4.1.10), the JWT/JWS header must contain the following information if correct content is to be provided to the backend:

A `typ` value of `JOSE` can be used by applications to indicate that this object is a JWS or JWE using JWS Compact Serialization or the JWE Compact Serialization. A `typ` value of `JOSE+JSON` can be used by applications to indicate that this object is a JWS or JWE using JWS JSON Serialization or JWE JSON Serialization.

The `cty` (content type) header parameter is used by JWS applications to declare the media type \[IANA.MediaTypes] of the secured content (the payload). To keep messages compact in typical scenarios, it is strongly recommended that senders omit the `application/` prefix of a media type value in a `cty` header parameter when no other `/` appears in the media type value.

{% hint style="info" %}
A recipient using the media type value must treat it as if `application/` were prepended to any `cty` value not containing a `/`.
{% endhint %}

{% tabs %}
{% tab title="Proxy API example" %}
{% hint style="warning" %}
This example will work for [v2 APIs and v4 proxy APIs.](../../overview/gravitee-api-definitions-and-execution-engines.md)

Currently, this policy can **not** be applied at the message level.
{% endhint %}

```
{
 "typ":"JOSE+JSON",
 "cty":"json",
 "alg":"RS256",
 "x5c":"string",
 "kid":"string"
}
```
{% endtab %}
{% endtabs %}

## Configuration

Policies can be added to flows that are assigned to an API or to a plan. Gravitee supports configuring policies [through the Policy Studio](../../guides/policy-design/) in the Management Console or interacting directly with the Management API.

When using the Management API, policies are added as flows either directly to an API or to a plan. To learn more about the structure of the Management API, check out the [reference documentation here.](../management-api-reference/)

{% code title="Sample Configuration" %}
```json
{
 "typ":"JOSE+JSON",
 "cty":"json",
 "alg":"RS256",
 "x5c":"string",
 "kid":"string"
}
```
{% endcode %}

### Reference

<table><thead><tr><th>Property</th><th data-type="checkbox">Required</th><th>Description</th><th>Type</th><th>Default</th></tr></thead><tbody><tr><td>checkCertificateValidity</td><td>false</td><td>Check if the certificate used to sign the JWT is correct and has valid <code>not_before</code> and <code>not_after</code> dates</td><td>boolean</td><td>false</td></tr><tr><td>checkCertificateRevocation</td><td>false</td><td>Check if the certificate used to sign the JWT is not revoked via the CRL Distribution Points. The CRL is stored inside the X509v3 CRL Distribution Extension Points.</td><td>boolean</td><td>false</td></tr></tbody></table>

To validate the token signature, the policy needs to use the JWS validator policy public key set in the APIM Gateway `gravitee.yml` file:

```
policy:
  jws:
    kid:
      default: ssh-rsa myValidationKey anEmail@domain.com
      kid-2016: /filepath/to/pemFile/certificate.pem
```

The policy will inspect the JWT/JWS header to extract the key id (`kid` attribute) of the public key. If no key id is found then it is set to `default`.

The gateway will be able to retrieve the corresponding public key and the JOSE Header using `x5c` (X.509 Certificate Chain). The header parameter will be used to verify certificate information and check that the JWT was signed using the private key corresponding to the specified public key.

### Phases

Policies can be applied to the request or the response of a Gateway API transaction. The request and response are broken up into [phases](broken-reference) that depend on the [Gateway API version](../../overview/gravitee-api-definitions-and-execution-engines.md). Each policy is compatible with a subset of the available phases.

The phases checked below are supported by the JWS policy:

<table data-full-width="false"><thead><tr><th width="202">v2 Phases</th><th width="139" data-type="checkbox">Compatible?</th><th width="198">v4 Phases</th><th data-type="checkbox">Compatible?</th></tr></thead><tbody><tr><td>onRequest</td><td>false</td><td>onRequest</td><td>true</td></tr><tr><td>onResponse</td><td>false</td><td>onResponse</td><td>false</td></tr><tr><td>onRequestContent</td><td>false</td><td>onMessageRequest</td><td>false</td></tr><tr><td>onResponseContent</td><td>false</td><td>onMessageResponse</td><td>false</td></tr></tbody></table>

## Errors

<table data-full-width="false"><thead><tr><th width="210">Phase</th><th width="171">HTTP status code</th><th width="387">Error template key</th></tr></thead><tbody><tr><td>onRequest</td><td><code>401</code></td><td>Bad token format, content, signature, certificate, expired token or any other issue preventing the policy from validating the token</td></tr></tbody></table>

## Changelogs

{% @github-files/github-code-block url="https://github.com/gravitee-io/gravitee-policy-jws/blob/master/CHANGELOG.md" %}
