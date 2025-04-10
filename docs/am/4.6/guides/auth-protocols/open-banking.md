# Open Banking

## Overview

[FAPI 1.0: Baseline](https://openid.net/specs/openid-financial-api-part-1-1_0.html) & [FAPI 1.0: Advanced](https://openid.net/specs/openid-financial-api-part-2-1_0.html) constitute the Financial-grade API (a.k.a OpenBanking). It is a highly secured OAuth profile that aims to provide specific implementation guidelines for security and interoperability.

## Protocol

FAPI 1.0 is based on [OAuth 2.0](https://tools.ietf.org/html/rfc6749) & [OpenID Connect](https://openid.net/connect) and will restrict some behaviors for security purposes. For example, with FAPI the client authentication mode is limited to `tls_client_auth` or `private_key_jwt` and the JWT signing algorithm must be PS256.

AM will perform some controls during the authentication flows in order to assure that the FAPI rules are respected.

To activate the FAPI profile on your security domain:

* Click **Settings > OIDC-Profile**
* Select the profile to enable
* Save your choice

## Configuration

FAPI expects secure communication between a Client and the Authorization Server, that’s why TLS v1.2 or v1.3 is required with a limited list of cipher suites. In order to enable TLS on the AM Gateway, please update the `gravitee.yaml` as below :

{% code overflow="wrap" %}
```yaml
http:
  secured: true
  ssl:
    clientAuth: request # Supports none, request, required
    tlsProtocols: TLSv1.2, TLSv1.3
    keystore:
      type: jks # Supports jks, pem, pkcs12
      path: ${gravitee.home}/security/keystore.jks
      password: secret
    truststore:
      type: jks # Supports jks, pem, pkcs12
      path: ${gravitee.home}/security/truststore.jks
      password: secret
    ciphers: TLS_DHE_RSA_WITH_AES_128_GCM_SHA256 , TLS_ECDHE_RSA_WITH_AES_128_GCM_SHA256, ...
```
{% endcode %}

## Client Registration

In order to provide a client configuration compatible with FAPI, the client have to register using the [Dynamic Client Registration](https://openid.net/specs/openid-connect-registration-1_0.html) endpoint.

Here's an example of a payload for a client following the FAPI 1.0.

{% code overflow="wrap" %}
```json
{
        "redirect_uris": ["https://mybank.com/callback"],
        "client_name": "client1",
        "application_type" : "web",
        "grant_types": [ "authorization_code","refresh_token"],
        "response_types" : [
                "code",
                "code id_token token",
                "code id_token",
                "code token"
        ],
        "scope":"openid payments",
        "jwks_uri": "https://mybank.com/.well-known/jwks_uri.json",
        "default_acr_values" : ["urn:mace:incommon:iap:silver"],
        "authorization_signed_response_alg" : "PS256",
        "id_token_signed_response_alg" : "PS256",
        "request_object_signing_alg" : "PS256",
        "token_endpoint_auth_method" : "tls_client_auth",
        "tls_client_auth_subject_dn": "C=FR, ST=France, L=Lille, O=mybank, OU=Client1, CN=mycompamybankgny.com, EMAILADDRESS=contact@mybank.com",
        "tls_client_certificate_bound_access_tokens": true,
        "tls_client_auth_san_dns": null,
        "tls_client_auth_san_uri": null,
        "tls_client_auth_san_ip": null,
        "tls_client_auth_san_email": null,
      }'
```
{% endcode %}

### Client Registration: OpenBanking Brasil

If your domain is configured for the Open Banking Brasil Financial-grade API Security Profile, the payload will also contain a `software_statement` and the request objects have to be encrypted using RSA-OAEP with A256GCM.

With the Open Banking Brasil Financial-grade API Security Profile, some scopes may receive a parameter. To create a **parameterized** scope:

* Go to **settings > scopes**
* Click <<+>> to create a new scope
* Complete the form and enable **Allow scope parameter**
* Save the new scope

Once activated, a scope may receive a parameter as a suffix. For example, the scope **consent** may be parameterized, and the scope **consent:myparameter** is considered as a valid scope by AM.
