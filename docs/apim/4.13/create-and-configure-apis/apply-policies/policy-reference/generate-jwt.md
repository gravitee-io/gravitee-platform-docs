---
description: An overview about the Generate JWT policy.
metaLinks:
  alternates:
    - generate-jwt.md
---

# Generate JWT

## Overview

You use the `generate-JWT` policy to generate a signed JWT with a configurable set of claims. This JWT can subsequently be forwarded to backend targets, or used in some other way.

When a signed JWT is generated, it is put in the `jwt.generated` attribute of the request execution context.

## Examples

{% hint style="warning" %}
This policy can be applied to v2 APIs, v4 HTTP proxy APIs, and v4 message APIs. It cannot be applied to v4 TCP proxy APIs.
{% endhint %}

#### HTTP proxy API example

Sample policy configuration:

```json
"policy-generate-jwt": {
    "signature":"RSA_RS256",
    "expiresIn":30,
    "expiresInUnit":"SECONDS",
    "issuer":"urn://gravitee-api-gw",
    "audiences":["graviteeam"],
    "customClaims":[],
    "id":"817c6cfa-6ae6-446e-a631-5ded215b404b",
    "content":"-----BEGIN PRIVATE KEY-----\nMIIEvgIBADANBgkqhkiG9w0BAQEFAASCBKgwggSkAgEAAoIBAQDg0MY5LcTnpM/N\nd9ohW/mls6CqF3PoVocwUpKSb324QFuSGvo5s2qzM1JkR2uNTS5lapGltF0Krc5j\nmUgKqVZUx3ie76ngvHTVrz9qNHe9znsTFndtpsaFZuNIiGT8X+eAYgqKUaoKA+3y\nNWynEmXL9ywtFtGommPO1iBwMYfbucuxBmwtklkzxCrFGftAsTJANy8T+CV61TpB\nP2LbFVngfT0uDgjfoG/KMSBUZR88YZNvEyj1mEDPvZPZD6vYUBlTMlWgAwAD+pUn\n6b/a1BsZ69mMvMzvOg9NhuwMLwGDwQ45Gh51Swnzk6a/Oamgpa/ehySfZkypJhPL\ndiutySELAgMBAAECggEBALjo/yFok9wzovfM7I0jqWKxLCS6xYsEII2OXSA0s6Mo\nzCiQJ9/twoVCYTI5zCycntyrmsBAaYavDmK9YJPkVC3HI18WoRNH7pETY4VnQlXL\nz08T24dE9WQkDC1MgkNSXocqHKFIKiOyt7PQXV3NtAzfcGZlrmyPECi/1k5xbt05\nmU1AaM0HAKP5kGmoANEWyaPhYSrShD3EQH8QEjPwrmua62e7kas7x5u5u01tFndv\nG1/rYlApvruwoczBdD3R8WQEdziFn09IcGZUnpBWDkPlEn62qLW8/3k+uF9An9dd\n1c0IoyNopefLvm9W4CXtzFEzJsre32BIutpj66EECAECgYEA+2GYTmd7lVAAMgj/\nMes+HNVqRtg5OiAggx6qvjhi+6hhMLeVKS8mqslMQXewHthbY0+PdyvKRCZnNURj\nUmeZxxk04kOJZqN5ak45NJ6T10PnlZ0vtf2Ym9Mmi4Q29Mzk9SCR9NtVuwRHhGmP\nzOPCXQCwFHeVkqzqkYHIji1ko0sCgYEA5PI5WkWFG/uAPxVZbQreyD1iRgTxEz8B\nn1XefxQ1IV8L5/n48XAgeK1NUbhr4jPSbXL98mX5/RdyCmZORdbPLDRqSVrRepQ3\nAXF82Xp2X9Py/Gn/pIZPXEW54ctnEiW8WVRD2XQ2df1sUq+H5gX/RraiI2O9/CyF\nixZkkC4tIUECgYEAw/lt15HtUpYv0NIawTv4DFqEo/5lft8U+aOq0Oj8ody/CE/W\nxWiw6GxOOquobiOV+3JHEkzdPwwBYhGSrOd/hywrgknMkGvZd/rLti36a9PQc187\nltHBa5nNbu8AORCTXlap8w4bY9UOPDhflwfousCShSJFRTfxFsbrJ4xT7MkCgYBQ\np8TsuHEcWo3jq3HFqH6zrGxinnsPfLLlnyqzOjs9dm6LWtUIuae229bRY1ceaYNI\na6prKuHW99uFLmWE1RhHSm/nR8dkl7KJH6IMO8hYGiMQKYeWPnrW1vmVQkMdcY3Z\nKoZ8pSRKjO0MdCo8LwCvuMeGEC1uGYEybsEeyiW8AQKBgBnkExWeD6KQQL9rrImq\nwhPqz9yuMpIsBtf93fDLXwmy/0VG9L6uDf/3MKl+RYs4PQGe+QQSmXTgqcbHr5ug\nNEFDDK0C9k0Gd0Zl/Z29H6vZWJH9E4ur/xZToeADc3sQT/Ga78LwF8s5EtOPuGVD\nOyCUoLQJgofJWKk2Tp5gKogB\n-----END PRIVATE KEY-----"
}
```

