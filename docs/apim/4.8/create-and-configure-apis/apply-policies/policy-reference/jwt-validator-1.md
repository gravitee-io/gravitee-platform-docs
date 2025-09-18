---
hidden: true
noIndex: true
---

# 4.9 JWT Validator

## Overview

You can use the `jwt` policy to validate the token signature and expiration date before sending the API call to the target backend.

Some authorization servers use OAuth2 protocol to provide access tokens. These access token can be in JWS/JWT format. For the RFC standards, see:

* JWS (JSON Web Signature) standard RFC: [https://tools.ietf.org/html/rfc7515](https://tools.ietf.org/html/rfc7515)
* JWT (JSON Web Token) standard RFC: [https://tools.ietf.org/html/rfc7519](https://tools.ietf.org/html/rfc7519)

A JWT is composed of three parts: a header, a payload and a signature. You can see some examples here: [http://jwt.io](https://www.jwt.io/).

* The header contains attributes indicating the algorithm used to sign the token.
* The payload contains some information inserted by the AS (Authorization Server), such as the expiration date and UID of the user.

Both the header and payload are encoded with Base64, so anyone can read the content.

* The third and last part is the signature (for more details, see the RFC).

### Usage

The policy will inspect the JWT:

* Header to extract the key id (`kid` attribute) of the public key. If no key id is found then it uses the `x5t` field.
  * If `kid` is present and no key corresponding is found, the token is rejected.
  * If `kid` is missing and no key corresponding to `x5t` is found, the token is rejected.
* Claims (payload) to extract the issuer (`iss` attribute)

Using these two values, the gateway can retrieve the corresponding public key.

Regarding the client\_id, the standard behavior is to read it from the `azp` claim, then if not found in the `aud` claim and finally in the `client_id` claim. You can override this behavior by providing a custom `clientIdClaim` in the configuration.

### Attributes

| Name       | Description                                                                                                                                         |
| ---------- | --------------------------------------------------------------------------------------------------------------------------------------------------- |
| jwt.token  | JWT token extracted from the `Authorization` HTTP header                                                                                            |
| jwt.claims | A map of claims registered in the JWT token body, used for extracting data from it. Only if `extractClaims` is enabled in the policy configuration. |

### **Example**

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

```bash
 {#context.attributes['jwt.claims']['iss']} 
```

### Errors

These templates are defined at the API level, in the "Entrypoint" section for v4 APIs, or in "Response Templates" for v2 APIs. The error keys sent by this policy are as follows:

| Key                                          |
| -------------------------------------------- |
| JWT\_MISSING\_TOKEN                          |
| JWT\_INVALID\_TOKEN                          |
| JWT\_INVALID\_CERTIFICATE\_BOUND\_THUMBPRINT |
| JWT\_REVOKED                                 |

## Phases

The `jwt` policy can be applied to the following API types and flow phases.

### Compatible API types

* `PROXY`
* `MESSAGE`

### Supported flow phases:

* Request

## Compatibility matrix

Strikethrough text indicates that a version is deprecated.

| Plugin version       | APIM                 |
| -------------------- | -------------------- |
| 6.x                  | 4.6.x to latest      |
| 5.x                  | 4.4.x to 4.5.x       |
| 4.x                  | 4.0.x to 4.3.x       |
| ~~2.x~~              | ~~3.18.x to 3.20.x~~ |
| ~~1.22.x~~           | ~~3.15.x to 3.17.x~~ |
| ~~1.20.x to 1.21.x~~ | ~~3.10.x to 3.14.x~~ |
| ~~Up to 1.19.x~~     | ~~Up to 3.9.x~~      |

### Configuration

#### Gateway configuration

**System proxy**

If the option useSystemProxy is checked, proxy information will be read from JVM\_OPTS, or from the gravitee.yml file if JVM\_OPTS is not set.

**Gateway keys**

If the JWKS resolver is set to GATEWAY\_KEYS then keys will be read from JVM\_OPTS, or from the gravitee.yml file if JVM\_OPTS is not set.

Examples:

gravitee.yml

```yaml
system:
  proxy:
    type: HTTP      # HTTP, SOCK4, SOCK5
    host: localhost
    port: 3128
    username: user
    password: secret
```

gravitee.yml

```yaml
policy:
  jwt:
    issuer:
      my.authorization.server:
        default: ssh-rsa myValidationKey anEmail@domain.com
        kid-2016: ssh-rsa myCurrentValidationKey anEmail@domain.com
```

#### Configuration options

| <p>Name<br><code>json name</code></p>                                              | <p>Type<br><code>constraint</code></p> | Mandatory | Default     | Description                                                                                                                                                                                                             |
| ---------------------------------------------------------------------------------- | -------------------------------------- | :-------: | ----------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| <p>Client ID claim<br><code>clientIdClaim</code></p>                               | string                                 |           |             | Claim where the client ID can be extracted. Configuring this field will override the standard behavior.                                                                                                                 |
| <p>Confirmation Method Validation<br><code>confirmationMethodValidation</code></p> | object                                 |           |             | <p><br>See "Confirmation Method Validation" section.</p>                                                                                                                                                                |
| <p>JWKS URL connect timeout<br><code>connectTimeout</code></p>                     | integer                                |           | `2000`      | Only applies when the resolver is JWKS\_URL                                                                                                                                                                             |
| <p>Extract JWT Claims<br><code>extractClaims</code></p>                            | boolean                                |           |             | Put claims into the 'jwt.claims' context attribute.                                                                                                                                                                     |
| <p>Follow HTTP redirects<br><code>followRedirects</code></p>                       | boolean                                |           |             | Only applies when the resolver is JWKS\_URL                                                                                                                                                                             |
| <p>Propagate Authorization header<br><code>propagateAuthHeader</code></p>          | boolean                                |           | `true`      | Allows to propagate Authorization header to the target endpoints                                                                                                                                                        |
| <p>JWKS resolver<br><code>publicKeyResolver</code></p>                             | enum (string)                          |     ✅     | `GIVEN_KEY` | <p>Define how the JSON Web Key Set is retrieved<br>Values: <code>GIVEN_KEY</code> <code>GATEWAY_KEYS</code> <code>JWKS_URL</code></p>                                                                                   |
| <p>JWKS URL request timeout<br><code>requestTimeout</code></p>                     | integer                                |           | `2000`      | Only applies when the resolver is JWKS\_URL                                                                                                                                                                             |
| <p>Resolver parameter<br><code>resolverParameter</code></p>                        | string                                 |           |             | Set the signature key GIVEN\_KEY or a JWKS\_URL following selected resolver (support EL).                                                                                                                               |
| <p>Revocation Check<br><code>revocationCheck</code></p>                            | object                                 |           |             | <p>Define revocation check details. If enabled, will check the configured claim of the token against a cached revocation list and deny if a match is found. Disabled by default.<br>See "Revocation Check" section.</p> |
| <p>Signature<br><code>signature</code></p>                                         | enum (string)                          |     ✅     | `RSA_RS256` | <p>Define how the JSON Web Token must be signed.<br>Values: <code>RSA_RS256</code> <code>RSA_RS384</code> <code>RSA_RS512</code> <code>HMAC_HS256</code> <code>HMAC_HS384</code> <code>HMAC_HS512</code></p>            |
| <p>Token Type Validation<br><code>tokenTypValidation</code></p>                    | object                                 |           |             | <p>Define the token type to validate<br>See "Token Type Validation" section.</p>                                                                                                                                        |
| <p>Use system proxy<br><code>useSystemProxy</code></p>                             | boolean                                |           |             | Use system proxy (make sense only when resolver is set to JWKS\_URL)                                                                                                                                                    |
| <p>User claim<br><code>userClaim</code></p>                                        | string                                 |           | `sub`       | Claim where the user can be extracted                                                                                                                                                                                   |

**Confirmation Method Validation (Object)**

| <p>Name<br><code>json name</code></p>                                                     | <p>Type<br><code>constraint</code></p> | Mandatory | Default | Description                                                                                    |
| ----------------------------------------------------------------------------------------- | -------------------------------------- | :-------: | ------- | ---------------------------------------------------------------------------------------------- |
| <p>Certificate Bound thumbprint (x5t#S256)<br><code>certificateBoundThumbprint</code></p> | object                                 |           |         | <p><br>See "Certificate Bound thumbprint (x5t#S256)" section.</p>                              |
| <p>Ignore missing CNF<br><code>ignoreMissing</code></p>                                   | boolean                                |           |         | Will ignore CNF validation if the token doesn't contain any CNF information. Default is false. |

**Certificate Bound thumbprint (x5t#S256) (Object)**

| <p>Name<br><code>json name</code></p>                                                       | <p>Type<br><code>constraint</code></p> | Mandatory | Default           | Description                                                                                                                          |
| ------------------------------------------------------------------------------------------- | -------------------------------------- | :-------: | ----------------- | ------------------------------------------------------------------------------------------------------------------------------------ |
| <p>Enable certificate bound thumbprint validation<br><code>enabled</code></p>               | boolean                                |           |                   | Will validate the certificate thumbprint extracted from the access\_token with the one provided by the client. The default is false. |
| <p>Extract client certificate from headers<br><code>extractCertificateFromHeader</code></p> | boolean                                |           |                   | Enabled to extract the client certificate from request header. Necessary when the M-TLS connection is handled by a proxy.            |
| <p>Header name<br><code>headerName</code></p>                                               | string                                 |           | `ssl-client-cert` | Name of the header where to find the client certificate.                                                                             |

**Revocation Check (Object)**

| <p>Name<br><code>json name</code></p>                                   | <p>Type<br><code>constraint</code></p> | Mandatory | Default | Description                                                                                                                                                                  |
| ----------------------------------------------------------------------- | -------------------------------------- | :-------: | ------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `additionalProperties`                                                  | string                                 |           |         |                                                                                                                                                                              |
| <p>Revocation list security configuration<br><code>auth</code></p>      | object                                 |           |         | <p><br>See "Revocation list security configuration" section.</p>                                                                                                             |
| <p>Revocation list connect timeout<br><code>connectTimeout</code></p>   | integer                                |           | `2000`  | The connect timeout in milliseconds for retrieving the revocation list. Default is 2000.                                                                                     |
| <p>Enable revocation check<br><code>enabled</code></p>                  | boolean                                |           |         | Will check if the token has been revoked. Default is false.                                                                                                                  |
| <p>Revocation list follow redirects<br><code>followRedirects</code></p> | boolean                                |           |         | If should follow redirects for revocation list requests. Default is false.                                                                                                   |
| <p>Revocation list refresh interval<br><code>refreshInterval</code></p> | integer                                |           | `300`   | The refresh interval in seconds for the cached revocation list. Default is 300.                                                                                              |
| <p>Revocation list request timeout<br><code>requestTimeout</code></p>   | integer                                |           | `2000`  | The request timeout in milliseconds for retrieving the revocation list. Default is 2000.                                                                                     |
| <p>Revocation claim<br><code>revocationClaim</code></p>                 | string                                 |           | `jti`   | The string claim which will be checked against the revocation list. Default is 'jti'.                                                                                        |
| <p>Revocation list URL<br><code>revocationListUrl</code></p>            | string                                 |           |         | The URL of the revocation list including protocol, should return a new line separated list of strings, content type text/plain. No default is provided, required if enabled. |
| <p>Revocation list use system proxy<br><code>useSystemProxy</code></p>  | boolean                                |           |         | If should use system proxy for revocation list requests. Default is false.                                                                                                   |

**Revocation list security configuration (Object)**

| <p>Name<br><code>json name</code></p> | <p>Type<br><code>constraint</code></p> | Mandatory | Description                                                                                                              |
| ------------------------------------- | -------------------------------------- | :-------: | ------------------------------------------------------------------------------------------------------------------------ |
| <p>Type<br><code>type</code></p>      | object                                 |     ✅     | <p>Type of Revocation list security configuration<br>Values: <code>none</code> <code>basic</code> <code>token</code></p> |

**Revocation list security configuration: No security `type = "none"`**

| <p>Name<br><code>json name</code></p> | <p>Type<br><code>constraint</code></p> | Mandatory | Default | Description |
| ------------------------------------- | -------------------------------------- | :-------: | ------- | ----------- |
| No properties                         |                                        |           |         |             |

**Revocation list security configuration: Basic security `type = "basic"`**

| <p>Name<br><code>json name</code></p>                           | <p>Type<br><code>constraint</code></p> | Mandatory | Default | Description                                                  |
| --------------------------------------------------------------- | -------------------------------------- | :-------: | ------- | ------------------------------------------------------------ |
| <p>Basic authentication configuration<br><code>basic</code></p> | object                                 |     ✅     |         | <p><br>See "Basic authentication configuration" section.</p> |

**Basic authentication configuration (Object)**

| <p>Name<br><code>json name</code></p>    | <p>Type<br><code>constraint</code></p>  | Mandatory | Description                                                                          |
| ---------------------------------------- | --------------------------------------- | :-------: | ------------------------------------------------------------------------------------ |
| <p>Password<br><code>password</code></p> | <p>string<br><code>[1, +Inf]</code></p> |     ✅     | Password which will be added to Authorization header in format 'basic user:password' |
| <p>Username<br><code>username</code></p> | <p>string<br><code>[1, +Inf]</code></p> |     ✅     | Username which will be added to Authorization header in format 'basic user:password' |

**Revocation list security configuration: Token security `type = "token"`**

| <p>Name<br><code>json name</code></p>                           | <p>Type<br><code>constraint</code></p> | Mandatory | Default | Description                                                  |
| --------------------------------------------------------------- | -------------------------------------- | :-------: | ------- | ------------------------------------------------------------ |
| <p>Token authentication configuration<br><code>token</code></p> | object                                 |     ✅     |         | <p><br>See "Token authentication configuration" section.</p> |

**Token authentication configuration (Object)**

| <p>Name<br><code>json name</code></p>    | <p>Type<br><code>constraint</code></p>  | Mandatory | Description                                                                 |
| ---------------------------------------- | --------------------------------------- | :-------: | --------------------------------------------------------------------------- |
| <p>Token value<br><code>value</code></p> | <p>string<br><code>[1, +Inf]</code></p> |     ✅     | Token value which will be added to Authorization header in format 'bearer ' |

**Token Type Validation (Object)**

| <p>Name<br><code>json name</code></p>                          | <p>Type<br><code>constraint</code></p> | Mandatory | Default | Description                                                                                                              |
| -------------------------------------------------------------- | -------------------------------------- | :-------: | ------- | ------------------------------------------------------------------------------------------------------------------------ |
| <p>Enable token type validation<br><code>enabled</code></p>    | boolean                                |           |         | Will validate the token type extracted from the access\_token with the one provided by the client. The default is false. |
| <p>Expected values<br><code>expectedValues</code></p>          | array (string)                         |           | `[JWT]` | List of expected token types. If the token type is not in the list, the validation will fail.                            |
| <p>Ignore case<br><code>ignoreCase</code></p>                  | boolean                                |           |         | Will ignore the case of the token type when comparing the expected values. Default is false.                             |
| <p>Ignore missing token type<br><code>ignoreMissing</code></p> | boolean                                |           |         | Will ignore token type validation if the token doesn't contain any token type information. Default is false.             |

### Changelogs

{% @github-files/github-code-block url="https://github.com/gravitee-io/gravitee-policy-jwt/blob/master/CHANGELOG.md" %}
