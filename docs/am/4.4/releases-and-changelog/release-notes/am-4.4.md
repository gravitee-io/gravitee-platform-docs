---
description: >-
  This article covers the new features released in Gravitee Access Management
  4.4
---

# AM 4.4

## Service Account

At the organizational level, it is now possible to create a service account for which you can generate an access token. This makes it convenient to grant access to the Management REST API for your automation processes without relying on a real user account.

A user can also manage personal access tokens associated with their account.

## Support of mTLS authentication for OIDC provider

In addition of the `client_secret_post` and `client_secret_basic` The OpenID Connect identity provider is now capable to the OpenId provider using mutual TLS authentication ([RFC 8705](https://datatracker.ietf.org/doc/html/rfc8705))

## Force Reset Password

As password is a sensitive aspect of user account security, you now have an option to force a user to reset their password at next sign in. This help you to create an account with temporary password and request a reset password during the first user authentication.

<figure><img src="../../.gitbook/assets/image (2).png" alt=""><figcaption></figcaption></figure>

## Password Policy at Identity Provider level

Password Policies are evolving in this new AM release to be more flexible. Until now, only one policy was possible at domain level and you had the option to override it at application level. This design was effective but had some drawbacks. One issue was the inconsistency of the policy applied to users linked to an identity provider enabled on two different applications, each with its own specific password policy. This was leading to a situation where a user may define a weaker password than expected if the two applications had not the same level of requirements. To solve this, it is now possible to define multiple password policies at domain level and assign those policies to the Identity provider so the policy is consistent for all users of a given  identity provider.&#x20;

{% hint style="danger" %}
Starting from 4.4.0, the password policy at application level is deprecated for removal in AM 4.6.0. Until 4.6.0, application policies will be applied as usual. If you are using them, you will either have to define policies and link them to your IdentityProviders or use a default policy at domain level before upgrading to 4.6 or upper versions.
{% endhint %}

{% hint style="info" %}
All identity providers will be using the gravitee.yml define policy unless they assign it to a password policy at domain level.
{% endhint %}

## User Management

### Optional email address

Email address can be configured as optional for user profile linked to a domain.&#x20;

### Password Encoding

If you are using MongoDB or RDBMS identity providers, you have the opportunity to configure the number of rounds for the hashing algorithm used on the user password.
