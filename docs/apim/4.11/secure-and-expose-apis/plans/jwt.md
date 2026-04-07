---
description: An overview about jwt.
metaLinks:
  alternates:
    - jwt.md
---

# JWT

## Overview

A JSON Web Token (JWT) is an open method for representing claims securely between two parties. It is digitally signed using an HMAC shared key or RSA public/private key pair. The JWT authentication type ensures that a JWT issued by a third party is valid by verifying its signature and expiration date. Only applications with approved JWTs can access APIs associated with a JWT plan.

{% hint style="info" %}
When an Identity Provider does not fully support the [OAuth2](oauth2.md) standard, use the JWT Plan .

For example, Azure Entra ID does not provide a token introspection endpoint. So, you must use the JWT Plan with the JWKS\_URL resolver like `https://login.microsoft.com/{tenant_id}/discovery/v2.0/keys` to introspect, validate, and extract token custom claims.
{% endhint %}

## Configuration

APIM uses client IDs to recognize applications that have subscribed to a JWT plan. The inbound JWT payload must include the `client_id` claim to establish a connection between the JWT and the APIM application subscription.

A JWT plan presents the following configuration options:

<figure><img src="../../.gitbook/assets/plan_jwt configure (1).png" alt=""><figcaption></figcaption></figure>

* **Signature:** Select the algorithm used to hash and encrypt your JWT
* **JWKS resolver:** Select a method to retrieve the JSON Web Key (JWK), which is often stored inside a JSON Web Key Set (JWKS) and required by the Gateway to validate the signature of the JWT:
  * **GIVEN\_KEY**: Provide a signature key as a resolver parameter according to the signature algorithm (`ssh-rsa`, `pem`, `crt` or `public-key` format
  *   **GATEWAY\_KEYS:** Search for public keys set in the API Gateway `gravitee.yml` configuration that match the authorization server `iss` (issuer) and `kid` (key ID) claims of the incoming JWT

      \{% code title="gravitee.yml" %\}

      ```yaml
      jwt:
        issuer:
          my.authorization.server:
            default: ssh-rsa myValidationKey anEmail@domain.com
            kid-2016: ssh-rsa myCurrentValidationKey anEmail@domain.com
      ```

      \{% endcode %\} \* **JWKS\_URL**: Provide a URL ending with `/.well-known/jwks.json` from which the Gateway can retrieve the JWKS
* **Use system proxy:** When using **JWKS\_URL**, optionally route the JWKS retrieval call through the Gateway's [system proxy](../../self-hosted-installation-guides/proxy-configuration/system-proxy-for-backend-apis.md). Enable this option when the Gateway reaches external identity providers (for example, Microsoft Entra ID or Google) through a corporate proxy.
*   **Extract JWT Claims:** Allow claims to be accessed in the `jwt.claims` context attribute during request/response via Gravitee Expression Language (EL), e.g., extract the issuer claim from the JWT:

    ```
    {#context.attributes['jwt.claims']['iss']}
    ```
* **Propagate Authorization header:** Propagate the header containing the JWT token to the backend APIs
* **User claim:** Set the payload claim where the user can be extracted. The default `sub` value is standard with JWTs.
* **Client ID claim:** Override the default claim where the client ID can be extracted. By default, the Gateway checks the `azp` claim, then the `aud` claim, and finally the `client_id` claim.
* **Ignore missing CNF:** Ignores CNF validation if the token doesn't contain any CNF information
* **Enable certificate bound thumbprint validation:** Validates the certificate thumbprint extracted from the `access_token` against the one provided by the client
* **Extract client certificate from headers:** Extracts the client certificate from the request header (provided in **Header name** field). Necessary when the mTLS connection is handled by a proxy.
* **Additional selection rule:** Allows you to use the EL to filter by contextual data (request headers, tokens, attributes, etc.) for plans of the same type (e.g., for two JWT plans, you can set different selection rules on each plan to determine which plan handles each request)

### JWKS retrieval through a corporate proxy

In enterprise environments where the Gateway reaches external identity providers through a corporate proxy, enable **Use system proxy** in the JWT plan configuration. This routes outbound JWKS retrieval calls (for example, to Microsoft Entra ID, Google, or Okta) through the system proxy configured at the Gateway level.

To configure the system proxy on the Gateway, see [System Proxy for Backend APIs](../../self-hosted-installation-guides/proxy-configuration/system-proxy-for-backend-apis.md).

{% hint style="warning" %}
**Adjust timeouts for proxy environments**

The default `connectTimeout` and `requestTimeout` for JWKS retrieval are both **2000 ms**. In environments where traffic routes through a corporate proxy, increase these values to account for additional proxy latency. Recommended starting values for enterprise proxy environments:

* `connectTimeout`: **5000 ms**
* `requestTimeout`: **10000 ms**

Configure these values in the JWT plan settings or in the API definition JSON.
{% endhint %}

Once JWT configuration is complete and the plan is created and published, your API will be JWT-secured and subscribed consumers must call the API with an `Authorization: Bearer your-JWT` HTTP header.