## Configuration

### Phases

The phases checked below are supported by the `generate-JWT` policy:

<table data-full-width="false"><thead><tr><th width="202">v2 Phases</th><th width="139" data-type="checkbox">Compatible?</th><th width="198">v4 Phases</th><th data-type="checkbox">Compatible?</th></tr></thead><tbody><tr><td>onRequest</td><td>true</td><td>onRequest</td><td>true</td></tr><tr><td>onResponse</td><td>false</td><td>onResponse</td><td>false</td></tr><tr><td>onRequestContent</td><td>false</td><td>onMessageRequest</td><td>false</td></tr><tr><td>onResponseContent</td><td>false</td><td>onMessageResponse</td><td>false</td></tr></tbody></table>

### Options

The `generate-JWT` policy can be configured with the following options:

<table>
    <thead>
        <tr>
            <th width="131">Property</th>
            <th width="103" data-type="checkbox">Required</th>
            <th width="210">Description</th>
            <th>Type</th>
            <th>Default</th>
        </tr>
    </thead>
    <tbody>
        <tr>
            <td>signature</td>
            <td>true</td>
            <td>Signature used to sign the token</td>
            <td>Algorithm</td>
            <td>RS256</td>
        </tr>
        <tr>
            <td>kid</td>
            <td>false</td>
            <td>key ID (<code>kid</code>) to include in the JWT header</td>
            <td>string</td>
            <td>-</td>
        </tr>
        <tr>
            <td>id</td>
            <td>false</td>
            <td>JWT ID (<code>jti</code>) claim is a unique identifier for the JWT</td>
            <td>string</td>
            <td>UUID</td>
        </tr>
        <tr>
            <td>audiences</td>
            <td>false</td>
            <td>JWT audience claim. Accepts a string or an array of strings</td>
            <td>List of string</td>
            <td>-</td>
        </tr>
        <tr>
            <td>issuer</td>
            <td>false</td>
            <td>Claim that identifies the issuer of the JWT</td>
            <td>string</td>
            <td>-</td>
        </tr>
        <tr>
            <td>subject</td>
            <td>false</td>
            <td>Claim that identifies or makes a statement about the subject of the JWT</td>
            <td>string</td>
            <td>-</td>
        </tr>
        <tr>
            <td>x509CertificateChain</td>
            <td>false</td>
            <td>Adds the certificate chain resolved from the key material as an <code>x5c</code> header. RS256 only. Valid values: <code>NONE</code>, <code>X5C</code></td>
            <td>string</td>
            <td>NONE</td>
        </tr>
        <tr>
            <td>x509CertSha1Thumbprint</td>
            <td>false</td>
            <td>Adds the SHA-1 thumbprint of the signing certificate as an <code>x5t</code> header. RS256 only</td>
            <td>boolean</td>
            <td>false</td>
        </tr>
        <tr>
            <td>x509CertSha256Thumbprint</td>
            <td>false</td>
            <td>Adds the SHA-256 thumbprint of the signing certificate as an <code>x5t#S256</code> header. RS256 only</td>
            <td>boolean</td>
            <td>false</td>
        </tr>
    </tbody>
</table>

### Attributes

The `generate-JWT` policy can be configured with the following attributes:

| Name            | Description                                                                         |
| --------------- | ----------------------------------------------------------------------------------- |
| `jwt.generated` | JWT generated by the policy |

