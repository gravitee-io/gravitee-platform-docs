---
description: This page provides the technical details of the JWT policy
hidden: true
---

# JWT Validator

## Overview

You can use the `jwt` policy to validate the token signature and expiration date before sending the API call to the target backend.

Some authorization servers use OAuth2 protocol to provide access tokens. These access token can be in JWS/JWT format. For the RFC standards, see:

* JWS (JSON Web Signature) standard RFC: [https://tools.ietf.org/html/rfc7515](https://tools.ietf.org/html/rfc7515)
* JWT (JSON Web Token) standard RFC: [https://tools.ietf.org/html/rfc7519](https://tools.ietf.org/html/rfc7519)

A JWT is composed of three parts: A header, a payload and a signature. Each must be base64 encoded. Examples can be found here: [http://jwt.io](http://jwt.io/).

* The header contains attributes indicating the algorithm used to sign the token.
* The payload contains information inserted by the AS (Authorization Server), such as the expiration date and UID of the user.
* The third and last part is the signature (for more details, see the RFC).

Functional and implementation information for the `jwt` policy is organized into the following sections:

* [Examples](jwt-validator.md#examples)
* [Configuration](jwt-validator.md#configuration)
* [Compatibility Matrix](jwt-validator.md#compatibility-matrix)
* [Errors](jwt-validator.md#errors)
* [Changelogs](jwt-validator.md#changelogs)

## Examples

{% hint style="warning" %}
This policy can be applied to v2 APIs and v4 HTTP proxy APIs. It cannot be applied to v4 message APIs or v4 TCP proxy APIs.
{% endhint %}

{% tabs %}
{% tab title="HTTP proxy API example" %}
Given the following JWT claims (payload):

```json
{
  "iss": "Gravitee.io AM",
  "sub": "1234567890",
  "name": "John Doe",
  "admin": true
}
```

You can extract the issuer from JWT using the following Expression Language statement:

```json
{#context.attributes['jwt.claims']['iss']}
```
{% endtab %}
{% endtabs %}

## Configuration

To validate the token signature, the policy needs to use the associated Authorization Servers public key.

The policy prompts you to choose between three (`GIVEN_KEY`, `GIVEN_ISSUER`, `GATEWAY_ISSUER`) methods to retrieve the required public key.

* `GIVEN_KEY` — You provide the key (in `ssh-rsa`, `pem`, `crt` or `public-key` format)
* `GIVEN_ISSUER` — If you want to filter on several authorization servers then you only need to specify the issuer name; the gateway will only accept JWTs with a permitted issuer attribute. If `GATEWAY_KEYS` is set, the issuer is also used to retrieve the public key from the `gravitee.yml` file.
* `GATEWAY_KEYS` — You can set some public keys in the APIM Gateway `gravitee.yml` file

```yaml
policy:
  jwt:
    issuer:
      my.authorization.server:
        default: ssh-rsa myValidationKey anEmail@domain.com
        kid-2016: ssh-rsa myCurrentValidationKey anEmail@domain.com
```

The policy will inspect the JWT:

* Header to extract the key id (`kid` attribute) of the public key. If no key id is found then it use the `x5t` field.
  * If `kid` is present and no key corresponding is found, the token is rejected.
  * If `kid` is missing and no key corresponding to `x5t` is found, the token is rejected.
* Claims (payload) to extract the issuer (`iss` attribute).

Using these two values, the Gateway can retrieve the corresponding public key.

Regarding the `client_id`, the standard behavior is to read it from the `azp` claim, then if not found in the `aud` claim and finally in the `client_id` claim. You can override this behavior by providing a custom `clientIdClaim` in the configuration.

### Phases

The phases checked below are supported by the `jwt` policy:

<table data-full-width="false"><thead><tr><th width="202">v2 Phases</th><th width="137" data-type="checkbox">Compatible?</th><th width="203.41136671177264">v4 Phases</th><th data-type="checkbox">Compatible?</th></tr></thead><tbody><tr><td>onRequest</td><td>true</td><td>onRequest</td><td>true</td></tr><tr><td>onResponse</td><td>false</td><td>onResponse</td><td>false</td></tr><tr><td>onRequestContent</td><td>false</td><td>onMessageRequest</td><td>false</td></tr><tr><td>onResponseContent</td><td>false</td><td>onMessageResponse</td><td>false</td></tr></tbody></table>

### Options

The `jwt` policy can be configured with the following options:

<table><thead><tr><th width="194">Property</th><th width="105" data-type="checkbox">Required</th><th width="224">Description</th><th>Type</th><th>Default</th></tr></thead><tbody><tr><td>publicKeyResolver</td><td>true</td><td>Used to resolve the public key needed to validate the signature</td><td>enum</td><td>GIVEN_KEY</td></tr><tr><td>resolverParameter</td><td>false</td><td>Needed if you use the <code>GATEWAY_KEYS</code> or <code>GIVEN_ISSUER</code> resolver (EL support)</td><td>string</td><td></td></tr><tr><td>useSystemProxy</td><td>false</td><td>Select this option if you want use system proxy (only useful when resolver is <code>JWKS_URL</code>)</td><td>boolean</td><td>false</td></tr><tr><td>extractClaims</td><td>false</td><td>Select this option if you want to extract claims into the request context</td><td>boolean</td><td>false</td></tr><tr><td>clientIdClaim</td><td>false</td><td>Required if the client_id should be read from non-standard claims (azp, aud, client_id)</td><td>string</td><td></td></tr></tbody></table>

#### Confirmation Method validation options

The following options are specific to Confirmation Method validation:

<table><thead><tr><th width="283">Property</th><th width="106" data-type="checkbox">Required</th><th width="338">Description</th><th>Type</th><th>Default</th></tr></thead><tbody><tr><td>confirmationMethodValidation.ignoreMissing</td><td>false</td><td>Will ignore CNF validation if the token doesn’t contain any CNF information.</td><td>boolean</td><td>false</td></tr><tr><td>confirmationMethodValidation.certificateBoundThumbprint.enabled</td><td>false</td><td>Will validate the certificate thumbprint extracted from the access_token using the one provided by the client.</td><td>boolean</td><td>false</td></tr><tr><td>confirmationMethodValidation.certificateBoundThumbprint.extractCertificateFromHeader</td><td>false</td><td>Enabled to extract the client certificate from request header. Necessary when the M-TLS connection is handled by a proxy.</td><td>boolean</td><td>false</td></tr><tr><td>confirmationMethodValidation.certificateBoundThumbprint.headerName</td><td>false</td><td>Name of the header under which to find the client certificate.</td><td>string</td><td>ssl-client-cert</td></tr></tbody></table>

### Attributes

The `jwt` policy can be configured with the following attributes:

<table><thead><tr><th width="159.5">Name</th><th>Description</th></tr></thead><tbody><tr><td>jwt.token</td><td>JWT token extracted from the <code>Authorization</code> HTTP header</td></tr><tr><td>jwt.claims</td><td>A map of claims registered in the JWT token body, used for extracting data from it. Only if <code>extractClaims</code> is enabled in the policy configuration.</td></tr></tbody></table>

## Compatibility matrix

The following is the compatibility matrix for APIM and the `jwt` policy:

| Plugin version   | Supported APIM versions |
| ---------------- | ----------------------- |
| 4.x+             | 4.0.x+                  |
| 2.x+             | 3.18.x to 3.20          |
| 1.22.x+          | 3.15.x to 3.17.x        |
| 1.20.x to 1.21.x | 3.10.x to 3.14.x        |
| Up to 1.19.x     | Up to 3.9.x             |

## Errors

<table data-full-width="false"><thead><tr><th width="205.5">HTTP status code</th><th width="387">Error template key</th></tr></thead><tbody><tr><td><code>401</code></td><td>Bad token format, content, signature, expired token or any other issue preventing the policy from validating the token</td></tr></tbody></table>

You can use the response template feature to override the default response provided by the policy. These templates must be defined at the API level (see the API Console **Response Templates** option in the API **Proxy** menu).

The error keys sent by the policy are as follows:

| Key                 | Parameters |
| ------------------- | ---------- |
| JWT\_MISSING\_TOKEN | -          |
| JWT\_INVALID\_TOKEN | -          |

## Changelogs

{% @github-files/github-code-block url="https://github.com/gravitee-io/gravitee-policy-jwt/blob/master/CHANGELOG.md" %}
