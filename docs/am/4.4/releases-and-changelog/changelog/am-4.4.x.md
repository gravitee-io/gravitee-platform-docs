---
description: >-
  This page contains the changelog entries for AM 4.4.x and any future minor or
  patch AM 4.4.x releases
---

# AM 4.4.x

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
