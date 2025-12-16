---
description: Overview of W3C Web Authentication.
---

# Passwordless (W3C Webauthn)

## Overview

AM supports [W3C Web Authentication (WebAuthn)](https://www.w3.org/TR/webauthn/), allowing users to authenticate their account without a password.

WebAuthn is supported in the Chrome, Firefox, and Edge browsers to different degrees, but support for credential creation and assertion using a U2F Token, such as those provided by Yubico and Feitian, is supported by all of them. For more information, see [WebAuthn.io](https://webauthn.io/).

If you are experiencing certificate issues with WebAuthn, remember to upload the latest version of the root certificate provided by your device supplier to AM.

{% hint style="warning" %}
This is the first AM version with WebAuthn support and Relying Party (RP) conformance tests are fairly new at the moment. This support’s specification and user interfaces may change.
{% endhint %}

## Enable passwordless authentication for an application

1. Log in to AM Console.
2. Click **Applications** and select your application.
3.  In the **Settings** tab, click **Login** and toggle on the **Passwordless** option.

    <figure><img src="https://docs.gravitee.io/images/am/current/graviteeio-am-userguide-passwordless.png" alt=""><figcaption><p>Activate passwordless login</p></figcaption></figure>

## Manage root certificates

WebAuthn relies on certificates to authenticate the device. These certificates can expire, so if you are experiencing certificate issues, check you have the latest version of the root certificate provided by your device supplier and if not, upload it to AM. Certificates can be uploaded to the WebAuthn settings page.

1. Log in to AM Console.
2. Select your **Security Domain**.
3. Click **Settings**, then click **WebAuthn** in the **Security** section.
4.  In the **Certificates** section, select the certificate details.

    <figure><img src="https://docs.gravitee.io/images/am/current/graviteeio-am-userguide-passwordless-certificates.png" alt=""><figcaption><p>Root certificate</p></figcaption></figure>

## Authenticate with WebAuthn

### Registration

Before users can use `Passwordless` authentication for your application, they first need to register their security devices (known as [Authenticators](https://www.w3.org/TR/webauthn/#usecase-new-device-registration)).

The first time users log in with their username/password, they will see the following screen:

<figure><img src="https://docs.gravitee.io/images/am/current/graviteeio-am-userguide-passwordless-enroll.png" alt=""><figcaption><p>Passworldless setup UI</p></figcaption></figure>

After the users complete the registration process, their authenticators are immediately registered and they are redirected to your application.

<figure><img src="https://docs.gravitee.io/images/am/current/graviteeio-am-userguide-passwordless-authenticators.png" alt=""><figcaption><p>Registered user</p></figcaption></figure>

#### **Remember device**

To improve user experience, AM can determine if a passwordless device is already enrolled (or not) for a user, and decide to prompt directly the passwordless login page the next time a user wants to sign in.

<figure><img src="https://docs.gravitee.io/images/am/current/graviteeio-am-userguide-passwordless-remember-device.png" alt=""><figcaption><p>Remember device settingon</p></figcaption></figure>

### Login

{% hint style="info" %}
Ensure your users have [registered their security devices.](passwordless-w3c-webauthn.md#registration)
{% endhint %}

If your application has `Passwordless` authentication enabled, a new link `Sign in with fingerprint, device or security key` will be displayed on the login page.

<figure><img src="https://docs.gravitee.io/images/am/current/graviteeio-am-userguide-passwordless-login-page.png" alt=""><figcaption><p>Passwordless login option</p></figcaption></figure>

By clicking on the link, users are redirected to the "Passwordless Login Page", where they need to enter their username and click `Sign in`. A security window will pop up, where they follow instructions to sign in.

<figure><img src="https://docs.gravitee.io/images/am/current/graviteeio-am-userguide-passwordless-login-username-page.png" alt=""><figcaption><p>Passworldess login page</p></figcaption></figure>

{% hint style="info" %}
The look and feel of the Passwordless forms can be overridden. See [custom pages](../branding/README.md#custom-pages) for more information.
{% endhint %}

## Managing WebAuthn

### Authenticators

WebAuthn authenticators are listed in the **Users > User > Credentials** section of AM Console. You can review and remove the credentials at any time.

### Global settings

Administrators of your security domain can manage the WebAuthn settings in **Settings > WebAuthn**.

They can update the following options:

| Name                              | Description                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                              |
| --------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| Origin                            | This value needs to match `window.location.origin` evaluated by the User Agent during registration and authentication.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                   |
| Relying party name                | Relying Party name for display purposes.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                 |
| Require resident key              | The Relying Party’s requirements in terms of resident credentials. If the parameter is set to true, the authenticator MUST create a client-side-resident public key credential source when creating a public key credential.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                             |
| User verification                 | The Relying Party’s requirements in terms of user verification. User verification ensures that the persons authenticating to a service are in fact who they say they are for the purposes of that service.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                               |
| Authenticator Attachment          | <p>Mechanism used by clients to communicate with authenticators;</p><p>- <code>unspecified</code> value means that the web browser will display all possibilities (both native devices and cross platform devices such as security key),</p><p>- <code>platform</code> value means only platform native devices will be displayed (ex: TouchID on MacOSX)</p><p>- <code>cross-platform</code> value means only devices able to work on all platforms will be displayed (ex: security keys such as Yubikey).</p>                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                          |
| Attestation Conveyance Preference | <p>WebAuthn Relying Parties may use AttestationConveyancePreference to specify their preference regarding attestation conveyance during credential generation.</p><p>- <code>none</code> This value indicates that the Relying Party is not interested in authenticator attestation. For example, in order to potentially avoid having to obtain user consent to relay identifying information to the Relying Party, or to save a roundtrip to an Attestation CA.</p><p>This is the default value.</p><p>- <code>indirect</code> This value indicates that the Relying Party prefers an attestation conveyance yielding verifiable attestation statements, but allows the client to decide how to obtain such attestation statements. The client MAY replace the authenticator-generated attestation statements with attestation statements generated by an Anonymization CA, in order to protect the user’s privacy, or to assist Relying Parties with attestation verification in a heterogeneous ecosystem.</p><p>Note: There is no guarantee that the Relying Party will obtain a verifiable attestation statement in this case. For example, in the case that the authenticator employs self attestation.</p><p>- <code>direct</code> This value indicates that the Relying Party wants to receive the attestation statement as generated by the authenticator.</p> |

## Watch this space

This is a brand new implementation of passwordless support in AM. We have lots of ideas to improve the user experience, including:

* Giving users the option to use their own webauthn device instead of defining a password during registration.
* Automatically detecting webauthn devices and removing the step where users must provide their username before they can use their webauthn device.
* Letting users manage their own device credentials (add, revoke).

We’d love to hear your feedback!