Read the token with `{#context.attributes['jwt.generated']}` in any field that supports the [Gravitee Expression Language](../../../gravitee-expression-language.md).

### X.509 certificate headers

Use the following options to add X.509 certificate headers (RFC 7515) to the protected header of JWTs signed with RS256:

* `x509CertificateChain`: Set to `X5C` to add the certificate chain of the signing certificate as an `x5c` header.
* `x509CertSha1Thumbprint`: Set to `true` to add the SHA-1 thumbprint of the DER-encoded signing certificate, in base64url form, as an `x5t` header (RFC 7515, section 4.1.7).
* `x509CertSha256Thumbprint`: Set to `true` to add the SHA-256 thumbprint of the DER-encoded signing certificate, in base64url form, as an `x5t#S256` header (RFC 7515, section 4.1.8).

The three options are independent of each other, and all of them are off by default. Both thumbprints hash only the signing certificate itself, never the other certificates of the chain.

The policy resolves the signing certificate from the configured key resolver:

* `INLINE` and `PEM`: Include the certificate, and optionally its chain, in the key material next to the private key. The policy selects the certificate whose public key matches the signing key and builds the `x5c` chain from that certificate outward. Certificates that don't link into that chain are dropped from the `x5c` header, and the gateway logs a warning.
* `JKS` and `PKCS12`: The policy uses the certificate chain that the keystore returns for the configured alias. The `x5c` header embeds that chain as stored in the keystore. The thumbprint headers require the first certificate of that chain to match the signing key.

If `x509CertSha1Thumbprint` or `x509CertSha256Thumbprint` is enabled and no certificate matching the signing key is available, the policy rejects every request with HTTP `500` and the message `Unable to generate JWT token`, logs the reason on the gateway, and doesn't generate a JWT. The `x5c` option behaves the same way for the `INLINE` and `PEM` key resolvers when the key material contains no usable certificate. For the `JKS` and `PKCS12` key resolvers, a missing certificate chain doesn't fail the request: the policy signs the JWT without the `x5c` header and logs a warning. If the chain is present but its first certificate doesn't match the signing key, the policy still embeds that chain as `x5c` and logs a warning; only the thumbprint headers are suppressed in that case.

When the signature is an HMAC algorithm, the three certificate options have no effect. The JWT is generated without certificate headers, no error is logged, and the Console disables the corresponding fields.

The policy resolves the signing key and certificate on first use and keeps them for the lifetime of the gateway process. After you rotate the key material, for example by replacing a keystore file at the same path, restart the gateway to pick up the new certificate.

The following example adds both thumbprint headers to JWTs signed with a PEM key file that includes the signing certificate:

```json
"policy-generate-jwt": {
    "signature": "RSA_RS256",
    "keyResolver": "PEM",
    "content": "/path/to/private-key-with-certificate.pem",
    "x509CertSha1Thumbprint": true,
    "x509CertSha256Thumbprint": true
}
```

## Compatibility matrix

The following is the compatibility matrix for APIM and the `generate-JWT` policy.

<table data-full-width="false">
    <thead>
        <tr>
            <th>Plugin Version</th>
            <th>Supported APIM versions</th>
        </tr>
    </thead>
    <tbody>
        <tr>
            <td>Up to 1.8.x</td>
            <td>All</td>
        </tr>
        <tr>
            <td>1.9.0 and later</td>
            <td>4.13.0 and later</td>
        </tr>
    </tbody>
</table>

## Errors

<table data-full-width="false">
    <thead>
        <tr>
            <th width="180">Phase</th>
            <th width="171">HTTP status code</th>
            <th width="387">Message</th>
        </tr>
    </thead>
    <tbody>
        <tr>
            <td>onRequest</td>
            <td><code>500</code></td>
            <td><code>Unable to generate JWT token</code></td>
        </tr>
    </tbody>
</table>

### Nested objects

To limit the processing time in the case of a nested object, the default max depth of a nested object has been set to 1000. This default value can be overridden using the environment variable `gravitee_policy_jsonxml_maxdepth`.

## Changelogs

{% @github-files/github-code-block url="https://github.com/gravitee-io/gravitee-policy-generate-jwt/blob/master/CHANGELOG.md" %}
