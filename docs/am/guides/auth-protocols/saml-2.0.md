# SAML 2.0

## Overview

[The Security Assertion Markup Language (SAML)](http://docs.oasis-open.org/security/saml/Post2.0/sstc-saml-tech-overview-2.0.html) standard defines an XML-based framework for describing and exchanging security information between on-line business partners.

Gravitee.io AM supports the SAML protocol and can serve both as Identity Provider (IdP) and Service Provider (SP) :

* [Configure Gravitee.io AM as SAML Service Provider](https://docs.gravitee.io/am/current/am\_userguide\_enterprise\_identity\_provider\_saml2.html)
* [Configure Gravitee.io AM as SAML Identity Provider](https://docs.gravitee.io/am/current/am\_devguide\_protocols\_saml2\_configuration.html)

### Participants

At a minimum, SAML exchanges take place between system entities referred to as a SAML asserting party and a SAML relying party. In many SAML use cases, a user, perhaps running a web browser or executing a SAML-enabled application, is also a participant, and may even be the asserting party.

Service provider (SP)

A relying party that uses assertions it has received from the Identity Provider (IdP) to grant the principal access to local resources.

Identity provider (IdP)

Entity that authenticates users and provides to service providers (SP) an authentication assertion that indicates a principal has been authenticated.

![graviteeio am devguide protocols saml overview](https://docs.gravitee.io/images/am/current/graviteeio-am-devguide-protocols-saml-overview.png)\


## Enable SAML 2.0 Identity Provider support

Currently AM supports the following SAML bindings :

* HTTP-Redirect

|   | HTTP-POST binding is planned for a future version of the SAML 2.0 IdP protocol plugin. |
| - | -------------------------------------------------------------------------------------- |

and the following options :

* Web Browser SSO Profile
* Single Logout Profile
* SP-Initiated flow
* Support for signed SAML assertions (SAML Request and SAML Response)

|   | Support for encrypted SAML assertions will be provided in a future version of the SAML 2.0 IdP protocol plugin. |
| - | --------------------------------------------------------------------------------------------------------------- |

### Activate SAML 2.0 IdP

|   | Be sure to have your SAML 2.0 IdP protocol plugin and your license key installed in your environment before configuring the connection. |
| - | --------------------------------------------------------------------------------------------------------------------------------------- |

1. Log in to AM Console.
2. Click **Settings > SAML 2.0**.
3. Enable **SAML 2.0 IdP support**.
4. Enter your IdP Entity ID.
5. Select your certificate to sign the SAML Response assertion.
6. Click **Save**.

|   | If you choose to not use a certificate, the SAML Response assertion will not be signed. |
| - | --------------------------------------------------------------------------------------- |

### Test the connection

To connect your applications to the AM SAML 2.0 IdP, you need at least the following information:

* **SingleSignOnService**, the SAML IdP Sign In URL : [https://AM\_GATEWAY/{domain}/saml2/idp/SSO](https://am\_gateway/%7Bdomain%7D/saml2/idp/SSO)
* **SingleLogoutService**, the SAML IdP Sign Out URL : [https://AM\_GATEWAY/{domain}/saml2/idp/logout](https://am\_gateway/%7Bdomain%7D/saml2/idp/logout)
* **Signing certificate**, the public signing certificate (encoded in PEM)

|   | SAML IdP metadata information can be found here : [https://AM\_GATEWAY/{domain}/saml2/idp/metadata](https://am\_gateway/%7Bdomain%7D/saml2/idp/metadata) |
| - | -------------------------------------------------------------------------------------------------------------------------------------------------------- |

You can test your SAML 2.0 connection using a web application created in AM.

1. In AM Console, create a new web application.
2. Click **Settings > SAML 2.0**.
3. Verify / update the SAML 2.0 application settings.
4. Select an identity provider to connect your users.
5. Call the Login page (the /saml/idp/SSO?SAMLRequest=…​ endpoint).
6. Enter username/password and click **Sign in**.
7. If everything us OK, your user will be redirected to the application **attribute consume service URL** with the SAML Response assertion as a parameter.

|   | SAML 2.0 IdP protocol is compatible out of the box with all the existing features of AM just like the OAuth 2.0/OpenId Connect protocol, such as : passwordless, MFA, social login, …​ |
| - | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
