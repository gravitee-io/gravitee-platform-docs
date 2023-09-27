---
description: Authorization, Authentication, and Identity Protocols Supported
---

# Auth Protocols

Gravitee Access Management (AM) relies on different authorization/authentication/identity protocols to define how applications can interact with it to authenticate, retrieve user information and make authorization decisions when accessing protected resources.

* OAuth 2.0: the OAuth 2.0 authorization framework enables a third-party application to obtain limited access to an HTTP service, either on behalf of a resource owner by brokering an approval interaction between the resource owner and the HTTP service, or by allowing the third-party application to obtain access on its own behalf.
* OpenID Connect: OpenID Connect 1.0 is a simple identity layer on top of the OAuth 2.0 protocol. It enables clients to verify the identity of the end user based on the authentication performed by an authorization server, as well as to obtain basic profile information about the end user in an interoperable and REST-like manner.
* UMA 2.0: User-Managed Access (UMA) is an OAuth-based protocol designed to give to an individual a unified control point for authorizing who and what can get access to their digital data, content and services, no matter where all those things live.
* SCIM 2.0: the System for Cross-domain Identity Management (SCIM) specification is designed to make managing user identities in cloud-based applications and services easier. Its intent is to reduce the cost and complexity of user management operations by providing a common user schema and extension model.
* FAPI 1.0: The Financial-grade API (FAPI) is a highly secured OAuth profile that aims to provide specific implementation guidelines for security and interoperability.
* CIBA 1.0: The Client-Initiated Backchannel Authentication Flow - Core 1.0 (CIBA) is an authentication flow where the Relying Party communicates with an OpenID Provider without redirects through the user’s browser.
* SAML 2.0: SAML 2.0 is an XML-based protocol that uses security tokens containing assertions to pass information about a principal (usually an end user) between a SAML authority, named an Identity Provider, and a SAML consumer, named a Service Provider.
