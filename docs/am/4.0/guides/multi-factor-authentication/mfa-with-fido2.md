# MFA with FIDO2

## Overview

FIDO2 plugin implements the functionalities so that the passwordless authentication flow can be used during the multi-factor authentication process. This plugin does not have its own configuration but rather uses an existing **WebAuthn** configuration.

{% hint style="info" %}
Please configure **WebAuthn** under the **Security** section so that the plugin works as expected. Check the [Passwordless (W3C WebAuthn)](../login/passwordless-w3c-webauthn.md) section for details.
{% endhint %}

## Create FIDO2 factor

Creating a FIDO2 factor is straightforward as the plugin uses **WebAuthn** configuration. Please follow the steps to create the factor plugin.

1. Select **Security > Multifactor Auth**.
2. Select the plus icon ![plus icon](https://docs.gravitee.io/images/icons/plus-icon.png).
3.  Select **FIDO2 Factor** and click **Next**. Here is a screenshot of the plugin you should see:



    <figure><img src="https://docs.gravitee.io/images/am/current/graviteeio-am-userguide-mfa-fido2.png" alt=""><figcaption><p>FIDO2 factor plugin</p></figcaption></figure>
4. Provide a suitable name.
5. Click **Create**.

## Configure application with FIDO2 plugin

1. In AM Console, select **Applications > Settings > Multifactor Auth**.
2. Toggle to enable the FIDO2 factor plugin.
3. Click **Save**.

Here is an example of an application that has the FIDO2 factor along with other factors.

<figure><img src="https://docs.gravitee.io/images/am/current/graviteeio-am-userguide-mfa-fido2-app-settings.png" alt=""><figcaption><p>Application with FIDO2 factor</p></figcaption></figure>

## Enrollment scenarios for FIDO2 factor plugin

The enrollment behavior for the FIDO2 plugin depends on a couple of things. First, the way the user decides to log on, and secondly whether the user already has a passwordless device registered or not. The plugin considers the following scenarios during enrollment:

1. The user provides a username and password during the login process and the user does not have a passwordless device registered.
2. The user provides a username and password during the login process. The user does not have a passwordless device registered and decides to execute the passwordless registration process after logging on.
3. The user provides a username and password during the login process and the user already has the device registered for passwordless login.
4. The user selects passwordless login options instead of providing a username and password.

## Enrollment step

The following diagram shows how enrollment occurs for the scenarios mentioned in the previous section. For simplicity, the diagram assumes the application has FIDO2 multi-factor enabled. Notice that this plugin ignores the **MFA challenge** step during the enrollment process in certain cases.

<figure><img src="https://docs.gravitee.io/images/am/current/graviteeio-am-userguide-mfa-fido2-enrollment-flow.png" alt=""><figcaption><p>Enrollment diagram</p></figcaption></figure>

## Challenge step

The following diagram shows only the challenge step. For simplicity, the diagram assumes the user has already enrolled to a FIDO2 factor plugin.




<figure><img src="https://docs.gravitee.io/images/am/current/graviteeio-am-userguide-mfa-fido2-challenge-flow.png" alt=""><figcaption><p>Challenge diagram</p></figcaption></figure>
