---
description: >-
  This page contains the changelog entries for AM 4.4.x and any future minor or
  patch AM 4.4.x releases
---

{% hint style="info" %}
When managing deployments using Helm, please note that the default startup, liveness, and readiness probes now use the httpGet method by default to request the internal API on the `/_node/health` endpoint. As a result, the internal API listens on `0.0.0.0` to allow the kubelet to check the component's status. If you don't provide custom probe definitions and have explicitly defined either the `api.http.services.core.http.host` or the `gateway.http.services.core.http.host`, ensure the value is set to `0.0.0.0`; otherwise, the probes will fail.
{% endhint %}

# AM 4.4.x

## Gravitee Access Management 4.4.26 - May 13, 2025

<details>

<summary>Bug fixes</summary>



**Management API**

* Users and Groups metadata not displayed for /members enpoint [#10515](https://github.com/gravitee-io/issues/issues/10515)
* Email notification fails when user doesn't have firstName [#10536](https://github.com/gravitee-io/issues/issues/10536)





</details>


## Gravitee Access Management 4.4.25 - May 6, 2025

<details>

<summary>Bug fixes</summary>

**Gateway**

* Filter audit type  [#10518](https://github.com/gravitee-io/issues/issues/10518)


**Other**

* Fail to enable the AM gateway service on SUSE [#10402](https://github.com/gravitee-io/issues/issues/10402)
* Use Gravitee GPG Key to sign RPM package [#10504](https://github.com/gravitee-io/issues/issues/10504)
* Support of FranceConnect API V2

</details>


## Gravitee Access Management 4.4.24 - April 25, 2025

<details>

<summary>Bug fixes</summary>

**Gateway**

* MFA "Remember Device" error when using CAS IDP [#10493](https://github.com/gravitee-io/issues/issues/10493)







</details>


## Gravitee Access Management 4.4.23 - April 11, 2025

<details>

<summary>Bug fixes</summary>

**Gateway**

* Problem with API management console application creation/update and DCR [#10232](https://github.com/gravitee-io/issues/issues/10232)
* Login button remains disabled when using a password manager [#10411](https://github.com/gravitee-io/issues/issues/10411)
* Setting max consecutive letters to 0 in password policies using mapi displays unnecessary password requirement [#10416](https://github.com/gravitee-io/issues/issues/10416)
* Unable to use id_token when configuring Azure though OpenId form [#10453](https://github.com/gravitee-io/issues/issues/10453)
* Error handling error=session_expired in Login Form [#10460](https://github.com/gravitee-io/issues/issues/10460)

**Management API**

* Prevent Ogranization IDP selection to send null [#10444](https://github.com/gravitee-io/issues/issues/10444)
* Fix audit log on user login failed [#10463](https://github.com/gravitee-io/issues/issues/10463)



**Other**

* Error in /ciba/authenticate/callback [#10412](https://github.com/gravitee-io/issues/issues/10412)
* MinLength value can be greater than maxLength value in a password policy when using the mapi [#10417](https://github.com/gravitee-io/issues/issues/10417)
* [AM][4.5.11] Error when character "ë" in a token [#10418](https://github.com/gravitee-io/issues/issues/10418)
* Management API does not check if user exists on domain when added to a group on creation of the group [#10468](https://github.com/gravitee-io/issues/issues/10468)

</details>


## Gravitee Access Management 4.4.22 - March 24, 2025

<details>

<summary>Bug fixes</summary>


* Upgrade the SAML IdentityProvider plugin


</details>


## Gravitee Access Management 4.4.21 - March 17, 2025

<details>

<summary>Bug fixes</summary>

**Gateway**

* MFA Challenge policy doesn't work when multiple redirect_uri are declared [#10407](https://github.com/gravitee-io/issues/issues/10407)
* Authentication fails when MFA Challenge policy is used [#10421](https://github.com/gravitee-io/issues/issues/10421)







</details>


## Gravitee Access Management 4.4.20 - March 11, 2025

<details>

<summary>Bug fixes</summary>

**Gateway**

* RememberDevice issue with uBlock [#10388](https://github.com/gravitee-io/issues/issues/10388)
* Fix regression on redirect URL [#10404](https://github.com/gravitee-io/issues/issues/10404)







</details>


## Gravitee Access Management 4.4.19 - February 28, 2025

{% hint style="warning" %}
This version contains a regression introduced by [#10344](https://github.com/gravitee-io/issues/issues/10344).
Please do not install this version if you are using Access Management to authenticate users on mobile applications.
{% endhint %}


<details>

<summary>Bug fixes</summary>

**Gateway**

* Redirect URL not whitelisted [#10344](https://github.com/gravitee-io/issues/issues/10344)
* Improve memory usage of Gateway [#10366](https://github.com/gravitee-io/issues/issues/10366)

**Management API**

* Remove default baseURL for loadPreAuthUserResource in HttpIdentityProvider [#10361](https://github.com/gravitee-io/issues/issues/10361)



**Other**

* Error with MFA (/resetPassword page) [#10341](https://github.com/gravitee-io/issues/issues/10341)
* [AM][4.4.11] French language in email not working  [#10349](https://github.com/gravitee-io/issues/issues/10349)
* Lors d'une redemande d'OPT, même OTP [#10374](https://github.com/gravitee-io/issues/issues/10374)

</details>


## Gravitee Access Management 4.4.18 - February 17, 2025

<details>

<summary>Bug fixes</summary>

**Gateway**

* Update AM documentation and OpenAPI spec [#10299](https://github.com/gravitee-io/issues/issues/10299)
* [CIBA] Http Authentication Device Notifier hide some scope [#10309](https://github.com/gravitee-io/issues/issues/10309)
* No logs from InvalidGrantException in the Audits in the UI [#10313](https://github.com/gravitee-io/issues/issues/10313)
* No logs from InvalidGrantException in the Audits in the UI [#10314](https://github.com/gravitee-io/issues/issues/10314)
* Error with MFA (Stuck in a Loop) [#10317](https://github.com/gravitee-io/issues/issues/10317)







</details>


## Gravitee Access Management 4.4.17 - January 31, 2025

<details>

<summary>Bug fixes</summary>

**Gateway**

* [Backport-4.4] oauth2 response strict mode [#10318](https://github.com/gravitee-io/issues/issues/10318)





**Other**

* Double quote prevent HTTP Provider to authenticate [#10277](https://github.com/gravitee-io/issues/issues/10277)

</details>


## Gravitee Access Management 4.4.16 - January 16, 2025

<details>

<summary>Bug fixes</summary>

**Gateway**

* Access token is generated from refresh token of deactivated user [#10258](https://github.com/gravitee-io/issues/issues/10258)



**Console**

* Bug Affichage : Administrative Roles box list illisible.  [#10256](https://github.com/gravitee-io/issues/issues/10256)
* Audit log details differ between roles [#10266](https://github.com/gravitee-io/issues/issues/10266)

**Other**

* Unable to update any reporters on domain and organisation level [#10259](https://github.com/gravitee-io/issues/issues/10259)

</details>


## Gravitee Access Management 4.4.15 - January 3, 2025

<details>

<summary>Bug fixes</summary>





**Console**

* Can't configure new SSO IDP or modify existing one [#10251](https://github.com/gravitee-io/issues/issues/10251)



</details>


## Gravitee Access Management 4.4.14 - December 20, 2024

<details>

<summary>Bug fixes</summary>







**Other**

* Certificates description on the right of the page refers to identity providers [#10201](https://github.com/gravitee-io/issues/issues/10201)

</details>


## Gravitee Access Management 4.4.13 - December 12, 2024

<details>

<summary>Bug fixes</summary>







**Other**

* Resize the client field for OAuth2 scope repository record [#10239](https://github.com/gravitee-io/issues/issues/10239)

</details>


## Gravitee Access Management 4.4.12 - December 12, 2024

<details>

<summary>Bug fixes</summary>

**Gateway**

* SMSFactorProvider - Invalid phone number [#10193](https://github.com/gravitee-io/issues/issues/10193)



**Console**

* Able to create Kafka reporter without Bootstrap server and Topic [#10156](https://github.com/gravitee-io/issues/issues/10156)

**Other**

* SlowQuery (asSorted) + Index non utilisé [#10194](https://github.com/gravitee-io/issues/issues/10194)
* Issue using LDAP Provider 2.1.0 (Operational attribute from LDAP) [#10229](https://github.com/gravitee-io/issues/issues/10229)

</details>


## Gravitee Access Management 4.4.11 - November 22, 2024

<details>

<summary>Bug fixes</summary>

**Gateway**

* Users are returned randomly via SCIM [#10147](https://github.com/gravitee-io/issues/issues/10147)
* Using the /introspect endpoint with a bearer token does not work in 4.4.9 [#10166](https://github.com/gravitee-io/issues/issues/10166)





**Other**

* Improve WebAuthn Credential search indexes [#10165](https://github.com/gravitee-io/issues/issues/10165)

</details>


## Gravitee Access Management 4.4.10 - November 8, 2024

<details>

<summary>Bug fixes</summary>



**Management API**

* Able to create a admin service user via the create domain user endpoint [#10127](https://github.com/gravitee-io/issues/issues/10127)
* System reporter can be deleted via API [#10155](https://github.com/gravitee-io/issues/issues/10155)





</details>


## Gravitee Access Management 4.4.9 - October 25, 2024

<details>

<summary>Bug fixes</summary>

**Gateway**

* why does "Skip MFA enrollment" also skips MFA validation on login [#10086](https://github.com/gravitee-io/issues/issues/10086)





**Other**

* /sendChallenge returns status code 0 [#10097](https://github.com/gravitee-io/issues/issues/10097)
* Original access token out of an OpenID federation is not able to be used for the mapping into the ID token going back to the application [#10104](https://github.com/gravitee-io/issues/issues/10104)
* Gravitee AM SAML not working [#10106](https://github.com/gravitee-io/issues/issues/10106)
* Error message on IP filtering policy always returns remote address [#10108](https://github.com/gravitee-io/issues/issues/10108)

</details>


## Gravitee Access Management 4.4.8 - October 14, 2024

<details>

<summary>Bug fixes</summary>

**Gateway**

* Able to update username using a blank space [#10015](https://github.com/gravitee-io/issues/issues/10015)
* AM Refresh token active set to false [#10065](https://github.com/gravitee-io/issues/issues/10065)
* The "path" parameter for SCIM patch requests does not function as expected [#10073](https://github.com/gravitee-io/issues/issues/10073)
* AM upgrade from 4.1.20 to 4.1.31 lead to 200% CPU on MongoDb cluster [#10084](https://github.com/gravitee-io/issues/issues/10084)
* Password rules not displayed in the registration confirmation webpage [#10089](https://github.com/gravitee-io/issues/issues/10089)







</details>


## Gravitee Access Management 4.4.7 - September 27, 2024

<details>

<summary>Bug fixes</summary>

**Gateway**

* Validate policy message double encoded [#9920](https://github.com/gravitee-io/issues/issues/9920)
* Introduce option to adapt the create App behaviour [#10024](https://github.com/gravitee-io/issues/issues/10024)
* MFA - initialisation of the phone field for the SMS factor [#10030](https://github.com/gravitee-io/issues/issues/10030)
* FingerprintJs is not called in the confirmRegistration/resetPassword page for auto login [#10031](https://github.com/gravitee-io/issues/issues/10031)
* Post logout redirection does not work properly. [#10038](https://github.com/gravitee-io/issues/issues/10038)



**Console**

* Password Policy - expiration date limited to 64 [#10028](https://github.com/gravitee-io/issues/issues/10028)

**Other**

* SAML IDP can't validate finalize authentication [#10042](https://github.com/gravitee-io/issues/issues/10042)

</details>


## Gravitee Access Management 4.4.6 - September 13, 2024

<details>

<summary>Bug fixes</summary>

**Gateway**

* Keeping query-params after the validate request policy has been triggered [#9907](https://github.com/gravitee-io/issues/issues/9907)
* Token mapper - user rolesPermissions are missing [#9918](https://github.com/gravitee-io/issues/issues/9918)
* Windows Hello issue registering webauthn [#9964](https://github.com/gravitee-io/issues/issues/9964)
* HTTP Factor Resource Error [#9988](https://github.com/gravitee-io/issues/issues/9988)
* MFA - missing Enrolled Factor in the Thymeleaf context [#9990](https://github.com/gravitee-io/issues/issues/9990)
* [AM][4.4.5] Orange plugin cannot be used for SMS MFA [#9997](https://github.com/gravitee-io/issues/issues/9997)
* Regression on OTP and France Connect Plugin  [#10000](https://github.com/gravitee-io/issues/issues/10000)
* Unable to login with Azure AD Provider [#10006](https://github.com/gravitee-io/issues/issues/10006)



**Console**

* Federated IdP - Domain Whitelist description is wrong during creation [#10002](https://github.com/gravitee-io/issues/issues/10002)

**Other**

* Possible to set empty Redirect URI on app [#9987](https://github.com/gravitee-io/issues/issues/9987)

</details>


## Gravitee Access Management 4.4.5 - August 30, 2024

<details>

<summary>Bug fixes</summary>

**Gateway**

* Bot detection plugin error [#9909](https://github.com/gravitee-io/issues/issues/9909)
* Windows Hello issue registering webauthn [#9964](https://github.com/gravitee-io/issues/issues/9964)

**Management API**

* Installation collection can have more than one entry [#9403](https://github.com/gravitee-io/issues/issues/9403)
* OAuth 2.0 - Current tokens still active when disabling an application [#9933](https://github.com/gravitee-io/issues/issues/9933)
* NPE  in filter sensitive information. [#9968](https://github.com/gravitee-io/issues/issues/9968)



**Other**

* Enable SSL using Secret Providers for AM via Kubernetes  [#9899](https://github.com/gravitee-io/issues/issues/9899)
* Error with MFA challenge policy in Registration Confirmation Flow [#9945](https://github.com/gravitee-io/issues/issues/9945)
* Make LDAP IDP non blocking [#9969](https://github.com/gravitee-io/issues/issues/9969)
* Configure the validation period for LDAP IDP [#9971](https://github.com/gravitee-io/issues/issues/9971)
* Fix connection leak on LDAP idp [#9973](https://github.com/gravitee-io/issues/issues/9973)

</details>


## Gravitee Access Management 4.4.4 - August 19, 2024

<details>

<summary>Bug fixes</summary>

**Gateway**

* Not double dash "--" in the returned code from an OAuth2 authentication flow [#9910](https://github.com/gravitee-io/issues/issues/9910)
* Secrets in responses of SSAM [#9926](https://github.com/gravitee-io/issues/issues/9926)

**Management API**

* Audits present twice during user creation [#9837](https://github.com/gravitee-io/issues/issues/9837)
* MFA - Invalid 2FA code  [#9929](https://github.com/gravitee-io/issues/issues/9929)





</details>


## Gravitee Access Management 4.4.3 - August 2, 2024

<details>

<summary>Bug fixes</summary>







**Other**

* [AM][GW] Set tl client header name behind reverse proxy through helm chart [#9874](https://github.com/gravitee-io/issues/issues/9874)
* Cannot save UserInfo Endpoint in UI - Save Button Disabled [#9879](https://github.com/gravitee-io/issues/issues/9879)
* Configuration via la console AM non prise en compte sur les gateways [#9888](https://github.com/gravitee-io/issues/issues/9888)
* MFA - weird behavior when user is going back to the previous enroll step [#9897](https://github.com/gravitee-io/issues/issues/9897)
* Error "ERR_TOO_MANY_REDIRECTS" when hide login form is enabled. [#9898](https://github.com/gravitee-io/issues/issues/9898)

</details>

## Gravitee Access Management 4.4.2 - July 19, 2024

<details>

<summary>Bug fixes</summary>

**Gateway**

* Propagate Message from Error Condition of HTTP IdP to Audit log. [#9841](https://github.com/gravitee-io/issues/issues/9841)
* Workaround to limit breaking change in 4.3 [#9862](https://github.com/gravitee-io/issues/issues/9862)
* Passwordless KO - Certificate provider is required to sign JWT [#9864](https://github.com/gravitee-io/issues/issues/9864)

**Management API**

*  Redirect to login when device credentials are deleted [#9859](https://github.com/gravitee-io/issues/issues/9859)

**Console**

* A switch has an incorrect state when revisiting page - Application Settings [#9433](https://github.com/gravitee-io/issues/issues/9433)

**Other**

* Expression language links within MFA page directing to APIM EL page [#9804](https://github.com/gravitee-io/issues/issues/9804)
* Switching between environments is broken when multiple environments linked in cockpit [#9844](https://github.com/gravitee-io/issues/issues/9844)
* "Rotate System Key" modifies application remember-device setting [#9857](https://github.com/gravitee-io/issues/issues/9857)

</details>


### Gravitee Access Management 4.4.1 - July 5, 2024 <a href="#gravitee-access-management-4.3.1-april-5-2024" id="gravitee-access-management-4.3.1-april-5-2024"></a>

<details>

<summary>Bug fixes</summary>

**Gateway**

* Fix NullPointer in OTP Factor [#9725](https://github.com/gravitee-io/issues/issues/9725)
* AM Gateway pod is not starting due to StackOverflowError [#9794](https://github.com/gravitee-io/issues/issues/9794)
* Invalid entry for auth\_flow\_ctx [#9803](https://github.com/gravitee-io/issues/issues/9803)

**Other**

* When creating user with preregistratoin, the password creation steps are skipped [#9839](https://github.com/gravitee-io/issues/issues/9839)

</details>

## Gravitee Access Management 4.4 - June 21, 2024

For more in-depth information on what's new, please refer to the [Gravitee AM 4.4 release notes](../release-notes/am-4.4.md).

{% hint style="warning" %}
The password policy at application level is deprecated for removal in AM 4.6.0. Please refer to the [release notes](../release-notes/am-4.4.md) for more details
{% endhint %}

<details>

<summary>What's new</summary>

## Service Account

At the organizational level, it is now possible to create a service account for which you can generate an access token. This makes it convenient to grant access to the Management REST API for your automation processes without relying on a real user account.

A user can also manage personal access tokens associated with their account.

## Support of mTLS authentication for OIDC provider

In addition of the `client_secret_post` and `client_secret_basic` The OpenID Connect identity provider is now capable to the OpenId provider using mutual TLS authentication.

## Force Reset Password

As password is a sensitive aspect of user account security, you now have an option to force a user to reset their password at next sign in. This help you to create an account with temporary password and request a reset password during the first user authentication.

## Password Policy at Identity Provider level

Password Policies are evolving in this new AM release to be more flexible. It is now possible to define multiple password policies at domain level and assign those policies to the Identity provider.&#x20;

## User Management

### Optional email address

Email address can be configured as optional for user profile linked to a domain.&#x20;

### Password Encoding

If you are using MongoDB or RDBMS identity providers, you have the opportunity to configure the number of rounds for the hashing algorithm used on the user password.

</details>

<details>

<summary>Breaking Changes</summary>

## Password Policies

Password Policies evolved to apply policies at IdentityProvider level.
If you are using Management REST API to provision the security domains, please note that the legacy data structure present into the Domain settings is now a dedicated resource with a new Endpoint on the REST API.
 
To create a policy at domain level, the endpoint to use is the createPasswordPolicy described in [OpenAPI specification](https://raw.githubusercontent.com/gravitee-io/gravitee-access-management/4.4.x/docs/mapi/openapi.yaml)

</details>