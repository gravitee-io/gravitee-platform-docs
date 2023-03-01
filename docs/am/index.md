# Gravitee.io Access Management (AM)

Gravitee.io Access Management (AM) is a flexible, lightweight and easy
to use open source Identity and Access Management solution. It offers a
centralized authentication and authorization service to deliver secure
access for authorized users to your applications and APIs from any
device.

## Authorization in AM

AM is based on OAuth2/OpenID Connect and SAML 2.0 protocols and acts as
an identity provider broker

### OAuth2

OAuth2 is an authorization framework that allows applications acting on
behalf of the end user to obtain limited access to HTTP services. [OAuth
2 RFC^](https://tools.ietf.org/html/rfc6749) defines two endpoints:

-   The **authorization endpoint** used to interact with the resource
    owner and obtain an authorization grant via user-agent redirection.

-   The **token endpoint** used by the client to obtain an access token
    by presenting its authorization grant.

For further information about OAuth2, view the [RFC
page^](https://tools.ietf.org/html/rfc6749).

### OpenID Connect

OpenID Connect is an identity layer on top of the OAuth 2.0 protocol. It
enables clients to verify the identity of the end user by using an
Authorization Server to authenticate and obtain basic profile
information about the end user.

For further information about OpenID Connect, view the [OpenID Connect
specifications^](http://openid.net/specs/openid-connect-core-1_0.html).

### SAML 2.0

The Security Assertion Markup Language (SAML) protocol is an
open-standard, XML-based framework for authentication and authorization
of users.

Gravitee AM can act as both SAML IdP for applications as well as
federate with SAML based Identity Providers for protocol mediation.

For further information about SAML 2.0, view the [SAML Tech Overview
2.0](http://docs.oasis-open.org/security/saml/Post2.0/sstc-saml-tech-overview-2.0.html)
