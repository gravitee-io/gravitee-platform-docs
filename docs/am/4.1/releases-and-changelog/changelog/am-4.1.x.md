---
description: >-
  This page contains the changelog entries for AM 4.1.x and any future minor or
  patch AM 4.1.x releases
---

# AM 4.1.x

## Gravitee Access Management 4.1.37 - February 17, 2025

<details>

<summary>Bug fixes</summary>









</details>


## Gravitee Access Management 4.1.36 - December 12, 2024

<details>

<summary>Bug fixes</summary>

**Other**

* SlowQuery (asSorted) + Index non utilisé [#10194](https://github.com/gravitee-io/issues/issues/10194)
* Issue using LDAP Provider 2.1.0 (Operational attribute from LDAP) [#10229](https://github.com/gravitee-io/issues/issues/10229)

</details>


## Gravitee Access Management 4.1.35 - November 22, 2024

<details>

<summary>Bug fixes</summary>

**Gateway**

* why does "Skip MFA enrollment" also skips MFA validation on login [#10086](https://github.com/gravitee-io/issues/issues/10086)
* Using the /introspect endpoint with a bearer token does not work in 4.4.9 [#10166](https://github.com/gravitee-io/issues/issues/10166)





**Other**

* Improve WebAuthn Credential search indexes [#10165](https://github.com/gravitee-io/issues/issues/10165)

</details>



## Gravitee Access Management 4.1.34 - October 14, 2024

<details>

<summary>Bug fixes</summary>

**Gateway**

* AM Refresh token active set to false [#10065](https://github.com/gravitee-io/issues/issues/10065)


</details>

## Gravitee Access Management 4.1.33 - October 9, 2024

<details>

<summary>Bug fixes</summary>

**Gateway**

* Able to update username using a blank space [#10015](https://github.com/gravitee-io/issues/issues/10015)
* AM upgrade from 4.1.20 to 4.1.31 lead to 200% CPU on MongoDb cluster [#10084](https://github.com/gravitee-io/issues/issues/10084)

</details>


## Gravitee Access Management 4.1.32 - September 27, 2024

<details>

<summary>Bug fixes</summary>

**Gateway**

* Introduce option to adapt the create App behaviour [#10024](https://github.com/gravitee-io/issues/issues/10024)
* MFA - initialisation of the phone field for the SMS factor [#10030](https://github.com/gravitee-io/issues/issues/10030)
* FingerprintJs is not called in the confirmRegistration/resetPassword page for auto login [#10031](https://github.com/gravitee-io/issues/issues/10031)
* Post logout redirection does not work properly. [#10038](https://github.com/gravitee-io/issues/issues/10038)



**Console**

* Password Policy - expiration date limited to 64 [#10028](https://github.com/gravitee-io/issues/issues/10028)

**Other**

* SAML IDP can't validate finalize authentication [#10042](https://github.com/gravitee-io/issues/issues/10042)

</details>


## Gravitee Access Management 4.1.31 - September 13, 2024

<details>

<summary>Bug fixes</summary>

**Gateway**

* Keeping query-params after the validate request policy has been triggered [#9907](https://github.com/gravitee-io/issues/issues/9907)
* MFA code asked on Active User session [#9908](https://github.com/gravitee-io/issues/issues/9908)
* Token mapper - user rolesPermissions are missing [#9918](https://github.com/gravitee-io/issues/issues/9918)
* Windows Hello issue registering webauthn [#9964](https://github.com/gravitee-io/issues/issues/9964)
* HTTP Factor Resource Error [#9988](https://github.com/gravitee-io/issues/issues/9988)
* [AM][4.4.5] Orange plugin cannot be used for SMS MFA [#9997](https://github.com/gravitee-io/issues/issues/9997)
* Regression on OTP and France Connect Plugin  [#10000](https://github.com/gravitee-io/issues/issues/10000)
* Unable to login with Azure AD Provider [#10006](https://github.com/gravitee-io/issues/issues/10006)



**Console**

* Federated IdP - Domain Whitelist description is wrong during creation [#10002](https://github.com/gravitee-io/issues/issues/10002)

**Other**

* Possible to set empty Redirect URI on app [#9987](https://github.com/gravitee-io/issues/issues/9987)

</details>


## Gravitee Access Management 4.1.30 - August 30, 2024

<details>

<summary>Bug fixes</summary>



**Management API**

* NPE  in filter sensitive information. [#9968](https://github.com/gravitee-io/issues/issues/9968)



**Other**

* Error with MFA challenge policy in Registration Confirmation Flow [#9945](https://github.com/gravitee-io/issues/issues/9945)
* Make LDAP IDP non blocking [#9969](https://github.com/gravitee-io/issues/issues/9969)
* Configure the validation period for LDAP IDP [#9971](https://github.com/gravitee-io/issues/issues/9971)
* Fix connection leak on LDAP idp [#9973](https://github.com/gravitee-io/issues/issues/9973)

</details>


## Gravitee Access Management 4.1.29 - August 27, 2024

<details>

<summary>Bug fixes</summary>







**Other**

* Installation collection can have more than one entry [#9403](https://github.com/gravitee-io/issues/issues/9403)
* Bot detection plugin error [#9909](https://github.com/gravitee-io/issues/issues/9909)
* OAuth 2.0 - Current tokens still active when disabling an application [#9933](https://github.com/gravitee-io/issues/issues/9933)
* Windows Hello issue registering webauthn [#9964](https://github.com/gravitee-io/issues/issues/9964)

</details>


## Gravitee Access Management 4.1.28 - August 19, 2024

<details>

<summary>Bug fixes</summary>

**Gateway**

* Not double dash "--" in the returned code from an OAuth2 authentication flow [#9910](https://github.com/gravitee-io/issues/issues/9910)
* Secrets in responses of SSAM [#9926](https://github.com/gravitee-io/issues/issues/9926)

**Management API**

* Audits present twice during user creation [#9837](https://github.com/gravitee-io/issues/issues/9837)
* MFA - Invalid 2FA code  [#9929](https://github.com/gravitee-io/issues/issues/9929)





</details>


## Gravitee Access Management 4.1.27 - August 2, 2024

<details>

<summary>Bug fixes</summary>

**Other**

* [AM][GW] Set tl client header name behind reverse proxy through helm chart [#9874](https://github.com/gravitee-io/issues/issues/9874)
* Cannot save UserInfo Endpoint in UI - Save Button Disabled [#9879](https://github.com/gravitee-io/issues/issues/9879)
* Configuration via la console AM non prise en compte sur les gateways [#9888](https://github.com/gravitee-io/issues/issues/9888)
* MFA - weird behavior when user is going back to the previous enroll step [#9897](https://github.com/gravitee-io/issues/issues/9897)
* Error "ERR_TOO_MANY_REDIRECTS" when hide login form is enabled. [#9898](https://github.com/gravitee-io/issues/issues/9898)

</details>


## Gravitee Access Management 4.1.26 - July 19, 2024

<details>

<summary>Bug fixes</summary>

**Gateway**

* Propagate Message from Error Condition of HTTP IdP to Audit log. [#9841](https://github.com/gravitee-io/issues/issues/9841)

**Management API**

*  Redirect to login when device credentials are deleted [#9859](https://github.com/gravitee-io/issues/issues/9859)

**Console**

* A switch has an incorrect state when revisiting page - Application Settings [#9433](https://github.com/gravitee-io/issues/issues/9433)

**Other**

* Switching between environments is broken when multiple environments linked in cockpit [#9844](https://github.com/gravitee-io/issues/issues/9844)

</details>


## Gravitee Access Management 4.1.25 - July 8, 2024

<details>

<summary>Bug fixes</summary>

**Gateway**

* OTPFactorProvider - An error occurs while validating 2FA code [#9725](https://github.com/gravitee-io/issues/issues/9725)
* null-1 entry in auth_flow_ctx table should not be stored in database [#9803](https://github.com/gravitee-io/issues/issues/9803)





**Other**

* When creating user with preregistratoin, the password creation steps are skipped [#9839](https://github.com/gravitee-io/issues/issues/9839)

</details>


## Gravitee Access Management 4.1.24 - June 21, 2024

<details>

<summary>Bug fixes</summary>

**Gateway**

* Heml duplication of configuration [#9778](https://github.com/gravitee-io/issues/issues/9778)


**Other**

* Improve the ingress configuration to redirect HTTPS [#9712](https://github.com/gravitee-io/issues/issues/9712)
* AM Gateway pod is not starting due to StackOverflowError [#9794](https://github.com/gravitee-io/issues/issues/9794)

</details>


## Gravitee Access Management 4.1.23 - June 6, 2024

<details>

<summary>Bug fixes</summary>

**Gateway**

* [AM] [3.21.18] User don't receive the email to recover his password with an uppercase email [#9624](https://github.com/gravitee-io/issues/issues/9624)
* Exception on start-up in Spring Boot applications after upgrade to AM 4.3.1 [#9667](https://github.com/gravitee-io/issues/issues/9667)
* Error Azure SCIM user update  [#9674](https://github.com/gravitee-io/issues/issues/9674)
* DCR new client using Template doesn't copy all parameters [#9691](https://github.com/gravitee-io/issues/issues/9691)
* Brute Force Detection not working to IDPs with Account Linking Policy [#9713](https://github.com/gravitee-io/issues/issues/9713)
* Source IP and user agent missing from FORGOT_PASSWORD_REQUESTED audit log [#9724](https://github.com/gravitee-io/issues/issues/9724)
* Domain not available into the ExpresionLanguage context [#9745](https://github.com/gravitee-io/issues/issues/9745)

**Management API**

* Not able to configure email notifier using Gravitee [#9581](https://github.com/gravitee-io/issues/issues/9581)

**Console**

* AM - Change error message when admin user tries to remove certificate tied to an application [#8952](https://github.com/gravitee-io/issues/issues/8952)

**Other**

* Editing HTTP Provider selects wrong password encoder [#9627](https://github.com/gravitee-io/issues/issues/9627)
* Email from [%s] is invalid - SMTP Resource [#9749](https://github.com/gravitee-io/issues/issues/9749)

</details>


## Gravitee Access Management 4.1.22 - May 24, 2024

<details>

<summary>Bug fixes</summary>

**Gateway**

* Error with MFA Challenge policy in Reset Password Flow [#9735](https://github.com/gravitee-io/issues/issues/9735)

**Other**

* Unable to remove a FORM at organization level [#9124](https://github.com/gravitee-io/issues/issues/9124)
* Application - Forms - Page not found error when enabling custom form again after being 'cleared' [#9492](https://github.com/gravitee-io/issues/issues/9492)
* Password Policy Blank value in dropbox when selecting value Unlimited

</details>

## Gravitee Access Management 4.1.21 - May 9, 2024

<details>

<summary>Bug fixes</summary>

**Other**

* There are no MFA logs [#9629](https://github.com/gravitee-io/issues/issues/9629)
* \_node/health endpoint is not accessible [#9698](https://github.com/gravitee-io/issues/issues/9698)
* Plugin "Orange Contact Everyone" is not compatible with version 4.3.2 [#9704](https://github.com/gravitee-io/issues/issues/9704)

</details>

## Gravitee Access Management 4.1.20 - April 29, 2024

<details>

<summary>Bug fixes</summary>

**Gateway**

* Issue with MFA and silent refresh token [#9622](https://github.com/gravitee-io/issues/issues/9622)
* \[WebAuthn] Problèmatique Authenticator "SecurityError : The operation is insecure." [#9686](https://github.com/gravitee-io/issues/issues/9686)

**Management API**

* Not able to add new attribute to User’s profile through AM REST Api when using Google Identity provider [#8434](https://github.com/gravitee-io/issues/issues/8434)
* AM - Application Analytics Timeout [#9405](https://github.com/gravitee-io/issues/issues/9405)

</details>

## Gravitee Access Management 4.1.19 - April 12, 2024

<details>

<summary>Bug fixes</summary>

**Console**

* Error when notifications are acknowledged [#9661](https://github.com/gravitee-io/issues/issues/9661)

**Other**

* Enrollment Flow Logic Bug [#9518](https://github.com/gravitee-io/issues/issues/9518)
* Improve CORS Domain settings and replace default values [#9531](https://github.com/gravitee-io/issues/issues/9531)

</details>

## Gravitee Access Management 4.1.18 - April 5, 2024

<details>

<summary>Bug fixes</summary>

**Gateway**

* Disable Application [#9584](https://github.com/gravitee-io/issues/issues/9584)

**Other**

* Expired records present in table ciba\_auth\_requests. Cron is not taken into account. [#9499](https://github.com/gravitee-io/issues/issues/9499)
* Logs too verbose in AM when GeoIP plugin is not available [#9633](https://github.com/gravitee-io/issues/issues/9633)
* Support SAML mixing response binding protocol [#9648](https://github.com/gravitee-io/issues/issues/9648)

</details>

## Gravitee Access Management 4.1.17 - March 28, 2024

<details>

<summary>Bug fixes</summary>

**Gateway**

* Login - MFA challenge should be prompted when prompt=login is used [#9497](https://github.com/gravitee-io/issues/issues/9497)
* Revert: Passwordless authentication doesn't take the IDP status into account (#9494) [#9615](https://github.com/gravitee-io/issues/issues/9615)
* User unable to authenticate when linked to different identities [#9616](https://github.com/gravitee-io/issues/issues/9616)
* Addition of WebAuthn Credentials info into the context [#9620](https://github.com/gravitee-io/issues/issues/9620)

**Console**

* No space between source IP and user agent in audit logs [#9458](https://github.com/gravitee-io/issues/issues/9458)
* User agent showing 'undefined' in audit logs [#9459](https://github.com/gravitee-io/issues/issues/9459)
* Fetch user group doesn't persist [#9609](https://github.com/gravitee-io/issues/issues/9609)

**Other**

* Linked accounts are not listed in the UI when using SQL database [#9610](https://github.com/gravitee-io/issues/issues/9610)

</details>

## Gravitee Access Management 4.1.16 - March 15, 2024

<details>

<summary>Bug fixes</summary>

**Gateway**

* Redirect executed with jwt-bearer grant\_type [#9505](https://github.com/gravitee-io/issues/issues/9505)
* Invalid Phone Number [#9519](https://github.com/gravitee-io/issues/issues/9519)

</details>

## Gravitee Access Management 4.1.15 - February 29, 2024

<details>

<summary>Bug fixes</summary>

**Gateway**

* Passwordless authentication doesn't take the IDP status into account [#9494](https://github.com/gravitee-io/issues/issues/9494)
* State parameter encoded twice with response\_mode set to form\_post [#9528](https://github.com/gravitee-io/issues/issues/9528)
* Passwordless registration appearing for users who have already authenticated with step up [#9568](https://github.com/gravitee-io/issues/issues/9568)

</details>

## Gravitee Access Management 4.1.14 - February 19, 2024

<details>

<summary>Bug fixes</summary>

**Gateway**

* Unable to finalize SAML authentication using HTTP-POST binding [#9485](https://github.com/gravitee-io/issues/issues/9485)
* Security Domain may not be loaded on Gateway startup [#9496](https://github.com/gravitee-io/issues/issues/9496)
* Custom email not being sent when resending account registered verification email [#9500](https://github.com/gravitee-io/issues/issues/9500)

**Console**

* Missing read password policy role [#8924](https://github.com/gravitee-io/issues/issues/8924)

**Other**

* Do not log stack trace when user has to provide password after webauthn authentication [#9503](https://github.com/gravitee-io/issues/issues/9503)
* SAML 2.0 Identity Provider requires AM dependency update [#9515](https://github.com/gravitee-io/issues/issues/9515)

</details>

## Gravitee Access Management 4.1.13 - February 9, 2024

<details>

<summary>Bug fixes</summary>

**Gateway**

* Invalid form parameter when ResponseMode is set to form\_post [#9179](https://github.com/gravitee-io/issues/issues/9179)
* SCIM search operator PR doesn't work as expected [#9265](https://github.com/gravitee-io/issues/issues/9265)
* WebAuthn: "Force authenticator integrity" - LastCheckedAt systematically updated at each webauthn login [#9327](https://github.com/gravitee-io/issues/issues/9327)

</details>

## Gravitee Access Management 4.1.12 - January 30, 2024

<details>

<summary>Bug fixes</summary>

**Gateway**

* Apply timeout on blockingGet in ManagementAPI filters [#9476](https://github.com/gravitee-io/issues/issues/9476)
* Authentication flow rejected due to redirect\_uri when PAR is used [#9478](https://github.com/gravitee-io/issues/issues/9478)
* MFA challenge should be prompted before registering a passwordless device [#9479](https://github.com/gravitee-io/issues/issues/9479)

</details>

## Gravitee Access Management 4.1.11 - January 30, 2024

<details>

<summary>Bug fixes</summary>

**Gateway**

* Passwordless not working for iOS v17.2.1 [#9470](https://github.com/gravitee-io/issues/issues/9470)
* Flow - Add WebAuthn credential register flow (improvement)

</details>

## Gravitee Access Management 4.1.10 - January 17, 2024

<details>

<summary>Bug fixes</summary>

**Gateway**

* Avoid BodyHandler processing for GET request [#9352](https://github.com/gravitee-io/issues/issues/9352)
* WebAuthnCredentialId is null into the EL context [#9455](https://github.com/gravitee-io/issues/issues/9455)

**Other**

* AEConnector not initialized properly since AM 4.1 [#9454](https://github.com/gravitee-io/issues/issues/9454)

</details>

## Gravitee Access Management 4.1.9 - December 22, 2023

<details>

<summary>Bug fixes</summary>

**Gateway**

* Session expired problem - X-XRF-TOKEN [#9398](https://github.com/gravitee-io/issues/issues/9398)
* 500 response received on creating user with /scim endpoint with duplicate externalId [#9421](https://github.com/gravitee-io/issues/issues/9421)
* Exclude null value from SCIM UserMapper [#9427](https://github.com/gravitee-io/issues/issues/9427)

**Management API**

* Unable to list users [#9125](https://github.com/gravitee-io/issues/issues/9125)

**Other**

* Connection leak into JdbcIdentityProvider [#9426](https://github.com/gravitee-io/issues/issues/9426)

</details>

## Gravitee Access Management 4.1.8 - December 11, 2023

<details>

<summary>Bug fixes</summary>

**Gateway**

* Original Parameters lost during redirect using SAML Handler [#9393](https://github.com/gravitee-io/issues/issues/9393)
* Avoid logging GeoIP error stackstrace [#9401](https://github.com/gravitee-io/issues/issues/9401)

**Other**

* Invalid value in Issuer for Response [#9409](https://github.com/gravitee-io/issues/issues/9409)
* MessageDigest Encoder is not ThreadSafe [#9413](https://github.com/gravitee-io/issues/issues/9413)
* Configuration files are being overwritten during YUM update [#9368](https://github.com/gravitee-io/issues/issues/9368)

</details>

## Gravitee Access Management 4.1.7 - November 22, 2023

<details>

<summary>Bug fixes</summary>

**Gateway**

* Don't keep FranceConnect Session active [#9382](https://github.com/gravitee-io/issues/issues/9382)

</details>

## Gravitee Access Management 4.1.6 - November 17, 2023

<details>

<summary>Bug fixes</summary>

**Gateway**

* Make the IDToken accessible in the UserMapper [#9381](https://github.com/gravitee-io/issues/issues/9381)
* Deadlock during generate AccessToken [#9238](https://github.com/gravitee-io/issues/issues/9238)
* Excessive number of ExpiredJWTException errors in Gravitee logs [#9261](https://github.com/gravitee-io/issues/issues/9261)

</details>

## Gravitee Access Management 4.1.5 - November 8, 2023

<details>

<summary>What's new</summary>

* Addition of Consent settings into the Chart values
* Improve FranceConnect IDP to accept additional query parameters

</details>

<details>

<summary>Bug fixes</summary>

**Other**

* Upgrade Groovy policy [#9229](https://github.com/gravitee-io/issues/issues/9229)
* EnrollmentMFA policy doesn't manage the `useVariableFactorSecurity` setting [#9365](https://github.com/gravitee-io/issues/issues/9365)

</details>

## Gravitee Access Management 4.1.4 - November 3, 2023

<details>

<summary>Bug fixes</summary>

**Gateway**

* Use SingleSignOut with linked accounts [#9358](https://github.com/gravitee-io/issues/issues/9358)

</details>

## Gravitee Access Management 4.1.3 - October 27, 2023

<details>

<summary>Bug fixes</summary>

**Gateway**

* Application error when using an undefined translation [#9237](https://github.com/gravitee-io/issues/issues/9237)
* Registration confirmation Javascript error (anti-XSRF token) [#9276](https://github.com/gravitee-io/issues/issues/9276)
* Quotes are lost in Gravitee AM forms [#9326](https://github.com/gravitee-io/issues/issues/9326)
* When a resource plugin has been removed from the installation, other resources may not be loaded [#9344](https://github.com/gravitee-io/issues/issues/9344)
* On error during CONNECT flow redirection is not processed [#9346](https://github.com/gravitee-io/issues/issues/9346)
* User created using SCIM is disabled when password is missing [#9347](https://github.com/gravitee-io/issues/issues/9347)

**Management API**

* Management API hangs completely [#9339](https://github.com/gravitee-io/issues/issues/9339)

**Other**

* EnrollMFA should be able to update the factor [#9350](https://github.com/gravitee-io/issues/issues/9350)

</details>

## Gravitee Access Management 4.1.2 - October 19, 2023

<details>

<summary>Bug fixes</summary>

**Gateway**

* Twilio Phone Extension with Self-Service API [#9289](https://github.com/gravitee-io/issues/issues/9289)

**Other**

* EnrichProfile reset factor defined by EnrollMFA policy [#9161](https://github.com/gravitee-io/issues/issues/9161)

</details>

## Gravitee Access Management 4.1.1 - October 16, 2023

<details>

<summary>Bug fixes</summary>

**Gateway**

* Align XSRF token TTL to the user session TTL [#9282](https://github.com/gravitee-io/issues/issues/9282)

**Management API**

* Wrong values returned by Gravitee AM Management API [#9141](https://github.com/gravitee-io/issues/issues/9141)
* AM Management API should start even with missing or unknown Identity Provider plugins [#9230](https://github.com/gravitee-io/issues/issues/9230)

**Other**

* MS SqlServer 10.2 onwards driver support [#9178](https://github.com/gravitee-io/issues/issues/9178)
* Upgrade script for 3.21.6 does not work as expected [#9288](https://github.com/gravitee-io/issues/issues/9288)
* Update Mongo script to create indices [#9291](https://github.com/gravitee-io/issues/issues/9291)

</details>

## Gravitee Access Management 4.1.0 - September 28, 2023

For more in-depth information on what's new, please refer to the [Gravitee AM 4.1 release notes](../release-notes/).

<details>

<summary>What's new</summary>

**Enterprise Edition**

The MFA Challenge policy is now available to apply an MFA step during actions such as reset password or unlock account.

**Twilio phone factor enhancement**

The MFA phone call factor can now use Twilio's sendDigits function to direct a call to an extension before playing the message with the MFA code.

**Account linking**

The new Account Linking feature automatically links user accounts with identical user attributes to bypass re-enrollment during authentication.

**Session management**

Consent to a new session cookie option prevents logout following a period of idling and extends the session expiration.

</details>

<details>

<summary>Breaking changes</summary>

* AM 4.1 requires Java 17 as the runtime
* The versions of the R2DBC drivers must be compatible with R2DBC-SPI 1.0 (i.e., the driver version must start with 1.x). Versions used:
  * postgresql: **1.0.2.RELEASE**\
    mariadb: **1.1.2**\
    mysql: **1.0.2**\
    mssql: **1.0.0.RELEASE**
  * **WARNING** ⚠️ **DO NOT** use the **1.0.2.RELEASE** for **mssql / SQLServer** as this version seems to be buggy (see [r2dbc/r2dbc-mssql#276](https://github.com/r2dbc/r2dbc-mssql/issues/276))
*   Default RDMS timeout and connection pool size values have changed:

    * New values:

    ```
        initialSize: 1
        maxSize: 50
        maxIdleTime: 30000
        maxLifeTime: -1
        maxAcquireTime: 3000
        maxCreateConnectionTime: 5000
    ```

    * Previous values:

    ```
        initialSize: 0
        maxSize: 10
        maxIdleTime: 30000
        maxLifeTime: 0 # not valid anymore with R2BC 1.x
        maxAcquireTime: 0 # not valid anymore with R2BC 1.x
        maxCreateConnectionTime: 0 # not valid anymore with R2BC 1.x
    ```

</details>
