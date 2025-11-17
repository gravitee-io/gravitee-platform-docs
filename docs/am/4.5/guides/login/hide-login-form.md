# Hide Login Form

## Overview

Hide Login Form enables you to hide the default Gravitee login form and only display upstream Identity Provider(s) configured and enabled for the application.

<figure><img src="https://docs.gravitee.io/images/am/current/graviteeio-am-userguide-hide-login-form-false.png" alt=""><figcaption><p>Login form where Hide Login Form is not enabled</p></figcaption></figure>

If you have one Identity provider configured for the application Gravitee AM will direct the user directly to the Identity Provider.

If you have multiple Identity Providers configured for the application Gravitee AM will display the Identity Providers to the user.

<figure><img src="https://docs.gravitee.io/images/am/current/graviteeio-am-userguide-hide-login-form-multiple-idp.png" alt=""><figcaption><p>Login form where Hide Login Form is enabled and multiple IdPs are enabled</p></figcaption></figure>

## Enable Hide Login Form

To enable Hide Login Form:

1. Log in to AM Console.
2. Make sure you have [configured at least one Identity Provider](../identity-providers/README.md) for the application.
3. Go to **Settings > Login** or **Application > "Your app" > Settings > Login**.
4. Switch on **Hide login form** and click **SAVE**.

<figure><img src="https://docs.gravitee.io/images/am/current/graviteeio-am-userguide-hide-login-form-settings.png" alt=""><figcaption><p>Settings page for an application with Hide Login Form enabled</p></figcaption></figure>
