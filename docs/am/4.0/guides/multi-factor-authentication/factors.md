---
description: Overview of Gravitee Access Management.
---

# Factors

## Overview

Gravitee Access Management (AM) supports various MFA factors for protecting user account access out of the box.

To create a new MFA Factor, visit your Security Domain **Settings > Multifactor Auth** section and configure the factor of your choice.

## Create an MFA factor

1. In AM Console, click **Settings > Multifactor Auth**.
2. Click the plus icon ![plus icon](https://docs.gravitee.io/images/icons/plus-icon.png).
3.  Select the factor type and click **Next**.

    <div align="center"><figure><img src="https://docs.gravitee.io/images/am/current/graviteeio-am-userguide-mfa-factor-types.png" alt=""><figcaption><p>Add new MFA factor</p></figcaption></figure></div>
4. Enter the factor details and click **Create**.
5. Click **Applications** and select your application.
6. Click the **Settings** tab, then click **Multifactor Auth**.
7.  Enable MFA by selecting an available factor.

    <figure><img src="https://docs.gravitee.io/images/am/current/graviteeio-am-userguide-mfa-application-factor.png" alt=""><figcaption><p>Enable MFA factor</p></figcaption></figure>

## OTP

One-Time Password (OTP) allows you to use an Authenticator application via your digital device (mobile phone), such as Google Authenticator, Microsoft Authenticator or Free OTP, to generate a one-time code which changes over time and will be used as the second factor to validate a user’s account.

If you enable an OTP type factor for your application, next time your users log in they will see the following screens:

<figure><img src="https://docs.gravitee.io/images/am/current/graviteeio-am-userguide-mfa-enroll.png" alt=""><figcaption><p>OTP MFA</p></figcaption></figure>

{% hint style="info" %}
The look and feel of the MFA forms can be overridden. See [custom pages](../branding/README.md#custom-pages) for more information.
{% endhint %}

## SMS

With SMS verification, you can receive a verification code on your mobile phone to be used as the second factor to validate a user’s account.

{% hint style="info" %}
SMS MFA requires a compatible [resource](../resources/README.md).

Some providers allow you to define the duration of the code sent by SMS. If possible we advise you to set a duration of 2 minutes.
{% endhint %}

If you enable an SMS type factor for your application, next time your users log in they will see the following screens:

<figure><img src="https://docs.gravitee.io/images/am/current/graviteeio-am-userguide-mfa-sms-enroll.png" alt=""><figcaption><p>SMS MFA screen 1</p></figcaption></figure>

<figure><img src="https://docs.gravitee.io/images/am/current/graviteeio-am-userguide-mfa-sms-challenge.png" alt=""><figcaption><p>SMS MFA screen 2</p></figcaption></figure>

{% hint style="info" %}
You can change the look and feel of forms using [custom pages](../branding/README.md#custom-pages). The enrollment form must send the phone number using the `phone` parameter in E.164 notation.
{% endhint %}

## Phone Call

With Phone call verification, you can receive a verification code via a phone call to be used as the second factor to validate a user’s account.

{% hint style="info" %}
Phone call MFA requires a compatible [resource](../resources/README.md).
{% endhint %}

If you enable a **Call** type factor for your application, the next time your users log in they will see the following screens:

<figure><img src="https://docs.gravitee.io/images/am/current/graviteeio-am-userguide-mfa-call-enroll.png" alt=""><figcaption><p>Voice call MFA screen 1</p></figcaption></figure>

<figure><img src="https://docs.gravitee.io/images/am/current/graviteeio-am-userguide-mfa-call-challenge.png" alt=""><figcaption><p>Voice call MFA screen 2</p></figcaption></figure>

{% hint style="info" %}
You can change the look and feel of forms using [custom pages](../branding/README.md#custom-pages). The enrollment form must send the phone number using the `phone` parameter in E.164 notation.
{% endhint %}

## Email

With Email verification, you can receive a verification code on your email address to be used as the second factor to validate a user’s account.

{% hint style="info" %}
Email MFA requires a compatible [resource](../resources/README.md).
{% endhint %}

Using the `email-am-factor` plugin configuration form, you can define the number of digits used to generate the verification code. The configured resource must be a [SMTP Resource](../resources/smtp-resource.md). The email template used by this plugin is defined in the design section of the domain or application.

<figure><img src="https://docs.gravitee.io/images/am/current/graviteeio-am-userguide-mfa-email-config.png" alt=""><figcaption><p>Email MFA configuration</p></figcaption></figure>

**Subject** and **Template** fields use the freemarker syntax to customize the message content. The generated **code** is available using the expression `${code}`. The user profile and the application are accessible using the expressions `${user}` and `${client}` (ex: `${client.clientName}` will return the application name and `${user.firstName}` will return the first name of the user.)

If you enable an Email type factor for your application, next time your users log in they will see the following screens:

<figure><img src="https://docs.gravitee.io/images/am/current/graviteeio-am-userguide-mfa-email-enroll.png" alt=""><figcaption><p>Email MFA screen 1</p></figcaption></figure>

<figure><img src="https://docs.gravitee.io/images/am/current/graviteeio-am-userguide-mfa-email-challenge.png" alt=""><figcaption><p>Email MFA screen 2</p></figcaption></figure>

{% hint style="info" %}
You can change the look and feel of forms using [custom pages](../branding/README.md#custom-pages). The enrollment form must send the email address using the `email` parameter.
{% endhint %}

## HTTP

{% hint style="info" %}
HTTP MFA requires a compatible [resource](../resources/README.md).
{% endhint %}

Multi-factor authentication (MFA) can take several forms such as :

* Security key
* FIDO 2 (biometrics)
* Mobile application (TOTP based)
* SMS
* and more

Most of the time, these MFA methods are backed with 3rd party vendors, which each comes with pros and cons. While we recommend that you explore Gravitee Identity and Access Management, we understand that some teams already have a vendor that they are happy with, and we want to make sure that we support those use cases as well.

Our Gravitee MFA HTTP plugin makes that a possibility. With our new Gravitee MFA HTTP plugin you can :

* Easily integrate your existing MFA solution into your Gravitee IAM and APIM strategies
* Bring some customization and offer a better user experience
* Facilitate solution migration

<figure><img src="https://docs.gravitee.io/images/am/current/graviteeio-am-userguide-mfa-factor-http.png" alt=""><figcaption><p>HTTP MFA integration</p></figcaption></figure>
